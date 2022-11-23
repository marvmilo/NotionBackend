import os
import datetime as dt
from notion_client import Client

def function():
    notion = Client(auth=os.environ["NOTION_TOKEN"])
    todo_database = notion.databases.query(database_id="25f492da-5bba-4306-9d53-f1e2e5b009d3")
    for page in todo_database["results"]:
        try:
            interval = page["properties"]["Wiederholungs Interval"]["number"]
            status = page["properties"]["Status"]["status"]["name"]
            unit = page["properties"]["Wiederholungs Einheit"]["select"]["name"]
            date = page["properties"]["Date"]["date"]["start"]
        except TypeError:
            unit = None
            date = None
        
        if interval and unit and date and status == "Done":
            if unit == "täglich":
                delta = dt.timedelta(days = interval)
            elif unit == "wöchentlich":
                delta = dt.timedelta(weeks = interval)
            elif unit == "monatlich":
                delta = dt.timedelta(days = interval*30)
            elif unit == "jährlich":
                delta = dt.timedelta(days = interval*365)
            
            next_date = (dt.datetime.now() - dt.timedelta(days = 1) + delta).strftime("%Y-%m-%d")
            new_date_property = page["properties"]["Date"]
            new_date_property["date"]["start"] = next_date
            
            notion.pages.update(page_id = page["id"], properties = {"Status": None})
            notion.pages.update(page_id = page["id"], properties = {"Date": new_date_property})
