import re
from playwright.async_api import async_playwright, Page, Locator
from bs4 import BeautifulSoup, ResultSet, Tag


async def crawler_danawa(url: str, category: str, selectors: dict):
    print('시작')
    page_Num = 1  # 다음 페이지
    results = []

    # 모든 사이트 공통 "next" 후보 리스트
    next_button_selectors = [
        '.pagination-box__item.pagination--next a',  # 다나와
        'a.next',  # 컴퓨존
    ]

    async with async_playwright() as p:
        # headless=True: 브라우저 창 안 띄움
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)

        # 카테고리 버튼 클릭 (예: CPU, 메모리, 그래픽카드 등)
        await page.locator(selectors["button"], has_text=category).click()
        await page.wait_for_timeout(1000 * 5)

        # 크롤링한거 분류
        while True:
            if (page_Num != 1 and page_Num % 10 == 1):
                # next 후보들 중 하나라도 있으면 클릭
                for selector in next_button_selectors:
                    next_button = page.locator(selector)
                    if await next_button.count() > 0 and await next_button.is_visible():
                        await next_button.click()
                        await page.wait_for_timeout(500)
                        await page.wait_for_load_state("load")
                        break  # 찾으면 바로 탈출

            elif (page_Num != 1):
                page_count = page.get_by_role(
                    "link", name=str(page_Num), exact=True)
                if (page_count.count() > 0):
                    await page_count.click()
                    await page.wait_for_timeout(500)
                    await page.wait_for_load_state("load")
                else:
                    break

            # 스크롤 내리기
            scroll_target = page.locator("#sr_list_wrap")
            await scroll_down(page, scroll_target)
            print("category :", category, " page_Num :", page_Num)

            # BeautifulSoup으로 HTML 파싱
            html = await page.content()
            soup = BeautifulSoup(html, "html.parser")
            items = soup.select(selectors["item"])
            await crawl_append(items, results, selectors)
            page_Num += 1

        page_Num = 1
        await browser.close()

    return results


async def crawl_append(items: ResultSet[Tag], results: list, selectors: dict):

    for item in items:
        try:
            title_tag = item.select_one(selectors["title"])
            price_tag = item.select_one(selectors["price"])
            link_tag = item.select_one(selectors["link"])
            if title_tag and price_tag:
                name = title_tag.text.strip()
                # 숫자만 남기고 정수 변환
                price = int(''.join(filter(str.isdigit, price_tag.text)))
                link_raw = link_tag.get("href")
                link_id = None
                if (link_raw == ""):
                    link_raw = link_tag.get("onclick")
                    link_id = re.search(r"\((\d+)", link_raw).group(1)
                else:
                    link_id = re.search(r"\('(\d+)", link_raw).group(1)
                link = selectors["href"] + link_id

                results.append({
                    "name": name,
                    "price": price,
                    "link": link
                })
        except Exception as e:
            print(f"오류 발생: {e}")
            continue


async def scroll_down(page: Page, scroll_target: Locator):
    previous_height = 0

    while await scroll_target.count() > 0:
        # 현재 스크롤 대상 div의 스크롤 높이
        current_height = await scroll_target.evaluate("el => el.scrollHeight")

        if current_height == previous_height:
            # 스크롤 해도 더 이상 변화가 없으면 멈춤
            break

        previous_height = current_height

        # 스크롤 대상 div를 제일 아래로 내림
        await scroll_target.evaluate("el => el.scrollTo(0, el.scrollHeight)")

        # 데이터가 로드될 시간을 주기
        await page.wait_for_timeout(1000)  # 1초 대기


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
    categorys = ["CPU", "쿨러", "메인보드", "메모리",
                 "그래픽카드", "SSD", "HDD", "케이스", "파워"]
    selectors_list = [
        {
            "button": ".pd_list_area > .pd_list:nth-child(1) dd > a",
            "item": "#estimateMainProduct .scroll_box > .tbl_list tr",
            "title": ".title_price > .subject > a",
            "price": ".low_price > span",
            "link": ".title_price > .subject > a",
            "href": "https://shop.danawa.com/pc/?controller=estimateDeal&methods=productInformation&productSeq="
        },
        {
            "button": ".category_sub li",
            "item": "#sr_list_item_tb tr",
            "title": "td.name > .imgbox > b",
            "price": "td.Sblack11 > span",
            "link": "td.name > .imgbox",
            "href": "https://www.compuzone.co.kr/product/product_detail.htm?opt_chk=Y&ProductNo="
        }
    ]
    for i in range(len(urls)):
        for category in categorys:
            parts = crawler_danawa(urls[i], category, selectors_list[i])
            # for p in parts:
            #     print(p)
            print(len(parts))
