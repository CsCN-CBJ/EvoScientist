# Structure Tree Specification

The structure tree is the central artifact of Phase A. It captures the complete hierarchical decomposition of the paper, from chapters down to individual paragraphs.

## File Location

Save the structure tree to `/paper/<paper-name>/structure.md` in the paper's work directory. This file is temporary — delete it after Phase B completes.

## Format

Use Markdown with YAML frontmatter blocks for each node. The tree is represented as nested sections.

```markdown
# Paper: [Title]

## 1 Introduction

id: "1"
level: chapter

### 1.1 Background and Motivation

id: "1.1"
level: section

#### Paragraph 1

id: "1.1.p1"
level: paragraph
rhetorical_mode: challenge-insight-solution
key_points:
  - "Task X is important but existing methods fail on Y"
  - "The key insight is Z"
  - "We propose a method based on Z"

#### Paragraph 2

id: "1.1.p2"
level: paragraph
rhetorical_mode: claim-evidence
key_points:
  - "Our method achieves SOTA on benchmark A"
  - "Evidence: Table 1 shows X% improvement"

### 1.2 Our Contributions

id: "1.2"
level: section

#### Paragraph 1
...
```

## Node Fields

### Required Fields (All Nodes)

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier. Use dot-separated hierarchy: `"1"`, `"1.1"`, `"1.1.p1"` |
| `level` | enum | One of: `chapter`, `section`, `subsection`, `paragraph` |

### Required Fields (Non-Leaf Nodes)

| Field | Type | Description |
|-------|------|-------------|
| (heading) | string | The section title, written as a Markdown heading |

### Required Fields (Leaf Nodes — Paragraph Level)

| Field | Type | Description |
|-------|------|-------------|
| `rhetorical_mode` | string | The organizational pattern for this paragraph. Can be any string — see `rhetorical-modes.md` for common options |
| `key_points` | list of strings | The specific points this paragraph must convey. At least one required |

### Optional Fields (Any Node)

| Field | Type | Description |
|-------|------|-------------|
| `purpose` | string | One-sentence description of what this section/paragraph must accomplish |
| `dependencies` | list of strings | IDs of nodes whose content this node references (for cross-reference tracking) |
| `word_target` | integer | Approximate word count target for this node |

## Levels

| Level | Markdown Heading | When to Use |
|-------|-----------------|-------------|
| `chapter` | `##` | Top-level sections of the paper (e.g., Introduction, Method) |
| `section` | `###` | Subdivisions within a chapter when the chapter covers multiple distinct topics |
| `subsection` | `####` | Further subdivisions when a section covers multiple distinct subtopics |
| `paragraph` | No heading (use `#### Paragraph N` as label) | Individual paragraphs — the leaf level of the tree |

## Rules

1. **Every path from root to leaf must end at `paragraph` level** — no intermediate level should be a leaf
2. **A `paragraph` node must never have children** — it is always a leaf
3. **`rhetorical_mode` is required on `paragraph` nodes and forbidden on all other nodes**
4. **`key_points` is required on `paragraph` nodes and optional on others**
5. **IDs must be unique across the entire tree**
6. **No placeholder content** — every `key_point` must be a concrete, specific statement, not "TBD" or "describe the method"

## Validation Checklist

Before proceeding to Phase B, verify:

- [ ] Every leaf node is at `paragraph` level
- [ ] Every `paragraph` node has `rhetorical_mode` and at least one `key_point`
- [ ] No node contains TBD, TODO, or similar placeholders
- [ ] IDs are unique and follow the dot-separated hierarchy
- [ ] The tree covers all research content that must appear in the paper
- [ ] No `paragraph` node has children
- [ ] No non-`paragraph` node has `rhetorical_mode`
