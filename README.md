This web scraper searches through Olx, Allegro and Allegro Lokalnie for items with the phrases you specify. It also utilizes maximum and minimum price filters, along with other settings. This is an upgrade to my older scraper project, designed for more flexible code, easier use, and refactoring.

Allegro currently blocks scraping, so in my program, Selenium web scraping with ChromeDriver is implemented to bypass Allegro's blockades. You need to install ChromeDriver in order to scrape Allegro. Sometimes it doesn’t work either, as Allegro requires CAPTCHA solving, which is not implemented in the code.

Example .bat file to run:
<br />
```batch
python scraper.py ^
--searches="C:/path/to/example.json" ^
--filename=example_data
```
Example .json file to run:
<br />
```json
[
    {
        "searched_phrase": "phrase_1",
        "min_price": 10,
        "max_price": 1000,
        "only_new": false,
        "max_page": 2,
        "unwanted_phrase": "unwanted_phrase_1",
        "by_date": true
    },
    {
        "searched_phrase": "phrase_2",
        "min_price": 20,
        "max_price": 2000,
        "only_new": true,
        "max_page": 4,
        "unwanted_phrase": "unwanted_phrase_2",
        "by_date": false
    }
]
```
For additional help, type:
<br />
```cmd
python scraper.py --help
```
