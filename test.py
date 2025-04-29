from playwright.sync_api import Playwright, sync_playwright
from bs4 import BeautifulSoup


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(
        "https://www.compuzone.co.kr/online/online_main.htm?bannerid=GNBBannerOnlineMain")
    page.locator(".category_sub li", has_text="CPU").click()

    # page.wait_for_timeout(3000)
    # page.wait_for_selector("#sr_list_item_tb")
    page.wait_for_load_state("networkidle")
    btn = page.locator("#sr_list_item_tb tr")
    print(btn.count())

    # page.goto(
    #     "https://shop.danawa.com/virtualestimate/?controller=estimateMain&methods=index&marketPlaceSeq=16")
    # test = page.locator(
    #     ".pagination-box__list .btn-pagination__arrow").count()
    # page.locator(
    #     ".pagination-box__list .btn-pagination__arrow").click()

    # page.wait_for_selector("#estimateMainProduct")
    # html = page.content()
    # print(html)
    # soup = BeautifulSoup(html, "html.parser")
    # items = soup.select("#estimateMainProduct  .scroll_box")
    # print(items)

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
