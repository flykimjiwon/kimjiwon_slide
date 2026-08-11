import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const packDir = dirname(fileURLToPath(import.meta.url));
const easyAiDir = resolve(packDir, "../..");
const indexPath = join(easyAiDir, "index.html");

const cover = {
  file: "01-cover-pixel-crew.png",
  alt: "설계 테이블을 중심으로 역할을 나눠 협업하는 픽셀크루 팀",
};

const visuals = [
  {
    file: "02-context-window-pixel-crew.png",
    alt: "컨텍스트 창의 토큰과 용량 한계를 함께 관리하는 픽셀크루 팀",
  },
  {
    file: "03-grounding-pixel-crew.png",
    alt: "두 출처를 조사하고 신뢰할 근거와 제외할 근거를 나누는 픽셀크루 팀",
  },
  {
    file: "04-multiagent-pixel-crew.png",
    alt: "리드가 빌더·검증자·리서처·기록자에게 작업을 위임하고 결과를 모으는 픽셀크루 팀",
  },
  {
    file: "05-mcp-a2a-pixel-crew.png",
    alt: "도구 허브에 연결하고 전문 역할 사이에서 작업을 릴레이하는 픽셀크루 팀",
  },
  {
    file: "06-rag-search-pixel-crew.png",
    alt: "질문에서 문서 검색과 검증을 거쳐 근거 있는 답을 만드는 픽셀크루 팀",
  },
  {
    file: "07-memory-wiki-pixel-crew.png",
    alt: "검색한 자료를 검증하고 분류해 위키 선반에 적재하는 픽셀크루 팀",
  },
  {
    file: "08-context-compaction-pixel-crew.png",
    alt: "가득 찬 컨텍스트를 핵심 정보만 남긴 작은 요약으로 압축하는 픽셀크루 팀",
  },
  {
    file: "09-loop-harness-pixel-crew.png",
    alt: "계획·승인·실행·관측·기록 단계를 반복하며 결과를 개선하는 픽셀크루 팀",
  },
];

const loopVisuals = [
  {
    file: "10-loop-repair-pixel-crew.png",
    alt: "목표 설정부터 구현과 실제 검증을 거쳐 실패 시 수리하고 성공 시 완료하는 픽셀크루 팀",
    ariaLabel: "루프 엔지니어링 픽셀크루 삽화 크게 보기",
    caption: "픽셀크루 · 설계자, 빌더, 검증자가 실패 원인을 수리해 다시 실행하고 통과할 때만 완료합니다.",
  },
  {
    file: "11-prompt-optimization-pixel-crew.png",
    alt: "프롬프트 후보를 평가하고 탈락한 후보를 다시 써 가장 좋은 하나를 고르는 픽셀크루 팀",
    ariaLabel: "자동 프롬프트 최적화 픽셀크루 삽화 크게 보기",
    caption: "픽셀크루 · 후보를 기계로 평가하고 탈락한 것은 다시 쓰며 가장 좋은 하나만 선택합니다.",
  },
];

function dataUri(filename) {
  const bytes = readFileSync(join(packDir, filename));
  return `data:image/png;base64,${bytes.toString("base64")}`;
}

function replaceImage(match, item) {
  const withAlt = match.replace(/\balt="[^"]*"/, `alt="${item.alt}"`);
  return withAlt.replace(/\bsrc="[^"]*"/, `src="${dataUri(item.file)}"`);
}

let html = readFileSync(indexPath, "utf8");

let coverCount = 0;
html = html.replace(/<img class="ghost-cover"[^>]*>/g, (match) => {
  coverCount += 1;
  return replaceImage(match, cover);
});

let visualIndex = 0;
html = html.replace(
  /(<figure class="ghost-visual[^>]*>\s*)<img\b[^>]*>/g,
  (match, figurePrefix) => {
    const item = visuals[visualIndex];
    if (!item) {
      throw new Error("EASY AI contains more ghost visuals than the redraw mapping.");
    }
    const image = match.slice(figurePrefix.length);
    visualIndex += 1;
    return `${figurePrefix}${replaceImage(image, item)}`;
  },
);

if (coverCount !== 1 || visualIndex !== visuals.length) {
  throw new Error(
    `Expected 1 cover and ${visuals.length} visuals, found ${coverCount} cover and ${visualIndex} visuals.`,
  );
}

const oldMultiagentCaption =
  "유령 팀 · 팀장이 일을 나눠 맡기고, 끝난 결과를 다시 모읍니다.";
const newMultiagentCaption =
  "픽셀크루 팀 · 역할을 나눠 맡고, 결과를 다시 모읍니다.";
if (html.includes(oldMultiagentCaption)) {
  html = html.replace(oldMultiagentCaption, newMultiagentCaption);
} else if (!html.includes(newMultiagentCaption)) {
  throw new Error("Could not find the multiagent Pixel Crew caption.");
}

const loopStart = html.indexOf('<section class="chapter" id="chloop">');
const graphStart = html.indexOf('<section class="chapter" id="chgraph">', loopStart);
if (loopStart < 0 || graphStart < 0) {
  throw new Error("Could not find the Loop and Graph Engineering chapter boundaries.");
}

let loopHtml = html.slice(loopStart, graphStart);
let loopVisualIndex = 0;
loopHtml = loopHtml.replace(
  /(<figure class="surface-card"><button\b[^>]*>)<img\b[^>]*>/g,
  (match, buttonPrefix) => {
    const item = loopVisuals[loopVisualIndex];
    if (!item) {
      throw new Error("Loop chapter contains more surface visuals than the redraw mapping.");
    }
    const button = buttonPrefix
      .replace(/\bdata-cap="[^"]*"/, `data-cap="${item.caption}"`)
      .replace(/\baria-label="[^"]*"/, `aria-label="${item.ariaLabel}"`);
    const image = match.slice(buttonPrefix.length);
    loopVisualIndex += 1;
    return `${button}${replaceImage(image, item)}`;
  },
);

if (loopVisualIndex !== loopVisuals.length) {
  throw new Error(
    `Expected ${loopVisuals.length} loop visuals, found ${loopVisualIndex}.`,
  );
}

html = `${html.slice(0, loopStart)}${loopHtml}${html.slice(graphStart)}`;

writeFileSync(indexPath, html);
console.log(
  `Embedded ${coverCount + visualIndex + loopVisualIndex} Pixel Crew images into ${indexPath}`,
);
