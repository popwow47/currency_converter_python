import flet as ft
import requests
from datetime import datetime, date
import re
import json
import os


class CurrencyConverter:
    def __init__(self):
        self.rates = {}
        self.crypto_rates = {}
        self.last_update = None
        self.request_count = 0

        # Фиатные валюты — SVG-флаги из папки flags
        self.fiat_currencies = [
            {"code": "USD", "name": "Доллар США", "symbol": "$", "icon": "us.svg", "type": "fiat"},
            {"code": "EUR", "name": "Евро", "symbol": "€", "icon": "eu.svg", "type": "fiat"},
            {"code": "GBP", "name": "Фунт стерлингов", "symbol": "£", "icon": "gb.svg", "type": "fiat"},
            {"code": "JPY", "name": "Японская йена", "symbol": "¥", "icon": "jp.svg", "type": "fiat"},
            {"code": "CNY", "name": "Китайский юань", "symbol": "¥", "icon": "cn.svg", "type": "fiat"},
            {"code": "RUB", "name": "Российский рубль", "symbol": "₽", "icon": "ru.svg", "type": "fiat"},
            {"code": "UAH", "name": "Украинская гривна", "symbol": "₴", "icon": "ua.svg", "type": "fiat"},
            {"code": "PLN", "name": "Польский злотый", "symbol": "zł", "icon": "pl.svg", "type": "fiat"},
            {"code": "CHF", "name": "Швейцарский франк", "symbol": "Fr", "icon": "ch.svg", "type": "fiat"},
            {"code": "CAD", "name": "Канадский доллар", "symbol": "C$", "icon": "ca.svg", "type": "fiat"},
            {"code": "AUD", "name": "Австралийский доллар", "symbol": "A$", "icon": "au.svg", "type": "fiat"},
            {"code": "NZD", "name": "Новозеландский доллар", "symbol": "NZ$", "icon": "nz.svg", "type": "fiat"},
            {"code": "SEK", "name": "Шведская крона", "symbol": "kr", "icon": "se.svg", "type": "fiat"},
            {"code": "NOK", "name": "Норвежская крона", "symbol": "kr", "icon": "no.svg", "type": "fiat"},
            {"code": "DKK", "name": "Датская крона", "symbol": "kr", "icon": "dk.svg", "type": "fiat"},
            {"code": "TRY", "name": "Турецкая лира", "symbol": "₺", "icon": "tr.svg", "type": "fiat"},
            {"code": "INR", "name": "Индийская рупия", "symbol": "₹", "icon": "in.svg", "type": "fiat"},
            {"code": "BRL", "name": "Бразильский реал", "symbol": "R$", "icon": "br.svg", "type": "fiat"},
            {"code": "MXN", "name": "Мексиканское песо", "symbol": "$", "icon": "mx.svg", "type": "fiat"},
            {"code": "ZAR", "name": "Южноафриканский рэнд", "symbol": "R", "icon": "za.svg", "type": "fiat"},
            {"code": "AED", "name": "Дирхам ОАЭ", "symbol": "د.إ", "icon": "ae.svg", "type": "fiat"},
            {"code": "SAR", "name": "Саудовский риял", "symbol": "﷼", "icon": "sa.svg", "type": "fiat"},
            {"code": "ILS", "name": "Израильский шекель", "symbol": "₪", "icon": "il.svg", "type": "fiat"},
            {"code": "EGP", "name": "Египетский фунт", "symbol": "ج.م", "icon": "eg.svg", "type": "fiat"},
            {"code": "JOD", "name": "Иорданский динар", "symbol": "د.أ", "icon": "jo.svg", "type": "fiat"},
            {"code": "KWD", "name": "Кувейтский динар", "symbol": "د.ك", "icon": "kw.svg", "type": "fiat"},
            {"code": "BHD", "name": "Бахрейнский динар", "symbol": "د.ب", "icon": "bh.svg", "type": "fiat"},
            {"code": "OMR", "name": "Оманский риал", "symbol": "﷼", "icon": "om.svg", "type": "fiat"},
            {"code": "QAR", "name": "Катарский риал", "symbol": "﷼", "icon": "qa.svg", "type": "fiat"},
            {"code": "IQD", "name": "Иракский динар", "symbol": "ع.د", "icon": "iq.svg", "type": "fiat"},
            {"code": "IRR", "name": "Иранский риал", "symbol": "﷼", "icon": "ir.svg", "type": "fiat"},
            {"code": "AFN", "name": "Афганский афгани", "symbol": "؋", "icon": "af.svg", "type": "fiat"},
            {"code": "KRW", "name": "Южнокорейская вона", "symbol": "₩", "icon": "kr.svg", "type": "fiat"},
            {"code": "SGD", "name": "Сингапурский доллар", "symbol": "S$", "icon": "sg.svg", "type": "fiat"},
            {"code": "HKD", "name": "Гонконгский доллар", "symbol": "HK$", "icon": "hk.svg", "type": "fiat"},
            {"code": "THB", "name": "Тайский бат", "symbol": "฿", "icon": "th.svg", "type": "fiat"},
            {"code": "MYR", "name": "Малайзийский ринггит", "symbol": "RM", "icon": "my.svg", "type": "fiat"},
            {"code": "IDR", "name": "Индонезийская рупия", "symbol": "Rp", "icon": "id.svg", "type": "fiat"},
            {"code": "PHP", "name": "Филиппинское песо", "symbol": "₱", "icon": "ph.svg", "type": "fiat"},
            {"code": "VND", "name": "Вьетнамский донг", "symbol": "₫", "icon": "vn.svg", "type": "fiat"},
            {"code": "PKR", "name": "Пакистанская рупия", "symbol": "Rs", "icon": "pk.svg", "type": "fiat"},
            {"code": "BDT", "name": "Бангладешская така", "symbol": "৳", "icon": "bd.svg", "type": "fiat"},
            {"code": "LKR", "name": "Шри-ланкийская рупия", "symbol": "රු", "icon": "lk.svg", "type": "fiat"},
            {"code": "NPR", "name": "Непальская рупия", "symbol": "रु", "icon": "np.svg", "type": "fiat"},
            {"code": "MMK", "name": "Мьянманский кьят", "symbol": "K", "icon": "mm.svg", "type": "fiat"},
            {"code": "KHR", "name": "Камбоджийский риель", "symbol": "៛", "icon": "kh.svg", "type": "fiat"},
            {"code": "LAK", "name": "Лаосский кип", "symbol": "₭", "icon": "la.svg", "type": "fiat"},
            {"code": "CZK", "name": "Чешская крона", "symbol": "Kč", "icon": "cz.svg", "type": "fiat"},
            {"code": "HUF", "name": "Венгерский форинт", "symbol": "Ft", "icon": "hu.svg", "type": "fiat"},
            {"code": "RON", "name": "Румынский лей", "symbol": "lei", "icon": "ro.svg", "type": "fiat"},
            {"code": "BGN", "name": "Болгарский лев", "symbol": "лв", "icon": "bg.svg", "type": "fiat"},
            {"code": "HRK", "name": "Хорватская куна", "symbol": "kn", "icon": "hr.svg", "type": "fiat"},
            {"code": "ISK", "name": "Исландская крона", "symbol": "kr", "icon": "is.svg", "type": "fiat"},
            {"code": "KZT", "name": "Казахстанский тенге", "symbol": "₸", "icon": "kz.svg", "type": "fiat"},
            {"code": "BYN", "name": "Белорусский рубль", "symbol": "Br", "icon": "by.svg", "type": "fiat"},
            {"code": "GEL", "name": "Грузинский лари", "symbol": "₾", "icon": "ge.svg", "type": "fiat"},
            {"code": "AMD", "name": "Армянский драм", "symbol": "֏", "icon": "am.svg", "type": "fiat"},
            {"code": "AZN", "name": "Азербайджанский манат", "symbol": "₼", "icon": "az.svg", "type": "fiat"},
            {"code": "UZS", "name": "Узбекский сум", "symbol": "сўм", "icon": "uz.svg", "type": "fiat"},
            {"code": "MAD", "name": "Марокканский дирхам", "symbol": "د.م", "icon": "ma.svg", "type": "fiat"},
            {"code": "TND", "name": "Тунисский динар", "symbol": "د.ت", "icon": "tn.svg", "type": "fiat"},
            {"code": "DZD", "name": "Алжирский динар", "symbol": "د.ج", "icon": "dz.svg", "type": "fiat"},
            {"code": "LYD", "name": "Ливийский динар", "symbol": "د.ل", "icon": "ly.svg", "type": "fiat"},
            {"code": "NGN", "name": "Нигерийская найра", "symbol": "₦", "icon": "ng.svg", "type": "fiat"},
            {"code": "KES", "name": "Кенийский шиллинг", "symbol": "Sh", "icon": "ke.svg", "type": "fiat"},
            {"code": "GHS", "name": "Ганский седи", "symbol": "₵", "icon": "gh.svg", "type": "fiat"},
            {"code": "ETB", "name": "Эфиопский быр", "symbol": "Br", "icon": "et.svg", "type": "fiat"},
            {"code": "UGX", "name": "Угандийский шиллинг", "symbol": "Sh", "icon": "ug.svg", "type": "fiat"},
            {"code": "TZS", "name": "Танзанийский шиллинг", "symbol": "Sh", "icon": "tz.svg", "type": "fiat"},
            {"code": "RWF", "name": "Руандийский франк", "symbol": "Fr", "icon": "rw.svg", "type": "fiat"},
            {"code": "MUR", "name": "Маврикийская рупия", "symbol": "₨", "icon": "mu.svg", "type": "fiat"},
            {"code": "MWK", "name": "Малавийская квача", "symbol": "MK", "icon": "mw.svg", "type": "fiat"},
            {"code": "ZMW", "name": "Замбийская квача", "symbol": "ZK", "icon": "zm.svg", "type": "fiat"},
            {"code": "BWP", "name": "Ботсванская пула", "symbol": "P", "icon": "bw.svg", "type": "fiat"},
            {"code": "NAD", "name": "Намибийский доллар", "symbol": "$", "icon": "na.svg", "type": "fiat"},
            {"code": "ARS", "name": "Аргентинское песо", "symbol": "$", "icon": "ar.svg", "type": "fiat"},
            {"code": "CLP", "name": "Чилийское песо", "symbol": "$", "icon": "cl.svg", "type": "fiat"},
            {"code": "COP", "name": "Колумбийское песо", "symbol": "$", "icon": "co.svg", "type": "fiat"},
            {"code": "PEN", "name": "Перуанский соль", "symbol": "S/", "icon": "pe.svg", "type": "fiat"},
        ]

        # Криптовалюты — эмодзи
        self.crypto_currencies = [
            {"code": "BTC", "name": "Bitcoin", "symbol": "₿", "icon": "🟠", "type": "crypto", "gecko_id": "bitcoin"},
            {"code": "ETH", "name": "Ethereum", "symbol": "Ξ", "icon": "🔷", "type": "crypto", "gecko_id": "ethereum"},
            {"code": "USDT", "name": "Tether", "symbol": "₮", "icon": "🟢", "type": "crypto", "gecko_id": "tether"},
            {"code": "BNB", "name": "Binance Coin", "symbol": "BNB", "icon": "🟡", "type": "crypto", "gecko_id": "binancecoin"},
            {"code": "XRP", "name": "Ripple", "symbol": "XRP", "icon": "⚪", "type": "crypto", "gecko_id": "ripple"},
            {"code": "ADA", "name": "Cardano", "symbol": "₳", "icon": "🔵", "type": "crypto", "gecko_id": "cardano"},
            {"code": "DOGE", "name": "Dogecoin", "symbol": "Ð", "icon": "🟡", "type": "crypto", "gecko_id": "dogecoin"},
            {"code": "SOL", "name": "Solana", "symbol": "◎", "icon": "🟣", "type": "crypto", "gecko_id": "solana"},
            {"code": "DOT", "name": "Polkadot", "symbol": "•", "icon": "🔴", "type": "crypto", "gecko_id": "polkadot"},
            {"code": "MATIC", "name": "Polygon", "symbol": "MATIC", "icon": "🟣", "type": "crypto", "gecko_id": "matic-network"},
            {"code": "LTC", "name": "Litecoin", "symbol": "Ł", "icon": "⚪", "type": "crypto", "gecko_id": "litecoin"},
            {"code": "SHIB", "name": "Shiba Inu", "symbol": "SHIB", "icon": "🔴", "type": "crypto", "gecko_id": "shiba-inu"},
            {"code": "TRX", "name": "Tron", "symbol": "TRX", "icon": "🔴", "type": "crypto", "gecko_id": "tron"},
            {"code": "AVAX", "name": "Avalanche", "symbol": "AVAX", "icon": "🔴", "type": "crypto", "gecko_id": "avalanche-2"},
            {"code": "UNI", "name": "Uniswap", "symbol": "UNI", "icon": "🦄", "type": "crypto", "gecko_id": "uniswap"},
            {"code": "LINK", "name": "Chainlink", "symbol": "LINK", "icon": "🔵", "type": "crypto", "gecko_id": "chainlink"},
            {"code": "XLM", "name": "Stellar", "symbol": "*", "icon": "⚫", "type": "crypto", "gecko_id": "stellar"},
            {"code": "ATOM", "name": "Cosmos", "symbol": "ATOM", "icon": "🔵", "type": "crypto", "gecko_id": "cosmos"},
            {"code": "XMR", "name": "Monero", "symbol": "ɱ", "icon": "🟠", "type": "crypto", "gecko_id": "monero"},
            {"code": "ETC", "name": "Ethereum Classic", "symbol": "ΞC", "icon": "🟢", "type": "crypto", "gecko_id": "ethereum-classic"},
            {"code": "BCH", "name": "Bitcoin Cash", "symbol": "BCH", "icon": "🟢", "type": "crypto", "gecko_id": "bitcoin-cash"},
            {"code": "ALGO", "name": "Algorand", "symbol": "ALGO", "icon": "⚫", "type": "crypto", "gecko_id": "algorand"},
            {"code": "VET", "name": "VeChain", "symbol": "VET", "icon": "🔵", "type": "crypto", "gecko_id": "vechain"},
            {"code": "FIL", "name": "Filecoin", "symbol": "FIL", "icon": "🔵", "type": "crypto", "gecko_id": "filecoin"},
            {"code": "ICP", "name": "Internet Computer", "symbol": "ICP", "icon": "🟣", "type": "crypto", "gecko_id": "internet-computer"},
            {"code": "NEAR", "name": "NEAR Protocol", "symbol": "NEAR", "icon": "⚫", "type": "crypto", "gecko_id": "near"},
            {"code": "APT", "name": "Aptos", "symbol": "APT", "icon": "🔵", "type": "crypto", "gecko_id": "aptos"},
            {"code": "HBAR", "name": "Hedera", "symbol": "ℏ", "icon": "⚫", "type": "crypto", "gecko_id": "hedera-hashgraph"},
            {"code": "QNT", "name": "Quant", "symbol": "QNT", "icon": "⚪", "type": "crypto", "gecko_id": "quant-network"},
            {"code": "ARB", "name": "Arbitrum", "symbol": "ARB", "icon": "🔵", "type": "crypto", "gecko_id": "arbitrum"},
        ]

        self.all_currencies = self.fiat_currencies + self.crypto_currencies

        self.requests_file = "api_requests.json"
        self.max_requests = 1500#2880
        self.load_request_count()

    def load_request_count(self):
        try:
            if os.path.exists(self.requests_file):
                with open(self.requests_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data.get('date') == str(date.today()):
                        self.request_count = data.get('count', 0)
                    else:
                        self.request_count = 0
                        self.save_request_count()
            else:
                self.request_count = 0
                self.save_request_count()
        except Exception:
            self.request_count = 0

    def save_request_count(self):
        try:
            data = {'date': str(date.today()), 'count': self.request_count}
            with open(self.requests_file, 'w', encoding='utf-8') as f:
                json.dump(data, f)
        except Exception:
            pass

    def increment_request_count(self):
        self.request_count += 1
        self.save_request_count()

    def get_remaining_requests(self):
        return self.max_requests - self.request_count

    def can_make_request(self):
        return self.request_count < self.max_requests

    @staticmethod
    def check_internet():
        try:
            requests.get("https://www.google.com", timeout=3)
            return True
        except Exception:
            return False

    def fetch_rates(self):
        if not self.can_make_request():
            return False, f"Достигнут лимит запросов ({self.max_requests}/день)"

        try:
            crypto_ids = ",".join([c["gecko_id"] for c in self.crypto_currencies if "gecko_id" in c])
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {
                "ids": crypto_ids,
                "vs_currencies": "usd,eur,rub,uah,gbp,jpy,cny,pln,chf,cad,aud,try,inr,brl,mxn,zar,aed,krw,sgd,hkd,thb"
            }
            response = requests.get(url, params=params, timeout=10)
            if response.status_code != 200:
                return False, "Ошибка CoinGecko API"

            crypto_data = response.json()
            self.crypto_rates = {}
            for crypto in self.crypto_currencies:
                gecko_id = crypto.get("gecko_id")
                if gecko_id and gecko_id in crypto_data:
                    self.crypto_rates[crypto["code"]] = crypto_data[gecko_id]

            fiat_response = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=10)
            if fiat_response.status_code == 200:
                fiat_data = fiat_response.json()
                self.rates = fiat_data["rates"]

            self.last_update = datetime.now()
            self.increment_request_count()
            return True, "Курсы успешно обновлены"
        except requests.exceptions.RequestException:
            return False, "Нет подключения к интернету"
        except Exception as e:
            return False, f"Ошибка загрузки курсов: {str(e)}"

    def convert(self, amount, from_code, to_code):
        if not amount:
            return None
        try:
            num_amount = float(amount.replace(",", "."))
            if num_amount <= 0:
                return None

            from_curr = next((c for c in self.all_currencies if c["code"] == from_code), None)
            to_curr = next((c for c in self.all_currencies if c["code"] == to_code), None)
            if not from_curr or not to_curr:
                return None

            from_type = from_curr["type"]
            to_type = to_curr["type"]

            if from_type == "crypto" and to_type == "crypto":
                if from_code in self.crypto_rates and to_code in self.crypto_rates:
                    from_usd = self.crypto_rates[from_code].get("usd")
                    to_usd = self.crypto_rates[to_code].get("usd")
                    if from_usd and to_usd and from_usd > 0:
                        return round(num_amount * (from_usd / to_usd), 8)

            elif from_type == "crypto" and to_type == "fiat":
                if from_code in self.crypto_rates:
                    rate = self.crypto_rates[from_code].get(to_code.lower())
                    if rate:
                        return round(num_amount * rate, 2)

            elif from_type == "fiat" and to_type == "crypto":
                if to_code in self.crypto_rates:
                    rate = self.crypto_rates[to_code].get(from_code.lower())
                    if rate and rate > 0:
                        return round(num_amount / rate, 8)

            elif from_type == "fiat" and to_type == "fiat":
                if from_code in self.rates and to_code in self.rates:
                    amount_in_usd = num_amount / self.rates.get(from_code, 1)
                    converted = amount_in_usd * self.rates.get(to_code, 1)
                    return round(converted, 2)

            return None
        except Exception:
            return None

    def get_exchange_rate(self, from_code, to_code):
        result = self.convert(1, from_code, to_code)
        return f"1 {from_code} = {result} {to_code}" if result is not None else ""

    def search_currencies(self, query, filter_type="all"):
        if not query:
            if filter_type == "fiat":
                return self.fiat_currencies
            elif filter_type == "crypto":
                return self.crypto_currencies
            return self.all_currencies

        query = query.lower()
        currencies = (
            self.fiat_currencies if filter_type == "fiat"
            else self.crypto_currencies if filter_type == "crypto"
            else self.all_currencies
        )
        return [c for c in currencies if query in c["code"].lower() or query in c["name"].lower()]


