# SKILL: Systems Paper Generation from Learned References

## 1. Title Organization Structure Patterns

**Primary Patterns (from corpus):**
- `[Project/System Name]: [Technical Subtitle with Problem-Solution Cue]` (e.g., "PERSEUS: A Fail-Slow Detection Framework for Cloud Storage Systems")
- `[Project/System Name]: [Problem Framing or Key Claim]` (e.g., "Fast, Transparent Filesystem Microkernel Recovery with Ananke")

**Implementation Rules:**
- **Project name first**, followed by colon
- **Subtitle should signal** either (a) problem-solution relationship or (b) key technical claim
- **Avoid generic phrases** like "A Study of" or "An Analysis of"
- **Include system domain cue** (e.g., "for Cloud Storage Systems", "with Metadata Write-Once File System")

## 2. Section Organization Structure Patterns

**Core Sequence (9-12 sections typical):**
```
Abstract → 1 Introduction → 2 Background/Architecture → 3 Motivation/Observation → 
4 [System Name] Design → 5 Implementation → 6 Evaluation → 
7 Discussion/Limitations → 8 Related Work → 9 Conclusion → References
```

**Variants Observed:**
- **Measurement papers:** Insert "Dataset Overview" after Background
- **Experience papers:** Use chronological sections (e.g., "EBS1", "EBS2", "EBS3")
- **Analysis papers:** May combine "Motivation" and "Observation"

**Section Naming Conventions:**
- Use **title case** for section headers
- **Introduction** always "1 Introduction" (not "Introduction" alone)
- **Design sections** named "[System Name] Design" or "[System Name] Overview"
- **Evaluation** always numbered, not "Experimental Evaluation"

## 3. Section-Specific Subsection/Paragraph Organization

### 3.1 Abstract (150-250 words, 2-3 paragraphs)
```
Paragraph 1: Problem statement + gap in existing approaches
Paragraph 2: System/approach overview + key techniques
Paragraph 3: Quantitative results + implications
```

### 3.2 Introduction (800-1200 words, 8-12 paragraphs)
```
¶1: Broad context + importance of problem domain
¶2: Specific problem statement + current limitations
¶3: High-level approach intuition
¶4: Key contributions (numbered or bulleted)
¶5-7: Detailed preview of each major contribution
¶8: Roadmap of paper sections
```

### 3.3 Background/Architecture (600-1000 words)
```
Subsection 2.1: System architecture overview (with figure reference)
Subsection 2.2: Key components/terminology definitions
Subsection 2.3: Relevant prior work assumptions
```

### 3.4 Motivation/Observation (800-1500 words)
```
Subsection 3.1: Problem symptom + evidence from data/traces
Subsection 3.2: Quantitative analysis (tables/figures)
Subsection 3.3: Limitations of existing approaches
```

### 3.5 Design Sections (1500-3000 words total)
```
4.1: Design goals/principles (bullet points)
4.2: High-level architecture (figure)
4.3: Core mechanism 1
4.4: Core mechanism 2
4.5: Consistency/security/recovery considerations
```

### 3.6 Evaluation (2000-4000 words)
```
6.1: Experimental setup (hardware, software, baselines)
6.2: Microbenchmarks (throughput, latency, overhead)
6.3: End-to-end performance
6.4: Sensitivity analysis
6.5: Case studies/production deployment results
```

### 3.7 Related Work (300-800 words)
```
Organize by: (1) Directly related systems, (2) Similar techniques in different domains, 
(3) Foundational work, (4) Contrast with current approach
```

## 4. Paragraph Writing Structure Patterns

**Standard Pattern (70-90 words per paragraph):**
```
[Sentence 1]: Setup/context establishing the paragraph's focus
[Sentence 2-3]: Method detail, observation, or mechanism description
[Final sentence]: Evidence summary, implication, or transition to next point
```

**Example Templates:**
- **Problem paragraph:** "Existing systems [do X] to achieve [Y]. However, this approach [has limitation Z]. As a result, [negative consequence] occurs under [conditions]."
- **Solution paragraph:** "To address [problem], we propose [technique]. Specifically, [component] [does action] by [mechanism]. This enables [benefit] while maintaining [constraint]."
- **Evidence paragraph:** "Figure N shows [observation] across [conditions]. The [metric] improves by [X]% compared to [baseline]. This demonstrates [implication] for [scenario]."

## 5. Word/Page Composition Guidelines

**Target Ranges (based on CORPUS_STATS):**
- **Total words:** 13,000-18,000 (median: 15,228)
- **Total pages:** 16-20 pages (median: 18 pages)
- **Words per page:** 800-900 (avg: 821.68)
- **Paragraph length:** 65-85 words (avg: 69 words)
- **Section count:** 8-11 sections (avg: 9.33)

