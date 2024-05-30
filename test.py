import os 
import requests
from bs4 import BeautifulSoup
import csv
import random
import lxml
from threading import Thread,Lock
from concurrent.futures import ThreadPoolExecutor
import time
import re
#lxml,thread6,beautifulsoup4,csv,requests,time
proxies = {
    'http': 'socks5h://127.0.0.1:9150',
    'https': 'socks5h://127.0.0.1:9150'
}
country_codes = {
    "Австралия": "countryAU",
    "Австрия": "countryAT",
    "Аландские острова": "countryAX",
    "Албания": "countryAL",
    "Алжир": "countryDZ",
    "Ангилья": "countryAI",
    "Ангола": "countryAO",
    "Андорра": "countryAD",
    "Антигуа и Барбуда": "countryAG",
    "Антарктида": "countryAQ",
    "Аргентина": "countryAR",
    "Армения": "countryAM",
    "Аруба": "countryAW",
    "Американское Самоа": "countryAS",
    "Багамы": "countryBS",
    "Бангладеш": "countryBD",
    "Барбадос": "countryBB",
    "Бахрейн": "countryBH",
    "Беларусь": "countryBY",
    "Белиз": "countryBZ",
    "Бельгия": "countryBE",
    "Бенин": "countryBJ",
    "Бермуды": "countryBM",
    "Болгария": "countryBG",
    "Боливия": "countryBO",
    "Бонэйр, Синт-Эстатиус и Саба": "countryBQ",
    "Босния и Герцеговина": "countryBA",
    "Ботсвана": "countryBW",
    "Бразилия": "countryBR",
    "Британская территория в Индийском океане": "countryIO",
    "Британские Виргинские острова": "countryVG",
    "Бруней": "countryBN",
    "Буркина-Фасо": "countryBF",
    "Бурунди": "countryBI",
    "Бутан": "countryBT",
    "Вануату": "countryVU",
    "Ватикан": "countryVA",
    "Великобритания": "countryGB",
    "Венгрия": "countryHU",
    "Венесуэла": "countryVE",
    "Восточный Тимор": "countryTL",
    "Вьетнам": "countryVN",
    "Габон": "countryGA",
    "Гаити": "countryHT",
    "Гайана": "countryGY",
    "Гамбия": "countryGM",
    "Гана": "countryGH",
    "Гваделупа": "countryGP",
    "Гватемала": "countryGT",
    "Гвинея": "countryGN",
    "Гвинея-Биссау": "countryGW",
    "Германия": "countryDE",
    "Гернси": "countryGG",
    "Гибралтар": "countryGI",
    "Гондурас": "countryHN",
    "Гонконг": "countryHK",
    "Гренада": "countryGD",
    "Гренландия": "countryGL",
    "Греция": "countryGR",
    "Грузия": "countryGE",
    "Гуам": "countryGU",
    "Дания": "countryDK",
    "Джерси": "countryJE",
    "Джибути": "countryDJ",
    "Доминика": "countryDM",
    "Доминиканская Республика": "countryDO",
    "Египет": "countryEG",
    "Замбия": "countryZM",
    "Западная Сахара": "countryEH",
    "Зимбабве": "countryZW",
    "Израиль": "countryIL",
    "Индия": "countryIN",
    "Индонезия": "countryID",
    "Иордания": "countryJO",
    "Ирак": "countryIQ",
    "Ирландия": "countryIE",
    "Исландия": "countryIS",
    "Испания": "countryES",
    "Италия": "countryIT",
    "Йемен": "countryYE",
    "Кабо-Верде": "countryCV",
    "Казахстан": "countryKZ",
    "Каймановы острова": "countryKY",
    "Камбоджа": "countryKH",
    "Камерун": "countryCM",
    "Канада": "countryCA",
    "Катар": "countryQA",
    "Кения": "countryKE",
    "Кипр": "countryCY",
    "Киргизия": "countryKG",
    "Кирибати": "countryKI",
    "Китай": "countryCN",
    "Кокосовыe острова (острова Килинг)": "countryCC",
    "Колумбия": "countryCO",
    "Коморские Острова": "countryKM",
    "Конго (ДРК)": "countryCD",
    "Конго (Республика)": "countryCG",
    "Коста-Рика": "countryCR",
    "Кот-д’Ивуар": "countryCI",
    "Куба": "countryCU",
    "Кувейт": "countryKW",
    "Кюрасао": "countryCW",
    "Лаос": "countryLA",
    "Латвия": "countryLV",
    "Лесото": "countryLS",
    "Либерия": "countryLR",
    "Ливан": "countryLB",
    "Ливия": "countryLY",
    "Литва": "countryLT",
    "Лихтенштейн": "countryLI",
    "Люксембург": "countryLU",
    "Маврикий": "countryMU",
    "Мавритания": "countryMR",
    "Мадагаскар": "countryMG",
    "Майотта": "countryYT",
    "Макао": "countryMO",
    "Македония": "countryMK",
    "Малави": "countryMW",
    "Малайзия": "countryMY",
    "Мали": "countryML",
    "Мальдивы": "countryMV",
    "Мальта": "countryMT",
    "Марокко": "countryMA",
    "Мартиника": "countryMQ",
    "Маршалловы Острова": "countryMH",
    "Мексика": "countryMX",
    "Микронезия": "countryFM",
    "Мозамбик": "countryMZ",
    "Молдова": "countryMD",
    "Монако": "countryMC",
    "Монголия": "countryMN",
    "Монтсеррат": "countryMS",
    "Мьянма (Бирма)": "countryMM",
    "Намибия": "countryNA",
    "Науру": "countryNR",
    "Непал": "countryNP",
    "Нигер": "countryNE",
    "Нигерия": "countryNG",
    "Нидерланды": "countryNL",
    "Никарагуа": "countryNI",
    "Новая Зеландия": "countryNZ",
    "Новая Каледония": "countryNC",
    "Норвегия": "countryNO",
    "ОАЭ": "countryAE",
    "Оман": "countryOM",
    "Острова Кука": "countryCK",
    "Острова Теркс и Кайкос": "countryTC",
    "Острова Херд и Макдональд": "countryHM",
    "Палау": "countryPW",
    "Палестина": "countryPS",
    "Панама": "countryPA",
    "Папуа – Новая Гвинея": "countryPG",
    "Парагвай": "countryPY",
    "Перу": "countryPE",
    "Питкерн": "countryPN",
    "Польша": "countryPL",
    "Португалия": "countryPT",
    "Пуэрто-Рико": "countryPR",
    "Реюньон": "countryRE",
    "Россия": "countryRU",
    "Руанда": "countryRW",
    "Румыния": "countryRO",
    "Сальвадор": "countrySV",
    "Самоа": "countryWS",
    "Сан-Марино": "countrySM",
    "Сан-Томе и Принсипи": "countryST",
    "Саудовская Аравия": "countrySA",
    "Свазиленд": "countrySZ",
    "Сейшельские Острова": "countrySC",
    "Сен-Бартелеми": "countryBL",
    "Сен-Пьер и Микелон": "countryPM",
    "Сенегал": "countrySN",
    "Сент-Винсент и Гренадины": "countryVC",
    "Сент-Китс и Невис": "countryKN",
    "Сент-Люсия": "countryLC",
    "Сербия": "countryRS",
    "Сингапур": "countrySG",
    "Синт-Мартен": "countrySX",
    "Сирия": "countrySY",
    "Словакия": "countrySK",
    "Словения": "countrySI",
    "Соломоновы Острова": "countrySB",
    "Сомали": "countrySO",
    "Суринам": "countrySR",
    "США": "countryUS",
    "Таджикистан": "countryTJ",
    "Тайвань": "countryTW",
    "Танзания": "countryTZ",
    "Того": "countryTG",
    "Токелау": "countryTK",
    "Тонга": "countryTO",
    "Тринидад и Тобаго": "countryTT",
    "Тристан-да-Кунья": "countryTA",
    "Тунис": "countryTN",
    "Туркменистан": "countryTM",
    "Турция": "countryTR",
    "Уганда": "countryUG",
    "Узбекистан": "countryUZ",
    "Украина": "countryUA",
    "Уоллис и Футуна": "countryWF",
    "Уругвай": "countryUY",
    "Фарерские острова": "countryFO",
    "Фиджи": "countryFJ",
    "Филиппины": "countryPH",
    "Финляндия": "countryFI",
    "Фолклендские острова (Мальвинские острова)": "countryFK",
    "Франция": "countryFR",
    "Французская Гвиана": "countryGF",
    "Французская Полинезия": "countryPF",
    "Французские Южные территории": "countryTF",
    "Хорватия": "countryHR",
    "Чад": "countryTD",
    "Черногория": "countryME",
    "Чехия": "countryCZ",
    "Чили": "countryCL",
    "Швейцария": "countryCH",
    "Швеция": "countrySE",
    "Шпицберген и Ян-Майен": "countrySJ",
    "Шри-Ланка": "countryLK",
    "Эквадор": "countryEC",
    "Экваториальная Гвинея": "countryGQ",
    "Эритрея": "countryER",
    "Эсватини": "countrySZ",
    "Эстония": "countryEE",
    "Эфиопия": "countryET",
    "ЮАР": "countryZA",
    "Южная Корея": "countryKR",
    "Южный Судан": "countrySS",
    "Ямайка": "countryJM",
    "Япония": "countryJP"
}
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
}

