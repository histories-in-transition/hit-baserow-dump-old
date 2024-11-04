import os
import json
from jsonpath_ng import parse

ORIG_FOLDER = "json"
DATA_DIR = "data"


def add_related_objects(MODEL_CONFIG):
    for x in MODEL_CONFIG:
        try:
            rel_obj = x["related_objects"]
        except KeyError:
            continue
        final_file = os.path.join(*x["final_file"])
        with open(final_file, "r") as fp:
            source_data = json.load(fp)

        for item in rel_obj:
            print(f"adding {item['lookup_field']} from {item['source_file']} to {final_file}")
            source_file = item["source_file"]
            lookup_field = item["lookup_field"]

            feed_path = os.path.join(DATA_DIR, f"{source_file}.json")
            with open(feed_path, "r") as fp:
                feed_data = json.load(fp)

            for key, value in source_data.items():
                object_id = value["id"]
                related_items = []
                for _, rel_value in feed_data.items():
                    for m in rel_value[lookup_field]:
                        if m["id"] == object_id:
                            related_items.append(rel_value)
                            break
                value[f"related__{source_file}"] = related_items
        with open(final_file, "w", encoding="utf-8") as fp:
            json.dump(source_data, fp, ensure_ascii=False, indent=2)


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


def add_view_labels(MODEL_CONFIG, ID_FIELD):
    for x in MODEL_CONFIG:
        file_name = os.path.join(*x["final_file"])
        print(f"now adding view labels to {file_name}")
        try:
            jsonpath_expr = parse(x["label_lookup_expression"])
        except KeyError:
            jsonpath_expr = parse(f"$.{ID_FIELD}")
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
        file_name = os.path.join(*x["final_file"])
        print(f"now adding next/prev to {file_name}")
        with open(file_name, "r", encoding="utf-8") as fp:
            data = json.load(fp)
        key_list = sorted(data.keys())
        for i, v in enumerate(key_list):
            prev_item = data[key_list[i - 1]][ID_FIELD]
            try:
                prev_label = data[key_list[i - 1]]["view_label"]
            except KeyError:
                prev_label = prev_item
            try:
                next_item = data[key_list[i + 1]][ID_FIELD]
                try:
                    next_label = data[key_list[i + 1]]["view_label"]
                except KeyError:
                    next_label = next_item
            except IndexError:
                next_item = data[key_list[0]][ID_FIELD]
                try:
                    next_label = data[key_list[0]]["view_label"]
                except KeyError:
                    next_label = next_item
            value = data[key_list[i]]

            value["prev"] = {"id": prev_item, "label": prev_label}
            value["next"] = {"id": next_item, "label": next_label}
        with open(file_name, "w", encoding="utf-8") as fp:
            json.dump(data, fp, ensure_ascii=False, indent=2)
