import { semanticScenes } from "./metaphor-catalogue.mjs";

const canonicalScenes = {
  "01": ["chain", ["window", "tokens", "document", "core"]], "02": ["split", ["document", "check", "cloud", "core"]],
  "03": ["loop", ["plan", "agent", "observe", "core"]], "04": ["hub", ["agent", "port", "server", "core"]],
  "05": ["cage", ["rail", "check", "danger", "core"]], "06": ["tree", ["agent", "agent", "agent", "core"]],
  "07": ["hub", ["agent", "shelf", "lens", "core"]], "08": ["chain", ["noise", "funnel", "document", "core"]],
  "09": ["hub", ["document", "toolwall", "rule", "core"]], "10": ["chain", ["agent", "plug", "server", "core"]],
  "11": ["hub", ["key", "document", "prompt", "core"]], "12": ["chain", ["agent", "bridge", "server", "core"]],
  "13": ["chain", ["agent", "card", "agent", "core"]], "14": ["chain", ["key", "gate", "check", "core"]],
  "15": ["chain", ["noise", "frame", "document", "core"]], "16": ["loop", ["danger", "wrench", "check", "core"]],
  "17": ["chain", ["core", "packets", "document", "core"]], "18": ["tree", ["plan", "route", "agent", "core"]],
  "19": ["tree", ["agent", "agent", "agent", "agent"]], "20": ["chain", ["agent", "turnstile", "stamp", "core"]],
  "21": ["cage", ["check", "danger", "scanner", "core"]], "22": ["chain", ["agent", "trace", "document", "core"]],
  "23": ["cage", ["agent", "server", "danger", "core"]], "24": ["hub", ["document", "tiles", "vector", "core"]],
  "25": ["tree", ["document", "switch", "core", "core"]], "26": ["chain", ["document", "cache", "core"]],
  "27": ["loop", ["seed", "document", "archive", "rule"]], "28": ["hub", ["board", "agent", "agent", "core"]],
  "29": ["chain", ["plug", "baton", "agent", "core"]], "30": ["cage", ["obstacle", "agent", "gate", "core"]]
};

export const clarityScenes = semanticScenes.flatMap(([number, slug, metaphorA, metaphorB]) => {
  const [canonicalPattern, canonicalItems] = canonicalScenes[number];
  return [
    { number, slug, version: "canonical", pattern: canonicalPattern, items: canonicalItems },
    { number, slug, version: "metaphor-a", pattern: metaphorA[1], items: metaphorA[2] },
    { number, slug, version: "metaphor-b", pattern: metaphorB[1], items: metaphorB[2] }
  ];
});