**Section Length Distribution:**
- Introduction: 800-1200 words (5-7% of total)
- Background: 600-1000 words (4-6%)
- Motivation: 800-1500 words (5-9%)
- Design: 1500-3000 words (9-18%)
- Implementation: 500-1500 words (3-9%)
- Evaluation: 2000-4000 words (12-24%)
- Related Work: 300-800 words (2-5%)
- Conclusion: 150-250 words (1-2%)
- References: 1500-3000 words (9-18%)

## 6. Hierarchical Logic Stream Workflow

**Level 1: Paper Structure (Macro)**
```
1. Define core contribution → 2. Map to standard section template → 
3. Allocate word budget per section → 4. Identify key figures/tables
```

**Level 2: Section Logic (Meso)**
```
For each section:
1. Determine 2-4 key messages for this section
2. Organize messages into logical flow (problem→solution→evidence)
3. Map each message to 1-2 paragraphs
4. Identify transitions between paragraphs
```

**Level 3: Paragraph Construction (Micro)**
```
For each paragraph:
1. Topic sentence: What this paragraph proves/shows
2. Supporting sentences: How/why/evidence
3. Concluding sentence: So what/implication
4. Check: Does this advance the section's argument?
```

**Level 4: Sentence Refinement**
```
For each sentence:
1. Subject-verb-object clarity
2. Technical term consistency
3. Connection to previous sentence
4. Avoid passive voice where possible
```

## 7. Evolve Hooks for User Thoughts and Iterative Refinement

**Input Prompts for Each Stage:**

**Stage 1: Paper Concept**
```
"What is the single most important contribution?"
"What problem keeps practitioners awake at night?"
"What existing approach fails and why?"
```

**Stage 2: Outline Refinement**
```
"Which section feels weakest in argument flow?"
"Where do readers likely get confused?"
"What evidence is missing for key claims?"
```

**Stage 3: Paragraph Development**
```
"Does this paragraph have one clear point?"
"What counterargument should we address here?"
"Is the evidence→claim connection explicit?"
```

**Stage 4: Polish**
```
"Are terms used consistently throughout?"
"Do figure references match discussion?"
"Is the contribution clear in abstract/intro/conclusion?"
```

**Iteration Protocol:**
1. **Generate** draft following structure patterns
2. **Identify** gaps using checklist below
3. **Revise** with focused prompts on weak areas
4. **Validate** against original contribution statement
5. **Repeat** until all checklist items pass

## 8. Practical Checklist for write.py

**Paper-Level Checks:**
- [ ] Title follows `[System]: [Technical Subtitle]` pattern
- [ ] Abstract has 3 paragraphs: problem, approach, results
- [ ] Introduction ends with explicit roadmap paragraph
- [ ] Contribution list matches depth of technical sections
- [ ] Total word count 13K-18K (adjust section allocations)
- [ ] Each major claim has supporting evidence section
- [ ] Conclusion mirrors abstract but adds future work

**Section-Level Checks:**
- [ ] Introduction: 8+ paragraphs, ends with roadmap
- [ ] Background: Defines terms used in later sections
- [ ] Motivation: Includes quantitative evidence
- [ ] Design: Has explicit goals/principles subsection
- [ ] Evaluation: Compares to 2+ relevant baselines
- [ ] Related Work: Explains why approach differs
- [ ] References: 40-80 citations, recent work included

**Paragraph-Level Checks:**
- [ ] Each paragraph 65-85 words
- [ ] First sentence establishes paragraph focus
- [ ] Last sentence provides implication/transition
- [ ] No paragraph repeats same point as adjacent
- [ ] Technical terms used consistently throughout
- [ ] Figure/table references placed at relevant discussion points

**Sentence-Level Checks:**
- [ ] Average sentence length 15-25 words
- [ ] Passive voice < 20% of sentences
- [ ] "We" used for actions taken in paper
- [ ] Claims qualified with "up to", "typically", "in our experiments"
- [ ] Avoid "very", "extremely", "revolutionary" (use quantitative comparisons)

**Style Alignment (per WRITER_PROFILE):**
- [ ] Problem-thesis-contribution alignment verified
- [ ] All claims backed by evidence in same/adjacent paragraph
- [ ] Terminology consistent from abstract through conclusion
- [ ] Concrete mechanism descriptions preferred over adjectives
- [ ] Claim→evidence transitions explicit with "Figure X shows", "Our results indicate"

**Implementation Notes for write.py:**
- Use section word counts as soft constraints
- Flag paragraphs deviating >20% from 75-word average
- Verify each "Design" subsection has corresponding "Evaluation" subsection
- Ensure figure references exist for all cited figures
- Check that all acronyms are defined at first use
- Validate that contribution list in introduction matches conclusion summary