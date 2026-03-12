from pathlib import Path

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pygments.formatters import HtmlFormatter

ROOT = Path(__file__).parent
TEMPLATES_DIR = ROOT / "templates"
CONTENT_BLOG_DIR = ROOT / "content" / "blog"
CODE_THEME = "catppuccin-mocha"
SUPPORTED_CODE_THEMES = {
    "catppuccin-latte",
    "catppuccin-frappe",
    "catppuccin-macchiato",
    "catppuccin-mocha",
}
REQUIRED_FRONTMATTER_FIELDS = (
    "slug",
    "title",
    "meta_description",
    "description",
    "pill",
    "published",
    "read_time",
    "topics",
)


def create_env() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html", "xml"]),
    )


def parse_markdown_post(path: Path, code_theme: str) -> dict:
    raw = path.read_text(encoding="utf-8")
    frontmatter: dict = {}
    body = raw

    if raw.startswith("---\n"):
        frontmatter_text, sep, remainder = raw[4:].partition("\n---\n")
        if sep:
            frontmatter = yaml.safe_load(frontmatter_text) or {}
            body = remainder

    slug = str(frontmatter.get("slug") or path.stem)
    content_html = markdown.markdown(
        body,
        extensions=[
            "fenced_code",
            "codehilite",
            "tables",
            "sane_lists",
            "attr_list",
        ],
        extension_configs={
            "codehilite": {
                "guess_lang": False,
                "use_pygments": True,
                "pygments_style": code_theme,
                "noclasses": False,
                "css_class": "codehilite",
            }
        },
    )

    return {
        **frontmatter,
        "slug": slug,
        "draft": bool(frontmatter.get("draft", False)),
        "content_html": content_html,
    }


def validate_markdown_post(post: dict, path: Path) -> None:
    missing = [field for field in REQUIRED_FRONTMATTER_FIELDS if not post.get(field)]
    if missing:
        raise ValueError(
            f"Missing required frontmatter in {path}: {', '.join(missing)}"
        )

    toc = post.get("toc")
    if toc is None:
        return

    if not isinstance(toc, list):
        raise ValueError(f"Frontmatter 'toc' must be a list in {path}")

    for i, item in enumerate(toc):
        if not isinstance(item, dict):
            raise ValueError(f"Frontmatter 'toc[{i}]' must be an object in {path}")
        if not item.get("id") or not item.get("label"):
            raise ValueError(
                f"Frontmatter 'toc[{i}]' must include non-empty id and label in {path}"
            )


def load_markdown_posts(code_theme: str) -> list[dict]:
    if not CONTENT_BLOG_DIR.exists():
        return []

    posts: dict[str, dict] = {}
    for path in sorted(CONTENT_BLOG_DIR.glob("*.md")):
        post = parse_markdown_post(path, code_theme)
        validate_markdown_post(post, path)
        if post["slug"] in posts:
            raise ValueError(f"Duplicate slug '{post['slug']}' in {path}")
        posts[post["slug"]] = post

    return [post for post in posts.values() if not post.get("draft", False)]


def render_template(env: Environment, src: str, dest: str, **context) -> None:
    template = env.get_template(src)
    output = template.render(**context)

    out_path = ROOT / dest
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(output, encoding="utf-8")


def get_code_theme_css(code_theme: str) -> str:
    """Generate CSS classes for the configured Catppuccin syntax flavor."""
    return HtmlFormatter(
        style=code_theme,
        cssclass="codehilite",
    ).get_style_defs(".codehilite")


def main() -> None:
    print("Running build process...")
    env = create_env()
    if CODE_THEME not in SUPPORTED_CODE_THEMES:
        choices = ", ".join(sorted(SUPPORTED_CODE_THEMES))
        raise ValueError(
            f"Unsupported CODE_THEME '{CODE_THEME}' in build.py. "
            f"Use one of: {choices}"
        )
    code_theme = CODE_THEME
    posts = load_markdown_posts(code_theme)
    code_theme_css = get_code_theme_css(code_theme)

    render_template(env, "index.html.j2", "index.html", blogs=posts)

    for i, post in enumerate(posts):
        print(f"\tProcessing blog post {i+1}/{len(posts)}")
        dest = f"blog/{post['slug']}.html"
        render_template(
            env,
            "blog/markdown_post.html.j2",
            dest,
            post=post,
            code_theme_css=code_theme_css,
        )

    print("Completed build process!")


if __name__ == "__main__":
    main()
