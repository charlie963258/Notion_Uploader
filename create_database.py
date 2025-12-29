import json
import os
from pprint import pprint
from notion_client import Client
from dotenv import load_dotenv
load_dotenv()

#DATABASE = os.environ["MT_BENCH_DATABASE"]
API_KEY = os.environ["TEST_TOKEN"]
DATABASE = os.environ["TEST_DATABASE"]

client = Client(auth=API_KEY)

database_pages = client.databases.update(
    **{
        "database_id": DATABASE,
        "properties": {
            "zh2en": {
                "number": {
                    "format": "number"
                }
            },
            "en2zh": {
                "number": {
                    "format": "number"
                }
            },
            "summary": {
                "number": {
                    "format": "number"
                }
            },
            "essay": {
                "number": {
                    "format": "number"
                }
            },
            "letter": {
                "number": {
                    "format": "number"
                }
            },
            "Vicuna": {
                "number": {
                    "format": "number"
                }
            },
            "14tasks": {
                "number": {
                    "format": "number"
                }
            },
            # "inst_level_loose_acc_stderr": {
            #     "number": {
            #         "format": "number"
            #     }
            # },
            "Date": {
                "date":{}
            }
        }
    }
)

print(client.databases.query(**{
    "database_id": DATABASE
}))