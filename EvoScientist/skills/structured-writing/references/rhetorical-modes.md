# Rhetorical Modes Reference

Rhetorical modes define how a paragraph is organized — the logical structure of its sentences. When you declare a mode for a paragraph in the structure tree, you are committing to that organizational pattern.

These modes are **references, not constraints**. You may use any of the modes listed below, or invent your own. The only requirement is that every paragraph in the structure tree declares its mode explicitly.

---

## Common Modes

### claim-evidence

**Structure:** Claim → Evidence → Explanation

**When to use:** Stating a result, advantage, or finding that needs backing.

**Example flow:**
1. State the claim: "Our method reduces latency by 40% compared to the baseline."
2. Present the evidence: "Table 3 shows that on Dataset X, the average latency drops from 200ms to 120ms."
3. Explain why: "This reduction comes from the sparse attention mechanism, which skips irrelevant tokens during decoding."

---

### challenge-insight-solution

**Structure:** Challenge → Insight → Solution

**When to use:** Introducing a new method by first establishing what's wrong and what key observation drives the fix.

**Example flow:**
1. Challenge: "Existing methods assume uniform token importance, leading to wasted computation on irrelevant regions."
2. Insight: "However, attention maps reveal that only 15% of tokens contribute meaningfully to the output in most steps."
3. Solution: "We propose a sparse attention selector that identifies and retains only high-contribution tokens."

---

### general-specific-general

**Structure:** General statement → Specific details → General conclusion

**Also known as:** 总-分-总

**When to use:** Providing an overview before diving into specifics, then summarizing.

**Example flow:**
1. General: "The model consists of three complementary modules."
2. Specific: "Module A handles feature extraction. Module B performs cross-attention fusion. Module C refines the output via iterative decoding."
3. General: "Together, these modules form an end-to-end pipeline that processes input in a single forward pass."

---

### data-analysis-conclusion

**Structure:** Present data → Analyze → Draw conclusion

**When to use:** Reporting experimental results, especially quantitative ones.

**Example flow:**
1. Data: "On the GLUE benchmark, our model achieves 92.1 average score (Table 2)."
2. Analysis: "The improvement is most pronounced on RTE (+3.2) and CoLA (+2.8), tasks requiring linguistic understanding rather than pattern matching."
3. Conclusion: "This suggests that our pre-training strategy particularly benefits tasks requiring deep syntactic and semantic processing."

---

### chronological

**Structure:** Step 1 → Step 2 → Step 3 → ...

**When to use:** Describing a process, algorithm, or pipeline where order matters.

**Example flow:**
1. "Given an input image I, the encoder first extracts multi-scale features F = {f₁, f₂, f₃}."
2. "The fusion module then aggregates F via cross-attention, producing a unified representation z."
3. "Finally, the decoder takes z and generates the output sequence autoregressively."

---

### comparison

**Structure:** A → B → Comparison → Conclusion

**When to use:** Contrasting two or more approaches to highlight differences.

**Example flow:**
1. A: "Method X processes all tokens uniformly."
2. B: "Method Y applies dynamic pruning based on attention scores."
3. Comparison: "While X guarantees complete coverage, Y achieves comparable quality at 40% of the computational cost."
4. Conclusion: "For latency-sensitive applications, Y offers a better efficiency-accuracy trade-off."

---

### problem-solution

**Structure:** Problem → Solution

**When to use:** A simpler variant of challenge-insight-solution when no deep insight is needed — just state the issue and the fix.

**Example flow:**
1. Problem: "The loss function does not penalize false negatives in the rare-class setting."
2. Solution: "We add a weighted cross-entropy term that increases the penalty for misclassifying rare-class samples."

---

### concession-rebuttal

**Structure:** Concede a point → Rebut with stronger point

**When to use:** Addressing potential objections, especially in limitation sections.

**Example flow:**
1. Concede: "While our method requires an additional pre-processing step, adding overhead to the pipeline..."
2. Rebut: "...this step enables real-time inference at deployment, reducing the total end-to-end latency by 3× compared to the baseline that skips pre-processing."

---

## Creating Custom Modes

If none of the above fits, create your own mode. The requirements are:

1. **Give it a descriptive name** — e.g., `theory-verification-implication`, `context-action-reflection`
2. **Define the structure** — list the sequence of logical steps
3. **Explain when to use it** — one sentence on applicable scenarios

In the structure tree, simply use your custom name as the `rhetorical_mode` value. The name itself should be self-explanatory enough that you can follow it during Phase B without needing to look up a definition.

## Important Notes

- A mode is a **plan, not a formula** — adapt the structure to the content. If a claim-evidence paragraph needs two pieces of evidence, add them.
- **Do not force content into a mode** — if the content doesn't fit, choose a different mode or create a custom one.
- **Consistency within a section** — if three consecutive paragraphs in a Results section all use data-analysis-conclusion, that's fine. But if they naturally call for different modes, use different modes.
- **The mode declaration is a commitment** — once you declare a mode in the structure tree, follow it when writing. If the mode doesn't work during writing, go back and update the structure tree first.
