import { useState } from "react";
import Nav         from "./components/Nav.jsx";
import Chat        from "./components/Chat.jsx";
import WikiBrowser from "./components/WikiBrowser.jsx";
import GraphMap    from "./components/GraphMap.jsx";
import WikiPage    from "./components/WikiPage.jsx";

let wikiData = null;
try {
  wikiData = (await import("./data/wiki_data.json", { assert: { type: "json" } })).default;
} catch {
  wikiData = null;
}

export default function App() {
  const [tab,       setTab]      = useState("Chat");
  const [apiKey,    setApiKey]   = useState("");
  const [showKey,   setShowKey]  = useState(false);
  const [mapPage,   setMapPage]  = useState(null);

  function handleMapSelect(page) {
    setMapPage(page);
    setTab("Wiki");
  }

  const noData = !wikiData;

  return (
    <div className="h-screen flex flex-col bg-court overflow-hidden" onClick={() => showKey && setShowKey(false)}>
      <div onClick={e => e.stopPropagation()}>
        <Nav tab={tab} setTab={setTab} apiKey={apiKey} setApiKey={setApiKey} showKey={showKey} setShowKey={setShowKey} />
      </div>

      {noData && (
        <div className="flex-1 flex items-center justify-center flex-col gap-4 text-muted">
          <p className="font-condensed text-2xl">No wiki_data.json found.</p>
          <p className="text-sm">Run <code className="text-volt">python build_wiki.py</code> to generate it.</p>
        </div>
      )}

      {!noData && (
        <main className="flex-1 overflow-hidden flex flex-col">
          {tab === "Chat" && <Chat wikiData={wikiData} apiKey={apiKey} />}
          {tab === "Wiki" && (
            mapPage
              ? <div className="flex-1 overflow-y-auto">
                  <div className="border-b border-rim px-6 py-3">
                    <button onClick={() => setMapPage(null)} className="text-muted text-sm hover:text-txt">
                      ← Back to index
                    </button>
                  </div>
                  <WikiPage
                    page={mapPage}
                    onNavigate={ref => {
                      const all = [...(wikiData.players||[]), ...(wikiData.concepts||[])];
                      const p = all.find(x => x.id===ref||x.title.toLowerCase()===ref.toLowerCase());
                      if (p) setMapPage(p);
                    }}
                  />
                </div>
              : <WikiBrowser wikiData={wikiData} />
          )}
          {tab === "Map" && <GraphMap wikiData={wikiData} onSelectPage={handleMapSelect} />}
        </main>
      )}
    </div>
  );
}
