import json
import os

import marko

from config import DATA_FOLDER, MODEL_CONFIG, ID_FIELD, DEFAULT_DELETE_FIELDS
from utils import add_view_labels, denormalize, add_prev_next, add_related_objects, remove_fields


os.makedirs(DATA_FOLDER, exist_ok=True)

fixme_file = os.path.join("json_dumps", "manuscripts.json")

print(f"fix markup in {fixme_file}")
with open(fixme_file, "r", encoding="utf-8") as fp:
    data = json.load(fp)

for _, value in data.items():
    text = value["quire_structure"]
    value["quire_structure"] = (
        marko.convert(text)
        .replace("strong>", "sup>")
        .replace("<p>", "")
        .replace("</p>", "")
    )

with open(fixme_file, "w", encoding="utf-8") as fp:
    json.dump(data, fp, ensure_ascii=False, indent=2)


fixme_file = os.path.join("json_dumps", "quires.json")

print(f"fix markup in {fixme_file}")
with open(fixme_file, "r", encoding="utf-8") as fp:
    data = json.load(fp)

for _, value in data.items():
    text = value["quire_structure"]
    value["quire_structure"] = (
        marko.convert(text)
        .replace("strong>", "sup>")
        .replace("<p>", "")
        .replace("</p>", "")
        .replace("\n", "")
    )

with open(fixme_file, "w", encoding="utf-8") as fp:
    json.dump(data, fp, ensure_ascii=False, indent=2)

denormalize(MODEL_CONFIG)
add_view_labels(MODEL_CONFIG, ID_FIELD)
add_prev_next(MODEL_CONFIG, ID_FIELD)
add_related_objects(MODEL_CONFIG)
remove_fields(MODEL_CONFIG, DEFAULT_DELETE_FIELDS)
