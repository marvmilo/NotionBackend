import time
import schedule
from dotenv import load_dotenv

load_dotenv()

import update_reccuring_tasks
import delete_old_tasks

schedule.every().day.at("00:00").do(update_reccuring_tasks.function)
schedule.every().day.at("00:00").do(delete_old_tasks.function)

while True:
    schedule.run_pending()
    time.sleep(1)