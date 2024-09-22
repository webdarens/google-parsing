from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup
import time
import requests
import re
import csv
import os
import random
from concurrent.futures import ThreadPoolExecutor
from threading import Timer

country_codes = {
    "Андорра": "countryAD",
    "Объединенные Арабские Эмираты": "countryAE",
    "Антигуа и Барбуда": "countryAG",
    "Ангилья": "countryAI",
    "Албания": "countryAL",
    "Армения": "countryAM",
    "Ангола": "countryAO",
    "Антарктида": "countryAQ",
    "Аргентина": "countryAR",
    "Американское Самоа": "countryAS",
    "Австрия": "countryAT",
    "Австралия": "countryAU",
    "Аруба": "countryAW",
    "Аландские острова": "countryAX",
    "Азербайджан": "countryAZ",
    "Босния и Герцеговина": "countryBA",
    "Барбадос": "countryBB",
    "Бангладеш": "countryBD",
    "Бельгия": "countryBE",
    "Буркина-Фасо": "countryBF",
    "Болгария": "countryBG",
    "Бахрейн": "countryBH",
    "Бурунди": "countryBI",
    "Бенин": "countryBJ",
    "Сен-Бартелеми": "countryBL",
    "Бермуды": "countryBM",
    "Бруней": "countryBN",
    "Боливия": "countryBO",
    "Бонэйр, Синт-Эстатиус и Саба": "countryBQ",
    "Бразилия": "countryBR",
    "Багамы": "countryBS",
    "Бутан": "countryBT",
    "Остров Буве": "countryBV",
    "Ботсвана": "countryBW",
    "Беларусь": "countryBY",
    "Белиз": "countryBZ",
    "Канада": "countryCA",
    "Кокосовыe острова (острова Килинг)": "countryCC",
    "Конго (ДРК)": "countryCD",
    "Центрально-Африканская Республика": "countryCF",
    "Конго (Республика)": "countryCG",
    "Швейцария": "countryCH",
    "Кот-д’Ивуар": "countryCI",
    "Острова Кука": "countryCK",
    "Чили": "countryCL",
    "Камерун": "countryCM",
    "Колумбия": "countryCO",
    "Коста-Рика": "countryCR",
    "Кабо-Верде": "countryCV",
    "Кюрасао": "countryCW",
    "Остров Рождества": "countryCX",
    "Кипр": "countryCY",
    "Чехия": "countryCZ",
    "Германия": "countryDE",
    "Джибути": "countryDJ",
    "Дания": "countryDK",
    "Доминика": "countryDM",
    "Доминиканская Республика": "countryDO",
    "Алжир": "countryDZ",
    "Эквадор": "countryEC",
    "Эстония": "countryEE",
    "Египет": "countryEG",
    "Западная Сахара": "countryEH",
    "Эритрея": "countryER",
    "Испания": "countryES",
    "Эфиопия": "countryET",
    "Финляндия": "countryFI",
    "Фиджи": "countryFJ",
    "Фолклендские острова (Мальвинские острова)": "countryFK",
    "Микронезия": "countryFM",
    "Фарерские острова": "countryFO",
    "Франция": "countryFR",
    "Габон": "countryGA",
    "Великобритания": "countryGB",
    "Гренада": "countryGD",
    "Грузия": "countryGE",
    "Французская Гвиана": "countryGF",
    "Гернси": "countryGG",
    "Гана": "countryGH",
    "Гибралтар": "countryGI",
    "Гренландия": "countryGL",
    "Гамбия": "countryGM",
    "Гвинея": "countryGN",
    "Гваделупа": "countryGP",
    "Экваториальная Гвинея": "countryGQ",
    "Греция": "countryGR",
    "Остров Южная Георгия и Южные Сандвичевы острова": "countryGS",
    "Гватемала": "countryGT",
    "Гуам": "countryGU",
    "Гвинея-Биссау": "countryGW",
    "Гайана": "countryGY",
    "Гонконг": "countryHK",
    "Остров Херд и острова Макдональд": "countryHM",
    "Гондурас": "countryHN",
    "Хорватия": "countryHR",
    "Гаити": "countryHT",
    "Венгрия": "countryHU",
    "Индонезия": "countryID",
    "Ирландия": "countryIE",
    "Израиль": "countryIL",
    "Остров Мэн": "countryIM",
    "Индия": "countryIN",
    "Британская территория в Индийском океане": "countryIO",
    "Ирак": "countryIQ",
    "Исландия": "countryIS",
    "Италия": "countryIT",
    "Джерси": "countryJE",
    "Ямайка": "countryJM",
    "Иордания": "countryJO",
    "Япония": "countryJP",
    "Кения": "countryKE",
    "Киргизия": "countryKG",
    "Камбоджа": "countryKH",
    "Кирибати": "countryKI",
    "Коморские Острова": "countryKM",
    "Сент-Китс и Невис": "countryKN",
    "Южная Корея": "countryKR",
    "Кувейт": "countryKW",
    "Каймановы острова": "countryKY",
    "Казахстан": "countryKZ",
    "Лаос": "countryLA",
    "Ливан": "countryLB",
    "Сент-Люсия": "countryLC",
    "Лихтенштейн": "countryLI",
    "Шри-Ланка": "countryLK",
    "Либерия": "countryLR",
    "Лесото": "countryLS",
    "Литва": "countryLT",
    "Люксембург": "countryLU",
    "Латвия": "countryLV",
    "Ливия": "countryLY",
    "Марокко": "countryMA",
    "Монако": "countryMC",
    "Молдова": "countryMD",
    "Черногория": "countryME",
    "Сен-Мартен": "countryMF",
    "Мадагаскар": "countryMG",
    "Маршалловы Острова": "countryMH",
    "Македония": "countryMK",
    "Мали": "countryML",
    "Мьянма (Бирма)": "countryMM",
    "Монголия": "countryMN",
    "Макао": "countryMO",
    "Северные Марианские острова": "countryMP",
    "Мартиника": "countryMQ",
    "Мавритания": "countryMR",
    "Монтсеррат": "countryMS",
    "Мальта": "countryMT",
    "Маврикий": "countryMU",
    "Мальдивы": "countryMV",
    "Малави": "countryMW",
    "Мексика": "countryMX",
    "Малайзия": "countryMY",
    "Мозамбик": "countryMZ",
    "Намибия": "countryNA",
    "Новая Каледония": "countryNC",
    "Нигер": "countryNE",
    "Остров Норфолк": "countryNF",
    "Нигерия": "countryNG",
    "Никарагуа": "countryNI",
    "Нидерланды": "countryNL",
    "Норвегия": "countryNO",
    "Непал": "countryNP",
    "Науру": "countryNR",
    "Ниуэ": "countryNU",
    "Новая Зеландия": "countryNZ",
    "Оман": "countryOM",
    "Панама": "countryPA",
    "Перу": "countryPE",
    "Французская Полинезия": "countryPF",
    "Папуа – Новая Гвинея": "countryPG",
    "Филиппины": "countryPH",
    "Пакистан": "countryPK",
    "Польша": "countryPL",
    "Сент-Пьер и Микелон": "countryPM",
    "Питкерн": "countryPN",
    "Пуэрто-Рико": "countryPR",
    "Палестина": "countryPS",
    "Португалия": "countryPT",
    "Палау": "countryPW",
    "Парагвай": "countryPY",
    "Катар": "countryQA",
    "Реюньон": "countryRE",
    "Румыния": "countryRO",
    "Сербия": "countryRS",
    "Россия": "countryRU",
    "Руанда": "countryRW",
    "Саудовская Аравия": "countrySA",
    "Соломоновы Острова": "countrySB",
    "Сейшельские Острова": "countrySC",
    "Швеция": "countrySE",
    "Сингапур": "countrySG",
    "Остров Святой Елены": "countrySH",
    "Словения": "countrySI",
    "Шпицберген и Ян-Майен": "countrySJ",
    "Словакия": "countrySK",
    "Сьерра-Леоне": "countrySL",
    "Сан-Марино": "countrySM",
    "Сенегал": "countrySN",
    "Сомали": "countrySO",
    "Суринам": "countrySR",
    "Южный Судан": "countrySS",
    "Сан-Томе и Принсипи": "countryST",
    "Сальвадор": "countrySV",
    "Синт-Мартен": "countrySX",
    "Свазиленд": "countrySZ",
    "Тристан-да-Кунья": "countryTA",
    "Тёркс и Кайкос": "countryTC",
    "Чад": "countryTD",
    "Французские Южные территории": "countryTF",
    "Того": "countryTG",
    "Таиланд": "countryTH",
    "Таджикистан": "countryTJ",
    "Токелау": "countryTK",
    "Восточный Тимор": "countryTL",
    "Туркменистан": "countryTM",
    "Тунис": "countryTN",
    "Тонга": "countryTO",
    "Турция": "countryTR",
    "Тринидад и Тобаго": "countryTT",
    "Тувалу": "countryTV",
    "Тайвань": "countryTW",
    "Танзания": "countryTZ",
    "Украина": "countryUA",
    "Уганда": "countryUG",
    "Малые Тихоокеанские Отдаленные острова США": "countryUM",
    "США": "countryUS",
    "Уругвай": "countryUY",
    "Узбекистан": "countryUZ",
    "Ватикан": "countryVA",
    "Сент-Винсент и Гренадины": "countryVC",
    "Венесуэла": "countryVE",
    "Британские Виргинские острова": "countryVG",
    "Американские Виргинские острова": "countryVI",
    "Вьетнам": "countryVN",
    "Вануату": "countryVU",
    "Уоллис и Футуна": "countryWF",
    "Самоа": "countryWS",
    "Косово": "countryXK",
    "Йемен": "countryYE",
    "Майотта": "countryYT",
    "ЮАР": "countryZA",
    "Замбия": "countryZM",
    "Зимбабве": "countryZW"
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

proxies = {}

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException

def with_timeout(timeout, func, *args, **kwargs):
    timer = Timer(timeout, timeout_handler)
    timer.start()
    try:
        result = func(*args, **kwargs)
    except TimeoutException:
        print(f"Function {func.__name__} timed out after {timeout} seconds")
        return None
    finally:
        timer.cancel()
    return result

def get_html_with_selenium(url):
    driver_path = EdgeService(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=driver_path)
    page_nums = [0,100,200,300]
    for page_num in page_nums:
        pag
        driver.get(url)

    while "sorry/index" in driver.current_url:
        print("Пожалуйста, пройдите каптчу")
        time.sleep(5)
    time.sleep(8)

    page_source = driver.page_source


    return page_source

def get_emails(url):
    emails = set()
    instagrams = set()
    telegrams = set()
    twitters = set()
    discords = set()
    facebooks = set()
    youtubes = set()
    reddits = set()
    vks = set()

    try:
        result = requests.get(url, headers=headers, proxies=proxies, timeout=120)
        result.raise_for_status()
        
        soup = BeautifulSoup(result.text, 'lxml')

        found_email = False
        found_instagram = False
        found_telegram = False
        found_discord = False
        found_facebook = False
        found_twitter = False
        found_reddit = False
        found_youtube = False
        found_vk = False

        texts = soup.stripped_strings
        for mail in soup.find_all('a', href=True):
            href = mail.get('href')

            if href.startswith('/cdn-cgi/l/email-protection#'):
                decoded_email = href.replace('/cdn-cgi/l/email-protection#', '')
                key = int(decoded_email[:2], 16)
                hex_str = decoded_email[2:]
                email = ''
                for i in range(0, len(hex_str), 2):
                    email += chr(int(hex_str[i:i+2], 16) ^ key)
                email = re.sub(r'\?subject.*', '', email)
                email = re.sub(r'\?Subject.*', '', email)
                emails.add(email)
                found_email = True

            elif href.startswith('mailto:') and not href.startswith('malito:?'):
                default_email = href.replace('mailto:', '')
                emails.add(default_email)
                found_email = True

        email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
        for text in texts:
            matches = email_pattern.findall(text)
            if matches:
                emails.update(matches)
                found_email = True

        social_media_domains = {
            'instagram.com': (instagrams, 'Инст не найден', found_instagram),
            't.me': (telegrams, 'Тг не найден', found_telegram),
            'twitter.com': (twitters, 'Твиттер не найден', found_twitter),
            'discord.gg': (discords, 'Дс не найден', found_discord),
            'facebook.com': (facebooks, 'Фейсбук не найден', found_facebook),
            'reddit.com': (reddits, 'Реддит не найден', found_reddit),
            'youtube.com': (youtubes, 'Ютуб не найден', found_youtube),
            'vk.com': (vks, 'Вк не найден', found_vk),
        }

        for link in soup.find_all('a', href=True):
            href = link.get('href')
            for domain, (collection, not_found_message, found_flag) in social_media_domains.items():
                if domain in href:
                    collection.add(href)
                    found_flag = True
                    break

        for domain, (collection, not_found_message, found_flag) in social_media_domains.items():
            if not found_flag:
                collection.add(not_found_message)

        if not found_email:
            emails.add('Почты на сайте не найдены')

    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return set(), set(), set(), set(), set(), set(), set(), set(), set()

    return emails, instagrams, telegrams, twitters, discords, facebooks, reddits, youtubes, vks

def get_google_url(google):
    links = set()
    try:
        html = get_html_with_selenium(google)
        soup = BeautifulSoup(html, 'html.parser')
        request_links = soup.find_all('div', class_='GyAeWb')

        for div in request_links:
            for a_tag in div.find_all('a', href=True):  
                href = a_tag.get('href')
                if not href.startswith('/search') and 'google' not in href and not href.startswith('/preferences?') and not href.startswith('#'):
                    links.add(href)
    except requests.exceptions.RequestException as e:
        print(f"Error accessing Google: {e}")
        return set()

    return links

def change_country(google, country):
    country = country.strip()
    if country in country_codes:
        country_code = country_codes[country]
        google = google + f"&cr={country_code}"
        return google
    else:
        return "Страна не поддерживается"

def process_country(country, search_term, start_position, num_iterations, file_path):
    count = 0
    for _ in range(1):
        a = 100
        google = "https://www.google.com/search?q=intext:&as_qdr=all&filter=&num=&start=&complete=1"
        google = change_country(google, country)
        if google == "Страна не поддерживается":
            print(google)
            continue
        google = google.replace("intext:", f"intext:{search_term}")
        google = google.replace("num=", f"num={a}")
        google = google.replace("start=", f"start={start_position}")

        websites = with_timeout(120, get_google_url, google)
        if websites is None:
            continue

        print(google)
        for site in websites:
            try:
                result = with_timeout(120, get_emails, site)
                if result is None:
                    continue
                result_emails, instagram_links, telegram_links, twitter_links, discord_links, facebook_links, reddits_links, youtube_links, vk_links = result
                for email, instagram, telegram, twitter, discord, facebook, reddit, youtube, vk in zip(result_emails, instagram_links, telegram_links, twitter_links, discord_links, facebook_links, reddits_links, youtube_links, vk_links):
                    print(site, email)
                    count += 1
                    with open(file_path, mode='a', encoding='utf-8', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([site, email, instagram, telegram, twitter, discord, facebook, reddit, youtube, vk, country])
            except ValueError as e:
                print(f"Ошибка при обработке сайта {site}: {e}")
                count += 1
        start_position += count

def main():
    start_position = 0 
    num_iterations = 3
    country_input = input('Введите страну для поиска (с полным списком стран можно ознакомиться в txt файле): ')
    search_term = input('Введите запрос, который нужно найти: ')
    numselection = int(input('Укажите, сколько хотите сделать запросов (лучшие настройки по умолчанию), либо пропустите написав 0: '))

    if numselection != 0:
        num_iterations = numselection

    safe_search_term = re.sub(r'[\\/*?:"<>|]', "_", search_term)
    home_dir = os.path.expanduser('~')
    desktop_dir = os.path.join(home_dir, 'Desktop')
    file_path = os.path.join(desktop_dir, f'{safe_search_term}.csv')

    with open(file_path, mode='w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Website', 'Email', 'Instagram', 'Telegram', 'Twitter', 'Discord', 'Facebook', 'Reddit', 'YouTube', 'VK', 'Country'])

    if country_input.lower() == "все":
        countries = list(country_codes.keys())
        mid_point = len(countries) // 2
        part1 = countries[:mid_point]
        part2 = countries[mid_point:]

        with ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(process_countries, part1, search_term, start_position, num_iterations, file_path)
            executor.submit(process_countries, part2, search_term, start_position, num_iterations, file_path)
    else:
        process_country(country_input, search_term, start_position, num_iterations, file_path)

def process_countries(countries, search_term, start_position, num_iterations, file_path):
    for country in countries:
        process_country(country, search_term, start_position, num_iterations, file_path)

if __name__ == "__main__":
    main()
