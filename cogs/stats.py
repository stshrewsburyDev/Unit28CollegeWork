from threading import Thread
from datetime import datetime
from time import sleep
import psutil, platform, flask, cpuinfo, sqlite3
from cogs import formatting


class Stats:
    stats = {"PY_VER": f"{platform.python_version()} {platform.python_compiler()}",
             "LIB": f"Flask - {flask.__version__}",
             "SQL": {"LIB": sqlite3.version, "SQL": sqlite3.sqlite_version},
             "STARTED": "None",
             "LAST_UPDATED": "None",
             "OS": f"{platform.system()} {platform.release()} (Version: {platform.version()})",
             "CPU": cpuinfo.get_cpu_info()["brand_raw"],
             "CPU_P": 0,
             "RAM": {"P": 0, "T": 0, "U": 0},
             "SWAP": {"P": 0, "T": 0, "U": 0},
             "DISC": {"P": 0, "T": 0, "U": 0}}


def update_stats():
    while True:
        ram = psutil.virtual_memory()
        swap = psutil.swap_memory()
        disc = psutil.disk_usage('/')

        Stats.stats["CPU_P"] = formatting.make_bar(psutil.cpu_percent(interval=1))
        Stats.stats["RAM"]["P"] = formatting.make_bar(ram.percent)
        Stats.stats["RAM"]["T"] = round(ram.total / 1024 / 1024 / 1024, 2)
        Stats.stats["RAM"]["U"] = round(ram.used / 1024 / 1024 / 1024, 2)
        Stats.stats["SWAP"]["P"] = formatting.make_bar(swap.percent)
        Stats.stats["SWAP"]["T"] = round(swap.total / 1024 / 1024 / 1024, 2)
        Stats.stats["SWAP"]["U"] = round(swap.used / 1024 / 1024 / 1024, 2)
        Stats.stats["DISC"]["P"] = formatting.make_bar(disc.percent)
        Stats.stats["DISC"]["T"] = round(disc.total / 1024 / 1024 / 1024, 2)
        Stats.stats["DISC"]["U"] = round(disc.used / 1024 / 1024 / 1024, 2)

        Stats.stats["LAST_UPDATED"] = datetime.now().strftime("%a %d %b %Y at %H:%M:%S")

        sleep(60)


def start(startup_time):
    Stats.stats["STARTED"] = startup_time
    process = Thread(target=update_stats)
    process.start()
