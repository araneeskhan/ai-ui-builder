import { useState, useRef, useEffect } from 'react';

/* ── Types ─────────────────────────────────────────── */
interface Settings {
  ollamaUrl: string;
  coderModel: string;
  visionModel: string;
  maxIterations: number;
}

interface LogEntry {
  timestamp: string;
  source: 'system' | 'coder' | 'vision' | 'error';
  message: string;
}

/* ── Icons (inline SVGs for zero dependencies) ────── */
const Icons = {
  settings: (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/>
      <circle cx="12" cy="12" r="3"/>
    </svg>
  ),
  copy: (
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <rect width="14" height="14" x="8" y="8" rx="2" ry="2"/>
      <path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>
    </svg>
  ),
  check: (
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="20 6 9 17 4 12"/>
    </svg>
  ),
  sparkle: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/>
    </svg>
  ),
  terminal: (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="4 17 10 11 4 5"/><line x1="12" x2="20" y1="19" y2="19"/>
    </svg>
  ),
  close: (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M18 6 6 18"/><path d="m6 6 12 12"/>
    </svg>
  ),
};

/* ── Helpers ───────────────────────────────────────── */
function getTime() {
  return new Date().toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });
}

/* ── App ───────────────────────────────────────────── */
export default function App() {
  const [prompt, setPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [htmlContent, setHtmlContent] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'preview' | 'code'>('preview');
  const [copied, setCopied] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [settings, setSettings] = useState<Settings>({
    ollamaUrl: 'http://localhost:3000',
    coderModel: 'qwen2.5-coder:1.5b',
    visionModel: 'moondream',
    maxIterations: 2,
  });

  const logsEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  const addLog = (source: LogEntry['source'], message: string) => {
    setLogs(prev => [...prev, { timestamp: getTime(), source, message }]);
  };

  const handleGenerate = async () => {
    if (!prompt.trim() || isGenerating) return;
    setIsGenerating(true);
    setHtmlContent(null);
    setActiveTab('preview');
    addLog('system', `Generation started`);

    try {
      const response = await fetch(`${settings.ollamaUrl}/agent/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });

      if (!response.ok) throw new Error(`Server responded with ${response.status}`);

      const data = await response.json();
      setHtmlContent(data.htmlContent);
      addLog('system', 'Generation complete');
    } catch (e: any) {
      addLog('error', e.message);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleCopy = () => {
    if (!htmlContent) return;
    navigator.clipboard.writeText(htmlContent);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
      handleGenerate();
    }
  };

  /* ── Render ──────────────────────────────────────── */
  return (
    <div className="flex h-screen w-full bg-zinc-950 text-zinc-100 font-sans select-none">

      {/* ── Left Panel ─────────────────────────────── */}
      <aside className="w-[380px] flex flex-col border-r border-zinc-800/80 bg-zinc-950">

        {/* Brand */}
        <header className="px-6 py-5 border-b border-zinc-800/80">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-zinc-800 flex items-center justify-center text-zinc-300">
                {Icons.sparkle}
              </div>
              <div>
                <h1 className="text-[15px] font-semibold text-zinc-100 tracking-tight">UI Architect</h1>
                <p className="text-[11px] text-zinc-500 font-medium">Multi-Agent Builder</p>
              </div>
            </div>
            <button
              onClick={() => setShowSettings(true)}
              className="w-8 h-8 rounded-lg border border-zinc-800 flex items-center justify-center text-zinc-500 hover:text-zinc-300 hover:border-zinc-700 hover:bg-zinc-800/50 transition-all cursor-pointer"
            >
              {Icons.settings}
            </button>
          </div>
        </header>

        {/* Prompt Area */}
        <div className="px-6 py-5 flex flex-col gap-4 flex-1">
          <div>
            <label className="text-[13px] font-medium text-zinc-400 mb-2 block">Describe your component</label>
            <textarea
              className="w-full h-36 bg-zinc-900 border border-zinc-800 rounded-xl px-4 py-3 text-[13px] text-zinc-200 placeholder:text-zinc-600 focus:outline-none focus:ring-1 focus:ring-zinc-600 focus:border-zinc-600 transition-all resize-none font-sans leading-relaxed"
              placeholder="e.g. A modern pricing card with a monthly/yearly toggle, feature list with check icons, and a highlighted 'Popular' badge..."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              onKeyDown={handleKeyDown}
            />
            <p className="text-[11px] text-zinc-600 mt-2">Press <kbd className="px-1.5 py-0.5 rounded bg-zinc-800 text-zinc-400 text-[10px] font-mono border border-zinc-700">Ctrl + Enter</kbd> to generate</p>
          </div>

          <button
            onClick={handleGenerate}
            disabled={isGenerating || !prompt.trim()}
            className="w-full h-10 rounded-lg bg-zinc-100 text-zinc-900 text-[13px] font-semibold hover:bg-white disabled:bg-zinc-800 disabled:text-zinc-600 transition-all cursor-pointer disabled:cursor-not-allowed"
          >
            {isGenerating ? 'Generating...' : 'Generate Component'}
          </button>

          {/* Model Info Pills */}
          <div className="flex gap-2 flex-wrap">
            <span className="text-[11px] text-zinc-500 bg-zinc-900 border border-zinc-800 rounded-md px-2.5 py-1 font-medium">
              Coder: {settings.coderModel}
            </span>
            <span className="text-[11px] text-zinc-500 bg-zinc-900 border border-zinc-800 rounded-md px-2.5 py-1 font-medium">
              Critic: {settings.visionModel}
            </span>
          </div>
        </div>

        {/* Terminal Logs */}
        <div className="border-t border-zinc-800/80 flex flex-col h-[280px]">
          <div className="px-6 py-3 flex items-center gap-2">
            <span className="text-zinc-500">{Icons.terminal}</span>
            <span className="text-[12px] font-medium text-zinc-500 uppercase tracking-wider">Logs</span>
            {isGenerating && (
              <span className="ml-auto flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-subtle-pulse"></span>
                <span className="text-[11px] text-emerald-500 font-medium">Running</span>
              </span>
            )}
          </div>
          <div className="flex-1 overflow-y-auto px-6 pb-4">
            {logs.length === 0 ? (
              <p className="text-[12px] text-zinc-700 italic">No activity yet</p>
            ) : (
              <div className="flex flex-col gap-1">
                {logs.map((log, i) => (
                  <div key={i} className="flex gap-3 text-[12px] font-mono leading-relaxed animate-fade-in">
                    <span className="text-zinc-700 shrink-0">{log.timestamp}</span>
                    <span className={
                      log.source === 'error' ? 'text-red-400' :
                      log.source === 'coder' ? 'text-blue-400' :
                      log.source === 'vision' ? 'text-violet-400' :
                      'text-zinc-400'
                    }>{log.message}</span>
                  </div>
                ))}
                <div ref={logsEndRef} />
              </div>
            )}
          </div>
        </div>
      </aside>

      {/* ── Main Canvas ────────────────────────────── */}
      <main className="flex-1 flex flex-col bg-zinc-950">

        {/* Toolbar */}
        <div className="h-12 border-b border-zinc-800/80 flex items-center justify-between px-5">
          <div className="flex items-center bg-zinc-900 rounded-lg border border-zinc-800 p-0.5">
            {(['preview', 'code'] as const).map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-4 py-1.5 rounded-md text-[12px] font-medium transition-all capitalize cursor-pointer ${
                  activeTab === tab
                    ? 'bg-zinc-800 text-zinc-100 shadow-sm'
                    : 'text-zinc-500 hover:text-zinc-300'
                }`}
              >
                {tab}
              </button>
            ))}
          </div>

          {htmlContent && (
            <button
              onClick={handleCopy}
              className="flex items-center gap-1.5 px-3 py-1.5 text-[12px] font-medium text-zinc-400 hover:text-zinc-200 bg-zinc-900 border border-zinc-800 rounded-lg hover:border-zinc-700 transition-all cursor-pointer"
            >
              {copied ? Icons.check : Icons.copy}
              {copied ? 'Copied' : 'Copy code'}
            </button>
          )}
        </div>

        {/* Progress Bar */}
        {isGenerating && (
          <div className="h-[2px] w-full bg-zinc-900 overflow-hidden">
            <div className="h-full w-[40%] bg-zinc-400 rounded-full animate-progress"></div>
          </div>
        )}

        {/* Canvas Content */}
        <div className="flex-1 relative overflow-hidden">

          {/* Loading State */}
          {isGenerating && !htmlContent && (
            <div className="absolute inset-0 flex items-center justify-center z-10 bg-zinc-950">
              <div className="flex flex-col items-center gap-5 animate-fade-in">
                <div className="relative w-10 h-10">
                  <div className="absolute inset-0 border-2 border-zinc-800 rounded-full"></div>
                  <div className="absolute inset-0 border-2 border-zinc-400 border-t-transparent rounded-full animate-spin"></div>
                </div>
                <div className="text-center">
                  <p className="text-[14px] font-medium text-zinc-300 mb-1">Building your component</p>
                  <p className="text-[12px] text-zinc-600">The agents are iterating on the design...</p>
                </div>
              </div>
            </div>
          )}

          {/* Empty State */}
          {!htmlContent && !isGenerating && (
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="flex flex-col items-center gap-4 max-w-[280px] text-center">
                <div className="w-12 h-12 rounded-xl bg-zinc-900 border border-zinc-800 flex items-center justify-center text-zinc-600">
                  {Icons.sparkle}
                </div>
                <div>
                  <p className="text-[14px] font-medium text-zinc-400 mb-1">No component yet</p>
                  <p className="text-[12px] text-zinc-600 leading-relaxed">Describe a UI component in the prompt area and click Generate to get started.</p>
                </div>
              </div>
            </div>
          )}

          {/* Preview Tab */}
          {htmlContent && activeTab === 'preview' && (
            <iframe
              className="w-full h-full border-0 animate-fade-in"
              srcDoc={`<!DOCTYPE html><html><head><script src="https://cdn.tailwindcss.com"></script><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"><style>body{font-family:'Inter',sans-serif;-webkit-font-smoothing:antialiased;}</style></head><body class="bg-slate-950 flex items-center justify-center min-h-screen text-white">${htmlContent}</body></html>`}
            />
          )}

          {/* Code Tab */}
          {htmlContent && activeTab === 'code' && (
            <div className="absolute inset-0 overflow-auto p-6 bg-zinc-950 animate-fade-in">
              <pre className="text-[13px] font-mono text-zinc-300 leading-relaxed whitespace-pre-wrap">
                <code>{htmlContent}</code>
              </pre>
            </div>
          )}
        </div>
      </main>

      {/* ── Settings Modal ─────────────────────────── */}
      {showSettings && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm" onClick={() => setShowSettings(false)}>
          <div
            className="w-[440px] bg-zinc-900 border border-zinc-800 rounded-2xl shadow-2xl animate-fade-in"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Modal Header */}
            <div className="flex items-center justify-between px-6 py-4 border-b border-zinc-800">
              <h2 className="text-[15px] font-semibold text-zinc-100">Settings</h2>
              <button onClick={() => setShowSettings(false)} className="text-zinc-500 hover:text-zinc-300 transition-colors cursor-pointer">
                {Icons.close}
              </button>
            </div>

            {/* Modal Body */}
            <div className="px-6 py-5 flex flex-col gap-5">
              <SettingsField
                label="Ollama Server URL"
                description="The address where your NestJS backend is running."
                value={settings.ollamaUrl}
                onChange={(v) => setSettings(s => ({ ...s, ollamaUrl: v }))}
              />
              <SettingsField
                label="Coder Model"
                description="The Ollama model used for writing HTML/Tailwind code."
                value={settings.coderModel}
                onChange={(v) => setSettings(s => ({ ...s, coderModel: v }))}
              />
              <SettingsField
                label="Vision Critic Model"
                description="The Ollama model used for analyzing screenshots."
                value={settings.visionModel}
                onChange={(v) => setSettings(s => ({ ...s, visionModel: v }))}
              />
              <div>
                <label className="text-[13px] font-medium text-zinc-300 block mb-1">Max Iterations</label>
                <p className="text-[11px] text-zinc-600 mb-2">How many refine cycles the agents will run.</p>
                <input
                  type="number"
                  min={1}
                  max={10}
                  className="w-full h-9 bg-zinc-800 border border-zinc-700 rounded-lg px-3 text-[13px] text-zinc-200 focus:outline-none focus:ring-1 focus:ring-zinc-600 font-mono"
                  value={settings.maxIterations}
                  onChange={(e) => setSettings(s => ({ ...s, maxIterations: Number(e.target.value) }))}
                />
              </div>
            </div>

            {/* Modal Footer */}
            <div className="flex justify-end gap-2 px-6 py-4 border-t border-zinc-800">
              <button
                onClick={() => setShowSettings(false)}
                className="px-4 py-2 rounded-lg text-[13px] font-medium text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800 transition-all cursor-pointer"
              >
                Cancel
              </button>
              <button
                onClick={() => setShowSettings(false)}
                className="px-4 py-2 rounded-lg bg-zinc-100 text-zinc-900 text-[13px] font-semibold hover:bg-white transition-all cursor-pointer"
              >
                Save Changes
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

/* ── Reusable Settings Field ───────────────────────── */
function SettingsField({ label, description, value, onChange }: {
  label: string;
  description: string;
  value: string;
  onChange: (v: string) => void;
}) {
  return (
    <div>
      <label className="text-[13px] font-medium text-zinc-300 block mb-1">{label}</label>
      <p className="text-[11px] text-zinc-600 mb-2">{description}</p>
      <input
        type="text"
        className="w-full h-9 bg-zinc-800 border border-zinc-700 rounded-lg px-3 text-[13px] text-zinc-200 focus:outline-none focus:ring-1 focus:ring-zinc-600 font-mono"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
}
