---
name: structured-writing
description: "Guides writing academic papers through top-down structure decomposition and node-by-node execution. Decomposes the paper into a hierarchical structure tree (chapter → section → subsection → paragraph), assigns rhetorical modes to leaf nodes, then writes each node in depth-first order. Replaces fixed-template writing with adaptive structure driven by content."
---

# Structured Writing: Top-Down Decomposition + Node Execution

Write academic papers by first decomposing the structure top-down, then executing each node in the structure tree. No fixed templates — the structure emerges from the content.

## When to Use

- User asks to write or draft a paper
- User wants to organize a paper's structure before writing
- User mentions "structured writing", "decompose paper", "outline first"

## When NOT to Use

- Running experiments → use `experiment-pipeline`
- Paper planning/story design → use `paper-planning`
- Self-reviewing a finished draft → use `paper-review`
- Responding to reviewer comments → use `paper-rebuttal`

---

## Core Principles

1. **Structure before content** — Always complete structure decomposition before writing a single paragraph
2. **Content drives structure** — The number of chapters, sections, and subsections is determined by the research content, not a fixed template
3. **Every leaf node declares its rhetorical mode** — No paragraph is written without first stating how it will be organized
4. **Depth-first execution** — Write each branch completely before moving to the next

---

## The Two Phases

```
Phase A: Structure Decomposition
    ↓  (hard gate: structure.md must exist and be complete)
Phase B: Node Execution
```

---

## Phase A: Structure Decomposition

<HARD-GATE>
Do NOT write any paragraph content until the full structure tree is decomposed down to the paragraph level and saved to `/structure.md`. Writing content before the structure is complete is the most common failure mode.
</HARD-GATE>

### Step A1: Gather Inputs

Read and understand the available research materials:

- Experiment plans and results
- Method descriptions
- Research goals and claims
- Any existing outlines or story summaries
- Academic memory files (injected via middleware, e.g. TASTE.md, WRITER.md)

### Step A2: Determine Chapter-Level Structure

Based on the research content, decide:

1. **What chapters does this paper need?** — Not every paper needs all 7 traditional sections. A short paper might only need 4; a journal article might need 10.
2. **What is the logical order?** — The order should serve the narrative, not a convention.
3. **What is each chapter's purpose?** — One sentence per chapter describing what it must accomplish.

Write each chapter as a top-level node in the structure tree.

### Step A3: Decompose Each Chapter

For each chapter, decide whether it needs subsections:

- **If the chapter covers a single coherent topic** → do NOT split into subsections; go directly to paragraph-level decomposition
- **If the chapter covers multiple distinct topics or modules** → split into subsections, then decompose each subsection

Repeat this decision recursively for each subsection.

See `references/decomposition-guide.md` for decision criteria.

### Step A4: Decompose to Paragraph Level

For each leaf section (a section/subsection with no children), determine:

1. **How many paragraphs?** — Each paragraph conveys exactly one message
2. **What is each paragraph's rhetorical mode?** — Declare the organizational pattern (see `references/rhetorical-modes.md`)
3. **What are the key points?** — List the specific points this paragraph must convey

### Step A5: Write Structure Document

Save the complete structure tree to `/structure.md` following the format in `references/structure-spec.md`.

<HARD-GATE>
After writing `/structure.md`, verify:
- Every leaf node has a `rhetorical_mode` declared
- Every leaf node has at least one `key_point`
- No node has a placeholder (TBD, TODO, etc.)
- The structure covers all research content that must be in the paper

If any check fails, fix the structure before proceeding to Phase B.
</HARD-GATE>

---

## Phase B: Node Execution

### Step B1: Read Structure

Read `/structure.md` and understand the complete tree.

### Step B2: Depth-First Traversal

Traverse the structure tree in depth-first order. For each node:

**Non-leaf node (chapter/section/subsection):**
- Write the section heading
- Write a brief introductory sentence if the section needs one (optional, not every section does)
- Proceed to children

**Leaf node (paragraph):**
1. Read the node's `rhetorical_mode` and `key_points`
2. Read `references/rhetorical-modes.md` if you want guidance on the declared mode
3. Write the paragraph following the declared mode and key points
4. After writing, run the quality self-check (see below)

### Step B3: Assemble

After all nodes are written, assemble the full paper. Remove the section heading markers from the structure tree and produce the final Markdown document.

### Step B4: Final Review

Read the assembled paper end-to-end. Check:

- [ ] Every claim in Abstract/Introduction is supported by evidence in the paper
- [ ] Terminology is consistent throughout
- [ ] Paragraph flow is smooth — each paragraph connects to the next
- [ ] No section is disproportionately short or long relative to its importance
- [ ] The paper tells a coherent story, not just a collection of sections

### Step B5: Clean Up

Delete `/structure.md` — it is a temporary working file.

---

## Quality Self-Check (Per Paragraph)

After writing each paragraph, verify:

- [ ] Does this paragraph convey exactly the key points declared in the structure?
- [ ] Does it follow the declared rhetorical mode?
- [ ] Is the first sentence a clear topic sentence?
- [ ] Does every sentence advance the paragraph's message?
- [ ] Are there unsupported claims? If yes, add a TODO marker or remove the claim
- [ ] Is the terminology consistent with the rest of the paper?

See `references/writing-quality.md` for the complete checklist.

---

## Hard Gates Summary

| Gate | Location | Check |
|------|----------|-------|
| No writing before structure | Start of Phase B | `/structure.md` exists and is complete |
| Leaf node completeness | End of Step A5 | Every leaf has `rhetorical_mode` + `key_points` |
| No placeholders | End of Step A5 | No TBD/TODO in structure |
| Per-paragraph quality | After each paragraph | Self-check list passed |

---

## Writing Principles

1. **One message per paragraph** — Each paragraph conveys exactly one point
2. **Topic sentence first** — The first sentence tells readers what this paragraph is about
3. **No fabricated results or citations** — If something is missing, add a TODO with the exact command needed
4. **Terminology consistency** — Use the same term throughout; do not alternate names
5. **Underclaim in prose, overdeliver in evidence** — Let tables and figures carry the strength
6. **Lead with mechanism, not only metric** — Explain why the method works before listing numbers
7. **State one meaningful limitation** — Controlled limitations increase credibility

---

## Reference Navigation

| Topic | Reference File | When to Load |
|-------|---------------|-------------|
| Structure tree format | `references/structure-spec.md` | Step A5: Writing structure document |
| Rhetorical modes | `references/rhetorical-modes.md` | Step A4: Choosing paragraph modes |
| Decomposition decisions | `references/decomposition-guide.md` | Step A3: Whether to split into subsections |
| Writing quality | `references/writing-quality.md` | After each paragraph, and Step B4 |
