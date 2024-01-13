import maigret
import asyncio
import logging

from maigret.result import QueryStatus
from maigret.sites import MaigretDatabase, MaigretSite
from maigret.report import save_json_report, generate_report_context

MAIGRET_DB_FILE = 'data.json' # wget https://raw.githubusercontent.com/soxoj/maigret/main/maigret/resources/data.json
COOKIES_FILE = "cookies.txt"  # wget https://raw.githubusercontent.com/soxoj/maigret/main/cookies.txt
id_type = "username"

# top popular sites from the Maigret database
TOP_SITES_COUNT = 100
# Maigret HTTP requests timeout
TIMEOUT = 30

def setup_logger(log_level, name):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    return logger

async def maigret_search(username):

    logger = setup_logger(logging.WARNING, 'maigret')

    db = MaigretDatabase().load_from_path(MAIGRET_DB_FILE)

    sites = db.ranked_sites_dict(top=TOP_SITES_COUNT)

    results = await maigret.search(username=username,
                                   site_dict=sites,
                                   timeout=TIMEOUT,
                                   logger= logger,
                                   id_type=id_type,
                                   cookies=COOKIES_FILE,
                                   )
    return results


async def search(username):

    try:
        results = await maigret_search(username)
    except Exception as e:
        return ['An error occurred, send username once again.'], []

    found_exact_accounts = []
    general_results = []
    general_results.append((username, id_type, results))

    for site, data in results.items():
        if data['status'].status != QueryStatus.CLAIMED:
            continue
        url = data['url_user']
        account_link = f'[{site}]({url})'

        # filter inaccurate results
        if not data.get('is_similar'):
            found_exact_accounts.append(account_link)

    if not found_exact_accounts:
        return [], []

    # full found results data
    results = list(filter(lambda x: x['status'].status == QueryStatus.CLAIMED, list(results.values())))

    return results


async def main(username):
  task1 = asyncio.create_task(search(username))
  await task1
  result = task1.result()
  return result