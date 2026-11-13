# Content Inventory and Maintenance Contract

The maintained checkout is `site/`. This inventory describes the authoritative
sources, public routes and preservation baseline after local consolidation.
Build, reading, catalog and automation changes are implemented; verification
results are recorded in `validation.md`. The original academic checkout remains
untouched. Scientific review is bounded by `content-audit.md`; nothing here
claims a remote deployment or comprehensive factual verification.

## Migration baseline and later changes

The interrupted migration was recovered from exact preview copies, Git history,
and the original file-writing records. Every recovered source was compared with
the immutable pre-migration SHA-256 manifest before obsolete paths were removed.

Recovery verified on 2026-11-14:

- 31/31 moved source files recovered with exact pre-migration bytes.
- 41 retained/moved source, resource and license hashes match the baseline.
- 299 original HTML anchors and 59 original navigation/automation markers remain.
- Coverage: 9 active local collections, 14 chapters, 4 publications, 2 external links.
- `python3 docs/verify-content-migration.py --require-clean` passes.
- Recovery originals and removed-path copies are backed up outside the repository
  at `/private/tmp/my-blogs-recovery-20261114/`; they are not build inputs.

After the documented local edits, verification reports **27 exact hashes and
14 explicitly recorded changes**, with all 299 original anchors and 59 markers
preserved. The fourteen chapters, four paper records, PDF, historical RL page,
series helper files and license retain their original bytes. Changes to shared
rendering and reading styles affect generated pages without rewriting these sources.

## JSON Contract

All three documents have `schema_version: 1`. Paths in `source` are relative to
the repository; local `url` values are root-relative public routes, never paths
relative to the source directory. `/foo/` and `/foo/index.html` name the same
output file and must be treated as a route collision, not two distinct pages.
Existing HTML must resolve its relative links against its public route.

### `content/site.json`

- `title`, `url`, `blog_url`: identity, canonical host, and `/blog/` main entrance.
- `navigation`: ordered `{label, url}` records. Blog label is `博客与笔记`.
- `topics`, `types`: ordered `{id, label}` dictionaries; IDs are the catalog values.
- `kinds`, `origins`, `statuses`, `review_statuses`: allowed enum values.
- `pages`: `{id, title, source, url}` for profile and CV; Markdown front matter
  remains imported verbatim, but these route mappings control output.
- `publications`: `source_glob`, `url_prefix`, `featured` publication IDs. Each
  Markdown filename stem is its ID. Existing front matter remains the only
  publication record, including title, excerpt, date, venue and paper link.
  Publication dates are not asserted to be content-update dates.
- `assets`: explicit `{source, url}` mappings. Preserve the entire shared assets
  tree; the listed files are the complete T1 baseline, not a ban on future assets.
- `catalog_defaults`: local published non-chapter entries, descending effective
  update date, then undated entries by stable title and ID. Chapters are available
  for search and series navigation, not extra collections.

Topics: `llm-foundations`, `multimodal`, `rl-post-training`, `agent`,
`training-inference`, `diffusion`. Labels exactly follow the six approved topics.
Types: `principles`, `system-guide`, `practical-guide`, `quick-reference`,
`interview-bank`, `frontier-tracker`, `series-tutorial`.
Source and form are independent from topic. Old `面试复习` maps to type; old
`外部笔记` maps to origin. Cross-topic information belongs in tags.

### `content/catalog.json`

Top-level `entries` is an array; every entry contains:

