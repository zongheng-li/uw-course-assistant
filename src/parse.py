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



courses = []
for block in blocks:
    courses.append(parse_block(block))

out_path = Path("data/courses.json")
out_path.write_text(json.dumps(courses, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Saved {len(courses)} courses to {out_path}")

with_req = 0
for course in courses:
    req = course["extras"].get("Requisites", "None")
    if req != "None":
        with_req += 1
print(f"Courses with real prerequisites: {with_req}")

labels = set()
for course in courses:
    for label in course["extras"]:
        labels.add(label)
print("All extra fields:", sorted(labels))



