// allow: SIZE_OK — deterministic renderer for the declarative semantic pixel-art catalogue.
import { execFileSync } from "node:child_process";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { semanticScenes } from "./metaphor-catalogue.mjs";
import { pixelAccents, pixelColors } from "./pixel-tokens.mjs";
import { glyphForName } from "./semantic-glyphs.mjs";

const out = dirname(fileURLToPath(import.meta.url));
const sizes = [["wide", 1672, 941], ["square", 941, 941], ["portrait", 753, 941]];
const c = pixelColors;
const paint = pixelAccents;
const r = (x, y, w, h, fill) => `<rect x="${Math.round(x)}" y="${Math.round(y)}" width="${Math.max(1, Math.round(w))}" height="${Math.max(1, Math.round(h))}" fill="${fill}"/>`;
const joinParts = (parts) => parts.flat(Infinity).filter(Boolean).join("");
const hash = (word) => [...word].reduce((total, char) => total + char.charCodeAt(0), 0);

function grid(width, height, u) {
  const dots = [];
  for (let y = u * 2; y < height; y += u * 5) for (let x = u * 2; x < width; x += u * 5) if ((x / (u * 5) + y / (u * 5)) % 2 < 1) dots.push(r(x, y, Math.max(4, u / 2), Math.max(4, u / 2), c.grid));
  return dots.join("");
}

function frame(x, y, w, h, accent = c.line) {
  return joinParts([r(x + 8, y + 8, w, h, c.shadow), r(x, y, w, h, c.panel), r(x, y, w, 9, accent), r(x, y, 9, h, accent), r(x + w - 9, y, 9, h, accent), r(x, y + h - 9, w, 9, accent)]);
}

function line(from, to, u, color = c.cyan) {
  const [x1, y1] = from, [x2, y2] = to;
  return joinParts([r(Math.min(x1, x2), y1 - u / 2, Math.abs(x2 - x1) || u, u, color), r(x2 - u / 2, Math.min(y1, y2), u, Math.abs(y2 - y1) || u, color), r(x2 - u, y2 - u, u * 2, u * 2, color)]);
}

function arrow(from, to, u, color = c.cyan) {
  const head = from[0] <= to[0] ? r(to[0] - u * 2, to[1] - u * 2, u * 2, u * 4, color) : r(to[0], to[1] - u * 2, u * 2, u * 4, color);
  return joinParts([line(from, to, u, color), head]);
}

function core(x, y, u) {
  return joinParts([r(x - u * 3 + 8, y - u * 3 + 8, u * 6, u * 6, c.shadow), r(x - u * 3, y - u * 3, u * 6, u * 6, c.cyan), r(x - u * 2, y - u * 2, u * 4, u * 4, c.blue), r(x - u, y - u, u * 2, u * 2, c.deep), r(x - u / 3, y - u / 3, u * 2 / 3, u * 2 / 3, c.white)]);
}

function check(x, y, u, color = c.green) {
  return joinParts([r(x, y + u, u, u, color), r(x + u, y + u * 2, u, u, color), r(x + u * 2, y, u, u * 3, color)]);
}

function danger(x, y, u) {
  return joinParts([frame(x, y, u * 8, u * 8, c.coral), r(x + u * 2, y + u * 2, u, u, c.coral), r(x + u * 3, y + u * 3, u, u, c.coral), r(x + u * 4, y + u * 4, u, u, c.coral), r(x + u * 4, y + u * 2, u, u, c.coral), r(x + u * 3, y + u * 3, u, u, c.coral), r(x + u * 2, y + u * 4, u, u, c.coral)]);
}

function ghost(x, y, u, fill = c.sky) {
  const rows = [[3, 0, 6], [2, 1, 8], [1, 2, 10], [1, 3, 10], [1, 4, 10], [1, 5, 10], [1, 6, 10], [1, 7, 10], [1, 8, 2], [4, 8, 4], [9, 8, 2]];
  return joinParts([rows.map(([col, row, width]) => [r(x + (col + .5) * u, y + (row + .5) * u, width * u, u, c.shadow), r(x + col * u, y + row * u, width * u, u, fill)]), r(x + u * 3, y + u * 3, u * 2, u, c.white), r(x + u * 4, y + u * 4, u, u, c.ink), r(x + u * 7, y + u * 3, u * 2, u, c.white), r(x + u * 7, y + u * 4, u, u, c.ink), r(x + u * 2, y + u * 5, u, u, c.pink), r(x + u * 9, y + u * 5, u, u, c.pink)]);
}

