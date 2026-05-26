export default function Nav({ tab, setTab, apiKey, setApiKey, showKey, setShowKey }) {
  const tabs = ["Chat", "Wiki", "Map"];
  return (
    <header className="h-14 bg-surface border-b border-rim flex items-center justify-between px-6">
      <div className="flex items-center gap-4">
        <span className="font-condensed font-black text-2xl tracking-widest text-volt">
          VMC WIKI
        </span>
        <span className="text-muted text-xs tracking-widest uppercase">v0.1</span>
      </div>

      <nav className="flex gap-1">
        {tabs.map(t => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`font-condensed font-700 text-sm tracking-widest uppercase px-4 py-1.5 rounded transition-all ${
              tab === t
                ? "bg-volt text-court"
                : "text-muted hover:text-txt"
            }`}
          >
            {t}
          </button>
        ))}
      </nav>

      <button
        onClick={() => setShowKey(v => !v)}
        className="text-muted hover:text-txt text-xs tracking-widest uppercase transition-colors"
      >
        {apiKey ? "🔑 Key set" : "Set API key"}
      </button>

      {showKey && (
        <div className="absolute top-14 right-0 z-50 bg-surface border border-rim rounded-lg p-4 shadow-xl w-80">
          <p className="text-xs text-muted mb-2">Anthropic API key (stored in memory only)</p>
          <input
            type="password"
            placeholder="sk-ant-..."
            value={apiKey}
            onChange={e => setApiKey(e.target.value)}
            className="w-full bg-court border border-rim rounded px-3 py-2 text-sm text-txt focus:outline-none focus:border-volt"
          />
          <button
            onClick={() => setShowKey(false)}
            className="mt-2 w-full bg-volt text-court font-condensed font-700 text-sm py-1.5 rounded"
          >
            Save
          </button>
        </div>
      )}
    </header>
  );
}
