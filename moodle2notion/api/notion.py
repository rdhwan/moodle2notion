import httpx
from uuid import UUID


class NotionError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def get_databases(api_key: str, database_id: str) -> dict[str, any]:
    headers = {"Authorization": f"Bearer {api_key}", "Notion-Version": "2022-06-28"}
    r = httpx.get(f"https://api.notion.com/v1/databases/{database_id}", headers=headers)

    data = r.json()

    if r.status_code != 200:
        raise NotionError(f"Cannot get database, {data['status']}: {data['message']}")

    return data


def get_pages(api_key: str, page_id: str) -> dict[str, any]:
    headers = {"Authorization": f"Bearer {api_key}", "Notion-Version": "2022-06-28"}
    r = httpx.get(f"https://api.notion.com/v1/pages/{page_id}", headers=headers)

    data = r.json()

    if r.status_code != 200:
        raise NotionError(f"Cannot get pages, {data['status']}: {data['message']}")

    return data


def query_database(api_key: str, database_id: str) -> list[str]:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28",
    }

    payload = {
        "filter": {
            "property": "Status",
            "select": {
                "equals": "In Progress",
            },
        },
    }

    r = httpx.post(
        f"https://api.notion.com/v1/databases/{database_id}/query",
        headers=headers,
        json=payload,
    )

    if r.status_code != 200:
        print(r.json())
        raise NotionError("Cannot do query")

    data = []
    for i in r.json()["results"]:
        if text := i["properties"]["ID"]["rich_text"]:
            data.append(text[0]["text"]["content"])

    return data


def create_data(
    api_key: str, database_id: str, assignments: list[dict[str, any]]
) -> list[int]:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28",
    }

    statuses = []
    for data in assignments:
        payload = {
            "parent": {"database_id": database_id},
            "properties": {
                "Name": {
                    "title": [
                        {
                            "text": {"content": data["name"]},
                        },
                    ],
                },
                "ID": {
                    "rich_text": [
                        {
                            "text": {"content": data["id"]},
                        },
                    ]
                },
                "Matkul": {
                    "select": {"name": data["course"]},
                },
                "Status": {
                    "select": {"name": "In Progress"},
                },
                "Due": {
                    "date": {
                        "start": data["due"],
                        "end": None,
                    },
                },
            },
        }
        r = httpx.post(
            f"https://api.notion.com/v1/pages", headers=headers, json=payload
        )

        statuses.append(r.status_code)

    return statuses
