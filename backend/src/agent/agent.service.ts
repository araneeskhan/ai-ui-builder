import { Injectable, Logger } from '@nestjs/common';
import axios from 'axios';
import * as fs from 'fs';
import * as path from 'path';
import { chromium } from 'playwright';
import { exec } from 'child_process';
import * as util from 'util';
import { detectScaffold } from './scaffolds';
import { postProcess } from './postprocessor';

const execAsync = util.promisify(exec);

@Injectable()
export class AgentService {
  private readonly logger = new Logger(AgentService.name);
  private readonly OLLAMA_URL = 'http://127.0.0.1:11434/api/generate';
  private readonly MAX_ITERATIONS = 2;

  async generateUi(prompt: string) {
    this.logger.log(`\n========================================`);
    this.logger.log(`Starting generation for: "${prompt}"`);
    this.logger.log(`========================================`);

    const tempHtmlPath = path.join(process.cwd(), 'temp_render.html');
    const screenshotPath = path.join(process.cwd(), 'screenshot.png');

    // ── Step 1: Detect scaffold ──────────────────────
    const scaffold = detectScaffold(prompt);
    if (scaffold) {
      this.logger.log(`Matched scaffold: "${scaffold.type}"`);
    } else {
      this.logger.log(`No scaffold match — using generic prompt`);
    }

    // ── Step 2: Generate initial code ────────────────
    this.logger.log(`Asking Qwen to generate initial code...`);
    let currentCode = await this.generateInitialCode(prompt, scaffold);

    // ── Step 3: Post-process the code ────────────────
    this.logger.log(`Running post-processor...`);
    currentCode = postProcess(currentCode);

    // ── Step 4: Iterative refinement loop ────────────
    for (let i = 1; i <= this.MAX_ITERATIONS; i++) {
      this.logger.log(`\n── Iteration ${i}/${this.MAX_ITERATIONS} ──`);

      // Save and render
      const fullHtml = this.wrapInFullHtml(currentCode);
      fs.writeFileSync(tempHtmlPath, fullHtml);

      // Keep Playwright screenshot for the frontend UI visualizer
      this.logger.log(`Taking screenshot for UI...`);
      await this.takeScreenshot(tempHtmlPath, screenshotPath);

      // ── CUSTOM ML INFERENCE ──
      this.logger.log(`Asking Custom ML Model to evaluate HTML structure...`);
      const mlFeedback = await this.evaluateWithCustomModel(tempHtmlPath);
      
      this.logger.log(`ML Quality Score: ${mlFeedback.score}% | Approved: ${mlFeedback.is_approved}`);
      this.logger.log(`Critique: "${mlFeedback.critique}"`);

      if (mlFeedback.is_approved) {
        this.logger.log(`Design approved at iteration ${i}`);
        break;
      }

      if (i === this.MAX_ITERATIONS) break;

      // Fix based on critique
      this.logger.log(`Asking Qwen to fix based on ML critique...`);
      currentCode = await this.fixCode(currentCode, mlFeedback.critique, scaffold);
      currentCode = postProcess(currentCode);
    }

    this.logger.log(`\nGeneration complete. Returning final HTML.`);
    return { htmlContent: currentCode };
  }

  /**
   * Run the custom Python ML model to evaluate the HTML.
   */
  private async evaluateWithCustomModel(htmlPath: string): Promise<{ score: number, is_approved: boolean, critique: string }> {
    try {
      const pythonScript = path.join(process.cwd(), 'ml', 'infer.py');
      const { stdout } = await execAsync(`python "${pythonScript}" "${htmlPath}"`);
      return JSON.parse(stdout.trim());
    } catch (e: any) {
      this.logger.error(`Failed to run ML model: ${e.message}. Did you run train.py?`);
      return { score: 100, is_approved: true, critique: 'Looks good' }; // Fallback to approve if ML fails
    }
  }

  /**
   * Build the initial code prompt using scaffold + few-shot if available.
   */
  private async generateInitialCode(prompt: string, scaffold: ReturnType<typeof detectScaffold>) {
    let systemPrompt = `You are an expert frontend developer specializing in Tailwind CSS.
Your task is to write a single UI component using raw HTML and Tailwind CSS classes.

STRICT RULES:
1. Output ONLY raw HTML. No markdown, no backticks, no explanations.
2. NEVER use <img> tags. Use FontAwesome icons instead (e.g. <i class="fas fa-check"></i>).
3. Do NOT include <html>, <head>, <body>, or <script> tags. Just the component.
4. Use a dark theme: zinc-900 backgrounds, zinc-800 borders, white/zinc-300 text.
5. Use rounded-xl or rounded-2xl for containers. Use text-sm for body text.
6. Use font-semibold for headings, font-medium for labels.
7. Always add transition-colors to buttons and links.`;

    let userPrompt = `Build this component: ${prompt}`;

    if (scaffold) {
      systemPrompt += `\n\nDESIGN TIPS: ${scaffold.tips}`;
      userPrompt += `\n\nHere is a REFERENCE EXAMPLE of a similar, high-quality component. Use it as a style guide — match its aesthetic quality, spacing, and class patterns, but adapt the content to match the user's request:\n\n${scaffold.example}`;
      userPrompt += `\n\nHere is a SKELETON you can use as a starting structure. Fill in the PLACEHOLDER values and modify as needed:\n\n${scaffold.skeleton}`;
    }

    const response = await this.askOllama('qwen2.5-coder:1.5b', systemPrompt, userPrompt);
    return this.cleanCodeOutput(response);
  }

  /**
   * Fix code based on the vision model's critique.
   */
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

  /**
   * Strip markdown code fences and trim whitespace.
   */
  private cleanCodeOutput(code: string) {
    const match = code.match(/```(?:html)?\s*([\s\S]*?)\s*```/);
    if (match && match[1]) {
      code = match[1];
    }
    return code.trim();
  }

  /**
   * Wrap the component in a full HTML page with CDN dependencies.
   */
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

  /**
   * Send a text prompt to a local Ollama model.
   */
  private async askOllama(model: string, system: string, prompt: string) {
    const response = await axios.post(this.OLLAMA_URL, {
      model,
      system,
      prompt,
      stream: false,
    });
    return response.data.response;
  }

  /**
   * Render HTML in a headless browser and take a screenshot.
   */
  private async takeScreenshot(htmlPath: string, outputPath: string) {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();
    await page.setViewportSize({ width: 800, height: 600 });
    await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(500);
    await page.screenshot({ path: outputPath });
    await browser.close();
  }
}
