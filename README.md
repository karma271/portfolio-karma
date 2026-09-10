## Minimal Portfolio

**Stack**: HTML + CSS only (no JavaScript).

A minimal, modern portfolio site built to highlight calm, considered work. It
focuses on typography, accessibility, and small design details rather than heavy
effects or dependencies.

### Structure

```
├── templates/                       # Jinja2 source templates
│   ├── index.html.j2                #   main page
│   ├── blog/
│   │   ├── _layout.html.j2          #   shared blog layout
│   │   └── markdown_post.html.j2    #   markdown-driven post renderer
│   └── partials/                    #   reusable header & footer fragments
├── content/
│   └── blog/                        # markdown blog posts with frontmatter
├── styles/main.css                  # layout, typography, and theming
├── fonts/                           # self-hosted WOFF2 files (see fonts/README.md)
├── assets/
│   ├── favicon.svg
│   └── images/                      # optional social preview image
├── build.py                         # renders templates → _site/ (deployable output)
├── pyproject.toml                   # Python project & dependency config
└── .github/workflows/deploy.yml     # GitHub Pages CI/CD
```

The deployable site is generated into `_site/` by `build.py` and excluded from
version control. Clone the repo and run the build to produce it. Only `_site/`
is published — templates, markdown sources, and build tooling stay out of the
deployed site.

### Themes

The site supports:

- **Auto** — respects the system `prefers-color-scheme`.
- **Light** — explicit light theme.
- **Dark** — explicit dark theme.

The toggle in the header is implemented using only CSS (`:has()` and radio
inputs); no JavaScript is required.

### Tactile feedback

Interactive elements (nav links, accordion headers, theme toggle, brand mark)
have subtle press-down effects on click/tap using CSS `:active` states. All
effects are GPU-composited transforms — no JavaScript, no extra dependencies.

A single CSS custom property controls everything. In `styles/main.css`:

```css
:root {
  --tactile: 1;   /* 1 = on, 0 = off */
}
```

Set `--tactile: 0` to disable all tactile effects without removing any code.
The `prefers-reduced-motion` media query also force-disables them automatically.

### Local development

**Prerequisites:** Python ≥ 3.13 and [uv](https://docs.astral.sh/uv/).

1. Install dependencies:

   ```bash
   uv sync
   ```

2. Build the site:

   ```bash
   uv run python build.py
   ```

This renders `templates/index.html.j2` -> `_site/index.html` and markdown posts
from `content/blog/*.md` -> `_site/blog/*.html`, and copies `styles/`, `fonts/`,
`assets/`, and `CNAME` alongside them. Re-run after any template or markdown
content change.

To preview the built site:

   ```bash
   python -m http.server -d _site 8000
   ```

### Code block syntax theme

Code block syntax highlighting flavor is set in `build.py` via the `CODE_THEME`
constant.

Supported values:

- `catppuccin-latte`
- `catppuccin-frappe`
- `catppuccin-macchiato`
- `catppuccin-mocha`

After changing `CODE_THEME`, run `uv run python build.py` to regenerate blog
HTML.

### Customization checklist

- **Branding**
  - Update the `<title>` and meta description in `templates/index.html.j2`.
  - Replace name and role text in the header and hero.
- **Content**
  - Rewrite About, Projects, and Experience copy in `templates/index.html.j2`.
  - Update project cards: titles, roles, years, and links.
  - Edit blog metadata and content in `content/blog/*.md`.
- **Contact**
  - Set your real email in the `mailto:` link.
  - Add or adjust external links in the contact section.
- **Assets**
  - Add your fonts to `fonts/` and ensure filenames match `styles/main.css`.
  - Export a `social-card.png` into `assets/images/` for Open Graph previews.

### Deployment

The site deploys to **GitHub Pages** via a GitHub Actions workflow
(`.github/workflows/deploy.yml`). On every push to `main`, the workflow:

1. Checks out the repo.
2. Installs Python 3.13 and the exact dependencies from `uv.lock` (`uv sync --locked`).
3. Runs `python build.py` to generate `_site/`.
4. Uploads `_site/` and deploys it to GitHub Pages.

The `CNAME` file pins the custom domain (`karmaindata.com`) and is copied into
`_site/` by the build. `uv.lock` is committed so CI and local builds resolve to
identical dependency versions.
