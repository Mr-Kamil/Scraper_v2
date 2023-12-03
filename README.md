This web scraper searches through Olx and Allegro Lokalnie for items with the phrases you specify. It also utilizes maximum and minimum price filters, along with other settings. This is an upgrade to my older scraper project, designed for more flexible code, easier use, and refactoring.

It is also capable of searching on Allegro, but please note that Allegro currently blocks scraping, so it is not implemented.

Example command:
python scraper.py --searched_phrase=laptop --min_price=100 --max_price=4000 --only_new=False --max_page=2 --unwanted_phrase=komputer --filename=test_2 --by_date=True

For additional help, type:
python scraper.py --help