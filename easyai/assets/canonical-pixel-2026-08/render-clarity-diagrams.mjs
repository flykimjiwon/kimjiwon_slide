// allow: SIZE_OK — deterministic, editable vector-to-PNG renderer for the high-legibility treatment.
import { execFileSync } from "node:child_process";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { clarityScenes } from "./clarity-catalogue.mjs";
import { clarityAccents, clarityColors } from "./clarity-tokens.mjs";

const out = dirname(fileURLToPath(import.meta.url));
const sizes = [["wide", 1672, 941], ["square", 941, 941], ["portrait", 753, 941]];
const c = clarityColors;
const r = (x, y, w, h, fill, extra = "") => `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${fill}" ${extra}/>`;
const rr = (x, y, w, h, fill, radius = 18, extra = "") => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${radius}" fill="${fill}" ${extra}/>`;
const circle = (cx, cy, radius, fill, extra = "") => `<circle cx="${cx}" cy="${cy}" r="${radius}" fill="${fill}" ${extra}/>`;
const path = (d, stroke, width = 6, extra = "") => `<path d="${d}" fill="none" stroke="${stroke}" stroke-width="${width}" stroke-linecap="round" stroke-linejoin="round" ${extra}/>`;
const joinParts = (parts) => parts.flat(Infinity).filter(Boolean).join("");
const hash = (word) => [...word].reduce((sum, char) => sum + char.charCodeAt(0), 0);
const accents = clarityAccents;

