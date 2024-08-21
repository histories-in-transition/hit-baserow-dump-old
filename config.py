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
]
