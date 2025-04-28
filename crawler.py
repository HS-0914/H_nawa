import re
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup, ResultSet, Tag


def crawler_danawa(url: str, category: str, selectors: dict):
    print('시작')
    page_Num = 1  # 다음 페이지
    results = []

    # 모든 사이트 공통 "next" 후보 리스트
    next_button_selectors = [
        '.pagination-box__item.pagination--next a',  # 다나와
        'a.next',  # 컴퓨존
    ]

    with sync_playwright() as p:
        # headless=True: 브라우저 창 안 띄움
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)

        # 카테고리 버튼 클릭 (예: CPU, 메모리, 그래픽카드 등)
        page.locator(selectors["button"], has_text=category).click()
        page.wait_for_selector(selectors["title"])
        # page.wait_for_timeout(1000 * 2)

        while True:
            if (page_Num != 1 and page_Num % 10 == 1):
                # next 후보들 중 하나라도 있으면 클릭
                for selector in next_button_selectors:
                    next_button = page.locator(selector)
                    if next_button.count() > 0 and next_button.is_visible():
                        next_button.click()
                        page.wait_for_selector(selectors["item"])

                        break  # 찾으면 바로 탈출

            elif (page_Num != 1):
                page_count = page.get_by_role("link", name=str(
                    page_Num), exact=True)
                if (page_count.count() > 0):
                    page_count.click()
                    page.wait_for_selector(selectors["item"])

                else:
                    break
            print("category :", category, " page_Num :", page_Num)

            # BeautifulSoup으로 HTML 파싱
            html = page.content()
            soup = BeautifulSoup(html, "html.parser")
            items = soup.select(selectors["item"])
            crawl_append(items, results, selectors)
            page_Num += 1

        page_Num = 1
        browser.close()

    return results


def crawl_append(items: ResultSet[Tag], results: list, selectors: dict):

    for item in items:
        try:
            title_tag = item.select_one(selectors["title"])
            price_tag = item.select_one(selectors["price"])
            print(title_tag, price_tag)

            if title_tag and price_tag:
                name = title_tag.text.strip()
                # 숫자만 남기고 정수 변환
                price = int(''.join(filter(str.isdigit, price_tag.text)))
                link_raw = title_tag.get("href")
                link_id = None
                if (link_raw is None):
                    link_raw = title_tag.get("onclick")
                    link_id = re.search(r"\((\d+)", link_raw).group(1)
                else:
                    link_id = re.search(r"\('(\d+)", link_raw).group(1)
                link = selectors["link"] + link_id

                results.append({
                    "name": name,
                    "price": price,
                    "link": link
                })
        except Exception as e:
            print(f"오류 발생: {e}")
            continue


"""
if __name__ == "__main__":
    url = "https://shop.danawa.com/virtualestimate/?controller=estimateMain&methods=index&marketPlaceSeq=16"
    category = ["CPU","쿨러","메인보드","메모리","그래픽카드","SSD","HDD","케이스", "파워"]
    selectors = {
        "item": "#estimateMainProduct .scroll_box > .tbl_list tr",
        "title": ".title_price > .subject > a",
        "price": ".low_price > span",
        "link": ".title_price > .subject > a"
    }

    parts = crawl_pc_parts(url, selectors)
    for p in parts:
        print(p)
"""
if __name__ == "__main__":
    urls = [
        "https://shop.danawa.com/virtualestimate/?controller=estimateMain&methods=index&marketPlaceSeq=16",
        "https://www.compuzone.co.kr/online/online_main.htm?bannerid=GNBBannerOnlineMain",
    ]
    categorys = ["CPU", "메인보드", "메모리",
                 "그래픽카드", "SSD", "HDD", "케이스", "파워"]
    selectors_list = [
        {
            "button": ".pd_list_area > .pd_list:nth-child(1) dd > a",
            "item": "#estimateMainProduct .scroll_box > .tbl_list tr",
            "title": ".title_price > .subject > a",
            "price": ".low_price > span",
            "link": "https://shop.danawa.com/pc/?controller=estimateDeal&methods=productInformation&productSeq="
        },
        {
            "button": ".category_sub li",
            "item": "#sr_list_item_tb tr",
            "title": ".imgbox > b",
            "price": ".Sblack11 > span",
            "link": "www.compuzone.co.kr/product/product_detail.htm?opt_chk=Y&ProductNo="
        }
    ]
    for i in range(1, 2):
        for category in categorys:
            parts = crawler_danawa(urls[i], category, selectors_list[i])
            for p in parts:
                print(p)
            print(len(parts))
