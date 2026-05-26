export default function WikiPage({ page, onNavigate }) {
  if (!page) return null;

  function renderContent(text) {
    const parts = text.split(/(\[\[.*?\]\])/g);
    return parts.map((part, i) => {
      const match = part.match(/^\[\[(.*?)\]\]$/);
      if (match) {
        return (
          <button
            key={i}
            onClick={() => onNavigate(match[1])}
            className="text-volt hover:underline font-semibold"
          >
            {match[1]}
          </button>
        );
      }
      return <span key={i}>{part}</span>;
    });
  }

  return (
    <article className="max-w-3xl mx-auto py-8 px-6">
      {/* Header */}
      <div className="mb-8">
        <span className={`text-xs font-condensed tracking-widest uppercase px-2 py-0.5 rounded mr-3 ${
          page.type === "player"
            ? "bg-volt text-court"
            : "bg-surface text-muted border border-rim"
        }`}>
          {page.type === "player" ? page.position || "Player" : "Concept"}
        </span>
        <h1 className="font-condensed font-black text-5xl tracking-wide mt-3 mb-4">{page.title}</h1>
        {page.nationality && (
          <p className="text-muted text-sm mb-4">{page.nationality}</p>
        )}
        <p className="text-txt text-base leading-relaxed border-l-2 border-volt pl-4">
          {renderContent(page.summary)}
        </p>
      </div>

      {/* Sections */}
      {page.sections?.map((section, i) => (
        <section key={i} className="mb-8">
          <h2 className="font-condensed font-700 text-2xl tracking-wide text-volt mb-3 pb-2 border-b border-rim">
            {section.heading}
          </h2>
          <div className="text-txt text-sm leading-relaxed wiki-content">
            {renderContent(section.content)}
          </div>
        </section>
      ))}

      {/* Related */}
      {page.related?.length > 0 && (
        <section className="mt-8 pt-6 border-t border-rim">
          <h3 className="text-muted text-xs tracking-widest uppercase mb-3">Related</h3>
          <div className="flex flex-wrap gap-2">
            {page.related.map(r => (
              <button
                key={r}
                onClick={() => onNavigate(r)}
                className="text-xs px-3 py-1.5 rounded-full border border-rim text-muted hover:border-volt hover:text-volt transition-all"
              >
                {r}
              </button>
            ))}
          </div>
        </section>
      )}
    </article>
  );
}
