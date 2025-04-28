from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def crawler(url: str, category: str, selectors: dict):
    print('시작')
    results = []

    with sync_playwright() as p:
        # headless=True: 브라우저 창 안 띄움
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        # page.goto("https://shop.danawa.com/virtualestimate/?controller=estimateMain&methods=index&marketPlaceSeq=16")
        print(page)
        # 카테고리 버튼 클릭 (예: CPU, 메모리, 그래픽카드 등)
        print(page.locator(str(selectors["button"]), has_text=str(category)))
        page.locator(str(selectors["button"]), has_text=str(category)).click()
        # 상품 테이블 로드 기다리기
        page.wait_for_selector(".tbl_list")

        # 여기서 BeautifulSoup 대신 Playwright로 직접 읽기 시작
        rows = page.locator(selectors["item"])

        print("rows", rows)

        for i in range(rows.count()):
            try:
                item = rows.nth(i)
                title_element = item.locator(selectors["title"])
                price_element = item.locator(selectors["price"])

                name = title_element.inner_text().strip()
                price_text = price_element.inner_text().strip()
                price = int(''.join(filter(str.isdigit, price_text)))
                link = title_element.get_attribute('href')

                results.append({
                    "name": name,
                    "price": price,
                    "link": link
                })
            except Exception as e:
                print(f"오류 발생: {e}")
                continue

        browser.close()

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
