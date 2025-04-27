from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def crawler(url: str, category: str, selectors: dict):
    print('시작')

    with sync_playwright() as p:
        # headless=True: 브라우저 창 안 띄움
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        # page.goto("https://shop.danawa.com/virtualestimate/?controller=estimateMain&methods=index&marketPlaceSeq=16")
        print(page)
        # 카테고리 버튼 클릭 (예: CPU, 메모리, 그래픽카드 등)
        print(page.locator(str(selectors["button"]), has_text=str(category)))
        page.locator(str(selectors["button"]), has_text=str(category)).click()
        # page.wait_for_timeout(1000 * 5)  # 렌더링 대기 (5초)
        page.wait_for_selector(".tbl_list")

        html = page.content()
        browser.close()

    # BeautifulSoup으로 HTML 파싱
    soup = BeautifulSoup(html, "html.parser")
    print(soup)
    items = soup.select(selectors["item"])

    results = []
    for item in items:
        try:
            title_tag = item.select_one(selectors["title"])
            price_tag = item.select_one(selectors["price"])

            if title_tag and price_tag:
                name = title_tag.text.strip()
                # 숫자만 남기고 정수 변환
                price = int(''.join(filter(str.isdigit, price_tag.text)))
                link = title_tag["href"]
                print(link)

                results.append({
                    "name": name,
                    "price": price,
                    "link": link
                })
        except Exception as e:
            print(f"오류 발생: {e}")
            continue

    return results


"""
if __name__ == "__main__":
    url = "https://shop.danawa.com/virtualestimate/?controller=estimateMain&methods=index&marketPlaceSeq=16"
    category = ["CPU","쿨러","메인보드","메모리","그래픽카드","SSD","HDD","케이스", "파워"]
    selectors = {
        "item": ".scroll_box > .tbl_list > tr",
        "title": ".title_price > .subject > a",
        "price": ".low_price > span",
        "link": ".title_price > .subject > a"
    }

    parts = crawl_pc_parts(url, selectors)
    for p in parts:
        print(p)
"""
if __name__ == "__main__":
    url = "https://shop.danawa.com/virtualestimate/?controller=estimateMain&methods=index&marketPlaceSeq=16"
    categorys = ["CPU", "쿨러", "메인보드", "메모리",
                 "그래픽카드", "SSD", "HDD", "케이스", "파워"]
    selectors = {
        "button": "a.pd_item_title",
        "item": ".scroll_box > .tbl_list > tr",
        "title": ".title_price > .subject > a",
        "price": ".low_price > span",
    }
    for category in categorys:
        parts = crawler(url, category, selectors)
        print(parts)
        for p in parts:
            print(p)
