import { useEffect, useRef, useState } from "react";
import * as d3 from "d3";

export default function GraphMap({ wikiData, onSelectPage }) {
  const svgRef   = useRef(null);
  const [locked, setLocked] = useState(false);
  const simRef   = useRef(null);

  useEffect(() => {
    if (!wikiData?.graph || !svgRef.current) return;

    const { nodes: rawNodes, links: rawLinks } = wikiData.graph;
    const allPages = [...(wikiData.players||[]), ...(wikiData.concepts||[])];

    const width  = svgRef.current.clientWidth  || 900;
    const height = svgRef.current.clientHeight || 600;

    d3.select(svgRef.current).selectAll("*").remove();

    const svg = d3.select(svgRef.current)
      .attr("width",  width)
      .attr("height", height);

    const nodes = rawNodes.map(n => ({ ...n }));
    const links = rawLinks.map(l => ({ ...l }));

    const sim = d3.forceSimulation(nodes)
      .force("link",   d3.forceLink(links).id(d=>d.id).distance(d => d.source.type==="player"||d.target?.type==="player" ? 130 : 90))
      .force("charge", d3.forceManyBody().strength(d => d.type==="player" ? -350 : -180))
      .force("center", d3.forceCenter(width/2, height/2))
      .force("collision", d3.forceCollide().radius(d => d.size + 10));

    simRef.current = sim;

    const link = svg.append("g")
      .selectAll("line")
      .data(links)
      .join("line")
      .attr("stroke", "#1E2530")
      .attr("stroke-width", 1.5)
      .attr("stroke-opacity", 0.8);

    const node = svg.append("g")
      .selectAll("g")
      .data(nodes)
      .join("g")
      .attr("cursor", "pointer")
      .call(d3.drag()
        .on("start", (e, d) => {
          if (!e.active) sim.alphaTarget(0.3).restart();
          d.fx = d.x; d.fy = d.y;
        })
        .on("drag",  (e, d) => { d.fx = e.x; d.fy = e.y; })
        .on("end",   (e, d) => {
          if (!e.active) sim.alphaTarget(0);
          if (!locked) { d.fx = null; d.fy = null; }
        })
      )
      .on("click", (e, d) => {
        const page = allPages.find(p => p.id === d.id);
        if (page) onSelectPage(page);
      })
      .on("mouseover", function(e, d) {
        d3.select(this).select("circle")
          .transition().duration(150)
          .attr("r", d.size + 4)
          .attr("stroke-width", 2.5);

        link.attr("stroke-opacity", l =>
          l.source.id===d.id||l.target.id===d.id ? 1 : 0.1
        ).attr("stroke", l =>
          l.source.id===d.id||l.target.id===d.id ? "#FFD100" : "#1E2530"
        );
      })
      .on("mouseout", function(e, d) {
        d3.select(this).select("circle")
          .transition().duration(150)
          .attr("r", d.size)
          .attr("stroke-width", 1.5);
        link.attr("stroke-opacity", 0.8).attr("stroke","#1E2530");
      });

    node.append("circle")
      .attr("r",    d => d.size)
      .attr("fill", d => d.type==="player" ? "#FFD100" : "#12151A")
      .attr("stroke", d => d.type==="player" ? "#E6B800" : "#2A3850")
      .attr("stroke-width", 1.5);

    node.append("text")
      .text(d => d.type==="player"
        ? d.label.split(" ").pop()
        : d.label.length > 16 ? d.label.split(" ").slice(0,2).join(" ") : d.label
      )
      .attr("text-anchor", "middle")
      .attr("dominant-baseline", "central")
      .attr("font-size", d => d.type==="player" ? "11px" : "9px")
      .attr("font-family", "Barlow Condensed, sans-serif")
      .attr("font-weight", "700")
      .attr("fill", d => d.type==="player" ? "#0C0D12" : "#8899AA")
      .attr("pointer-events", "none");

    sim.on("tick", () => {
      link
        .attr("x1", d=>d.source.x).attr("y1", d=>d.source.y)
        .attr("x2", d=>d.target.x).attr("y2", d=>d.target.y);
      node.attr("transform", d=>`translate(${d.x},${d.y})`);
    });

    return () => sim.stop();
  }, [wikiData]);

  function toggleLock() {
    setLocked(v => {
      if (!v && simRef.current) {
        simRef.current.nodes().forEach(d => { d.fx=d.x; d.fy=d.y; });
      } else if (simRef.current) {
        simRef.current.nodes().forEach(d => { d.fx=null; d.fy=null; });
        simRef.current.alpha(0.3).restart();
      }
      return !v;
    });
  }

  return (
    <div className="flex-1 flex flex-col overflow-hidden relative">
      <div className="absolute top-4 right-4 z-10 flex gap-2">
        <div className="flex gap-4 items-center bg-surface border border-rim rounded-lg px-4 py-2 text-xs text-muted">
          <span><span className="inline-block w-3 h-3 rounded-full bg-volt mr-1.5"/>Players</span>
          <span><span className="inline-block w-3 h-3 rounded-full bg-surface border border-rim mr-1.5"/>Concepts</span>
        </div>
        <button
          onClick={toggleLock}
          className={`text-xs font-condensed tracking-widest uppercase px-4 py-2 rounded-lg border transition-all ${
            locked
              ? "bg-volt text-court border-volt"
              : "bg-surface border-rim text-muted hover:border-volt hover:text-txt"
          }`}
        >
          {locked ? "Locked" : "Lock"}
        </button>
      </div>

      <p className="absolute bottom-4 left-1/2 -translate-x-1/2 text-muted text-xs">
        Drag nodes · Hover to highlight connections · Click to open wiki page
      </p>

      <svg ref={svgRef} className="w-full h-full" />
    </div>
  );
}
