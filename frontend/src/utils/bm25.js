/**
 * BM25 search — memoized index so it builds once per doc set, not per query.
 */

const k1 = 1.5, b = 0.75;

function tokenize(text) {
  return text.toLowerCase().replace(/[^a-z0-9\s]/g, " ").split(/\s+/).filter(Boolean);
}

function buildIndex(docs) {
  const tf = [], df = {}, lengths = [];
  for (const doc of docs) {
    const text   = [doc.title, doc.summary, ...(doc.sections || []).map(s => s.content)].join(" ");
    const tokens = tokenize(text);
    const freq   = {};
    for (const t of tokens) freq[t] = (freq[t] || 0) + 1;
    tf.push(freq);
    lengths.push(tokens.length);
    for (const t of Object.keys(freq)) df[t] = (df[t] || 0) + 1;
  }
  const avgLen = lengths.reduce((a, b) => a + b, 0) / (lengths.length || 1);
  return { tf, df, lengths, avgLen, N: docs.length };
}

function scoreDoc(query, idx, index) {
  const { tf, df, lengths, avgLen, N } = index;
  let s = 0;
  for (const t of tokenize(query)) {
    const f   = tf[idx][t] || 0;
    const idf = Math.log((N - (df[t] || 0) + 0.5) / ((df[t] || 0) + 0.5) + 1);
    s += idf * (f * (k1 + 1)) / (f + k1 * (1 - b + b * (lengths[idx] / avgLen)));
  }
  return s;
}

// Cache: weakly keyed on the docs array reference so it resets when wiki reloads
const cache = new WeakMap();

function getIndex(docs) {
  if (!cache.has(docs)) cache.set(docs, buildIndex(docs));
  return cache.get(docs);
}

export function search(query, docs, topK = 5) {
  if (!query.trim() || !docs?.length) return [];
  const index = getIndex(docs);
  return docs
    .map((doc, i) => ({ doc, score: scoreDoc(query, i, index) }))
    .filter(x => x.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, topK)
    .map(x => x.doc);
}