function icon(name, x, y, unit) {
  const accent = accents[hash(name) % accents.length], box = () => rr(x, y, unit * 1.8, unit * 1.32, c.paper, unit * .18, `stroke="${c.line}" stroke-width="4"`);
  const card = (bar = accent) => joinParts([box(), rr(x + unit * .22, y + unit * .2, unit * 1.36, unit * .14, bar, unit * .07), r(x + unit * .22, y + unit * .53, unit * 1.1, unit * .1, c.line), r(x + unit * .22, y + unit * .78, unit * .82, unit * .1, c.line)]);
  if (name === "core") return joinParts([circle(x + unit * .9, y + unit * .66, unit * .62, c.coreHalo), circle(x + unit * .9, y + unit * .66, unit * .41, c.cyan), circle(x + unit * .9, y + unit * .66, unit * .21, c.blue), circle(x + unit * .9, y + unit * .66, unit * .08, c.paper)]);
  if (name === "agent") return joinParts([circle(x + unit * .9, y + unit * .37, unit * .26, c.agent), rr(x + unit * .43, y + unit * .69, unit * .94, unit * .46, c.agent, unit * .23), circle(x + unit * .8, y + unit * .38, unit * .04, c.ink), circle(x + unit, y + unit * .38, unit * .04, c.ink), circle(x + unit * 1.16, y + unit * .9, unit * .075, c.blue)]);
  if (name === "ghost") return joinParts([rr(x + unit * .4, y + unit * .22, unit, unit * .88, c.paper, unit * .34, `stroke="${c.cyan}" stroke-width="5"`), circle(x + unit * .72, y + unit * .51, unit * .06, c.ink), circle(x + unit * 1.08, y + unit * .51, unit * .06, c.ink), rr(x + unit * .58, y + unit * .82, unit * .64, unit * .09, c.cyan, unit * .045)]);
  if (["document", "summary", "prompt", "plan", "orders", "mail", "card"].includes(name)) return card(name === "prompt" ? c.pink : name === "summary" ? c.green : accent);
  if (name === "server") return joinParts([box(), [0.28, .57, .86].map((offset) => [rr(x + unit * .25, y + unit * offset, unit * 1.3, unit * .16, c.serverSurface, unit * .08), circle(x + unit * 1.4, y + unit * (offset + .08), unit * .06, c.green)])]);
  if (name === "window") return joinParts([box(), r(x + unit * .2, y + unit * .24, unit * 1.4, unit * .14, c.cyan), r(x + unit * .86, y + unit * .45, unit * .08, unit * .65, c.line), r(x + unit * .32, y + unit * .62, unit * .34, unit * .28, c.windowSurface), r(x + unit * 1.1, y + unit * .62, unit * .34, unit * .28, c.windowSurface)]);
  if (name === "frame") return joinParts([rr(x + unit * .18, y + unit * .18, unit * 1.44, unit * .96, c.paper, unit * .14, `stroke="${c.blue}" stroke-width="7"`), r(x + unit * .37, y + unit * .44, unit * .22, unit * .22, c.pink), r(x + unit * .79, y + unit * .44, unit * .22, unit * .22, c.yellow), r(x + unit * 1.19, y + unit * .44, unit * .22, unit * .22, c.green), path(`M ${x + unit * .36} ${y + unit * .86} H ${x + unit * 1.43}`, c.cyan, 6)]);
  if (name === "cache") return joinParts([box(), [0.3, .57, .84].map((offset, index) => [rr(x + unit * .27, y + unit * offset, unit * 1.12, unit * .13, c.serverSurface, unit * .06), index === 1 ? path(`M ${x + unit * 1.18} ${y + unit * .46} Q ${x + unit * 1.57} ${y + unit * .64} ${x + unit * 1.18} ${y + unit * .82}`, c.green, 5) : ""])]);
  if (name === "tokens") return joinParts([box(), [0.27, .52, .77].map((offset, index) => rr(x + unit * (.31 + (index % 2) * .1), y + unit * offset, unit * (1.1 - (index % 2) * .2), unit * .13, accents[index], unit * .06))]);
  if (name === "bag") return joinParts([rr(x + unit * .17, y + unit * .42, unit * 1.46, unit * .72, c.yellow, unit * .16), path(`M ${x + unit * .55} ${y + unit * .42} V ${y + unit * .22} Q ${x + unit * .9} ${y + unit * .06} ${x + unit * 1.25} ${y + unit * .22} V ${y + unit * .42}`, c.yellow, 8), circle(x + unit * .9, y + unit * .78, unit * .1, c.paper)]);
  if (name === "compass") return joinParts([circle(x + unit * .9, y + unit * .66, unit * .61, c.compassSurface), circle(x + unit * .9, y + unit * .66, unit * .5, c.cyan), `<path d="M ${x + unit * .9} ${y + unit * .19} L ${x + unit * 1.13} ${y + unit * .66} L ${x + unit * .9} ${y + unit * 1.13} L ${x + unit * .67} ${y + unit * .66} Z" fill="${c.paper}"/>`, `<path d="M ${x + unit * .9} ${y + unit * .19} L ${x + unit * 1.13} ${y + unit * .66} L ${x + unit * .9} ${y + unit * .66} Z" fill="${c.coral}"/>`]);
  if (name === "anchor") return joinParts([path(`M ${x + unit * .9} ${y + unit * .16} V ${y + unit * 1.05} M ${x + unit * .46} ${y + unit * .45} H ${x + unit * 1.34}`, c.blue, 9), path(`M ${x + unit * .26} ${y + unit * .87} Q ${x + unit * .9} ${y + unit * 1.34} ${x + unit * 1.54} ${y + unit * .87}`, c.blue, 9), circle(x + unit * .9, y + unit * .16, unit * .12, c.blue)]);
  if (["lens", "observe"].includes(name)) return joinParts([circle(x + unit * .7, y + unit * .55, unit * .43, c.lensSurface, `stroke="${c.cyan}" stroke-width="8"`), path(`M ${x + unit} ${y + unit * .86} L ${x + unit * 1.45} ${y + unit * 1.2}`, c.yellow, 10)]);
  if (name === "gear") return joinParts([circle(x + unit * .9, y + unit * .66, unit * .47, c.blue), circle(x + unit * .9, y + unit * .66, unit * .18, c.paper), [0, .5, 1, 1.5].map((turn) => `<rect x="${x + unit * .82}" y="${y + unit * .05}" width="${unit * .16}" height="${unit * .32}" rx="${unit * .06}" fill="${c.blue}" transform="rotate(${turn * 90} ${x + unit * .9} ${y + unit * .66})"/>`)]);
  if (name === "map") return joinParts([rr(x, y + unit * .16, unit * 1.8, unit * 1.04, c.mapSurface, unit * .14, `stroke="${c.green}" stroke-width="5"`), path(`M ${x + unit * .54} ${y + unit * .2} V ${y + unit * 1.16} M ${x + unit * 1.18} ${y + unit * .2} V ${y + unit * 1.16}`, c.line, 4), path(`M ${x + unit * .25} ${y + unit * .92} Q ${x + unit * .85} ${y + unit * .42} ${x + unit * 1.5} ${y + unit * .7}`, c.yellow, 7)]);
  if (["shelf", "pantry", "archive", "drawers", "toolwall", "directory", "vector"].includes(name)) return joinParts([box(), [0.3, .62, .94].map((offset, index) => [r(x + unit * .23, y + unit * offset, unit * 1.34, unit * .08, c.line), rr(x + unit * (.32 + (index % 2) * .46), y + unit * (offset - .18), unit * .26, unit * .23, accents[index], unit * .05)])]);
  if (name === "funnel" || name === "filter") return joinParts([`<path d="M ${x + unit * .12} ${y + unit * .2} H ${x + unit * 1.68} L ${x + unit * 1.1} ${y + unit * .82} V ${y + unit * 1.2} H ${x + unit * .7} V ${y + unit * .82} Z" fill="${c.filterSurface}" stroke="${c.cyan}" stroke-width="6" stroke-linejoin="round"/>`, circle(x + unit * .9, y + unit * 1.03, unit * .1, c.yellow)]);
  if (name === "press") return joinParts([rr(x + unit * .16, y + unit * .14, unit * 1.48, unit * .2, c.yellow, unit * .08), rr(x + unit * .16, y + unit * .98, unit * 1.48, unit * .2, c.yellow, unit * .08), rr(x + unit * .48, y + unit * .45, unit * .84, unit * .42, c.pressSurface, unit * .1), path(`M ${x + unit * .9} ${y + unit * .38} V ${y + unit * .45} M ${x + unit * .9} ${y + unit * .94} V ${y + unit * .87}`, c.coral, 7)]);
  if (name === "cube") return joinParts([`<path d="M ${x + unit * .35} ${y + unit * .42} L ${x + unit * .9} ${y + unit * .14} L ${x + unit * 1.45} ${y + unit * .42} L ${x + unit * .9} ${y + unit * .7} Z" fill="${c.cubeTop}"/>`, `<path d="M ${x + unit * .35} ${y + unit * .42} L ${x + unit * .9} ${y + unit * .7} V ${y + unit * 1.24} L ${x + unit * .35} ${y + unit * .96} Z" fill="${c.blue}"/>`, `<path d="M ${x + unit * .9} ${y + unit * .7} L ${x + unit * 1.45} ${y + unit * .42} V ${y + unit * .96} L ${x + unit * .9} ${y + unit * 1.24} Z" fill="${c.navy}"/>`]);
  if (name === "rail") return joinParts([rr(x + unit * .12, y + unit * .3, unit * .18, unit * .8, c.yellow, unit * .08), rr(x + unit * 1.5, y + unit * .3, unit * .18, unit * .8, c.yellow, unit * .08), path(`M ${x + unit * .3} ${y + unit * .52} H ${x + unit * 1.5} M ${x + unit * .3} ${y + unit * .9} H ${x + unit * 1.5}`, c.cyan, 7)]);
  if (name === "obstacle") return joinParts([rr(x + unit * .18, y + unit * .78, unit * 1.48, unit * .18, c.yellow, unit * .08), [0.4, .75, 1.1].map((offset) => path(`M ${x + unit * offset} ${y + unit * .76} L ${x + unit * (offset + .23)} ${y + unit * .38}`, c.coral, 8))]);
  if (name === "checkpoint") return joinParts([rr(x + unit * .2, y + unit * .2, unit * .18, unit * .92, c.yellow, unit * .08), rr(x + unit * 1.42, y + unit * .2, unit * .18, unit * .92, c.yellow, unit * .08), rr(x + unit * .48, y + unit * .3, unit * .84, unit * .52, c.paper, unit * .1, `stroke="${c.green}" stroke-width="5"`), path(`M ${x + unit * .65} ${y + unit * .56} L ${x + unit * .83} ${y + unit * .7} L ${x + unit * 1.15} ${y + unit * .43}`, c.green, 6)]);
  if (name === "screen") return joinParts([rr(x + unit * .2, y + unit * .22, unit * 1.4, unit * .86, c.paper, unit * .13, `stroke="${c.cyan}" stroke-width="6"`), r(x + unit * .38, y + unit * .4, unit * 1.04, unit * .18, c.blue), path(`M ${x + unit * .48} ${y + unit * .78} H ${x + unit * 1.32}`, c.green, 6)]);
  if (["gate", "scanner", "turnstile", "pen", "aquarium"].includes(name)) return joinParts([rr(x + unit * .2, y + unit * .2, unit * .18, unit * .92, c.yellow, unit * .08), rr(x + unit * 1.42, y + unit * .2, unit * .18, unit * .92, c.yellow, unit * .08), rr(x + unit * .35, y + unit * .36, unit * 1.1, unit * .18, c.cyan, unit * .08), name === "scanner" ? path(`M ${x + unit * .45} ${y + unit * .78} H ${x + unit * 1.35}`, c.green, 7) : ""]);
  if (["key", "plug", "port", "baton", "bridge", "pipe", "bucket", "switch"].includes(name)) return joinParts([rr(x + unit * .18, y + unit * .54, unit * 1.28, unit * .2, accent, unit * .1), circle(x + unit * .3, y + unit * .64, unit * .24, c.connectorSurface, `stroke="${accent}" stroke-width="7"`), r(x + unit * 1.15, y + unit * .48, unit * .14, unit * .34, c.yellow)]);
  if (["noise", "packets", "trace", "tiles", "bins", "stack", "postal"].includes(name)) return joinParts([[.12, .63, 1.12].map((offset, index) => rr(x + unit * offset, y + unit * (.34 + (index % 2) * .34), unit * .38, unit * .3, accents[index], unit * .08))]);
  if (["danger", "wrench", "spiral", "stamp", "lab", "replay", "seed", "campfire", "board", "coat"].includes(name)) return joinParts([circle(x + unit * .9, y + unit * .66, unit * .54, c.warmSurface), path(`M ${x + unit * .44} ${y + unit * .85} L ${x + unit * .78} ${y + unit * .32} L ${x + unit * 1.06} ${y + unit * .8} L ${x + unit * 1.38} ${y + unit * .46}`, accent, 9), circle(x + unit * .9, y + unit * .66, unit * .1, c.paper)]);
  return card(accent);
}

