import json
import os

from config import DATA_FOLDER, DENORMALIZE_CONFIG


os.makedirs(DATA_FOLDER, exist_ok=True)

for x in DENORMALIZE_CONFIG:
    print(x["table_label"])
    final_file = os.path.join(*x["final_file"])
    to_delete = x.get("fields_to_delete", [])
    for y in x["fields"]:
        source_file = os.path.join(*y["source_file"])
        with open(source_file, "r", encoding="utf-8") as f:
            source_data = json.load(f)
        print(f"  - {y['field_name']}")
        seed_file = os.path.join(os.path.join(*y["seed_file"]))
        with open(seed_file, "r", encoding="utf-8") as f:
            seed_data = json.load(f)
        for key, value in source_data.items():
            old_values = value[y["field_name"]]
            new_values = []
            for old_val in old_values:
                new_values.append(seed_data[f"{old_val['id']}"])
            value[y["field_name"]] = new_values
        print(f"  saving {x['table_label']} as {final_file}")
        with open(final_file, "w", encoding="utf-8") as f:
            json.dump(source_data, f, ensure_ascii=False, indent=2)
