from playwright.sync_api import sync_playwright
import json


def save(item_to_save, actual_page):
    # saves data per site in json format
    with open(f'quotes_{actual_page}.json', 'w') as f:
        json.dump(item_to_save, f)


def string(encoded_string):
    return encoded_string.encode("utf-8").decode('unicode_escape').encode('ascii', 'ignore')


def quotes(actual_page):
    # returns a list containing the elements for each quote
    quotes_to_scrape = actual_page.locator('div.col-md-8').last.locator('div.quote')   # selects all quotes
    quotes_list = list()

    for quote in quotes_to_scrape.all():                                        # iterate through the quotes' data
        text = quote.locator('span.text').inner_text()                         # quote's text
        author = quote.locator('small.author').inner_text()                     # quote's author

        tags_box = quote.locator('div.tags')
        tags_list = [tag.inner_text().split(' ')[1:] for tag in tags_box.all()]
        tags = tags_list[0]                                                     # quote's tags (in list)

        quotes_to_list = dict()
        quotes_to_list['author'] = author
        quotes_to_list['tags'] = tags
        quotes_to_list['quote'] = text.encode('ascii', 'ignore').decode()
        quotes_list.append(quotes_to_list)

    return quotes_list


with sync_playwright() as playwright:

    browser = playwright.chromium.launch()
    page = browser.new_page()
    page.goto('https://quotes.toscrape.com/page/1/')

    page_no = 1
    next_btn = page.locator('nav ul.pager a').get_by_text('Next ')

    while not next_btn.count() == 0:
        print(f'Scraping {page_no}...')
        q = quotes(actual_page=page)
        save(item_to_save=q, actual_page=page_no)
        next_btn.click()
        print(f'...page {page_no} has been scraped.')
        page_no += 1

    print('Every page from the site has been scraped. Please check the project folder for the saved data.')
    page.close()
