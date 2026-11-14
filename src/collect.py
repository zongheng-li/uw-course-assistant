import requests
import time
from pathlib import Path

depts = ["comp_sci"]
headers = {"User-Agent": "uw-course-assistant (student project; github.com/zongheng-li)"}

for dept in depts:
    url = f"https://guide.wisc.edu/courses/{dept}/"
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    out_path = Path(f"data/raw/{dept}.html")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(response.text, encoding="utf-8")

    print(f"Saved {dept}: {len(response.text)} characters")
    time.sleep(1.5)