| Field | Contract |
| --- | --- |
| `id` | Unique stable lowercase kebab ID |
| `kind` | `post`, `series`, `chapter`, `external` |
| `title`, `summary` | Nonempty strings, shared by generated displays |
| `source` | One existing `content/` HTML/Markdown file for local entries; `null` for external entries |
| `url` | Unique unchanged local public route, or actual HTTP(S) external link |
| `topic`, `type` | One ID from the respective site dictionary |
| `tags` | String array; technical keywords, not a replacement for topic |
| `origin` | `local` or `external` |
| `status` | `published`, `draft`, `archived`; drafts never publish; archive excluded from default list |
| `review_status` | `unreviewed`, `needs-review`, `reviewed`; migration sets all to `unreviewed`, independently of publication status |
| `updated` | ISO calendar date with evidence, or `null`; never build/Git time |
| `updated_source` | `null`, except frontier `{kind: "html-element", id: "last-updated", attribute: "datetime"}` |
| `series`, `order` | Chapters reference a `kind: "series"` ID and a unique positive contiguous order; other entries use `null` |
| `featured` | Boolean, not duplicated title/URL card content |
| `related` | Existing IDs, no self-reference or duplicates |

The DLM landing page is one collection, not a 15th chapter. The fourteen chapter
entries have explicit order 1-14; do not infer order by scanning filenames.
The historical RL entry is archived and not a tenth active collection.
Two external links are catalog records, not local chapters to import.
Publication and personal-page records are deliberately not duplicated in catalog.

All `updated` fields are `null` at migration. Frontier's effective date is
extracted from the single valid `time#last-updated[datetime]`, currently
`2026-11-10`; do not store a second mutable copy in the catalog. Reject missing,
duplicate or invalid dates. Invalid is not silently replaced by today's date.
Other bodies may mention years or content ranges; those are not sufficient
evidence of the last substantive edit. No dates were inferred.

### `content/redirects.json`

- `defaults`: preserve query and fragment; visible fallback is mandatory.
- `redirects`: ordered `{from, to, query_policy?}` local routes. Directory routes
  generate `index.html` and thereby also preserve explicit old `index.html` URLs.
- `copies`: `{from, to}` asset aliases, notably the old PDF; copy bytes, do not
  redirect a PDF using an HTML document.
- `query_compatibility.blog`: `q`, `topic`, `type` names; old `category` values
  translate to topic/type/origin according to `legacy_values`. Preserve unknown
  unrelated query keys and the fragment. Existing valid new keys take precedence.
  Unknown legacy values clear catalog filters and display a notice rather than
  claiming an empty matching category. The generated blog implements this policy.
- Targets must be registered local output routes or valid target anchors; no
  duplicate `from`, route collisions, missing targets or redirect chains.
- Existing post and chapter URLs are direct outputs, not redundant redirects.

`/wyx0226.github.io/` compatibility is local preparation. The old project Pages
site can still own that prefix; this migration does not disable it or claim that
local routes are already live.

## Authoritative File List

| Collection ID | New source | Unchanged public route |
| --- | --- | --- |
| `llm-frontier-2026` | `content/posts/llm-frontier-2026/index.html` | `/llm-frontier-2026.html` |
| `agentic-rl-guide` | `content/posts/agentic-rl-guide/index.html` | `/agentic-rl-guide.html` |
| `dlm-survey` | `content/series/dlm-survey/index.html` | `/dlm-survey/` |
| `transformer-decoder-flow` | `content/posts/transformer-decoder-flow/index.html` | `/transformer-decoder-flow.html` |
| `rl-interview-guide` | `content/posts/rl-interview-guide/index.html` | `/rl-interview-guide.html` |
| `agent-harness-guide` | `content/posts/agent-harness-guide/index.html` | `/agent-harness-guide.html` |
| `distributed-training-guide` | `content/posts/distributed-training-guide/index.html` | `/distributed-training-guide.html` |
| `llm-interview-bank` | `content/posts/llm-interview-bank/index.html` | `/llm-interview-bank.html` |
| `vlm-knowledge-interview` | `content/posts/vlm-knowledge-interview/index.html` | `/vlm-knowledge-interview.html` |

