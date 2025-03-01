import time
from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch()
    with browser.new_context(
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    ) as ctx:
        page = ctx.new_page()
        page.goto("https://teach.italki.com/application")

        with ctx.expect_page() as new_page_info:
            check_list_btn = page.get_by_text("CHECK THE LIST").click()
            page.screenshot(path="home_page.png")
            new_page = new_page_info.value

        while True:
            new_page.screenshot(path="info_page.png")
            table = new_page.locator("table", has_text="Language")
            datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            table.screenshot(path=f"table_{datetime}.png")
            chinese_tr = table.locator("tr", has_text="Chinese")
            res = chinese_tr.inner_text().lower()
            print(res)
            if "open" in res:
                print("FOUND!!!")
                break
            time.sleep(10 * 60)
            new_page.reload()

    browser.close()
