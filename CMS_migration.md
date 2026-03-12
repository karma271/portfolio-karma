# CMS Migration Plan (Pages CMS)

## Scope and intent

This plan migrates only the **Notes/blog content workflow** to Pages CMS while keeping the current portfolio design, templates, and style system intact.

- In scope: blog content authoring, metadata management, build pipeline for blog pages.
- Out of scope: redesigning About/Projects/Experience/Contact sections.
- Status: implementation has been executed on branch `blog_cms_migrate`.

---

## Branch strategy (do this first)

Use a dedicated feature branch so migration work is isolated and easy to review/revert.

### Recommended branch name

- `feat/pages-cms-blog-migration`

### Branch workflow

1. Branch from latest `main`.
2. Keep migration commits small and topical.
3. Use PR-based review into `main`.
4. Do not delete legacy blog source until parity is verified.
5. Keep rollback simple by preserving old source until final cutover commit.

### Suggested commit grouping

- Commit 1: add markdown content model + parser scaffolding.
- Commit 2: add Pages CMS config and admin wiring.
- Commit 3: migrate existing posts to markdown.
- Commit 4: switch index/blog generation to markdown source.
- Commit 5: cleanup deprecated files (only after validation).

---

## Architecture decision

## Legacy state

- Metadata source: markdown frontmatter in `content/blog/*.md`
- Blog content source: markdown body in `content/blog/*.md`
- Rendering: `build.py` + Jinja templates -> `index.html` and `blog/*.html`

## Target state

- Metadata + body source: `content/blog/*.md` (frontmatter + markdown body)
- CMS editing surface: Pages CMS (Git-based editing)
- Rendering remains static: existing Jinja layout + build script
- Public styling remains controlled by `styles/main.css`

This keeps the site minimal and maintainable while simplifying blog publishing.

---

## Content model

Define one markdown file per post at `content/blog/<slug>.md`.

### Frontmatter schema (proposed)

- `slug` (string, required)
- `title` (string, required)
- `meta_description` (string, required)
- `description` (string, required)
- `pill` (string, required)
- `published` (string or date, required)
- `read_time` (string, required)
- `topics` (string, required initially; can evolve to array)
- `toc` (optional list of id/label objects)
- `draft` (boolean, optional, default false)

### Markdown body

- Main article content authored in markdown.
- Keep heading IDs predictable for TOC anchors.
- Use fenced code blocks for future language highlighting:
  - ` ```bash `
  - ` ```python `
  - ` ```rust `

---

## Pages CMS plan

Configure Pages CMS as a Git-backed editor for blog content files.

### Collection setup

- Collection name: `blog`
- Folder: `content/blog`
- Create/delete enabled
- Slug derived from filename/frontmatter slug
- Fields mapped to frontmatter keys above
- Body field uses markdown editor

### Editorial workflow

Use **PR-based** content changes where possible:

- Editors create/update posts in CMS.
- CMS writes commits/PRs to repo.
- Changes are reviewed before merge to `main`.

This preserves quality and avoids accidental production edits.

---

## Build pipeline migration

Update `build.py` to support markdown-driven blog generation without changing visual templates.

### Planned changes

1. Add markdown + frontmatter loader.
2. Parse all `content/blog/*.md` into post objects.
3. Convert markdown body to HTML.
4. Render blog post pages using existing blog layout template.
5. Render homepage blog list from parsed markdown posts.

### Template strategy

- Keep `templates/blog/_layout.html.j2`.
- Add a generic post body template that injects `post.content_html`.
- Avoid per-post body templates going forward.

---

## TOC handling approach

Two viable paths:

1. **Manual TOC in frontmatter** (minimal initial complexity)
2. **Auto-generate TOC from headings** (better ergonomics later)

Recommended rollout:

- Phase 1: manual TOC for deterministic output and low risk.
- Phase 2: optional auto-TOC once markdown flow is stable.

---

## Syntax highlighting plan (future-ready)

Goal: support language-specific fenced code blocks with minimal overhead.

### Option A (fastest): Prism runtime

- Add lightweight Prism assets only on blog pages.
- Continue using language tags in markdown blocks.

### Option B (cleanest output): build-time highlighting

- Perform highlighting during `build.py` processing.
- Ship static highlighted HTML/CSS (no runtime JS).

Recommendation:

- Start with Option A for speed.
- Revisit Option B if you want zero client-side JS later.

---

## Migration phases (safe rollout)

## Phase 0 - Preparation (feature branch) [DONE]

- Create branch `blog_cms_migrate`.
- Tag or note current `main` commit for rollback reference.
- Confirm current build/deploy is green before changes.

## Phase 1 - Introduce markdown source [DONE]

- Add `content/blog/` with one canonical example post.
- Implement parser in build script while keeping legacy source intact.
- Ensure local build can render at least one markdown post.

## Phase 2 - CMS wiring [PENDING]

- Add Pages CMS configuration and admin access setup.
- Map CMS fields to frontmatter schema.
- Validate create/edit flow against feature branch.

## Phase 3 - Migrate existing posts [DONE]

- Convert existing posts into markdown files.
- Preserve slugs and metadata parity.
- Keep old templates temporarily for comparison.

## Phase 4 - Switch source of truth [DONE]

- Point homepage blog list generation to markdown-derived data.
- Use markdown frontmatter as the single metadata source of truth.
- Verify rendered output parity (content + visuals).

## Phase 5 - Cleanup [DONE]

- Remove deprecated blog source files only after parity checks pass.
- Keep cleanup as its own commit for easy rollback.

---

## Validation checklist

## Functional

- New markdown post appears in Notes list.
- Individual post page renders fully.
- TOC anchors work.
- Draft handling works as expected.

## Visual

- Typography, spacing, and theme behavior match existing design.
- Inline and block code are readable and consistent.

## Integrity

- No broken links from `index.html` to post pages.
- Metadata values are rendered correctly.
- Existing post URLs remain stable.

## Build/deploy

- `build.py` succeeds locally.
- CI deploy still succeeds on branch and after merge.

---

## Risk management and rollback

## Risks

- Schema drift between CMS and build script expectations.
- URL breakage if slug handling changes.
- Content regression during conversion from HTML templates to markdown.

## Mitigations

- Enforce required frontmatter fields.
- Keep slug policy strict.
- Use side-by-side rendering checks before cutover.
- Merge cleanup only after successful parity validation.

## Rollback strategy

- Revert merge commit or feature PR.
- Since migration is branch-contained, rollback impact remains isolated.
- Keep legacy source until final cleanup commit is approved.

---

## Definition of done

Migration is complete when all conditions are met:

- Blog content source is markdown in `content/blog`.
- Pages CMS can create/edit blog posts through Git.
- Site rendering remains visually consistent with existing portfolio style.
- Build/deploy pipeline remains stable.
- Legacy blog source removed only after verified parity and approved PR merge.

