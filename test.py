from playwright.sync_api import Playwright, sync_playwright
from bs4 import BeautifulSoup


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(
        "https://shop.danawa.com/virtualestimate/?controller=estimateMain&methods=index&marketPlaceSeq=16")
    page.get_by_role("link", name="CPU").click()
    page.wait_for_selector("#estimateMainProduct")
    html = page.content()
    print(html)
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select("#estimateMainProduct  .scroll_box")
    print(items)

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
