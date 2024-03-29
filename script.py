import maigret
import asyncio
import logging

from maigret.result import QueryStatus
from maigret.sites import MaigretDatabase

MAIGRET_DB_FILE = 'data.json' # wget https://raw.githubusercontent.com/soxoj/maigret/main/maigret/resources/data.json
COOKIES_FILE = "cookies.txt"  # wget https://raw.githubusercontent.com/soxoj/maigret/main/cookies.txt
id_type = "username"

# Maigret HTTP requests timeout
TIMEOUT = 30

def setup_logger(log_level, name):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    return logger

async def maigret_search(username, top):

    logger = setup_logger(logging.WARNING, 'maigret')
    db = MaigretDatabase().load_from_path(MAIGRET_DB_FILE)

    sites = db.ranked_sites_dict()
    #retrieve all keys of the sites object
    top3000keys = list(sites.keys())

    # delete unnecessery keys from the sites object for each call's json results
    def delKeys(check_top):
        for key in top3000keys:
            if key not in check_top:
                del sites[key]

    if top == 100: 
        topKeys = top3000keys[0:100]
        delKeys(topKeys)
    if top == 500: 
        topKeys = top3000keys[100:500]
        delKeys(topKeys)
    if top == 1000:
        topKeys = top3000keys[500:1000]
        delKeys(topKeys)
    if top == 1500:
        topKeys = top3000keys[1000:1500]
        delKeys(topKeys)
    if top == 2000:
        topKeys = top3000keys[1500:2000] 
        delKeys(topKeys)
    if top == 2500:
        topKeys = top3000keys[2000:2500]
        delKeys(topKeys)
    if top == 3000:
        topKeys = top3000keys[2500:2630]
        delKeys(topKeys)
    

    results = await maigret.search(username=username,
                                   site_dict=sites,
                                   timeout=TIMEOUT,
                                   logger= logger,
                                   id_type=id_type,
                                   cookies=COOKIES_FILE,
                                   )
    return results

def generate_json_report(username: str, results: dict):
    # is_report_per_line = report_type.startswith("ndjson")
    all_json = {}

    for sitename in results:
        site_result = results[sitename]
        # TODO: fix no site data issue
        if not site_result or not site_result.get("status"):
            continue

        if site_result["status"].status != QueryStatus.CLAIMED:
            continue

        data = dict(site_result)
        data["status"] = data["status"].json()
        data["site"] = data["site"].json
        for field in ["future", "checker"]:
            if field in data:
                del data[field]

        all_json[sitename] = data

    return all_json


async def search(username, top):
    try:
        results = await maigret_search(username, top)
    except Exception as e:
        return ['An error occurred, send username once again.'], []

    json_result = generate_json_report(username, results)

    return json_result


async def main(username, top):
  task1 = asyncio.create_task(search(username, top))
  await task1
  result = task1.result()
  return result