| Order | Chapter ID | File in `content/series/dlm-survey/` |
| --- | --- | --- |
| 1 | `dlm-ddpm` | `s00a_ddpm.html` |
| 2 | `dlm-flow-sde` | `s00b_flow_sde.html` |
| 3 | `dlm-overview` | `s01_overview.html` |
| 4 | `dlm-discrete` | `s02_discrete.html` |
| 5 | `dlm-block` | `s03_block.html` |
| 6 | `dlm-continuous` | `s04_continuous.html` |
| 7 | `dlm-paradigms` | `s05_paradigms.html` |
| 8 | `dlm-scaling` | `s06_scaling.html` |
| 9 | `dlm-speculative` | `s07_speculative.html` |
| 10 | `dlm-elbo-rl` | `s08_elbo_rl.html` |
| 11 | `dlm-commercial` | `s09_commercial.html` |
| 12 | `dlm-comparison` | `s10_comparison.html` |
| 13 | `dlm-loop-transformer` | `s11_loop_transformer.html` |
| 14 | `dlm-vae` | `s12_vae.html` |

Each chapter still outputs to `/dlm-survey/<same-file>`. The series `shared.css`,
`style.css`, `s12_vae_summary.md` and legacy `generate.py` move into that same
source directory. The importer remains byte-identical and auxiliary, not an
alternate way of building the authoritative fourteen chapters. Only the two CSS
files are public assets; Python and Markdown auxiliary files are not public.

Other sources and retained resources:

- `content/about.md` -> `content/pages/about.md`, output `/about/`.
- `content/cv.md` -> `content/pages/cv.md`, output `/cv/`.
- `legacy/rl-interview-guide.html` -> `content/archive/rl-interview-guide/index.html`,
  output `/legacy/rl-interview-guide.html`; catalog links to the current guide.
- `content/notes.json` -> `content/archive/notes-before-migration.json`, provenance
  only, never read as the active registry or published as a source file.
- Four unchanged `content/publications/*.md`: `2024-stm-dynamic-graph-fraud`,
  `2026-locality-aware-dlm`, `2026-semantic-diffusion-lm`,
  `2026-semantic-dlm-plus`, output `/publication/<id>/`.
- `assets/Curriculum_Vitae.pdf` and `licenses/academic-pages-MIT.txt` retain original
  bytes. Shared `assets/site/site.css` and `catalog.js` have documented changes;
  `reading.css` is a new rendering layer.
- Existing `.nojekyll` remains. Root and academic generated output is removed
  only after baseline source/resource preservation is checked.

External URLs are unchanged:
`https://stein-wang0226.github.io/mllm-interview-notes/` and
`https://stein-wang0226.github.io/llm-study-notes/`.

## Preservation Evidence

`docs/content-migration-manifest.json` is a generated immutable **pre-migration**
snapshot of the uncommitted files, not Git HEAD. Each file records `before`,
`after`, `action`, source `sha256`, byte length, public route, all original HTML
IDs/named anchors, H1-H3 headings, local/external links and automation/navigation
markers. It includes every existing public file, removed generated outputs,
publications, original license, helper materials, and the existing home template.
Never regenerate it to make later edits appear preserved.

Verification commands:

```bash
python3 docs/verify-content-migration.py
python3 docs/verify-content-migration.py --require-clean
python3 docs/verify-content-migration.py --require-clean --allow-content-changes
```

The first command checks baseline SHA values or an exact documented SHA/reason
in `content-changes.json`. `--require-clean` additionally rejects obsolete root
outputs and duplicate old sources; this is the normal acceptance command.
The relaxed last command may report otherwise undocumented **catalog HTML source**
changes and is useful for investigation, not for final acceptance.
All commands keep checking original anchors and markers, current links,
resource/PDF/license bytes, unique routes and collection coverage. They never
rewrite the baseline or describe changed bodies as byte-identical. Personal and
publication record changes require explicit reconciliation.

The limited DPO correction and reading additions are listed in `content-audit.md`;
other scientific claims and original publication dates remain unreviewed.
CV PDF and online CV can differ; neither is inferred from the other. Local build
and UI checks are separate evidence in `validation.md`. Online is not synchronized.
