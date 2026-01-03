# Using `--dump-dom` in chromium is an option if http request is not sufficient

import sys

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <wiki>", file=sys.stderr)
    wiki = sys.argv[-1]
    soup = BeautifulSoup(requests.get(f"https://{wiki}.fandom.com/wiki/Special:AllPages").text, "html.parser")
    pages = set()
    for anchor in soup.select(".mw-allpages-body > .mw-allpages-chunk > li > a"):
        pages.add(anchor.get("href"))
    # for page in tqdm(pages):
    #     soup = BeautifulSoup(requests.get(f"https://{wiki}.fandom.com/{page}").text, "html.parser")
    cookies = {
        'wikia_beacon_id': 'io1DkMwFY4',
        '_b2': 'v13EdVp8-5.1659785624076',
        'WikiaLifetimeSource': 'https%3A%2F%2Fduckduckgo.com%2F',
        'fandom_global_id': 'f329bb60-d0c1-4957-b517-4be1ec6ec68a',
        'fan_visited_wikis': '244592,1242,1490395,2175921,2295257,4039,524772,1544,2395,1206155,2293902,559,1113133,290964,2814820,1091593,879797,177,3035,1465205,746667,2827,84058,1782460,2099443,3064978,2734512,3125,2294057,1204240,1988812,29474,2542521,1263209,14301,1947441,122703,2228844,7857,22782,3277882,2264559,3104482,1358984,3066960,2671257,1884659,1752064,120639,1686627,2294461',
        'ag': '1',
        'AMP_264a9266b5': 'JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJkYTExMDVhYS02ZDE3LTQyMjAtYmIxNy00ZWRkYWQ2MmRkYWElMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNjg5MzY1MzkzNDQ1JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTY4OTM2NTU2OTQxOCUyQyUyMmxhc3RFdmVudElkJTIyJTNBMTElN0Q=',
        'AMP_MKTG_264a9266b5': 'JTdCJTIycmVmZXJyZXIlMjIlM0ElMjJodHRwcyUzQSUyRiUyRnd3dy5nb29nbGUuY29tJTJGJTIyJTJDJTIycmVmZXJyaW5nX2RvbWFpbiUyMiUzQSUyMnd3dy5nb29nbGUuY29tJTIyJTdE',
        'AMP_6765a55f49': 'JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjIyMDY3YTA4YS0zOGYzLTRiYzYtYTQwMi1lZjdmOTJjNmMzMzQlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzE1MDE0Mjg1MjgwJTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTcxNTAxNjA2Nzg1MyUyQyUyMmxhc3RFdmVudElkJTIyJTNBODIyJTJDJTIycGFnZUNvdW50ZXIlMjIlM0EwJTdE',
        'AMP_MKTG_6765a55f49': 'JTdCJTdE',
        'basset': 'icFeaturedVideoPlayer-0_A_90:false|icConnatixPlayer-0_B_95:true',
        'wikia_session_id': 'RJ8U2mjqX9',
        'eb': '73',
        'euconsent-v2': 'CPt3fQAPt3fQACNAFAENDLCgAAAAAAAAACiQAAAOCgDAB-AIsAZ8A6QDBAHBAAAA.YAAAAAAAAAAA',
        'tracking-opt-in-status': 'rejected',
        'addtl_consent': '1~',
        '_cq_duid': '1.1712155922.nAd39LdfI5XbKrTO',
        'VEE': 'visualeditor',
        'csrf_token_7edb4307044064c5213d44940aa94f48ab88fe0b5ead052fbb75851a981aa6c4': 'yUhQtWoWmVty3NwN6W1NU53GuzF/ZZTZO8qX86oFsb8=',
        'Geo': '{%22region%22:%22D%22%2C%22city%22:%22netivot%22%2C%22country_name%22:%22israel%22%2C%22country%22:%22IL%22%2C%22continent%22:%22AS%22}',
        'Geo': 'OK',
        'sessionId': '469e6715-1ced-4aef-82ef-df24aa484025',
        'pvNumber': '9',
        'pvNumberGlobal': '9',
        'tracking_session_id': '469e6715-1ced-4aef-82ef-df24aa484025',
        'pv_number_global': '9',
        'pv_number': '9',
        'disable_no_video_exp': '1',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://picotron.fandom.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://picotron.fandom.com/wiki/Special:Export',
        # 'Cookie': 'wikia_beacon_id=io1DkMwFY4; _b2=v13EdVp8-5.1659785624076; WikiaLifetimeSource=https%3A%2F%2Fduckduckgo.com%2F; fandom_global_id=f329bb60-d0c1-4957-b517-4be1ec6ec68a; fan_visited_wikis=244592,1242,1490395,2175921,2295257,4039,524772,1544,2395,1206155,2293902,559,1113133,290964,2814820,1091593,879797,177,3035,1465205,746667,2827,84058,1782460,2099443,3064978,2734512,3125,2294057,1204240,1988812,29474,2542521,1263209,14301,1947441,122703,2228844,7857,22782,3277882,2264559,3104482,1358984,3066960,2671257,1884659,1752064,120639,1686627,2294461; ag=1; AMP_264a9266b5=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJkYTExMDVhYS02ZDE3LTQyMjAtYmIxNy00ZWRkYWQ2MmRkYWElMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNjg5MzY1MzkzNDQ1JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTY4OTM2NTU2OTQxOCUyQyUyMmxhc3RFdmVudElkJTIyJTNBMTElN0Q=; AMP_MKTG_264a9266b5=JTdCJTIycmVmZXJyZXIlMjIlM0ElMjJodHRwcyUzQSUyRiUyRnd3dy5nb29nbGUuY29tJTJGJTIyJTJDJTIycmVmZXJyaW5nX2RvbWFpbiUyMiUzQSUyMnd3dy5nb29nbGUuY29tJTIyJTdE; AMP_6765a55f49=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjIyMDY3YTA4YS0zOGYzLTRiYzYtYTQwMi1lZjdmOTJjNmMzMzQlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzE1MDE0Mjg1MjgwJTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTcxNTAxNjA2Nzg1MyUyQyUyMmxhc3RFdmVudElkJTIyJTNBODIyJTJDJTIycGFnZUNvdW50ZXIlMjIlM0EwJTdE; AMP_MKTG_6765a55f49=JTdCJTdE; basset=icFeaturedVideoPlayer-0_A_90:false|icConnatixPlayer-0_B_95:true; wikia_session_id=RJ8U2mjqX9; eb=73; euconsent-v2=CPt3fQAPt3fQACNAFAENDLCgAAAAAAAAACiQAAAOCgDAB-AIsAZ8A6QDBAHBAAAA.YAAAAAAAAAAA; tracking-opt-in-status=rejected; addtl_consent=1~; _cq_duid=1.1712155922.nAd39LdfI5XbKrTO; VEE=visualeditor; csrf_token_7edb4307044064c5213d44940aa94f48ab88fe0b5ead052fbb75851a981aa6c4=yUhQtWoWmVty3NwN6W1NU53GuzF/ZZTZO8qX86oFsb8=; Geo={%22region%22:%22D%22%2C%22city%22:%22netivot%22%2C%22country_name%22:%22israel%22%2C%22country%22:%22IL%22%2C%22continent%22:%22AS%22}; Geo=OK; sessionId=469e6715-1ced-4aef-82ef-df24aa484025; pvNumber=9; pvNumberGlobal=9; tracking_session_id=469e6715-1ced-4aef-82ef-df24aa484025; pv_number_global=9; pv_number=9; disable_no_video_exp=1',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    data = {
        'title': 'Special:Export',
        'catname': '',
        'pages': 'Memory\r\nBtn()',
        'curonly': '1',
        'wpDownload': '1',
        'wpEditToken': '+\\',
    }

    response = requests.post('https://picotron.fandom.com/wiki/Special:Export', cookies=cookies, headers=headers, data=data)


