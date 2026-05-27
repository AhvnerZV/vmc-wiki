import { useState } from "react";
import WikiPage from "./WikiPage.jsx";

export default function WikiBrowser({ wikiData, onSelectPage }) {
  const [selected, setSelected] = useState(null);
  const [filter, setFilter]     = useState("all");

  const players  = wikiData?.players  || [];
  const concepts = wikiData?.concepts || [];
  const allPages = [...players, ...concepts];

  function selectPage(page) {
    setSelected(page);
    if (onSelectPage) onSelectPage(page); // keep App state in sync
  }

  function navigateTo(ref) {
    const page = allPages.find(p =>
      p.id === ref ||
      p.title.toLowerCase() === ref.toLowerCase() ||
      p.id.includes(ref.toLowerCase().replace(/\s+/g, "-"))
    );
    if (page) selectPage(page);
  }

  function goBack() {
    setSelected(null);
    if (onSelectPage) onSelectPage(null);
  }

  if (selected) {
    return (
      <div className="flex-1 overflow-y-auto">
        <div className="border-b border-rim px-6 py-3">
          <button
            onClick={goBack}
            className="text-muted text-sm hover:text-txt flex items-center gap-2 transition-colors"
          >
            ← Back to index
          </button>
        </div>
        <WikiPage page={selected} onNavigate={navigateTo} />
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto p-8">
      <div className="max-w-5xl mx-auto">
        <div className="flex items-end justify-between mb-8">
          <div>
            <h1 className="font-condensed font-black text-5xl tracking-wide">WIKI INDEX</h1>
            <p className="text-muted text-sm mt-1">
              {players.length} players · {concepts.length} concepts
            </p>
          </div>
          <div className="flex gap-2">
            {["all", "players", "concepts"].map(f => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`font-condensed text-sm tracking-widest uppercase px-4 py-1.5 rounded border transition-all ${
                  filter === f
                    ? "bg-volt text-court border-volt"
                    : "border-rim text-muted hover:border-volt hover:text-txt"
                }`}
              >
                {f}
              </button>
            ))}
          </div>
        </div>

        {(filter === "all" || filter === "players") && (
          <section className="mb-10">
            <h2 className="text-muted text-xs tracking-widest uppercase mb-4">Players</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {players.map(p => (
                <button
                  key={p.id}
                  onClick={() => selectPage(p)}
                  className="text-left p-5 bg-surface border border-rim rounded-xl hover:border-volt group transition-all"
                >
                  <span className="text-xs font-condensed tracking-widest text-volt uppercase">
                    {p.position}
                  </span>
                  <h3 className="font-condensed font-black text-2xl tracking-wide mt-1 group-hover:text-volt transition-colors">
                    {p.title}
                  </h3>
                  <p className="text-muted text-xs mt-1 mb-3">{p.nationality}</p>
                  <p className="text-txt text-sm leading-relaxed line-clamp-2">{p.summary}</p>
                  <div className="flex flex-wrap gap-1 mt-3">
                    {(p.tags || []).slice(0, 3).map(t => (
                      <span key={t} className="text-xs bg-court text-muted px-2 py-0.5 rounded-full border border-rim">
                        {t}
                      </span>
                    ))}
                  </div>
                </button>
              ))}
            </div>
          </section>
        )}

        {(filter === "all" || filter === "concepts") && (
          <section>
            <h2 className="text-muted text-xs tracking-widest uppercase mb-4">Concepts</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {concepts.map(c => (
                <button
                  key={c.id}
                  onClick={() => selectPage(c)}
                  className="text-left p-5 bg-surface border border-rim rounded-xl hover:border-volt group transition-all"
                >
                  <span className="text-xs bg-surface text-muted border border-rim rounded px-2 py-0.5 font-condensed tracking-wider uppercase">
                    Concept
                  </span>
                  <h3 className="font-condensed font-700 text-xl tracking-wide mt-2 group-hover:text-volt transition-colors">
                    {c.title}
                  </h3>
                  <p className="text-txt text-sm leading-relaxed mt-2 line-clamp-2">{c.summary}</p>
                  <p className="text-muted text-xs mt-3">
                    Related: {(c.related || []).slice(0, 3).join(", ")}
                  </p>
                </button>
              ))}
            </div>
          </section>
        )}
      </div>
    </div>
  );
}