function document(x, y, u, accent = c.cyan) {
  return joinParts([r(x + 6, y + 6, u * 8, u * 10, c.shadow), r(x, y, u * 8, u * 10, c.white), r(x, y, u * 8, u, accent), [3, 5, 7].map((row) => r(x + u * 2, y + u * row, u * 4.5, u / 2, c.line))]);
}

function server(x, y, u) {
  return joinParts([frame(x, y, u * 9, u * 12, c.blue), [2, 5, 8].map((row) => [r(x + u * 2, y + u * row, u * 5, u, c.sky), r(x + u * 7, y + u * row, u, u, c.green)])]);
}

const families = {
  agent: new Set(["ghost", "badge"]), paper: new Set(["document", "summary", "prompt", "card", "plan", "orders", "mail"]), rack: new Set(["server", "shelf", "archive", "toolwall", "drawers", "pantry", "vector", "directory"]), round: new Set(["compass", "lens", "gear", "spiral", "core"]), link: new Set(["plug", "key", "baton", "bridge", "pipe", "bucket", "anchor", "port"]), guard: new Set(["rail", "filter", "gate", "checkpoint", "turnstile", "screen", "obstacle", "pen", "aquarium", "scanner"]), pack: new Set(["bag", "tokens", "noise", "cube", "bins", "tiles", "stack", "coat"]), trail: new Set(["trace", "packets", "train", "route", "switch", "postal", "funnel", "press", "mold", "wrench", "seed", "campfire", "board", "dispatcher", "elevator", "window", "map", "pin", "org"])
};

function familyFor(name) {
  return Object.entries(families).find(([, items]) => items.has(name))?.[0] || "paper";
}

function glyph(name, x, y, u) {
  const specific = glyphForName({ name, x, y, u, c, paint, hash, r, frame, core, check, danger, ghost, document, server });
  if (specific) return specific;
  if (name === "core") return core(x + u * 4, y + u * 4, u);
  if (name === "ghost") return ghost(x, y, u);
  if (name === "danger") return danger(x, y, u);
  if (name === "check" || name === "rule") return joinParts([frame(x, y, u * 8, u * 8, c.green), check(x + u * 2, y + u * 2, u)]);
  if (name === "document" || name === "summary" || name === "prompt") return document(x, y, u, name === "summary" ? c.green : name === "prompt" ? c.pink : c.cyan);
  if (name === "server") return server(x, y, u);
  const accent = paint[hash(name) % paint.length], family = familyFor(name);
  if (family === "agent") return joinParts([ghost(x, y, u, accent), r(x + u * 5, y + u, u * 2, u * 2, c.yellow)]);
  if (family === "rack") return joinParts([frame(x, y, u * 10, u * 9, accent), [2, 4, 6].map((row) => [r(x + u * 2, y + u * row, u * 6, u, c.white), r(x + u * 8, y + u * row, u, u, c.green)])]);
  if (family === "round") return joinParts([frame(x, y, u * 9, u * 9, accent), r(x + u * 2, y + u * 2, u * 5, u * 5, c.white), r(x + u * 3, y + u * 3, u * 3, u * 3, accent), r(x + u * 4, y + u * 4, u, u, c.deep)]);
  if (family === "link") return joinParts([r(x + u, y + u * 3, u * 8, u * 2, accent), r(x + u * 3, y + u, u * 3, u * 6, accent), r(x + u * 4, y + u * 2, u, u * 2, c.white), r(x + u * 4, y + u * 5, u, u * 2, c.yellow)]);
  if (family === "guard") return joinParts([frame(x, y, u * 11, u * 9, accent), r(x + u * 2, y + u * 2, u, u * 6, c.yellow), r(x + u * 8, y + u * 2, u, u * 6, c.yellow), r(x + u * 2, y + u * 4, u * 7, u, c.white), check(x + u * 4, y + u * 5, u / 2)]);
  if (family === "pack") return joinParts([frame(x, y + u, u * 10, u * 7, accent), r(x + u * 3, y, u * 4, u * 2, accent), [2, 4, 6].map((row) => r(x + u * 2, y + u * row, u * 6, u / 2, c.white))]);
  if (family === "trail") return joinParts([frame(x, y, u * 11, u * 8, accent), [1, 3, 5, 7, 9].map((col, index) => r(x + u * col, y + u * (2 + (index % 2) * 2), u, u, paint[(hash(name) + index) % paint.length]))]);
  return document(x, y, u, accent);
}

