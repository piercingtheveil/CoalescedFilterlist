import requests
from pathlib import Path

sources_file = Path("sources.md")
output_file = Path("coalesced.txt")

urls = []

for line in sources_file.read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if line and not line.startswith("#"):
        urls.append(line)

merged = []
seen = set()

merged.append("! Combined filter list")
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

output_file.write_text("
".join(merged) + "\n", encoding="utf-8")
print(f"Wrote {output_file}")
