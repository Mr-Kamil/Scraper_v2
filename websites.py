
class Olx():
    HTML_TAGS = {
        'titles': ['h6', 'css-16v5mdi er34gjf0'],
        'prices': ['p', 'css-10b0gli er34gjf0'],
        'urls': ['a', 'css-rc5s2u'],
        'max_page': ['a', "css-1mi714g"],
        }


    def __init__(
            self, searched_phrase: str, min_price: int, max_price: int, only_new: bool, by_date: bool
            ) -> None:
        
        self.base_url = 'https://www.olx.pl'
        self.searched_phrase = searched_phrase

        self.min_price = min_price
        self.max_price = max_price
        self.only_new = only_new
        self.by_date = by_date


    def get_url(self, page: str) -> str:
        self.url = self.base_url + f'/oferty/q-{self.searched_phrase}/'
        self.url += '?'

        if page:
            self.url += f'page={page}'

        if self.by_date:
            self.url += f'&search%5Border%5D=created_at:desc'

        if self.min_price:
            self.url += f'&search%5Bfilter_float_price:from%5D={self.min_price}'

        if self.max_price:
            self.url += f'&search%5Bfilter_float_price:to%5D={self.max_price}'

        if self.only_new:
            self.url += f'&search%5Bfilter_enum_state%5D%5B0%5D=new'

        return self.url


    def get_scraping_tags(self):
        return self.HTML_TAGS
    

    def __str__(self):
        return 'OLX'

        
class AllegroLokalnie():
    HTML_TAGS = {
        'titles': ['h3', 'mlc-itembox__title'],
        'prices': ['span', 'ml-offer-price__dollars'],
        'urls': ['a', 'mlc-card mlc-itembox'],
        'max_page_all_lok': ['div', 'data-mlc-listing-bottom-pagination', 'pages_count'],
        }


    def __init__(
            self, searched_phrase: str, min_price: int, max_price: int, only_new: bool, by_date: bool
            ) -> None:
        self.base_url = 'https://allegrolokalnie.pl'
        self.searched_phrase = searched_phrase.replace('-', '%20')

        self.min_price = min_price
        self.max_price = max_price
        self.only_new = only_new
        self.by_date = by_date


    def get_url(self, page: int) -> str:
        self.url = self.base_url + f'/oferty/q/{self.searched_phrase}/'
        
        if self.only_new:
            self.url += f'nowe'

        self.url += '?'

        if self.by_date:
            pass

        if self.min_price:
            self.url += f'price_from={self.min_price}'

        if self.max_price:
            self.url += f'&price_to={self.max_price}'

        if page:
            self.url += f'&page={page}'

        return self.url
    

    def get_scraping_tags(self):
        return self.HTML_TAGS
    

    def __str__(self):
        return 'Allegro Lokalnie'

class Allegro():
    scrapping_data_html_dict = {
        'titles': ['h2', "mgn2_14 m9qz_yp meqh_en mpof_z0 mqu1_16 m6ax_n4 mp4t_0 m3h2_0 mryx_0 munh_0 mj7a_4"],
        'prices': ['span', "mli8_k4 msa3_z4 mqu1_1 mgmw_qw mp0t_ji m9qz_yo mgn2_27 mgn2_30_s"],
        'urls_allegro': ['h2', "mgn2_14 m9qz_yp meqh_en mpof_z0 mqu1_16 m6ax_n4 mp4t_0 m3h2_0 mryx_0 munh_0 mj7a_4"],
        'max_page': ['span', "_1h7wt mgmw_wo mh36_8 mvrt_8 _6d89c_wwgPl _6d89c_oLeFV"]
        }

    def __init__(self, searched_phrase: str, min_price: int, max_price: int, only_new: bool) -> None:
        self.base_url = 'https://allegrolokalnie.pl'
        self.url = self.base_url + f'/oferty/q/{searched_phrase}/'

        self.min_price = min_price
        self.max_price = max_price
        self.only_new = only_new

    def get_url(self, page: int) -> str:

        if self.only_new:
            self.url += f'nowe'

        self.url += '?'

        if self.min_price:
            self.url += f'price_from={self.min_price}'

        if self.max_price:
            self.url += f'&price_to={self.max_price}'

        if page:
            self.url += f'&page={page}'

        return self.url
    
    def get_scraping_data(self):
        return self.scrapping_data_html_dict
