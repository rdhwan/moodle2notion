import datetime
import httpx
import html


class MoodleError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def get_token(url: str, username: str, password: str) -> str:
    r = httpx.get(
        url
        + f"login/token.php?service=moodle_mobile_app&username={username}&password={password}"
    )

    data: dict[str, any] = r.json()

    if data.get("errorcode"):
        raise MoodleError("Invalid token, please retry")

    return data["token"]


def get_timeline(url: str, token: str) -> list[dict[str, any]]:
    r = httpx.get(
        url
        + f"/webservice/rest/server.php?wstoken={token}&moodlewsrestformat=json&wsfunction=core_calendar_get_action_events_by_timesort"
    )

    data: dict[str, any] = r.json()

    if data.get("errorcode"):
        raise MoodleError("Invalid token, please retry")

    return [
        {
            "id": str(i["id"]),
            "name": html.unescape(i["name"]),
            "course": html.unescape(i["course"]["fullname"]),
            "due": datetime.datetime.fromtimestamp(i["timesort"]).strftime("%Y-%m-%d"),
        }
        for i in data["events"]
    ]
