# Consolidating the academic site and research notes

## Destination and provenance

- Maintained repository: `stein-wang0226/stein-wang0226.github.io`, branch `main`.
- Destination baseline: `41ea2752875e27fa51bef619713649a4ddb98fd0`.
- Academic source: `stein-wang0226/wyx0226.github.io`, branch `master`, snapshot `9fffe57`.
- The source checkout is shallow. This migration imports content into the main
  repository; it does not claim that the two Git commit graphs have been merged.
- The old checkout and remote remain unchanged so the original content can be recovered.

The local maintained checkout is `/Users/bytedance/Desktop/my_blogs/site`.
The former `.codex_repo_inspect/stein-wang0226.github.io` path is a symbolic link
to this same checkout, preserving callers that still use the old location.

## Imported content

| Old source | Maintained source / destination |
|---|---|
| `_pages/about.md` | `content/pages/about.md` → `/about/` |
| `_pages/cv.md` | `content/pages/cv.md` → `/cv/` |
| `_publications/*.md` (four records) | `content/publications/` → `/publications/` and `/publication/<slug>/` |
| `assets/Curriculum_Vitae.pdf` | Same asset path |
| `vlm-knowledge-interview.html` | `content/posts/vlm-knowledge-interview/index.html` → original root URL |
| `rl-interview-guide.html` | `content/archive/rl-interview-guide/index.html` → `/legacy/rl-interview-guide.html` |
| `LICENSE` | `licenses/academic-pages-MIT.txt` |

Research claims, publication dates and CV statements are imported from the
existing source; this migration does not independently fact-check or update them.
The PDF is the original asset and may differ from the Markdown CV.

The main repository's RL guide is substantially different from the source
version. Both are retained. The old Jekyll theme, demo pages, example attachments,
Sass vendor tree, example comments, Leaflet talk map and notebook generators are
not needed to render the imported personal content and are not copied into the
maintained site. The original source retains those files.

## Routes

Existing root research pages and `dlm-survey/` routes are retained. The old project
prefix `/wyx0226.github.io/` is represented by static redirect pages for:

- The homepage, `about/`, `about.html`, `cv/`, `resume/`, `publications/`,
  `year-archive/` and `sitemap/`.
- All four `/publication/<slug>/` detail routes.
- The VLM page and original RL page.
- The original `/assets/Curriculum_Vitae.pdf` download path (byte-identical copy).

Redirects retain query strings and fragments using JavaScript and provide a
visible fallback link. `/notes/` and `/year-archive/` lead to `/blog/`, which
restores former category filters or explains unknown values. These compatibility routes take effect
under the main site **only after the old project Pages site is disabled**;
an active project site can continue to own that prefix.

## Finish the remote cutover

1. Review the local consolidated site and changes.
2. Commit and push the consolidated main repository.
3. Change the main repository's Pages source to GitHub Actions and verify the
   published profile, publications, notes search, CV download and chapter links.
4. Disable Pages for the old repository so main-site compatibility routes can
   handle its previous project prefix. Verify the old links after that change.
5. Add an explanatory README to the old repository, then archive it if desired.
   Do not delete the old repository; preserving its history costs no ongoing site maintenance.

Local migration and validation do not establish deployment status. Check the
main repository's Actions runs and the live `/build-info.json` for the deployed commit.
The two source commit graphs are not claimed to be merged; this is content
consolidation into one active repository with original history retained.

## Source / artifact separation

All articles are maintained under `content/posts/` or `content/series/`.
Root article HTML and generated academic pages were removed only after the
31 migrated source files matched their original hashes and deprecated paths
had separate backups. Public URLs remain registered in the catalog and redirects.
Builds render to an external directory, never back into sources. See
`docs/content-inventory.md`, immutable `content-migration-manifest.json` and
`docs/content-audit.md` for preservation and bounded later edits.
Personal statements remain in about/CV, while duplicate manual lists now use
catalog/publication records. The existing CV PDF and four paper records remain unchanged.

The `.automation/` runner now edits only
`content/posts/llm-frontier-2026/index.html`; its backup, state and insertion
markers remain, and validation uses the same external artifact as preview/CI.
No scheduler or remote configuration was changed during local implementation.

## Local acceptance

Local acceptance is complete: 52 HTML pages / 64 public files; 33 reading and
entry pages checked at 390, 768 and 1440px; keyboard, original interactions,
legacy parameters, disabled JavaScript and original PDF downloads verified.
An isolated source snapshot builds without prior outputs, and its repeated build
and export match the preview bytes. Preservation and limitations are recorded in
`docs/validation.md`. The content audit still lists unresolved scientific claims
and missing answers; this migration does not claim those were all completed.

The original acceptance preview used `http://127.0.0.1:8766/`. Use `make preview`
for a new local session; confirm publishing through the remote checks above.
