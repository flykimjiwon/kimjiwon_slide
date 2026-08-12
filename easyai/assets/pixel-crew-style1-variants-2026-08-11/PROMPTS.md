# Prompt Set

## A/B 공통 스타일 프롬프트

```text
Use case: scientific-educational
Asset type: 16:9 landscape illustration for a Korean AI engineering presentation
Input images: Image 1 is the only style reference. Match its exact visual language, character proportions, rendering, and palette; Image 2 is a concept reference only and must not control the style.
Style/medium: premium 3D voxel pixel art on a deep navy-black background, subtle square dot grid, luminous cyan right-angle signal paths, electric blue core light, softly beveled block pixels, clean cinematic glow. Use the same cute rectangular Pixel Crew: cyan architect, yellow builder, coral validator, purple researcher, green records operator; square white eyes with black square pupils, tiny pink square cheeks, block arms and three-prong block feet.
Composition/framing: exactly 16:9 landscape, 1672×941 preferred, generous safe margins, one instantly readable educational metaphor, no cropping of characters or key props.
Constraints: create a brand-new scene, not an edit. No readable text, letters, numbers, logos, trademarks, watermark, interface screenshot, speech bubbles, maze, pellets, PAC-MAN references, or round ghost silhouettes. Do not add extra visual styles.
```

## 장면 프롬프트

각 문장은 위 공통 프롬프트의 `Primary request` 뒤에 붙여 사용했습니다.

