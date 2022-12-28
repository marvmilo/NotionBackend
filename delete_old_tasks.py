import os
import datetime as dt
from notion_client import Client

todo_database_id = "08ca089e-8b53-4804-9632-4fc0c91ad58c"

def function():
    notion = Client(auth=os.environ["NOTION_TOKEN"])
    next_cursor = None
    
    while True:
        todo_database = notion.databases.query(database_id=todo_database_id, start_cursor = next_cursor)
        next_cursor = todo_database["next_cursor"]
        for page in todo_database["results"]:
            delete_timestamp = dt.datetime.now() - dt.timedelta(days = 31)
            task_timestamp = dt.datetime.strptime(page["properties"]["Last edited time"]["last_edited_time"], "%Y-%m-%dT%H:%M:%S.%fZ")
            status = page["properties"]["Status"]["status"]["name"]
            
            if task_timestamp < delete_timestamp and status == "Done":
                notion.pages.update(page_id = page["id"], archived = True)
        
        if not next_cursor:
            break
