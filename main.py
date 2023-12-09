from playwright.sync_api import sync_playwright
import json


def save(item_to_save, actual_page):
    # saves the elements per quote into json
    with open(f'quotes_{actual_page}.json', 'w') as f:
        json.dump(item_to_save, f)


def quotes():
    # returns the elements per quote
    quotes_to_scrape = page.locator('div.col-md-8').last.locator('div.quote')   # selects all quotes
    quotes_list = list()

    for quote in quotes_to_scrape.all():                                        # iterate through the quotes
        text = quote.locator('span.text').inner_text()                          # quote's text
        author = quote.locator('small.author').inner_text()                     # quote's author

        tags_box = quote.locator('div.tags')
        tags_list = [tag.inner_text().split(' ')[1:] for tag in tags_box.all()]
        tags = tags_list[0]                                                     # quote's tags (in list)

        quotes_to_list = dict()
        quotes_to_list['author'] = author
        quotes_to_list['tags'] = tags
        quotes_to_list['quote'] = text
        quotes_list.append(quotes_to_list)

    return quotes_list


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(
        headless=False,
        slow_mo=500
    )

    page_no = 1
    page = browser.new_page()
    page.goto('https://quotes.toscrape.com/page/1/')

    q = quotes()

    save(item_to_save=q, actual_page=page_no)

    page.close()
