import time
from datetime import datetime
import schedule


def job():
    from mysolmate import adjust_min_injection
    adjust_min_injection()


job()
schedule.every(15).minutes.do(job)

while True:
    now = datetime.now()
    print(f"Main loop at {now}")
    schedule.run_pending()
    time.sleep(60)
