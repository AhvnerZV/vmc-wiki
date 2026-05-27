import { useState } from "react";
import Nav         from "./components/Nav.jsx";
import Chat        from "./components/Chat.jsx";
import WikiBrowser from "./components/WikiBrowser.jsx";
import GraphMap    from "./components/GraphMap.jsx";
import WikiPage    from "./components/WikiPage.jsx";
import wikiData    from "./data/wiki_data.json";

const hasData = wikiData?.players?.length > 0;

export default function App() {
  const [tab,      setTab]     = useState("Chat");
  const [apiKey,   setApiKey]  = useState("");
  const [showKey,  setShowKey] = useState(false);
  const [mapPage,  setMapPage] = useState(null);

  function handleMapSelect(page) {
    setMapPage(page);
    setTab("Wiki");
  }

  const allPages = [...(wikiData?.players || []), ...(wikiData?.concepts || [])];

  function navigateWiki(ref) {
    const page = allPages.find(p =>
      p.id === ref ||
      p.title.toLowerCase() === ref.toLowerCase() ||
      p.id.includes(ref.toLowerCase().replace(/\s+/g, "-"))
    );
    if (page) setMapPage(page);
  }

  return (
    <div
      className="h-screen flex flex-col bg-court overflow-hidden"
      onClick={() => showKey && setShowKey(false)}
    >
      <div onClick={e => e.stopPropagation()}>
        <Nav
          tab={tab} setTab={setTab}
          apiKey={apiKey} setApiKey={setApiKey}
          showKey={showKey} setShowKey={setShowKey}
        />
      </div>

      {!hasData && (
        <div className="flex-1 flex flex-col items-center justify-center gap-4 text-center px-6">
          <p className="font-condensed font-black text-3xl text-volt tracking-widest">
            WIKI NOT BUILT YET
          </p>
          <p className="text-muted text-sm max-w-sm">
            Run the pipeline to generate your wiki. The app will load automatically once it's ready.
          </p>
          <code className="bg-surface border border-rim rounded-lg px-4 py-3 text-volt text-sm">
            python build_wiki.py
          </code>
        </div>
      )}

      {hasData && (
        <main className="flex-1 overflow-hidden flex flex-col">
          {tab === "Chat" && (
            <Chat wikiData={wikiData} apiKey={apiKey} />
          )}

          {tab === "Wiki" && (
            mapPage
              ? (
                <div className="flex-1 overflow-y-auto">
                  <div className="border-b border-rim px-6 py-3">
                    <button
                      onClick={() => setMapPage(null)}
                      className="text-muted text-sm hover:text-txt transition-colors"
                    >
                      ← Back to index
                    </button>
                  </div>
                  <WikiPage page={mapPage} onNavigate={navigateWiki} />
                </div>
              )
              : <WikiBrowser wikiData={wikiData} onSelectPage={setMapPage} />
          )}

          {tab === "Map" && (
            <GraphMap wikiData={wikiData} onSelectPage={handleMapSelect} />
          )}
        </main>
      )}
    </div>
  );
}
