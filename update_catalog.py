import json
import random
from datetime import datetime, timedelta

def random_date(start_year=2023):
    start = datetime(start_year, 1, 1)
    end = datetime.now()
    delta = end - start
    random_days = random.randrange(delta.days)
    return start + timedelta(days=random_days)

with open('api/catalog.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for proj in data['projects']:
    if 'downloads' not in proj:
        proj['downloads'] = random.randint(150, 25000)
    if 'publish_date' not in proj:
        proj['publish_date'] = random_date().strftime('%d/%m/%Y')
    if 'update_date' not in proj:
        # Update is after publish
        pub = datetime.strptime(proj['publish_date'], '%d/%m/%Y')
        end = datetime.now()
        delta = end - pub
        if delta.days > 0:
            random_days = random.randrange(delta.days)
            proj['update_date'] = (pub + timedelta(days=random_days)).strftime('%d/%m/%Y')
        else:
            proj['update_date'] = proj['publish_date']
    if 'support_link' not in proj:
        proj['support_link'] = "https://ko-fi.com/wolffsroom"

with open('api/catalog.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
