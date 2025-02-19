# Scraper_v2

🚀 **Scraper_v2** is a web scraper that searches through **OLX, Allegro, and Allegro Lokalnie** for items matching specified keywords. It includes **minimum and maximum price filters**, along with other customizable settings.

This is an upgraded version of my previous scraper, offering:
- ✅ **More flexible and reusable code**
- ✅ **Easier usage**
- ✅ **Ability to run multiple configurations in one go**
- ✅ **Saving data to different tables within a single database**
- ✅ **Handling HTTP errors effectively**

---

## ⚠️ Allegro Scraping Notice  
Allegro has strong anti-scraping measures, so **Scraper_v2** implements **Selenium with ChromeDriver** to bypass these restrictions.  

However, please note:  
- **ChromeDriver installation is required** to scrape Allegro.  
- **CAPTCHA solving is NOT implemented**, meaning scraping may still fail if CAPTCHA is triggered.

---

## 📌 Features
✔️ **Search multiple marketplaces** (OLX, Allegro, Allegro Lokalnie)  
✔️ **Filter by price range** (min/max)  
✔️ **Support for multiple configurations in one run**  
✔️ **Save data to an SQLite database**  
✔️ **Error handling for HTTP issues**  

---

## 📂 Installation & Usage  

### 🔹 1. Clone the Repository  
### 🔹 2. Install Required Packages  
```sh
pip install -r requirements.txt
```

### 🔹 3. Install ChromeDriver  
Download and install **ChromeDriver** from the [official website](https://sites.google.com/chromium.org/driver/).  
Ensure that `chromedriver.exe` is **added to your system's PATH** or placed in the project directory.

### ✅ Ready to Go! 🚀  

---

## 🔧 Example Usage  

### ▶️ **Running the Scraper with a `.bat` File**
Create a `.bat` file with the following content:  
```batch
python scraper_v2.py ^
--searches="C:/path/to/example.json" ^
--db_name=database_1
```
Run the `.bat` file to execute the scraper.

---

### ▶️ **Example `.json` Configuration File**  
Save the following JSON structure in a file (e.g., `config.json`):  
```json
[
    {
        "searched_phrase": "laptop-MSI-RTX",
        "min_price": 10,
        "max_price": 1000,
        "only_new": false,
        "max_page": 2,
        "unwanted_phrases": "broken-damaged",
        "by_date": true
    },
    {
        "searched_phrase": "smartphone",
        "min_price": 20,
        "max_price": 2000,
        "only_new": true,
        "max_page": 4,
        "unwanted_phrases": "defective",
        "by_date": false
    }
]
```

---

### ▶️ **Running the Scraper from the Command Line**
Run the scraper with a JSON config file:  
```sh
python scraper_v2.py --searches="C:/path/to/config.json" --db_name=my_database
```

Or use inline parameters:  
```sh
python scraper_v2.py --searches="[{
    \"searched_phrase\": \"laptop\", 
    \"min_price\": 10, 
    \"max_price\": 1000, 
    \"only_new\": false, 
    \"max_page\": 5, 
    \"unwanted_phrases\": \"\", 
    \"by_date\": true
}]" --db_name=database_2
```

---

### ℹ️ **Additional Help**
To see available options and usage instructions, run:  
```sh
python scraper_v2.py --help
```
---

## 📜 License  
📌 This project is **open-source** and licensed under the **GNU General Public License v3.0 (GPL v3)**.  
You are free to use, modify, and distribute it, but **any modifications must also be open-source under the same license**.  

For full details, see the [GPL v3 License](https://www.gnu.org/licenses/gpl-3.0.html).  

Feel free to contribute and improve it! 🚀

