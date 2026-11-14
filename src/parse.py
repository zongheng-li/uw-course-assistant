import json
from pathlib import Path
from bs4 import BeautifulSoup


def clean(text):
    return " ".join(text.split())


def parse_block(block):
    code = clean(block.select_one("span.courseblockcode").get_text())

    full_title = clean(block.select_one("p.courseblocktitle").get_text(" "))
    parts = full_title.split("—", 1)
    title = parts[1].strip()

    credits_el = block.select_one("p.courseblockcredits")
    credits = clean(credits_el.get_text())

    desc_el = block.select_one("p.courseblockdesc")
    description = clean(desc_el.get_text(" "))

    extras = {}
    for label_el in block.select("span.cbextra-label"):
        label = clean(label_el.get_text()).rstrip(":")
        data_el = label_el.find_next("span", class_="cbextra-data")
        extras[label] = clean(data_el.get_text(" "))

    return {
        "code": code,
        "title": title,
        "credits": credits,
        "description": description,
        "extras": extras,
    }


html = Path("data/raw/comp_sci.html").read_text(encoding="utf-8")
soup = BeautifulSoup(html, "html.parser")
blocks = soup.select("div.courseblock")
print(f"Found {len(blocks)} courses")

for block in blocks:
    course = parse_block(block)
    if course["code"] == "COMP SCI 540":
        print(json.dumps(course, indent=2, ensure_ascii=False))
        break