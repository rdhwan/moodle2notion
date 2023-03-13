import datetime
import time
import yaml
from api import moodle, notion
import schedule
import logging

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)["config"]


CURR_TOKEN = ""


def job() -> None:
    """
    This job fetch data from Moodle and create pages in Notion if it doesn't exists
    """

    global CURR_TOKEN

    if not CURR_TOKEN:
        print(f"{datetime.datetime.now().ctime()} : Getting first token")

        CURR_TOKEN = moodle.get_token(
            config["moodle"]["host"],
            config["moodle"]["username"],
            config["moodle"]["password"],
        )

    try:
        timeline_data = moodle.get_timeline(config["moodle"]["host"], CURR_TOKEN)
        print(f"{datetime.datetime.now().ctime()} : Trying to use last token")

    except moodle.MoodleError as r:
        CURR_TOKEN = moodle.get_token(
            config["moodle"]["host"],
            config["moodle"]["username"],
            config["moodle"]["password"],
        )
        print(f"{datetime.datetime.now().ctime()} : Token updated")

        timeline_data = moodle.get_timeline(config["moodle"]["host"], CURR_TOKEN)

    if not timeline_data:
        print("The timeline is probably empty or the server error.")
        return

    query = notion.query_database(
        config["notion"]["api_key"], config["notion"]["database"]
    )

    entries = []
    for data in timeline_data:
        if data["id"] not in query:
            entries.append(data)

    res = notion.create_data(
        config["notion"]["api_key"], config["notion"]["database"], entries
    )

    if not res:
        print(f"{datetime.datetime.now().ctime()} : Nothing updated")
    else:
        print(f"{datetime.datetime.now().ctime()}: Items updated")


if __name__ == "__main__":
    print(
        f"{datetime.datetime.now().ctime()}: Application startup complete. Will update every 30 minutes."
    )
    schedule.every(30).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
