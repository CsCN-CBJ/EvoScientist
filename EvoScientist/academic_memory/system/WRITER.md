```markdown
# SKILL: Systems Paper Generation from Learned References

## 1. Title Organization Structure Patterns
**Pattern:** `[Project/System Name]: [Problem Framing or Key Claim]`
- **Project/System Name:** Capitalized, concise identifier (e.g., "ThinkAhead", "WOFS")
- **Problem/Claim:** Active phrasing highlighting contribution or core insight
- **Examples:**
  - "ThinkAhead: Preloading Images for Virtual Disks with ThinkAhead"
  - "WOFS: Fast and Synchronous Crash Consistency with Metadata Write-Once File System"

## 2. Section Organization Structure Patterns
**Core Sequence:** Abstract → 1 Introduction → 2 Background → 3 [Analysis/Observations] → 4 [Design/Model] → 5 Implementation → 6 Evaluation → 7 [Discussion/Related Work] → 8 Conclusion → References

**Variants Observed:**
- `3 Trace Analysis` (data-driven) or `3 Observations and Motivations` (insight-driven)
- `7 Related Work` (standalone) or `7 Discussions and Future Work` (combined)
- Design sections may be `4 ThinkAhead Design` or `4 Metadata Write-Once File System Model`

**Default Template:**
```
1. Abstract
2. Introduction
3. Background
4. [Analysis/Motivation]
5. [System Design/Model]
6. Implementation
7. Evaluation
8. Related Work
9. Conclusion
10. References
```

## 3. Section-Specific Subsection/Paragraph Organization

### Abstract (150-170 words)
- **Paragraph 1:** Problem context + current approach limitations
- **Paragraph 2:** Proposed system + key results/contributions

### Introduction (700-900 words)
- **P1:** Broad domain importance + specific problem statement
- **P2:** Current solution critique with concrete drawbacks
- **P3:** Data-driven motivation (e.g., "Our trace analysis shows...")
- **P4:** System overview + design goals
- **P5:** Contributions enumerated (typically 3-4 bullet points)
- **P6:** Paper roadmap

### Background (700-1300 words)
- **2.1** Core technology stack components
- **2.2** Related mechanisms/standards
- **2.3** Terminology definitions and scope
- Each subsection: 2-3 paragraphs explaining concepts essential for later sections

### Analysis/Motivation Section (1400-3300 words)
- **Opening paragraph:** Study methodology and dataset
- **Middle paragraphs:** Data observations → implications → limitations of existing approaches
- **Closing paragraph:** Clear design requirements extracted from analysis

### Design/Model Section (1900-2600 words)
- **Opening:** Design goals (bulleted list)
- **5.1 Overview:** Architectural diagram + component descriptions
- **5.2+:** Each core component with: challenge → solution → mechanism details
- Use consistent terminology established in Background

### Implementation (350-2000 words)
- **P1:** Code statistics + major components
- **P2-3:** Key implementation details (queues, data structures, algorithms)
- **P4:** Deployment considerations

### Evaluation (2800-4200 words)
- **P1:** Research questions (bulleted)
- **P2:** Experimental setup (hardware, dataset splits, metrics)
- **Subsections:** 6.1 Baseline comparison, 6.2 Component analysis, 6.3 Sensitivity studies
- Each subsection: methodology → results → interpretation

### Related Work (290-580 words)
- Grouped by approach category (2-3 paragraphs)
- Each paragraph: Related work summary → differentiation from current system
- Structure: "Category X does Y. However, they lack Z. Our system addresses this by..."

### Conclusion (160-180 words)
- **P1:** System recap + key achievements
- **P2:** Future work + acknowledgments

## 4. Paragraph Writing Structure Patterns
**Core Pattern:** `Setup/Context → Method/Observation Detail → Evidence/Implication`

**Template Sentences:**
- **Setup:** "We present [analysis] to characterize [process] and evaluate [impact]..."
- **Detail:** "The [component] employs [technique] to address [challenge] by..."
- **Evidence:** "Evaluation shows [metric] improves by [value] compared to [baseline]..."

**Paragraph Length:** 70-100 words (2-4 sentences)
- Avoid paragraphs > 120 words
- Technical descriptions: 80-90 words optimal

## 5. Word/Page Composition Guidelines

### Overall Targets (based on CORPUS_STATS)
- **Total words:** 15,000-17,500 (aligned with median 15,316)
- **Total pages:** 17-21 (assuming ~800 words/page)
- **Sections:** 10-11 main sections

### Section Allocation (Percentage of Total)
- Abstract: 1% (150-170 words)
- Introduction: 4-6% (600-900 words)
- Background: 5-8% (750-1,400 words)
- Analysis/Motivation: 10-20% (1,500-3,500 words)
- Design/Model: 12-16% (1,800-2,800 words)
- Implementation: 2-4% (300-700 words)
- Evaluation: 18-25% (2,700-4,400 words)
- Related Work: 2-4% (300-700 words)
- Conclusion: 1% (150-180 words)
- References: 12-25% (1,800-4,300 words)

### Writer Profile Alignment
- **Problem-thesis-contribution alignment:** Ensure each section explicitly connects to core thesis
- **Evidence-grounded claims:** Every claim followed by data reference or logical justification
- **Consistent terminology:** Maintain glossary terms from Background throughout

## 6. Hierarchical Logic Stream Workflow

### Level 1: Macro Structure (Paper Outline)
```
1. Define core contribution statement
2. Map to section template (Section 2)
3. Allocate word counts per section (Section 5)
4. Establish terminology glossary
```

### Level 2: Section Development
```
For each section:
1. Determine section's role in argument flow
2. List key points (3-5) supporting section thesis
3. Organize points into subsections (if needed)
4. Assign paragraph count per point
```

### Level 3: Paragraph Construction
```
For each paragraph:
1. Topic sentence (setup/context)
2. Supporting detail (method/observation)
3. Evidence/implication sentence
4. Transition to next paragraph (if needed)
```

### Level 4: Sentence Refinement
```
For each sentence:
1. Check technical accuracy
2. Ensure claim-evidence linkage
3. Apply style guidelines (concise, concrete)
4. Verify terminology consistency
```

## 7. Evolve Hooks for Iterative Refinement

### Thought Integration Points
```
[USER_THOUGHT]: Insert at relevant section/paragraph
  - Problem refinement → Introduction/Abstract
  - Design insight → Design/Model section
  - Experimental idea → Evaluation section
  - Related work connection → Related Work section
