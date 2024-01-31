import maigret
import asyncio
import logging
import json

from maigret.result import QueryStatus
from maigret.sites import MaigretDatabase

MAIGRET_DB_FILE = 'data.json' # wget https://raw.githubusercontent.com/soxoj/maigret/main/maigret/resources/data.json
COOKIES_FILE = "cookies.txt"  # wget https://raw.githubusercontent.com/soxoj/maigret/main/cookies.txt
id_type = "username"

# top popular sites from the Maigret database
# TOP_SITES_COUNT = 50
# Maigret HTTP requests timeout
TIMEOUT = 30

def setup_logger(log_level, name):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    return logger

async def maigret_search(username, top):

    logger = setup_logger(logging.WARNING, 'maigret')

    db = MaigretDatabase().load_from_path(MAIGRET_DB_FILE)

    #collect top100 anyway
    top100sites = db.ranked_sites_dict(top=100)
    #retrieve keys of top100 sites
    top100keys = list(top100sites.keys())

    #if top100 is our goal - leave everything as it is
    if top == 100: 
        sites = top100sites
    #if not - collect top-500 and delete from this dictionary top100 keys
    elif top > 100:
        sites = db.ranked_sites_dict(top=500)
        for k in top100keys:
            del sites[k]

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
