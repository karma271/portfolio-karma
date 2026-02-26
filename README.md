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
│   │   └── blog_*.html.j2           #   individual posts
│   └── partials/                    #   reusable header & footer fragments
├── styles/main.css                  # layout, typography, and theming
├── fonts/                           # self-hosted WOFF2 files (see fonts/README.md)
├── assets/
│   ├── favicon.svg
│   └── images/                      # optional social preview image
├── blogs.json                       # blog metadata (titles, descriptions, TOC)
├── build.py                         # renders templates → static HTML
├── pyproject.toml                   # Python project & dependency config
└── .github/workflows/deploy.yml     # GitHub Pages CI/CD
```

`index.html` and `blog/*.html` are **generated** by `build.py` and excluded
from version control. Clone the repo and run the build to produce them.

### Themes

The site supports:

- **Auto** — respects the system `prefers-color-scheme`.
- **Light** — explicit light theme.
- **Dark** — explicit dark theme.

The toggle in the header is implemented using only CSS (`:has()` and radio
inputs); no JavaScript is required.

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

This renders `templates/index.html.j2` → `index.html` and each
`templates/blog/blog_*.html.j2` → `blog/blog_*.html`. Re-run after any
template or `blogs.json` change.

### Customization checklist

- **Branding**
  - Update the `<title>` and meta description in `templates/index.html.j2`.
  - Replace name and role text in the header and hero.
- **Content**
  - Rewrite About, Projects, and Experience copy in `templates/index.html.j2`.
  - Update project cards: titles, roles, years, and links.
  - Edit blog metadata (titles, descriptions, dates) in `blogs.json`.
  - Edit blog post content in `templates/blog/blog_*.html.j2`.
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
2. Installs Python 3.13 and Jinja2.
3. Runs `python build.py` to generate the HTML.
4. Uploads and deploys the result to GitHub Pages.

A `CNAME` file pins the custom domain.
