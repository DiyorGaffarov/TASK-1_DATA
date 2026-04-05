import re
import json

with open("dataset/task1_d.json", "r") as f:
    data = f.read()

data = re.sub(r":(\w+)=>", r'"\1":', data)

data = re.sub(r'(?<![a-zA-Z]):\s*([a-zA-Z_]\w*)', r'"\1"', data)

data = data.replace("\\'", "'")

books = json.loads(data)
print(f"Successfully loaded {len(books)} records")

with open("dataset/task1_d_processed.json", "w", encoding="utf-8") as f:
    json.dump(books, f, indent=4, ensure_ascii=False)


