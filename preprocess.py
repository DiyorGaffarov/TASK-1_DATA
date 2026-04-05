import re
import json

with open("dataset/task1_d.json", "r") as f:
    data = f.read()

# Convert Ruby-style → JSON
data = re.sub(r":(\w+)=>", r'"\1":', data)   # keys
data = data.replace("'", '"')                # quotes

books = json.loads(data)