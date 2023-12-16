This web scraper searches through Olx, Allegro and Allegro Lokalnie for items with the phrases you specify. It also utilizes maximum and minimum price filters, along with other settings. This is an upgrade to my older scraper project, designed for more flexible code, easier use, and refactoring.

Allegro currently blocks scraping, so in my program, Selenium web scraping with ChromeDriver is implemented to avoid Allegro blockades. You need to install ChromeDriver in order to scrape Allegro.

Example command:
<br />python scraper.py --searched_phrase=laptop --min_price=100 --max_price=4000 --only_new=False --max_page=2 --unwanted_phrase=komputer --filename=test_2 --by_date=True

For additional help, type:
<br />python scraper.py --help
