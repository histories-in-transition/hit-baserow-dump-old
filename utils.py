import os
import json
from jsonpath_ng import parse

ORIG_FOLDER = "json"


def denormalize(MODEL_CONFIG):
    print("starting denormalizing")
    for x in MODEL_CONFIG:
        print(x["table_label"])
        final_file = os.path.join(*x["final_file"])
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


def add_view_labels(MODEL_CONFIG):
    for x in MODEL_CONFIG:
        print("now adding view labels")
        file_name = os.path.join(*x["final_file"])
        try:
            jsonpath_expr = parse(x["label_lookup_expression"])
        except KeyError:
            continue
        print(f"    - {jsonpath_expr} for {file_name}")
        with open(file_name, "r", encoding="utf-8") as fp:
            data = json.load(fp)
            for key, value in data.items():
                try:
                    value["view_label"] = jsonpath_expr.find(value)[0].value
                except IndexError:
                    value["view_label"] = f"NO MATCH FOR {x['label_lookup_expression']}"
        with open(file_name, "w", encoding="utf-8") as fp:
            json.dump(data, fp, ensure_ascii=False, indent=2)


def add_prev_next(MODEL_CONFIG, ID_FIELD):
    for x in MODEL_CONFIG:
        print("now adding view labels")
        file_name = os.path.join(*x["final_file"])
        with open(file_name, "r", encoding="utf-8") as fp:
            data = json.load(fp)
        key_list = sorted(data.keys())
        for i, v in enumerate(key_list):
            prev_item = data[key_list[i - 1]][ID_FIELD]
            try:
                next_item = data[key_list[i + 1]][ID_FIELD]
            except IndexError:
                next_item = data[key_list[0]]
            value = data[key_list[i]]

            value["prev"] = {
                "id": f"{prev_item}.html"}
            
            value["next"] = f"{next_item}.html"