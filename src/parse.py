from pathlib import Path
from bs4 import BeautifulSoup

html = Path("data/raw/comp_sci.html").read_text(encoding="utf-8")
soup = BeautifulSoup(html, "html.parser")

blocks = soup.select("div.courseblock")
print(f"Found {len(blocks)} courses")

for block in blocks[:5]:
    title = block.select_one("p.courseblocktitle")
    print(title.get_text(" ", strip=True))