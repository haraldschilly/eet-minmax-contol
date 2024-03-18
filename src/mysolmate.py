import sys, os
from datetime import datetime
import pytz

from solmate_sdk import SolMateAPIClient

SERIAL_NUM = os.environ['SOLMATE_SERIAL_NUM']


def adjust_min_injection():
    client = SolMateAPIClient(SERIAL_NUM)
    client.connect()
    client.quickstart()

    #print(f"Your SolMate online status is: {client.check_online()}")

    check = client.check_online()
    if check:
        print('Online')
    else:
        print('Offline')
        sys.exit(1)

    vals = client.get_live_values()
    print(f"Your SolMate live values are: {vals}")
    pv_w = vals['pv_power']
    print(f"PV: {pv_w:.0f} W")
    bat_pct = 100 * vals['battery_state']
    print(f"BAT: {bat_pct:.0f}%")

    inj = client.get_injection_settings()
    inj_min = inj['user_minimum_injection']
    inj_max = inj['user_maximum_injection']
    print(f"user injection: min:{inj_min} / max:{inj_max}")

    # print(client.get_milestones_savings())

    # print(client.get_software_version())

    # print(client.get_grid_mode())

    # print(client.get_recent_logs())

    # get the local local time in Vienna/Austria
    vienna = pytz.timezone('Europe/Vienna')
    now = datetime.now(vienna)
    print(f"Time in Vienna: {now}")

    # if the now time is between 0:00 and 6:00, then set the min injection to 0
    if 0 <= now.hour < 6:
        if inj_min != 0 or inj_max != 200:
            print("After midnight: changing injection to 0/200")
            print(client.set_min_injection(0))
            print(client.set_max_injection(200))
            return True
    else:
        if inj_max != 800:
            print("changing max injection to 800")
            print(client.set_max_injection(800))
            return True

    if (bat_pct > 50 and pv_w > 100) or (bat_pct > 90):
        if inj_min == 0:
            print("changing min injection to 50")
            print(client.set_min_injection(50))
            return True
    else:
        if inj_min != 0:
            print("changing min injection to 0")
            print(client.set_min_injection(0))
            return True
    print("all good, no change needed")
    return False


if __name__ == "__main__":
    adjust_min_injection()
