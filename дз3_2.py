import urllib.request
from html.parser import HTMLParser

class USDExchangeRateParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_row = False
        self.cell_index = 0
        self.is_usd_row = False
        self.current_cells = []
        self.usd_rate = None

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.in_table = True
        elif tag == 'tr' and self.in_table:
            self.in_row = True
            self.current_cells = []
            self.cell_index = 0
        elif tag == 'td' and self.in_row:
            self.current_cells.append('')

    def handle_endtag(self, tag):
        if tag == 'tr' and self.in_row:
            if len(self.current_cells) >= 5 and self.current_cells[1].strip() == 'USD':
                rate_str = self.current_cells[4].strip().replace(',', '.')
                try:
                    self.usd_rate = float(rate_str)
                except ValueError:
                    pass
            self.in_row = False
        elif tag == 'table':
            self.in_table = False

    def handle_data(self, data):
        if self.in_row and self.current_cells:
            self.current_cells[-1] += data

def get_usd_exchange_rate():
    url = "https://bank.gov.ua/ua/markets/exchangerates"
    response = urllib.request.urlopen(url)
    html_content = response.read().decode('utf-8')

    parser = USDExchangeRateParser()
    parser.feed(html_content)

    if parser.usd_rate is None:
        raise Exception("Курс долара США не знайдено.")
    return parser.usd_rate

class CurrencyConverter:
    def __init__(self, rate):
        self.rate = rate

    def convert(self, amount_uah):
        return round(amount_uah / self.rate, 2)

def main():
    try:
        rate = get_usd_exchange_rate()
        print(f"Поточний курс гривні до долара США: {rate} грн за 1 USD.")
        amount = float(input("Введіть суму в гривнях: "))
        converter = CurrencyConverter(rate)
        result = converter.convert(amount)
        print(f"Це приблизно {result} USD.")
    except Exception as e:
        print(f"Помилка: {e}")

if __name__ == "__main__":
    main()