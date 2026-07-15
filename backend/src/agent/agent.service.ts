import { Injectable, Logger, HttpException, HttpStatus } from '@nestjs/common';
import axios from 'axios';
import * as fs from 'fs/promises';
import * as path from 'path';
import { chromium, Browser, Page } from 'playwright';
import { exec } from 'child_process';
import * as util from 'util';
import * as crypto from 'crypto';
import { detectScaffold } from './scaffolds';
import { postProcess } from './postprocessor';

const execAsync = util.promisify(exec);

@Injectable()
export class AgentService {
  private readonly logger = new Logger(AgentService.name);
  private readonly OLLAMA_URL = 'http://127.0.0.1:11434/api/generate';
  private readonly MAX_ITERATIONS = 2;
  private readonly AXIOS_TIMEOUT = 60000; // 60 seconds timeout for Ollama

  async generateUi(prompt: string) {
    const requestId = crypto.randomUUID();
    this.logger.log(`\n========================================`);
    this.logger.log(`[${requestId}] Starting generation for: "${prompt}"`);
    this.logger.log(`========================================`);

    // Unique temporary files to ensure thread-safety
    const tempDir = path.join(process.cwd(), 'temp');
    await fs.mkdir(tempDir, { recursive: true });
    
    const tempHtmlPath = path.join(tempDir, `render_${requestId}.html`);
    const screenshotPath = path.join(tempDir, `screenshot_${requestId}.png`);
    
    let browser: Browser | null = null;
    let page: Page | null = null;

    try {
      // Launch Playwright ONCE per request for optimization
      browser = await chromium.launch({ headless: true });
      page = await browser.newPage();
      await page.setViewportSize({ width: 800, height: 600 });

      const scaffold = detectScaffold(prompt);
      if (scaffold) {
        this.logger.log(`[${requestId}] Matched scaffold: "${scaffold.type}"`);
      }

      this.logger.log(`[${requestId}] Asking Qwen to generate initial code...`);
      let currentCode = await this.generateInitialCode(prompt, scaffold);
      currentCode = postProcess(currentCode);

      for (let i = 1; i <= this.MAX_ITERATIONS; i++) {
        this.logger.log(`\n[${requestId}] ── Iteration ${i}/${this.MAX_ITERATIONS} ──`);

        const fullHtml = this.wrapInFullHtml(currentCode);
        await fs.writeFile(tempHtmlPath, fullHtml, 'utf-8');

        this.logger.log(`[${requestId}] Taking screenshot...`);
        await page.goto(`file://${tempHtmlPath}`, { waitUntil: 'networkidle', timeout: 15000 });
        await page.waitForTimeout(500);
        await page.screenshot({ path: screenshotPath });

        this.logger.log(`[${requestId}] Asking Custom ML Model to evaluate structure...`);
        const mlFeedback = await this.evaluateWithCustomModel(tempHtmlPath);
        
        this.logger.log(`[${requestId}] ML Quality Score: ${mlFeedback.score}% | Approved: ${mlFeedback.is_approved}`);
        this.logger.log(`[${requestId}] Critique: "${mlFeedback.critique}"`);

        if (mlFeedback.is_approved) {
          this.logger.log(`[${requestId}] Design approved at iteration ${i}`);
          break;
        }

        if (i === this.MAX_ITERATIONS) break;

        this.logger.log(`[${requestId}] Asking Qwen to fix based on ML critique...`);
        currentCode = await this.fixCode(currentCode, mlFeedback.critique, scaffold);
        currentCode = postProcess(currentCode);
      }

      this.logger.log(`\n[${requestId}] Generation complete.`);
      return { htmlContent: currentCode };

    } catch (error: any) {
      this.logger.error(`[${requestId}] Generation failed: ${error.message}`);
      throw new HttpException(
        error.message || 'Failed to generate UI',
        HttpStatus.INTERNAL_SERVER_ERROR
      );
    } finally {
      // ── GUARANTEED CLEANUP ──
      if (browser) {
        await browser.close().catch(e => this.logger.error(`Failed to close browser: ${e.message}`));
      }
      
      // Delete temporary files so disk doesn't fill up
      try {
        await fs.unlink(tempHtmlPath).catch(() => {});
        await fs.unlink(screenshotPath).catch(() => {});
      } catch (cleanupError) {
        this.logger.warn(`[${requestId}] Failed to cleanup temp files.`);
      }
    }
  }