```

### Iteration Protocol
```
1. Generate draft following workflow (Levels 1-4)
2. Identify weak sections (low evidence, unclear logic)
3. Apply USER_THOUGHT to specific weak points
4. Regenerate affected paragraphs/sections
5. Re-check overall coherence and flow
```

### Style Enforcement
```
After each iteration:
1. Scan for vague adjectives → replace with concrete mechanisms
2. Check each claim has explicit evidence reference
3. Ensure problem-thesis-contribution alignment in each section
4. Verify terminology consistency against glossary
```

## 8. Practical Checklist for write.py

### Pre-Generation
- [ ] Core contribution statement defined (1 sentence)
- [ ] Section template selected and customized
- [ ] Word allocation per section calculated
- [ ] Terminology glossary established
- [ ] USER_THOUGHTS integrated into outline

### Per-Section Generation
- [ ] Section thesis aligns with paper's core contribution
- [ ] Paragraph count matches word allocation
- [ ] Each paragraph follows Setup→Detail→Evidence pattern
- [ ] Transitions between paragraphs clear
- [ ] Technical descriptions concrete and specific

### Post-Generation Validation
- [ ] Total word count within 15,000-17,500 range
- [ ] Each claim supported by evidence or logical justification
- [ ] Consistent terminology throughout
- [ ] Abstract captures problem + solution + results
- [ ] Introduction ends with clear contributions list
- [ ] Evaluation addresses all research questions
- [ ] Related Work differentiates from existing approaches

### Style Compliance
- [ ] Sentences concise (avoid > 25 words without technical necessity)
- [ ] Active voice preferred
- [ ] Concrete mechanism descriptions over generic adjectives
- [ ] Claim-evidence transitions explicit ("Our results show...", "This demonstrates...")
- [ ] No undefined acronyms or terms

### Iteration Ready
- [ ] Weak sections flagged for USER_THOUGHT input
- [ ] Logic flow diagrammatically verifiable
- [ ] Contribution visibility maximized in Abstract/Introduction/Conclusion
```

*Last updated based on analysis of 2 systems papers (FAST'26, OSDI'25) with 30,632 total words, targeting 10-11 sections, 15,000-17,500 words total. Writer profile enforces problem-thesis-contribution alignment, evidence-grounded claims, and consistent terminology.*