def main(page: ft.Page):
    page.title = "Конвертер валют"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.window.width = 420
    page.window.height = 900
    page.window.resizable = False

    converter = CurrencyConverter()

    selected_from = {"code": "USD"}
    selected_to = {"code": "EUR"}

    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        theme_icon.icon = ft.Icons.DARK_MODE if page.theme_mode == ft.ThemeMode.DARK else ft.Icons.LIGHT_MODE
        page.update()

    theme_icon = ft.IconButton(icon=ft.Icons.LIGHT_MODE, on_click=toggle_theme, tooltip="Переключить тему")

    status_icon = ft.Icon(name=ft.Icons.WIFI, color=ft.Colors.GREEN, size=20)
    status_text = ft.Text("Подключено", color=ft.Colors.GREEN, size=12)

    api_counter = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.ANALYTICS_OUTLINED, size=16, color=ft.Colors.BLUE_700),
            ft.Text(f"{converter.request_count} из {converter.max_requests} запросов",
                    size=12, color=ft.Colors.BLUE_700, weight=ft.FontWeight.W_500)
        ], spacing=5),
        bgcolor=ft.Colors.BLUE_50,
        padding=8,
        border_radius=8,
        margin=ft.margin.only(top=5, bottom=10)
    )

    exchange_rate_text = ft.Text("", size=11, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER, italic=True)

    error_banner = ft.Container(
        content=ft.Text("", color=ft.Colors.WHITE),
        bgcolor=ft.Colors.RED_400,
        padding=10,
        border_radius=8,
        visible=False
    )

    amount_field = ft.TextField(
        label="Сумма",
        hint_text="Введите сумму",
        value="1",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=380,
        text_size=18
    )

    def create_currency_dialog(is_from=True):
        search_field = ft.TextField(
            hint_text="Поиск валюты...",
            prefix_icon=ft.Icons.SEARCH,
            width=350,
            autofocus=True
        )

        filter_buttons = ft.Row([
            ft.ElevatedButton("Все", on_click=lambda e: update_filter("all"), data="all"),
            ft.ElevatedButton("Фиат", on_click=lambda e: update_filter("fiat"), data="fiat"),
            ft.ElevatedButton("Крипто", on_click=lambda e: update_filter("crypto"), data="crypto"),
        ], spacing=5)

        currency_list = ft.ListView(spacing=5, height=350, width=350)

        current_filter_local = "all"

        def update_filter(filter_type):
            nonlocal current_filter_local
            current_filter_local = filter_type
            update_list(search_field.value)

            for btn in filter_buttons.controls:
                if btn.data == filter_type:
                    btn.bgcolor = ft.Colors.INDIGO
                    btn.color = ft.Colors.WHITE
                else:
                    btn.bgcolor = None
                    btn.color = None
            filter_buttons.update()

        def update_list(query=""):
            currency_list.controls.clear()
            filtered = converter.search_currencies(query, current_filter_local)
            for currency in filtered:
                if currency["type"] == "fiat":
                    leading_control = ft.Image(
                        src=currency["icon"],
                        width=32,
                        height=24,
                        fit=ft.ImageFit.CONTAIN,
                    )
                else:
                    leading_control = ft.Text(currency["icon"], size=30)

                currency_list.controls.append(
                    ft.ListTile(
                        leading=leading_control,
                        title=ft.Text(f"{currency['code']}", weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(f"{currency['symbol']} {currency['name']}"),
                        on_click=lambda e, c=currency: select_currency(c, is_from)
                    )
                )
            currency_list.update()

        def on_search_change(e):
            update_list(e.control.value)

        search_field.on_change = on_search_change

        dialog = ft.AlertDialog(
            title=ft.Text("Выберите валюту"),
            content=ft.Column([filter_buttons, search_field, currency_list], tight=True, width=350, height=500),
            actions=[ft.TextButton("Закрыть", on_click=lambda e: page.close(dialog))],
        )

        def on_dialog_open(e):
            update_filter("all")

        dialog.on_open = on_dialog_open

        return dialog

   

    def select_currency(currency, is_from):
        if is_from:
            selected_from["code"] = currency["code"]
            # Обновляем изображение (флаг или эмодзи крипты)
            from_button.content.controls[0].src = currency["icon"] if currency["type"] == "fiat" else None
            from_button.content.controls[0].src = currency["icon"]  
           
            if currency["type"] == "fiat":
                from_button.content.controls[0] = ft.Image(
                    src=currency["icon"],
                    width=32,
                    height=24,
                    fit=ft.ImageFit.CONTAIN,
                )
            else:
                from_button.content.controls[0] = ft.Text(currency["icon"], size=30)

            # Обновляем текст
            from_button.content.controls[1].controls[0].value = currency["code"]
            from_button.content.controls[1].controls[1].value = f"{currency['symbol']} {currency['name']}"

           
            from_button.update()
        else:
            selected_to["code"] = currency["code"]
            if currency["type"] == "fiat":
                to_button.content.controls[0] = ft.Image(
                    src=currency["icon"],
                    width=32,
                    height=24,
                    fit=ft.ImageFit.CONTAIN,
                )
            else:
                to_button.content.controls[0] = ft.Text(currency["icon"], size=30)

            to_button.content.controls[1].controls[0].value = currency["code"]
            to_button.content.controls[1].controls[1].value = f"{currency['symbol']} {currency['name']}"

            to_button.update()

        perform_conversion()
        update_exchange_rate()

        if is_from:
            page.close(from_dialog)
        else:
            page.close(to_dialog)

    from_dialog = create_currency_dialog(is_from=True)
    to_dialog = create_currency_dialog(is_from=False)

    def open_from_dialog(e):
        page.open(from_dialog)

    def open_to_dialog(e):
        page.open(to_dialog)

    from_button = ft.Container(
        content=ft.Row([
            ft.Image(src="us.svg", width=32, height=24, fit=ft.ImageFit.CONTAIN),
            ft.Column([
                ft.Text("USD", weight=ft.FontWeight.BOLD, size=16),
                ft.Text("$ Доллар США", size=12, color=ft.Colors.GREY_700),
            ], spacing=2),
            ft.Icon(ft.Icons.ARROW_DROP_DOWN)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        bgcolor=ft.Colors.SURFACE,
        padding=15,
        border_radius=12,
        width=380,
        on_click=open_from_dialog,
        ink=True
    )

    to_button = ft.Container(
        content=ft.Row([
            ft.Image(src="eu.svg", width=32, height=24, fit=ft.ImageFit.CONTAIN),
            ft.Column([
                ft.Text("EUR", weight=ft.FontWeight.BOLD, size=16),
                ft.Text("€ Евро", size=12, color=ft.Colors.GREY_700),
            ], spacing=2),
            ft.Icon(ft.Icons.ARROW_DROP_DOWN)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        bgcolor=ft.Colors.SURFACE,
        padding=15,
        border_radius=12,
        width=380,
        on_click=open_to_dialog,
        ink=True
    )

    result_container = ft.Container(
        content=ft.Column([
            ft.Text("Результат:", size=14, color=ft.Colors.WHITE70),
            ft.Text("", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
        ]),
        bgcolor=ft.Colors.INDIGO,
        padding=20,
        border_radius=12,
        visible=False
    )

    update_button = ft.ElevatedButton(
        text="Обновить курсы",
        icon=ft.Icons.REFRESH,
        width=380,
        height=50,
        bgcolor=ft.Colors.INDIGO,
        color=ft.Colors.WHITE
    )

    last_update_text = ft.Text("", size=11, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER)

    def update_api_counter():
        remaining = converter.get_remaining_requests()
        api_counter.content.controls[1].value = f"{converter.request_count} из {converter.max_requests} запросов"
        if remaining <= 0:
            api_counter.bgcolor = ft.Colors.RED_50
            api_counter.content.controls[0].color = ft.Colors.RED_700
            api_counter.content.controls[1].color = ft.Colors.RED_700
        elif remaining < 100:
            api_counter.bgcolor = ft.Colors.ORANGE_50
            api_counter.content.controls[0].color = ft.Colors.ORANGE_700
            api_counter.content.controls[1].color = ft.Colors.ORANGE_700
        else:
            api_counter.bgcolor = ft.Colors.BLUE_50
            api_counter.content.controls[0].color = ft.Colors.BLUE_700
            api_counter.content.controls[1].color = ft.Colors.BLUE_700
        api_counter.update()

    def validate_number_input(e):
        value = e.control.value
        if value:
            cleaned = re.sub(r'[^\d.,]', '', value).replace(",", ".")
            parts = cleaned.split('.')
            if len(parts) > 2:
                cleaned = parts[0] + '.' + parts[1]
            e.control.value = cleaned
            e.control.update()
        perform_conversion()

    def update_exchange_rate():
        rate_str = converter.get_exchange_rate(selected_from["code"], selected_to["code"])
        exchange_rate_text.value = rate_str
        exchange_rate_text.update()

    def perform_conversion():
        amount = amount_field.value or "0"
        result = converter.convert(amount, selected_from["code"], selected_to["code"])
        if result is not None:
            result_container.content.controls[1].value = f"{result} {selected_to['code']}"
            result_container.visible = True
        else:
            result_container.visible = False
        result_container.update()

    def update_status(is_online, message=""):
        if is_online:
            status_icon.name = ft.Icons.WIFI
            status_icon.color = ft.Colors.GREEN
            status_text.value = "Подключено"
            status_text.color = ft.Colors.GREEN
            error_banner.visible = False
            update_button.disabled = False
        else:
            status_icon.name = ft.Icons.WIFI_OFF
            status_icon.color = ft.Colors.RED
            status_text.value = "Нет подключения"
            status_text.color = ft.Colors.RED
            if message:
                error_banner.content.value = message
                error_banner.visible = True
            update_button.disabled = True
        page.update()

    def on_update_click(e):
        if not converter.can_make_request():
            error_banner.content.value = f"Лимит запросов исчерпан! ({converter.max_requests}/день)"
            error_banner.visible = True
            page.update()
            return

        update_button.disabled = True
        update_button.text = "Обновление..."
        page.update()

        is_online = converter.check_internet()
        if is_online:
            success, message = converter.fetch_rates()
            if success:
                last_update_text.value = f"Обновлено: {converter.last_update.strftime('%d.%m.%Y %H:%M')}"
                last_update_text.update()
                perform_conversion()
                update_exchange_rate()
                update_api_counter()
                update_status(True)
            else:
                update_status(False, message)
        else:
            update_status(False, "Нет подключения к интернету")

        update_button.text = "Обновить курсы"
        update_button.disabled = False
        page.update()

    def swap_currencies(e):
        # Сохраняем текущие валюты
        from_code = selected_from["code"]
        to_code = selected_to["code"]

        # Находим объекты валют
        from_curr = next((c for c in converter.all_currencies if c["code"] == from_code), None)
        to_curr = next((c for c in converter.all_currencies if c["code"] == to_code), None)

        if not from_curr or not to_curr:
            return

        # Меняем местами коды в выбранных валютах
        selected_from["code"] = to_code
        selected_to["code"] = from_code

       
        if to_curr["type"] == "fiat":
            from_button.content.controls[0] = ft.Image(
                src=to_curr["icon"],
                width=32,
                height=24,
                fit=ft.ImageFit.CONTAIN,
            )
        else:
            from_button.content.controls[0] = ft.Text(to_curr["icon"], size=30)

        from_button.content.controls[1].controls[0].value = to_curr["code"]
        from_button.content.controls[1].controls[1].value = f"{to_curr['symbol']} {to_curr['name']}"
        from_button.update()

        
        if from_curr["type"] == "fiat":
            to_button.content.controls[0] = ft.Image(
                src=from_curr["icon"],
                width=32,
                height=24,
                fit=ft.ImageFit.CONTAIN,
            )
        else:
            to_button.content.controls[0] = ft.Text(from_curr["icon"], size=30)

        to_button.content.controls[1].controls[0].value = from_curr["code"]
        to_button.content.controls[1].controls[1].value = f"{from_curr['symbol']} {from_curr['name']}"
        to_button.update()

        # Пересчитываем результат и курс
        perform_conversion()
        update_exchange_rate()

   

    amount_field.on_change = validate_number_input
    update_button.on_click = on_update_click

    swap_button = ft.IconButton(
        icon=ft.Icons.SWAP_VERT,
        icon_color=ft.Colors.INDIGO,
        icon_size=30,
        on_click=swap_currencies
    )

    page.add(
        ft.Column([
            ft.Row([
                ft.Text("Конвертер валют", size=28, weight=ft.FontWeight.BOLD, expand=True),
                theme_icon
            ]),
            ft.Row([status_icon, status_text], alignment=ft.MainAxisAlignment.CENTER),
            api_counter,
            error_banner,
            ft.Container(height=10),
            amount_field,
            ft.Container(height=10),
            ft.Text("Из", size=14, weight=ft.FontWeight.BOLD),
            from_button,
            ft.Container(content=swap_button, alignment=ft.alignment.center),
            ft.Text("В", size=14, weight=ft.FontWeight.BOLD),
            to_button,
            ft.Container(height=10),
            exchange_rate_text,
            ft.Container(height=10),
            result_container,
            ft.Container(height=20),
            update_button,
            ft.Container(height=10),
            last_update_text
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

    update_api_counter()
    on_update_click(None)


if __name__ == "__main__":
    ft.app(target=main, assets_dir="flags")