function positions(pattern, width, height, u, count) {
  const cx = width / 2, cy = height / 2, portrait = height > width * 1.15;
  const chain = portrait ? Array.from({ length: count }, (_, index) => [cx - u * 5, u * 6 + index * ((height - u * 26) / Math.max(1, count - 1))]) : Array.from({ length: count }, (_, index) => [u * 6 + index * ((width - u * 22) / Math.max(1, count - 1)), cy - u * 4]);
  const hub = [[cx - u * 5, cy - u * 5], [u * 6, u * 7], [width - u * 15, u * 7], [cx - u * 5, height - u * 14]];
  const loop = [[cx - u * 14, cy - u * 10], [cx + u * 5, cy - u * 10], [cx + u * 5, cy + u * 5], [cx - u * 14, cy + u * 5]];
  const tree = portrait ? [[cx - u * 5, u * 5], [cx - u * 15, cy - u * 2], [cx + u * 5, cy - u * 2], [cx - u * 5, height - u * 14]] : [[cx - u * 5, u * 5], [u * 6, cy], [cx - u * 5, cy], [width - u * 15, cy]];
  return (pattern === "hub" ? hub : pattern === "loop" ? loop : pattern === "tree" ? tree : chain).slice(0, count);
}

function scene(pattern, items, width, height, u) {
  if (pattern === "cage") return joinParts([frame(u * 5, u * 5, width - u * 10, height - u * 10, c.yellow), glyph(items[0], width / 2 - u * 5, height / 2 - u * 5, u), glyph(items[1], u * 8, height / 2 - u * 5, u), items[2] ? glyph(items[2], width - u * 16, height / 2 - u * 5, u) : "", danger(width - u * 12, u * 7, u)]);
  const pts = positions(pattern, width, height, u, items.length);
  const wires = pattern === "hub" ? pts.slice(1).map((pt) => arrow([pts[0][0] + u * 5, pts[0][1] + u * 4], [pt[0] + u * 5, pt[1] + u * 4], Math.max(8, u / 2))) : pts.slice(0, -1).map((pt, index) => arrow([pt[0] + u * 5, pt[1] + u * 4], [pts[index + 1][0] + u * 5, pts[index + 1][1] + u * 4], Math.max(8, u / 2), items[index] === "danger" ? c.coral : c.cyan));
  return joinParts([wires, pts.map((pt, index) => glyph(items[index], pt[0], pt[1], u))]);
}

function makeSvg(width, height, pattern, items) {
  const u = height > width * 1.15
    ? Math.max(12, Math.floor(width / 50))
    : width > height * 1.15
      ? Math.max(16, Math.floor(height / 34))
      : Math.max(16, Math.floor(width / 45));
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" shape-rendering="crispEdges">${r(0, 0, width, height, c.canvas)}${grid(width, height, u)}${scene(pattern, items, width, height, u)}</svg>`;
}

const temp = mkdtempSync(join(tmpdir(), "easyai-semantic-pixels-"));
try {
  for (const [number, slug, a, b] of semanticScenes) for (const [version, label, pattern, items] of [["metaphor-a", ...a], ["metaphor-b", ...b]]) for (const [ratio, width, height] of sizes) {
    const base = `${number}-${slug}-${version}-${ratio}`;
    const source = join(temp, `${base}.svg`);
    writeFileSync(source, makeSvg(width, height, pattern, items));
    execFileSync("sips", ["-s", "format", "png", source, "--out", join(out, `${base}.png`)], { stdio: "inherit" });
  }
} finally {
  rmSync(temp, { recursive: true, force: true });
}