| 파일 | Primary request |
| --- | --- |
| `01-cover-a.png` | Five Pixel Crew specialists gather around a glowing horizontal system blueprint table while the cyan architect points from the blueprint to a floating blue intelligence core. Clear symmetrical hero composition; teamwork and AI engineering planning are obvious at a glance. |
| `01-cover-b.png` | Stage the five Pixel Crew specialists in a shallow mission-control semicircle, each contributing one tool or evidence object as cyan signal paths converge into a suspended electric-blue core above a compact project map. More dynamic diagonal composition than variant A while remaining calm and presentation-ready. |
| `02-context-window-a.png` | Show a finite glowing glass-like tray with a strict rectangular capacity; the crew carefully selects a few document, image, code, and message tiles to fit inside while excess tiles wait outside. The boundary and limited capacity must be instantly readable without text. |
| `02-context-window-b.png` | Depict a luminous rectangular aperture into the AI core: only the most relevant information blocks pass through the opening while older and low-priority blocks fade into a neat waiting rail outside. Use a clear left-to-right educational flow, no text. |
| `03-grounding-a.png` | The crew pins a small set of trusted evidence cards to a glowing claim core using straight cyan connectors; the purple researcher verifies a source with a magnifier and the green records operator holds the source trail. Make evidence-to-answer linkage unmistakable. |
| `03-grounding-b.png` | In a compact evidence library, the crew retrieves only verified document tiles from illuminated shelves and feeds them through a cyan validation gate into the blue intelligence core. Clear left-to-right flow and visible rejected dim tiles, no text. |
| `04-multiagent-a.png` | Five color-coded specialists work simultaneously around one shared plan: research, architecture, building, validation, and records. Their cyan task lines remain distinct and converge cleanly on one finished artifact in the center. |
| `04-multiagent-b.png` | Arrange the five specialists as connected work cells in a relay: evidence passes to planning, then construction, testing, and final record. Use a dynamic diagonal handoff composition with one shared state token traveling between them. |
| `05-mcp-a2a-a.png` | Show two layers clearly without text: standardized plug-like adapters connect agents to tools and data sources below, while peer-to-peer cyan bridges connect agent characters to one another above. The cyan architect demonstrates both connection types. |
| `05-mcp-a2a-b.png` | Build a glowing protocol transit hub: tool/data ports dock around the outside, agent workstations connect across the center, and standardized cyan connector blocks allow different shapes to interoperate. Keep it architectural and instantly legible. |
| `06-rag-search-a.png` | The purple researcher scans an indexed wall of document tiles, selects three relevant evidence blocks, and routes them through cyan ranking lanes into the blue answer core while irrelevant documents remain dim. |
| `06-rag-search-b.png` | Use a radar-like cyan search beam over a field of document blocks; the crew ranks and retrieves only the nearest relevant pieces into a compact context tray beside the AI core. Strong focal hierarchy, no literal text. |
| `07-memory-wiki-a.png` | The green records operator and purple researcher maintain a shared illuminated knowledge cabinet; new fact tiles are checked, indexed, and placed into organized slots that every crew member can access through cyan paths. |
| `07-memory-wiki-b.png` | Show a living knowledge tree made of linked notebook and document blocks: the crew adds one verified memory, updates a nearby branch, and retrieves an older fact for the blue core. Emphasize persistent shared knowledge without text. |
| `08-context-compaction-a.png` | A long bulky rail of message, code, image, and tool-result blocks enters a luminous cyan compression chamber; the crew preserves only key facts and outputs one compact bright summary capsule toward the AI core. |
| `08-context-compaction-b.png` | Use a clear funnel metaphor: many large context tiles are sorted by the crew, duplicates and noise move to a dim side tray, and a small dense stack containing the essential colored signals exits toward the blue core. |
| `09-loop-harness-a.png` | Place build, test, inspect, and repair stations on a cyan closed loop around the AI core, enclosed by visible permission guardrails and a tool dock. A glowing state block advances checkpoint by checkpoint until the validator passes it. |
| `09-loop-harness-b.png` | Build a protected circular work track inside a rectangular safety frame: the cyan architect sets the goal, yellow builder changes the artifact, coral validator tests it, and failures route back while permissions and tools remain visibly bounded. |
| `10-loop-repair-a.png` | A red failed-test block leaves the validator, follows a cyan return path to the yellow builder's repair bench, then rejoins the build-test loop as a green checked artifact. Show failure, repair, and retry as one clear cycle. |
| `10-loop-repair-b.png` | The crew diagnoses a cracked code cube under a magnifier, repairs it with pixel tools, and sends it through a compact test gate again; the before-and-after state is linked by one luminous return arrow, no text. |
| `11-prompt-optimization-a.png` | Several abstract instruction tiles enter parallel evaluation gates; the coral validator scores them using only colored bars and symbols, weak candidates return for revision, and one bright best candidate reaches the blue core. No letters or words. |
| `11-prompt-optimization-b.png` | Show an evolutionary branching tree of abstract prompt blocks: the crew mutates and tests each branch, dim branches stop, and the strongest clean branch converges on a glowing selected tile. Use symbols only, no literal text. |
| `12-graph-system-map-a.png` | Build a clear top-down network of agent characters, tool stations, data stores, one human review node, and a glowing state token traveling along cyan edges. Keep the central architecture highly legible and balanced. |
| `12-graph-system-map-b.png` | Create an isometric orchestration control room: the cyan architect surveys a layered node-and-edge map connecting agents, tools, tests, memory, and human approval, with one bright state cube marking the current position. |
| `13-graph-fanout-join-a.png` | One incoming task cube splits into four cyan lanes toward specialist Pixel Crew members; their distinct outputs then converge through a precise join gate into one polished result cube. Strong symmetric diagram composition. |
| `13-graph-fanout-join-b.png` | Arrange four specialist workbenches across the scene after a single task distributor; finished component blocks travel on separate rails and lock together at the right into one complete artifact. Dynamic left-to-right flow. |
| `14-human-checkpoint-a.png` | An agent workflow visibly pauses at a luminous cyan approval gate where a human reviewer hand and control panel examine the artifact; approved work continues toward the blue core while the crew waits behind the boundary. |
| `14-human-checkpoint-b.png` | Stage a staffed review station at a fork: the human reviewer can route the current state cube forward to execution or back to the repair crew. Make pause, review, and decision obvious using shapes and lighting only. |
| `15-failure-routing-state-a.png` | A glowing state cube arrives at a central switch and, according to the visible failure shape, routes along separate cyan paths to retry, specialist repair, human review, or safe stop nodes. The crew monitors each distinct destination. |
| `15-failure-routing-state-b.png` | Use an isometric railway-switch metaphor: the current state token controls a cyan track junction while different failure artifacts are sent to a retry loop, repair bench, approval checkpoint, or locked terminal. Make cause-dependent routing obvious without text. |
| `16-graph-engineering-closing-a.png` | Create a panoramic finale: all five Pixel Crew members stand around a completed luminous execution graph that clearly connects several small loops, parallel branches, tool nodes, memory, tests, and one human approval gate into a single successful outcome. Heroic but calm, suitable for the very bottom of the presentation. |
| `16-graph-engineering-closing-b.png` | Show the crew on an elevated isometric orchestration control deck surveying a finished network of connected work loops below; cyan paths branch and rejoin around the blue intelligence core, with tools, state, failure recovery, and human review all visible as one coherent system. Strong closing tableau with generous margins. |

