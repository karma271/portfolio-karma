## Minimal Portfolio

**Stack**: HTML + CSS only (no JavaScript).

This is a minimal, modern portfolio site built to highlight calm, considered work. It focuses on typography, accessibility, and small design details rather than heavy effects or dependencies.

### Structure

- `index.html` — single-page portfolio.
- `styles/main.css` — layout, typography, and theming.
- `fonts/` — local WOFF2 font files (see `fonts/README.md`).
- `assets/favicon.svg` — SVG favicon used by the `<link rel="icon">` tag.
- `assets/images/` — optional social preview image, see `assets/images/README.md`.
- `blog/` — individual blog post pages (`blog_1.html`, `blog_2.html`, ...).
- `templates/` — Jinja2 templates and partials used to generate the HTML.
- `build.py` — small Python build script to render templates to static HTML.

### Themes

The site supports:

- **Auto** — respects the system `prefers-color-scheme`.
- **Light** — explicit light theme.
- **Dark** — explicit dark theme.
- **Reader** — high-comfort, text-focused theme (~72ch max width).

The toggle in the header is implemented using only CSS (`:has()` and radio inputs); no JavaScript is required.

### Customization checklist

- **Branding**
  - Update the `<title>` and meta description in `index.html`.
  - Replace "Your Name" and role text in the header and hero.
- **Contact**
  - Set your real email in the `mailto:` link.
  - Add or adjust external links in the contact section.
- **Content**
  - Rewrite About, Projects, and Experience copy to match your work.
  - Update project cards: titles, roles, years, and links.
  - Update blog cards in the “Notes & writing” section and their corresponding
    `blog/blog_X.html` pages (titles, dates, and body copy).
- **Assets**
  - Add your fonts to `fonts/` and ensure filenames match `styles/main.css`.
  - Export a `social-card.png` into `assets/images/` for Open Graph previews.

### Template-based build (optional but recommended)

To avoid repeating the header and footer across pages, the project includes a
tiny Python + Jinja2 build step:

- Install dependencies (once):

  ```bash
  pip install -r requirements.txt
  ```

- Regenerate `index.html` and the blog pages from templates:

  ```bash
  python build.py
  ```

Edit the files under `templates/` (for example `templates/index.html.j2` and
`templates/blog/blog_1.html.j2`); then run `python build.py` to update the
corresponding `.html` files in the project root and `blog/` directory.

Open `index.html` in a browser to view the site. No build step is required.


