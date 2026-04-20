# Decomposition Decision Guide

When decomposing the structure tree, the key decision at each node is: **should this node have children, or should it go directly to paragraph-level?** This guide provides criteria for that decision at every level.

---

## Chapter Level (Top-Level Sections)

### Decision: What chapters does the paper need?

**Input:** Research content, claims, experiment results.

**Process:**

1. List every major topic that must appear in the paper
2. Group related topics that belong together
3. Each group becomes a chapter

**Do NOT default to the traditional 7-section structure.** Common academic papers use Introduction → Method → Experiments → Conclusion, but a short paper might combine Method+Experiments, and a journal article might split Method into three chapters.

**Criteria for a chapter:**
- It addresses a distinct reader question (What's the problem? How does it work? Does it work? What does it mean?)
- It can stand as a coherent unit — removing it would leave a gap, not just shorten a section
- It typically spans multiple paragraphs

**Minimum:** 3 chapters (a paper with fewer is probably too short for this skill).
**Maximum:** No hard limit, but if you exceed 8, consider whether some should be subsections instead.

---

## Section Level

### Decision: Does this chapter need sections?

**Split into sections when:**
- The chapter covers **2 or more distinct topics** that each need their own narrative
- Different sections serve **different purposes** within the chapter (e.g., Method chapter: "Overview" vs. "Module A" vs. "Module B")
- A reader would expect **navigational headings** to find specific content

**Do NOT split into sections when:**
- The chapter covers a **single coherent topic** — e.g., a short Introduction that flows from motivation to contributions without needing subsections
- Splitting would create sections with only one paragraph each — that's over-fragmentation
- The chapter is naturally short (3-5 paragraphs)

### How many sections?

- **2-5 sections** is typical for a chapter
- If a chapter has 6+ sections, some might be better as subsections grouped under a parent section
- If a chapter has only 1 section, the section level is unnecessary — go directly to paragraphs

---

## Subsection Level

### Decision: Does this section need subsections?

Apply the same logic as sections, but one level deeper:

**Split into subsections when:**
- The section covers multiple sub-modules or sub-topics
- Each sub-module has its own motivation, design, and advantage (the Method three-element pattern)
- The section would be too long without sub-structure (typically >8 paragraphs)

**Do NOT split into subsections when:**
- The section is a natural narrative unit (e.g., "Experimental Setup" that walks through dataset, metrics, and implementation in a few paragraphs)
- Each "subsection" would only be 1-2 paragraphs — they're better as consecutive paragraphs in the section
- The content flows naturally without needing navigational breaks

### Depth limit

**Maximum depth: chapter → section → subsection → paragraph.** Do not go deeper. If you find yourself wanting sub-subsections, the content probably needs to be reorganized at a higher level.

---

## Paragraph Level

### Decision: How many paragraphs, and what mode for each?

This is always the leaf level. There are no further splits.

**How many paragraphs in a section/subsection:**

1. List every distinct message the section must convey
2. Each distinct message = one paragraph
3. If two messages are tightly coupled (one cannot be understood without the other), they may share a paragraph — but only if they share the same rhetorical mode

**Choosing the rhetorical mode:**

1. Ask: "What is this paragraph trying to do?"
   - Make a claim and back it up → `claim-evidence`
   - Introduce a problem and solve it → `challenge-insight-solution` or `problem-solution`
   - Give an overview then details → `general-specific-general`
   - Present numbers and interpret → `data-analysis-conclusion`
   - Describe a process → `chronological`
   - Compare approaches → `comparison`
2. If none of the common modes fit, create a custom one
3. Declare the mode in the structure tree — this is your commitment

**Key points per paragraph:**

- List the **specific factual points** this paragraph must convey
- These are not vague ("describe the method") but concrete ("our method uses sparse attention to reduce computation by 40%")
- 1-4 key points per paragraph is typical

---

## Common Mistakes

1. **Over-splitting:** Creating sections/subsections with only one paragraph. This adds navigation overhead without value. Merge into the parent.
2. **Under-splitting:** A 15-paragraph section with no sub-structure. Readers get lost. Find logical groupings.
3. **Premature paragraph planning:** Declaring paragraphs before you've finished decomposing at the section level. Always finish higher levels first, then go deeper.
4. **Forcing a template:** "Every Method section must have an Overview subsection." No — only if the content calls for it.
5. **Skipping the rhetorical mode:** Writing a paragraph node without declaring its mode. This defeats the purpose of the decomposition phase.

---

## Quick Reference

| Level | Split when... | Don't split when... |
|-------|--------------|-------------------|
| Chapter | Distinct reader questions | Topics are tightly coupled |
| Section | 2+ distinct topics within chapter | Single coherent narrative |
| Subsection | 2+ sub-modules, long section (>8 paragraphs) | Short section (3-5 paragraphs) |
| Paragraph | Never — this is the leaf level | — |
