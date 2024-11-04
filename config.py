import os
from acdh_baserow_pyutils import BaseRowClient


BASEROW_DB_ID = 577
BASEROW_URL = "https://baserow.acdh-dev.oeaw.ac.at/api/"
BASEROW_USER = os.environ.get("BASEROW_USER")
BASEROW_PW = os.environ.get("BASEROW_PW")
BASEROW_TOKEN = os.environ.get("BASEROW_TOKEN")
JSON_FOLDER = "json_dumps"
TEI_FOLDER = "tei"
DATA_FOLDER = "data"

try:
    br_client = BaseRowClient(
        BASEROW_USER, BASEROW_PW, BASEROW_TOKEN, br_base_url=BASEROW_URL
    )
except KeyError:
    br_client = None


DENORMALIZE_CONFIG = [
    {
        "table_label": "PLACES",
        "final_file": [DATA_FOLDER, "places.json"],
        "fields": [
            {
                "field_name": "country",
                "seed_file": [JSON_FOLDER, "places.json"],
                "source_file": [JSON_FOLDER, "places.json"],
            }
        ],
    },
    {
        "table_label": "GENRES",
        "final_file": [DATA_FOLDER, "genres.json"],
        "fields": [
            {
                "field_name": "main_genre",
                "seed_file": [JSON_FOLDER, "genres.json"],
                "source_file": [JSON_FOLDER, "genres.json"],
            }
        ],
    },
    {
        "table_label": "ORGS",
        "final_file": [DATA_FOLDER, "orgs.json"],
        "fields": [
            {
                "field_name": "settlement",
                "seed_file": [JSON_FOLDER, "places.json"],
                "source_file": [JSON_FOLDER, "libraries_organisations.json"],
            }
        ],
    },
    {
        "table_label": "WORKS",
        "label_lookup_expression": "$.title",
        "final_file": [DATA_FOLDER, "works.json"],
        "fields": [
            {
                "field_name": "source_text",
                "seed_file": [JSON_FOLDER, "works.json"],
                "source_file": [JSON_FOLDER, "works.json"],
            },
            {
                "field_name": "genre",
                "seed_file": [DATA_FOLDER, "genres.json"],
                "source_file": [DATA_FOLDER, "works.json"],
            },
            {
                "field_name": "author",
                "seed_file": [JSON_FOLDER, "people.json"],
                "source_file": [DATA_FOLDER, "works.json"],
            },
        ],
    },
    {
        "table_label": "MANUSCRIPTS DATED",
        "label_lookup_expression": "$..shelfmark[0].value",
        "final_file": [DATA_FOLDER, "manuscripts_dated.json"],
        "fields": [
            {
                "field_name": "date",
                "seed_file": [JSON_FOLDER, "dates.json"],
                "source_file": [JSON_FOLDER, "manuscripts_dated.json"],
            },
            {
                "field_name": "authority",
                "seed_file": [JSON_FOLDER, "bibliography.json"],
                "source_file": [DATA_FOLDER, "manuscripts_dated.json"],
            },
        ],
    },
    {
        "table_label": "MANUSCRIPTS",
        "label_lookup_expression": "$..shelfmark[0].value",
        "final_file": [DATA_FOLDER, "manuscripts.json"],
        "fields": [
            {
                "field_name": "orig_place",
                "seed_file": [DATA_FOLDER, "places.json"],
                "source_file": [JSON_FOLDER, "manuscripts.json"],
            },
            {
                "field_name": "library_full",
                "seed_file": [DATA_FOLDER, "orgs.json"],
                "source_file": [DATA_FOLDER, "manuscripts.json"],
            },
            {
                "field_name": "manuscripts_dated",
                "seed_file": [DATA_FOLDER, "manuscripts_dated.json"],
                "source_file": [DATA_FOLDER, "manuscripts.json"],
            },
            {
                "field_name": "provenance",
                "seed_file": [DATA_FOLDER, "orgs.json"],
                "source_file": [DATA_FOLDER, "manuscripts.json"],
            },
        ],
    },
    {
        "table_label": "HANDS DATED",
        "final_file": [DATA_FOLDER, "hands_dated.json"],
        "fields": [
            {
                "field_name": "authority",
                "seed_file": [JSON_FOLDER, "bibliography.json"],
                "source_file": [JSON_FOLDER, "hands_dated.json"],
            },
            {
                "field_name": "dated",
                "seed_file": [JSON_FOLDER, "dates.json"],
                "source_file": [DATA_FOLDER, "hands_dated.json"],
            },
        ],
    },
    {
        "table_label": "HANDS PLACES",
        "final_file": [DATA_FOLDER, "hands_placed.json"],
        "fields": [
            {
                "field_name": "authority",
                "seed_file": [JSON_FOLDER, "bibliography.json"],
                "source_file": [JSON_FOLDER, "hands_placed.json"],
            },
            {
                "field_name": "place",
                "seed_file": [DATA_FOLDER, "places.json"],
                "source_file": [DATA_FOLDER, "hands_placed.json"],
            },
        ],
    },
    {
        "table_label": "HANDS",
        "final_file": [DATA_FOLDER, "hands.json"],
        "fields": [
            {
                "field_name": "scribe",
                "seed_file": [JSON_FOLDER, "people.json"],
                "source_file": [JSON_FOLDER, "hands.json"],
            },
            {
                "field_name": "hands_dated",
                "seed_file": [DATA_FOLDER, "hands_dated.json"],
                "source_file": [DATA_FOLDER, "hands.json"],
            },
            {
                "field_name": "hands_placed",
                "seed_file": [DATA_FOLDER, "hands_placed.json"],
                "source_file": [DATA_FOLDER, "hands.json"],
            },
        ],
    },
    {
        "table_label": "CODICOLIGAL UNIT",
        "label_lookup_expression": "$..label[0].value",
        "final_file": [DATA_FOLDER, "cod_units.json"],
        "fields": [
            {
                "field_name": "prov_place",
                "seed_file": [DATA_FOLDER, "places.json"],
                "source_file": [JSON_FOLDER, "cod_units.json"],
            },
            {
                "field_name": "quire",
                "seed_file": [JSON_FOLDER, "quires.json"],
                "source_file": [DATA_FOLDER, "cod_units.json"],
            },
        ],
    },
    {
        "table_label": "MS ITEMS",
        "final_file": [DATA_FOLDER, "ms_items.json"],
        "label_lookup_expression": "$..label[0].value",
        "fields": [
            {
                "field_name": "cod_unit",
                "seed_file": [DATA_FOLDER, "cod_units.json"],
                "source_file": [JSON_FOLDER, "ms_items.json"],
            },
            {
                "field_name": "hands_role",
                "seed_file": [JSON_FOLDER, "hands_role.json"],
                "source_file": [DATA_FOLDER, "ms_items.json"],
            },
            {
                "field_name": "title_work",
                "seed_file": [DATA_FOLDER, "works.json"],
                "source_file": [DATA_FOLDER, "ms_items.json"],
            },
            {
                "field_name": "manuscript",
                "seed_file": [DATA_FOLDER, "manuscripts.json"],
                "source_file": [DATA_FOLDER, "ms_items.json"],
            },
        ],
    },
    {
        "table_label": "HANDS ROLE",
        "final_file": [DATA_FOLDER, "hands_role.json"],
        "fields": [
            {
                "field_name": "ms_item",
                "seed_file": [DATA_FOLDER, "ms_items.json"],
                "source_file": [JSON_FOLDER, "hands_role.json"],
            },
        ],
    },
    {
        "table_label": "STRATA",
        "label_lookup_expression": "$..label[0].value",
        "final_file": [DATA_FOLDER, "strata.json"],
        "fields": [
            {
                "field_name": "hand_role",
                "seed_file": [DATA_FOLDER, "hands_role.json"],
                "source_file": [JSON_FOLDER, "strata.json"],
            },
        ],
    },
    {
        "table_label": "HANDS",
        "label_lookup_expression": "$..label[0].value",
        "final_file": [DATA_FOLDER, "hands.json"],
        "fields": [
            {
                "field_name": "hands_role",
                "seed_file": [DATA_FOLDER, "hands_role.json"],
                "source_file": [DATA_FOLDER, "hands.json"],
            },
        ],
    },
]