function positions(pattern, width, height, unit, count) {
  const portrait = height > width * 1.15, cx = width / 2, cy = height / 2, stepX = (width - unit * 4.3) / Math.max(1, count - 1), stepY = (height - unit * 4) / Math.max(1, count - 1);
  const chain = portrait ? Array.from({ length: count }, (_, index) => [cx - unit * .9, unit * 1.3 + index * stepY]) : Array.from({ length: count }, (_, index) => [unit * 1.25 + index * stepX, cy - unit * .66]);
  const hub = [[cx - unit * .9, cy - unit * .66], [unit * 1.25, unit * 1.25], [width - unit * 3.05, unit * 1.25], [cx - unit * .9, height - unit * 2.1]];
  const loop = [[cx - unit * 2.25, cy - unit * 1.65], [cx + unit * .45, cy - unit * 1.65], [cx + unit * .45, cy + unit * .45], [cx - unit * 2.25, cy + unit * .45]];
  const tree = portrait ? [[cx - unit * .9, unit * 1.1], [unit * 1.05, cy - unit * .2], [width - unit * 2.85, cy - unit * .2], [cx - unit * .9, height - unit * 2.05]] : [[cx - unit * .9, unit * 1.05], [unit * 1.15, cy - unit * .45], [width - unit * 3, cy - unit * .45], [cx - unit * .9, height - unit * 2.15]];
  return (pattern === "hub" ? hub : pattern === "loop" ? loop : ["tree", "split"].includes(pattern) ? tree : chain).slice(0, count);
}