def get_emails(url):
    emails = set()

    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()  # Проверка на ошибки HTTP
        
        soup = BeautifulSoup(result.text, 'lxml')

        for mail in soup.find_all('a', href=True):
            href = mail.get('href')

            # for decoded email
            if href.startswith('/cdn-cgi/l/email-protection#'):
                decoded_email = href.replace('/cdn-cgi/l/email-protection#', '')
                key = int(decoded_email[:2], 16)
                hex_str = decoded_email[2:]
                email = ''
                for i in range(0, len(hex_str), 2):
                    email += chr(int(hex_str[i:i+2], 16) ^ key)
                if not email.startswith('?subject') and not email.startswith('д.') and not email.startswith('ул.'):
                    pattern = r'(?<!^)\?subject.*'
                    email = re.sub(pattern, '', email)
                    emails.add(email)

            # for default email
            elif href.startswith('mailto:'):
                default_email = href.replace('mailto:', '')
                if not default_email.startswith('?subject') and not default_email.startswith('д.') and not default_email.startswith('ул.'):
                    pattern = r'(?<!^)\?subject.*'
                    default_email = re.sub(pattern, '', default_email)
                    emails.add(default_email)
                    


    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
        # Обработка ошибки, например, попробуйте использовать другой прокси или пропустите этот сайт
        return set()  # Возвращаем пустой набор email-адресов в случае ошибки

    return emails

