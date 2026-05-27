import { useState, useRef, useEffect } from "react";
import { search } from "../utils/bm25.js";

function buildSystemPrompt(pages) {
  const kb = pages.map(p =>
    `[${p.title} — ${p.type}]\n${p.summary}\n${p.sections.map(s=>`${s.heading}: ${s.content}`).join("\n")}`
  ).join("\n\n---\n\n");

  return `You are the VMC Wiki AI Coach — an elite volleyball knowledge assistant built on a structured wiki of world-class players and concepts.

Answer questions using the retrieved wiki content below. Be specific, cite player names, and reference technical details. End every response with a bold "Key Takeaway:" that summarises the core lesson in one sentence.

If the answer isn't in the context, say: "I don't have specific information on that — try asking about serving, passing, setting, attacking, blocking, or mental performance."

RETRIEVED WIKI CONTENT:
${kb}`;
}

// Strip UI-only fields before sending to the API
function toApiMessages(messages) {
  return messages.map(({ role, content }) => ({ role, content }));
}

export default function Chat({ wikiData, apiKey }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput]       = useState("");
  const [loading, setLoading]   = useState(false);
  const bottomRef               = useRef(null);

  const allPages = [...(wikiData?.players || []), ...(wikiData?.concepts || [])];

  // Read pre-baked env key as fallback, prefer UI-entered key
  const resolvedKey = apiKey || import.meta.env.VITE_ANTHROPIC_API_KEY || "";

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages]);

  const examples = [
    "How does León approach his jump serve?",
    "What's De Cecco's system for reading blocks?",
    "How should I reset mentally after an error?",
    "Compare Brizard and De Cecco's setting styles",
  ];

  async function send(text) {
    const q = (text || input).trim();
    if (!q || loading) return;
    if (!resolvedKey) {
      alert("Set your Anthropic API key first (top right).");
      return;
    }

    setInput("");
    const relevant = search(q, allPages, 5);
    const userMsg  = { role: "user", content: q };
    const newMsgs  = [...messages, userMsg];
    setMessages(newMsgs);
    setLoading(true);

    try {
      const res = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: {
          "Content-Type":      "application/json",
          "x-api-key":         resolvedKey,
          "anthropic-version": "2023-06-01",
        },
        body: JSON.stringify({
          model:      "claude-sonnet-4-20250514",
          max_tokens: 800,
          system:     buildSystemPrompt(relevant),
          messages:   toApiMessages(newMsgs), // stripped — no extra fields
        }),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err?.error?.message || `API error ${res.status}`);
      }

      const data  = await res.json();
      const reply = data.content?.[0]?.text || "No response.";
      const cited = relevant.map(p => p.title);
      setMessages(m => [...m, { role: "assistant", content: reply, sources: cited }]);
    } catch (e) {
      // Show a clean error without leaking internal details
      const safe = e.message?.startsWith("API error") || e.message?.includes("status")
        ? e.message
        : "Something went wrong. Check your API key and try again.";
      setMessages(m => [...m, { role: "assistant", content: safe, sources: [] }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex h-full">
      {/* Sidebar */}
      <aside className="w-56 bg-surface border-r border-rim flex-shrink-0 p-4 overflow-y-auto">
        <p className="text-muted text-xs tracking-widest uppercase mb-3">Roster</p>
        {(wikiData?.players || []).map(p => (
          <div key={p.id} className="mb-2 p-2 rounded bg-court border border-rim">
            <p className="text-txt text-xs font-semibold">{p.title}</p>
            <span className="text-volt text-xs font-condensed tracking-wider">{p.position}</span>
          </div>
        ))}
        <p className="text-muted text-xs tracking-widest uppercase mt-4 mb-3">Concepts</p>
        {(wikiData?.concepts || []).map(c => (
          <div key={c.id} className="mb-2 p-2 rounded bg-court border border-rim">
            <p className="text-muted text-xs">{c.title}</p>
          </div>
        ))}
      </aside>

      {/* Chat area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* API key warning banner */}
        {!resolvedKey && (
          <div className="bg-amber-900/30 border-b border-amber-700/50 px-6 py-2 text-amber-400 text-xs">
            ⚠ API key not set. Your key is sent directly from the browser — do not use this on a public network.
          </div>
        )}
        {resolvedKey && (
          <div className="bg-surface border-b border-rim px-6 py-2 text-muted text-xs">
            ⚠ API key is sent from your browser. For production use, proxy requests through a backend.
          </div>
        )}

        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.length === 0 && (
            <div className="flex flex-col items-center justify-center h-full gap-6">
              <h2 className="font-condensed font-black text-4xl tracking-widest text-center">
                ASK THE WORLD'S BEST
              </h2>
              <p className="text-muted text-sm text-center max-w-md">
                Coaching intelligence drawn from elite player wiki pages. Ask anything about volleyball technique, tactics, or mindset.
              </p>
              <div className="grid grid-cols-2 gap-3 w-full max-w-xl">
                {examples.map(ex => (
                  <button
                    key={ex}
                    onClick={() => send(ex)}
                    className="text-left p-3 bg-surface border border-rim rounded-lg text-sm text-muted hover:border-volt hover:text-txt transition-all"
                  >
                    {ex}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((m, i) => (
            <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
              <div className={`max-w-[70%] rounded-xl p-4 text-sm leading-relaxed ${
                m.role === "user"
                  ? "bg-volt text-court font-semibold rounded-br-sm"
                  : "bg-surface border border-rim rounded-bl-sm"
              }`}>
                <p className="whitespace-pre-wrap">{m.content}</p>
                {m.sources?.length > 0 && (
                  <div className="flex flex-wrap gap-1 mt-2 pt-2 border-t border-rim">
                    {m.sources.map(s => (
                      <span key={s} className="text-xs bg-court text-muted px-2 py-0.5 rounded-full border border-rim">
                        {s}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="bg-surface border border-rim rounded-xl rounded-bl-sm p-4">
                <div className="flex gap-1">
                  {[0, 1, 2].map(i => (
                    <span key={i} className="w-2 h-2 bg-volt rounded-full animate-bounce"
                      style={{ animationDelay: `${i * 0.15}s` }} />
                  ))}
                </div>
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        {/* Input */}
        <div className="border-t border-rim p-4 flex gap-3">
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === "Enter" && !loading && send()}
            placeholder="Ask about serve technique, setting, blocking, mental performance..."
            className="flex-1 bg-surface border border-rim rounded-lg px-4 py-3 text-sm text-txt focus:outline-none focus:border-volt placeholder-muted"
          />
          <button
            onClick={() => send()}
            disabled={loading || !input.trim()}
            className="bg-volt text-court font-condensed font-black text-sm tracking-widest px-6 rounded-lg disabled:opacity-40 hover:bg-yellow-300 transition-colors"
          >
            ASK
          </button>
          {messages.length > 0 && (
            <button onClick={() => setMessages([])} className="text-muted text-xs hover:text-txt px-2">
              Clear
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