function connector(from, to, unit, color = c.cyan) {
  const [x1, y1] = from, [x2, y2] = to, mx = (x1 + x2) / 2;
  return path(`M ${x1} ${y1} H ${mx} V ${y2} H ${x2}`, color, Math.max(5, unit * .075), `marker-end="url(#arrow)"`);
}

function scene(pattern, items, width, height, unit) {
  const points = positions(pattern, width, height, unit, items.length), centers = points.map(([x, y]) => [x + unit * .9, y + unit * .66]);
  if (pattern === "cage") return joinParts([rr(unit * .55, unit * .55, width - unit * 1.1, height - unit * 1.1, c.mapSurface, unit * .34, `stroke="${c.yellow}" stroke-width="7"`), points.map((point, index) => icon(items[index], point[0], point[1], unit)), centers.slice(0, -1).map((point, index) => connector(point, centers[index + 1], unit, items[index] === "danger" ? c.coral : c.cyan))]);
  const wires = pattern === "hub" ? centers.slice(1).map((point) => connector(centers[0], point, unit)) : centers.slice(0, -1).map((point, index) => connector(point, centers[index + 1], unit, items[index] === "danger" ? c.coral : c.cyan));
  if (pattern === "loop" && centers.length > 2) wires.push(connector(centers.at(-1), centers[0], unit, c.green));
  return joinParts([wires, points.map((point, index) => icon(items[index], point[0], point[1], unit))]);
}

function svg(width, height, pattern, items) {
  const unit = Math.max(56, Math.round(Math.min(width, height) / 8.5));
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}"><defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="${c.cyan}"/></marker></defs>${r(0, 0, width, height, c.surface)}<circle cx="${width * .09}" cy="${height * .15}" r="${unit * .32}" fill="${c.surfaceAccent}"/><circle cx="${width * .9}" cy="${height * .84}" r="${unit * .44}" fill="${c.warmAccent}"/>${rr(unit * .38, unit * .46, width - unit * .76, height - unit * .76, c.shadow, unit * .34)}${rr(unit * .38, unit * .38, width - unit * .76, height - unit * .76, c.paper, unit * .34)}<g>${scene(pattern, items, width, height, unit)}</g></svg>`;
}

const temp = mkdtempSync(join(tmpdir(), "easyai-clarity-diagrams-"));
try {
  for (const item of clarityScenes) for (const [ratio, width, height] of sizes) {
    const base = `${item.number}-${item.slug}-${item.version}-clarity-${ratio}`;
    const source = join(temp, `${base}.svg`);
    writeFileSync(source, svg(width, height, item.pattern, item.items));
    execFileSync("sips", ["-s", "format", "png", source, "--out", join(out, `${base}.png`)], { stdio: "ignore" });
  }
} finally {
  rmSync(temp, { recursive: true, force: true });
}