def get_google_url(google):
    links = set()
    try:
        response = requests.get(google, headers=headers) 
        if response.status_code ==200:
            print(f"Status code: {response.status_code}[+]Всё работает исправно")
        elif response.status_code == 429:
            print(f"Status code: {response.status_code}[-]Вы получили временную ip блокировку")
        soup = BeautifulSoup(response.text, 'lxml')
        reqest_links = soup.find_all('div', class_='GyAeWb')

        for div in reqest_links:
            spans = div.find_all('span')
            for a_tag in div.find_all('a', href=True):  
                href = a_tag.get('href')
                if not href.startswith('/search') and 'google' not in href and not href.startswith('/preferences?') and not href.startswith('#'):
                    links.add(href)
    except requests.exceptions.RequestException as e:
        return set() 

    return links

def change_country(google, country):
    if country in country_codes:
        country_code = country_codes[country]
        google = google + f"&cr={country_code}"
        return google
    else:
        return "Страна не поддерживается"

def main():
    start_position = 0 
    num_iterations = 3
    country_input = input('Введите страну для поиска(с полным списком стран можно ознакомиться в txt файле) :')
    search_term = input('Введите запрос, который нужно найти :')
    numselection = int(input('Укажите, сколько хотите сделать запросов(лучшие настройки по умолчанию), либо пропустие написав 0 :'))

    homeDir = os.path.expanduser('~')
    desktop_dir = homeDir + r'\Desktop'
    file_path = os.path.join(desktop_dir, 'Emails.csv')
    print(f"\n\nТаблица находится в {file_path}\n\n")
    if numselection != 0:
        num_iterations = numselection
    with ThreadPoolExecutor(max_workers=6) as executor:
        count = 0
        for _ in range(num_iterations):
            a = random.randint(300,400)
            google = "https://www.google.com/search?q=intext:&as_qdr=all&filter=&num=&start=&complete=1"
            user_country =  country_input
            google = change_country(google, user_country)
            google = google.replace("intext:", f"intext:{search_term}")
            google = google.replace("num=", f"num={a}")
            google = google.replace("start=", f"start={start_position}")

            websites = get_google_url(google)
            print(google)
            for site in websites:
                resultEmails = get_emails(site)
                for email in resultEmails:
                    print(site, email)
                    count+=1
                    with open(file_path, mode='a', encoding='utf-8', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([site, email])
            start_position += count
        print('парсинг завершен')
        time.sleep(40)

if __name__ == '__main__':
    main()