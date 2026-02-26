import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape


ROOT = Path(__file__).parent
TEMPLATES_DIR = ROOT / "templates"


def create_env() -> Environment:
  return Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(["html", "xml"]),
  )


def load_blogs() -> list[dict]:
  with open(ROOT / "blogs.json", encoding="utf-8") as f:
    return json.load(f)


def render_template(env: Environment, src: str, dest: str, **context) -> None:
  template = env.get_template(src)
  output = template.render(**context)

  out_path = ROOT / dest
  out_path.parent.mkdir(parents=True, exist_ok=True)
  out_path.write_text(output, encoding="utf-8")


def main() -> None:
  env = create_env()
  blogs = load_blogs()

  render_template(env, "index.html.j2", "index.html", blogs=blogs)

  for post in blogs:
    src = f"blog/{post['slug']}.html.j2"
    dest = f"blog/{post['slug']}.html"
    render_template(env, src, dest, post=post)


if __name__ == "__main__":
  main()
