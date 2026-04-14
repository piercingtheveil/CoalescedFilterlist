import requests
from pathlib import Path

def load_urls(path):
    urls = []
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#"):
            urls.append(line)
    return urls


def build_list(source_file, output_file, title):
    urls = load_urls(source_file)
    merged = []
    seen = set()

    merged.append(f"! {title}")
    merged.append("! Auto-generated from source lists")
    merged.append("")

    session = requests.Session()
    session.headers.update({"User-Agent": "list-builder/1.0"})

    for url in urls:
        merged.append(f"! Source: {url}")
        try:
            r = session.get(url, timeout=60)
            r.raise_for_status()

            for line in r.text.splitlines():
                line = line.rstrip()
                if not line or line in seen:
                    continue
                seen.add(line)
                merged.append(line)

            merged.append("")

        except Exception as e:
            merged.append(f"! Failed to fetch {url}: {e}")
            merged.append("")

    out_path = Path(output_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(merged) + "\n", encoding="utf-8")
    print(f"Wrote {output_file}")

build_list("Sources-Expert.md", "Expert.txt", "Expert")
build_list("Sources-Green.md", "Green.txt", "Green")