## C안 공통 스타일 프롬프트 · 손발 없는 원본형

```text
Use case: scientific-educational
Asset type: 16:9 landscape illustration for a Korean AI engineering presentation
Input images: Image 1 is the mandatory character anatomy and silhouette reference. Image 2 is only the premium 3D voxel material, lighting, palette, and background reference; ignore every limb shown in Image 2.
Hard anatomy lock: every colored crew character must be one uninterrupted rounded-rectangular pixel ghost body exactly like Image 1, ending only in a compact scalloped pixel hem. Absolutely zero external limbs or limb-like shapes: no arms, forearms, elbows, hands, fingers, gloves, shoulders, legs, knees, feet, shoes, boots, toes, side appendages, or separate blocks below the body. Props and tools float independently with visible air gaps or sit on autonomous stations; characters never hold or touch anything. Show action only through cyan paths, beams, tokens, and machines.
Style/medium: premium 3D voxel pixel art on a deep navy-black background, subtle square dot grid, luminous cyan right-angle signal paths, electric-blue core glow, softly beveled block pixels, clean cinematic light. Use body-only cyan, yellow, coral, purple, and green crew ghosts with square white eyes, black square pupils, and tiny pink cheeks.
Composition/framing: exactly 16:9 landscape, 1672×941 preferred, generous safe margins, no cropping.
Constraints: no readable text, letters, numbers, logos, trademarks, watermark, interface screenshot, speech bubbles, maze, pellets, PAC-MAN references, or round ghost silhouettes. Before rendering, check every character twice and remove any arm, hand, leg, or foot-like protrusion.
```

Image 1은 `../ghost-crew-hero.svg`를 1672×941 PNG로 변환한 실루엣 기준이며, Image 2는 `../pixel-crew-redraw-2026-08-10/01-cover-pixel-crew.png`입니다.

| 파일 | C안 Primary request |
| --- | --- |
| `01-cover-c.png` | Five body-only crew ghosts surround a glowing system-blueprint table; floating tools and evidence icons remain separate while cyan paths converge into a blue core. |
| `02-context-window-c.png` | A finite glowing tray accepts only selected information tiles while excess tiles wait outside; selection is performed by autonomous cyan lanes. |
| `03-grounding-c.png` | Trusted evidence cards connect directly to a claim core; a separate magnifier and records cabinet verify and preserve the source trail. |
| `04-multiagent-c.png` | Five body-only specialists occupy separate work cells whose task lines converge on one finished artifact. |
| `05-mcp-a2a-c.png` | Standardized adapters connect autonomous stations to tools and data below while cyan bridges connect body-only agent ghosts above. |
| `06-rag-search-c.png` | A cyan search beam selects and ranks three relevant documents into a context tray beside the answer core. |
| `07-memory-wiki-c.png` | Verified facts enter a shared knowledge cabinet, update linked memory, and return through cyan retrieval paths. |
| `08-context-compaction-c.png` | Bulky context tiles enter an autonomous compression chamber; noise moves aside and one compact summary exits. |
| `09-loop-harness-c.png` | Build, test, inspect, and repair stations form a guarded closed loop around the core while one state token advances through checkpoints. |
| `10-loop-repair-c.png` | A failed cube returns to an autonomous repair station and rejoins the test loop as a checked artifact; tools float separately. |
| `11-prompt-optimization-c.png` | Abstract instruction tiles pass through parallel evaluation gates; weak candidates return and one best candidate reaches the core. |
| `12-graph-system-map-c.png` | A balanced node-and-edge system links body-only crew, tools, data, an abstract human review bust, and one moving state token. |
| `13-graph-fanout-join-c.png` | One task splits into four specialist lanes and their separate outputs converge through an autonomous join gate. |
| `14-human-checkpoint-c.png` | A workflow pauses at an approval gate using only an abstract head-and-shoulders reviewer icon, never a human hand. |
| `15-failure-routing-state-c.png` | A central state switch routes distinct failure shapes to retry, repair, human review, or safe stop nodes. |
| `16-graph-engineering-closing-c.png` | Five body-only ghosts hover around a completed graph with loops, branches, tools, memory, tests, recovery, review, and one successful outcome. |
