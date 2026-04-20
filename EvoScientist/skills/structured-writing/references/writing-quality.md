# Writing Quality Checklist

Use this checklist at two points: after writing each paragraph (micro check) and after assembling the full paper (macro check).

---

## Micro Check (After Each Paragraph)

Run this after writing every paragraph during Phase B.

### Content Alignment

- [ ] Does this paragraph convey exactly the key points declared in the structure tree?
- [ ] Are there key points in the structure tree that are missing from the paragraph?
- [ ] Did I add content not declared in the structure tree? If so, is it necessary? If not, remove it.

### Rhetorical Mode Compliance

- [ ] Does the paragraph follow its declared rhetorical mode?
- [ ] Is the logical structure of the mode visible in the paragraph? (Can a reader identify the claim, the evidence, the transition?)
- [ ] If the mode didn't work during writing, did I go back and update the structure tree first?

### Paragraph Mechanics

- [ ] Is the first sentence a clear topic sentence?
- [ ] Does every sentence advance the paragraph's message?
- [ ] Can any sentence be removed without losing information? If yes, remove it.
- [ ] Is the paragraph a reasonable length? (3-8 sentences is typical; 1-2 is likely too thin; 10+ likely needs splitting)

### Claims and Evidence

- [ ] Are there unsupported claims in this paragraph? If yes, either add evidence or mark with TODO
- [ ] Are numerical results precise? (Not "significant improvement" but "+3.2% on BLEU")
- [ ] Are figures/tables referenced by number, not vague description?

### Language

- [ ] Is the terminology consistent with the rest of the paper?
- [ ] Are there unnecessary adjectives or superlatives? ("significantly", "dramatically", "substantially" — replace with numbers)
- [ ] Is the sentence structure varied? (Not all sentences starting with "We...")

---

## Macro Check (After Full Paper Assembly)

Run this after Step B4, when the complete paper is assembled.

### Narrative Coherence

- [ ] Does the paper tell a coherent story from start to finish?
- [ ] Can a reader understand the contribution by reading only the Abstract and Introduction?
- [ ] Does each chapter connect to the next? Are there jarring transitions?

### Claim-Evidence Audit

- [ ] Go through every claim in the Abstract and Introduction
- [ ] For each claim: is there a specific experiment, table, or figure that supports it?
- [ ] Are there claims with no supporting evidence anywhere in the paper?

### Structural Balance

- [ ] Is each section proportionally sized relative to its importance?
- [ ] Is the Method section dominating at the expense of Experiments (or vice versa)?
- [ ] Are there sections that feel like filler?

### Consistency

- [ ] Is terminology used consistently throughout the paper? (Not switching between "model" and "framework" for the same thing)
- [ ] Are notation and symbols consistent? (Not using both x and X for the same variable)
- [ ] Are cross-references accurate? (Does "as shown in Table 3" actually point to Table 3?)

### Completeness

- [ ] Does the paper address the research goal stated in the Introduction?
- [ ] Are all experiments described in the Experiments section referenced from the Introduction or Method?
- [ ] Is there a limitations discussion?
- [ ] Are all figures and tables referenced in the text?

### Common Weaknesses to Check

- [ ] **Missing motivation:** Does every module/section explain WHY, not just WHAT?
- [ ] **Hidden assumptions:** Are assumptions stated explicitly or left implicit?
- [ ] **Overclaiming:** Are the claims in the Abstract stronger than what the experiments actually show?
- [ ] **Missing baselines:** Are there recent SOTA methods that should be compared against?
- [ ] **No failure analysis:** Does the paper acknowledge when and why the method fails?

---

## Red Flags — Stop and Fix

- A paragraph with no topic sentence
- A claim in the Abstract/Introduction with no supporting experiment
- A section with only one paragraph that should have more (likely under-developed)
- A section with 10+ paragraphs and no sub-structure (likely over-long)
- The same information stated in two different places with different wording
- A "filler" paragraph that doesn't advance the paper's argument
