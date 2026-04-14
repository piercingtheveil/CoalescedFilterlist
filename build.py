import requests
from pathlib import Path

def load_urls(path):
    urls = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
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

    for url in urls:
        merged.append(f"! Source: {url}")
        try:
            r = requests.get(url, timeout=60)
            r.raise_for_status()

            for line in r.text.splitlines():
                line = line.rstrip()
                if not line:
                    continue

                if line in seen:
                    continue

                seen.add(line)
                merged.append(line)

            merged.append("")

        except Exception as e:
            merged.append(f"! Failed to fetch {url}: {e}")
            merged.append("")

         Path(output_file).write_text("
         ".join(merged) + "
         ", encoding="utf-8")
         print(f"Wrote {output_file}")

build_list("Sources-Expert.md", "Expert.txt", "Expert")
build_list("Sources-Green.md", "Green.txt", "Green")