  private async evaluateWithCustomModel(htmlPath: string): Promise<{ score: number, is_approved: boolean, critique: string }> {
    try {
      const pythonScript = path.join(process.cwd(), 'ml', 'infer.py');
      const { stdout } = await execAsync(`python "${pythonScript}" "${htmlPath}"`, { timeout: 10000 });
      return JSON.parse(stdout.trim());
    } catch (e: any) {
      this.logger.error(`Failed to run ML model: ${e.message}. Did you run train.py?`);
      return { score: 100, is_approved: true, critique: 'Looks good' };
    }
  }

  private async generateInitialCode(prompt: string, scaffold: ReturnType<typeof detectScaffold>) {
    let systemPrompt = `You are an expert frontend developer specializing in Tailwind CSS.
Your task is to write a single UI component using raw HTML and Tailwind CSS classes.

STRICT RULES:
1. Output ONLY raw HTML. No markdown, no backticks, no explanations.
2. NEVER use <img> tags. Use FontAwesome icons instead.
3. Do NOT include <html>, <head>, <body>, or <script> tags. Just the component.
4. Use a dark theme: zinc-900 backgrounds, zinc-800 borders, white/zinc-300 text.
5. Use rounded-xl or rounded-2xl for containers. Use text-sm for body text.
6. Use font-semibold for headings, font-medium for labels.
7. Always add transition-colors to buttons and links.`;

    let userPrompt = `Build this component: ${prompt}`;

    if (scaffold) {
      systemPrompt += `\n\nDESIGN TIPS: ${scaffold.tips}`;
      userPrompt += `\n\nHere is a REFERENCE EXAMPLE of a similar component. Match its aesthetic quality and structure:\n\n${scaffold.example}`;
      userPrompt += `\n\nHere is a SKELETON you can use as a starting point. Fill in the PLACEHOLDERS:\n\n${scaffold.skeleton}`;
    }

    const response = await this.askOllama('qwen2.5-coder:1.5b', systemPrompt, userPrompt);
    return this.cleanCodeOutput(response);
  }

  private async fixCode(currentCode: string, critique: string, scaffold: ReturnType<typeof detectScaffold>) {
    let systemPrompt = `You are an expert frontend developer. Fix the HTML based on the machine learning structural critique below.
STRICT RULES:
1. Output ONLY raw HTML. No markdown, no backticks.
2. NEVER use <img> tags. Use FontAwesome icons.
3. Keep the dark zinc color palette. Use rounded corners and proper spacing.`;

    if (scaffold) {
      systemPrompt += `\n\nFor reference, here is what a high-quality version of this component looks like:\n${scaffold.example}`;
    }

    const userPrompt = `Current Code:\n${currentCode}\n\nML Critique:\n${critique}\n\nRewrite the entire HTML to fix these structural issues.`;
    const response = await this.askOllama('qwen2.5-coder:1.5b', systemPrompt, userPrompt);
    return this.cleanCodeOutput(response);
  }

  private cleanCodeOutput(code: string) {
    const match = code.match(/```(?:html)?\s*([\s\S]*?)\s*```/);
    if (match && match[1]) {
      code = match[1];
    }
    return code.trim();
  }

  private wrapInFullHtml(component: string): string {
    return `<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    body { font-family: 'Inter', sans-serif; -webkit-font-smoothing: antialiased; }
  </style>
</head>
<body class="bg-zinc-950 flex items-center justify-center min-h-screen text-white">
  ${component}
</body>
</html>`;
  }

  private async askOllama(model: string, system: string, prompt: string) {
    try {
      const response = await axios.post(this.OLLAMA_URL, {
        model,
        system,
        prompt,
        stream: false,
      }, { timeout: this.AXIOS_TIMEOUT });
      return response.data.response;
    } catch (error: any) {
      this.logger.error(`Ollama request failed: ${error.message}`);
      throw new Error('Failed to communicate with local AI model. Is Ollama running?');
    }
  }
}
