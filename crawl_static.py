import requests
from bs4 import BeautifulSoup


def crawl_pc_parts(url: str, selectors: dict, limit: int = 10):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        raise Exception(f"요청 실패: {res.status_code}")

    soup = BeautifulSoup(res.text, "html.parser")
    items = soup.select(selectors["item"])

    results = []

    for item in items[:limit]:
        try:
            name = item.select_one(selectors["title"]).text.strip()
            price_raw = item.select_one(selectors["price"]).text.strip().replace(
                ",", "").replace("원", "")
            price = int(''.join(filter(str.isdigit, price_raw)))
            link_tag = item.select_one(selectors["link"])
            link = link_tag["href"] if link_tag and "href" in link_tag.attrs else "N/A"

            results.append({
                "name": name,
                "price": price,
                "link": link
            })
        except Exception as e:
            print(f"크롤링 오류: {e}")
            continue

    return results


if __name__ == "__main__":
    url = "https://shop.danawa.com/virtualestimate/?controller=estimateMain&methods=index&marketPlaceSeq=16&logger_kw=dnw_gnb_esti"
    selectors = {
        "item": "tbl_list > tbody > tr",
        "title": ".title_price > .subject > a",
        "price": ".low_price > span",
        "link": ".title_price > .subject > a"
    }

    parts = crawl_pc_parts(url, selectors)
    for p in parts:
        print(p)
