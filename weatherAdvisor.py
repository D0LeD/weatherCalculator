import requests
from bs4 import BeautifulSoup
import time

class Node: 
	def __init__(self, key, value): 
		self.key = key 
		self.value = value 
		self.next = None

class Day: # класс который сожержит данные по конкретному дню 
    def __init__(self, date_text, phrase, temperature, precipitation):
        self.date = date_text
        self.phrase = phrase
        self.temperature = temperature
        self.precipitation = precipitation

    def __str__(self): # функция для вывода данных в таблицу 
        normalizeddate = "          " + self.date
        for _ in range (0, 14-len(self.date)):
            normalizeddate = normalizeddate + " "

        normalizedtemperature = "              " + self.temperature + "C"
        for _ in range (0, 15-len(self.temperature)):
            normalizedtemperature = normalizedtemperature + " "

        normalizedprecipitation = "                " + self.precipitation
        for _ in range(0, 17-len(self.precipitation)):
            normalizedprecipitation = normalizedprecipitation + " "

        normalizedphrase = "            " + self.phrase
        return f"{normalizeddate}|{normalizedtemperature}|{normalizedprecipitation}|{normalizedphrase}"


class HashTable:
	def __init__(self, capacity): 
		self.capacity = capacity 
		self.size = 0
		self.table = [None] * capacity 

	def _hash(self, key): 
		return hash(key) % self.capacity 
		
	def add(self, key, value):
		index = self._hash(key)
		new_node = Node(key, value)
		new_node.next = self.table[index]
		self.table[index] = new_node
		self.size += 1
      
def get_weather_for_day(day): # функция парсинга данных с сайта с погодой
    if day == 1:
        url = 'https://www.accuweather.com/en/lv/riga/225780/weather-tomorrow/225780'
    elif day == 2:
        url = 'https://www.accuweather.com/en/lv/riga/225780/weather-tomorrow/225780'
    else:
        url = f'https://www.accuweather.com/en/lv/riga/225780/daily-weather-forecast/225780?day={day}' 
    
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
    #делаем вид что мы не скрипт
    response = requests.get(url, headers=headers)
    if response.status_code != 200: # если не 200, то плохо...
        print(f"Error downlowding page: {response.status_code}")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser') #объект для парсинга

    # 📅 Дата (только месяц и число)
    date_elem = soup.select_one('.subnav-pagination div')
    if date_elem:
        full_date = date_elem.text.strip()
        try:
            date_text = full_date.split(', ')[1]  # "May 18"
        except IndexError:
            date_text = full_date
    else:
        date_text = f"Day {day}"

    #фраза
    phrase_elem = soup.select_one('.half-day-card-content .phrase')
    phrase = phrase_elem.text.strip() if phrase_elem else 'N/A' #если найден, удаляем пробелы strip()

    # 🌡 Температура
    temp_high = 'N/A'

    half_day_cards = soup.select('.half-day-card')

    for card in half_day_cards:
        label = card.select_one('.hi-lo-label')
        value = card.select_one('.temperature')
        if label and value:
            text = value.get_text(strip=True)
            if 'Hi' in label.text:
                temp_high = text

    # 🌧 Осадки
    precipitation = 'N/A'
    all_precip = soup.select('p.panel-item')

    for p in all_precip:
        if 'Precipitation' in p.text:
            val = p.select_one('span.value')
            precipitation = val.text.strip() if val else 'N/A'
            break

    return {
        'day': day,
        'date': date_text, 
        'phrase': phrase,
        'temp_high': temp_high.strip('Hi'),
        'precipitation': precipitation  
    }

def calculateScore(day, ratiotemperature, ratioprecipitation): # функция рассчитываюшая оценку для каждого дня
    try:
        temperature = int(day.temperature.strip('°'))
        precipitation = int(day.precipitation.strip('%'))
        return temperature*(ratiotemperature/100) - (precipitation/20)*(ratioprecipitation/100)
    except:
        return None 
    
def createDataBase(ratiotemperature, ratioprecipitation, daysforanalysis): # функция создаюшая hashtable из данныйх с сайта
    database = HashTable(daysforanalysis)
    for day in range(1, daysforanalysis+1):
        data = get_weather_for_day(day) # вот здесь берется новый день
        if data:
            # Парсим данные и создаём объект класса Day
            d = Day(
                date_text=data['date'],
                phrase=data['phrase'],
                temperature=data['temp_high'],
                precipitation=data['precipitation']
            )
            database.add(round(calculateScore(d, ratiotemperature, ratioprecipitation), 3), d) # добавляем новый день в таблицу с рассчитаной оценкой
            
            if (day/daysforanalysis)*100 > 75: # вывод процентов при загрузке
                print(f"🔍 Almost there... {round((day/daysforanalysis)*100, 2)}% done")
            else:
                print(f"🔍 Analyzing data... {round((day/daysforanalysis)*100, 2)}% done")

        time.sleep(1.5) # задержка для сайта (избегаем банчика)
    return database

def main():
    ratiotemperature, ratioprecipitation = 50, 50 

    while True : # Цикл главного меню
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print("☀️  Welcome to the Weather Advisor! ☀️")
        print("📋 Choose an option: ")
        print("  1️⃣  Let's find out which day is the best!")
        print("  2️⃣  Let's change the scoring ratio!")
        print("  0️⃣  Exit the programm :c")
        choice = input()

        match choice:
            case "1":
                processWeather(ratioprecipitation, ratiotemperature)
            case "2":
                ratiotemperature, ratioprecipitation = changeRatios(ratiotemperature, ratioprecipitation)
                print(ratiotemperature, ratioprecipitation)
            case "0":
                break
            case _:
                print("⚠️ Unknown command ⚠️")
        
def processWeather(ratiotemperature, ratioprecipitation): # цикл начала работы с погодой
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print("🔍 Let's find out which day is the best!🔍")

    while True:
        print("📅 Enter number of days to analyze (1 - 31)")

        try:
            numberofdays = int(input()) # Пробуем преобразовать в int
        except ValueError: # Если не получилось (например, введено "abc")
            print("⚠️ Error: Input must be number")
            continue
        if numberofdays < 1 or numberofdays > 31:
            print("⚠️ Error: Input must be in range (1 - 31)")
            continue

        print(f"🌤️  Select how many top weather days to show from the next {numberofdays} days: ") 
        try:
            numberofbestdays = int(input())
        except ValueError:
            print("⚠️ Error: Input must be number")
            continue
        if numberofbestdays < 0 or numberofbestdays > numberofdays:
            print(f"⚠️ Error: Input must be in range (1 - {numberofdays})")
            continue

        database = createDataBase(ratiotemperature, ratioprecipitation, numberofdays)
        findBestDays(database, numberofbestdays)
        print("\n 0️⃣  Return to main menu")
        match input():
            case "0":
                return
            case _:
                print("⚠️ Unknown command ⚠️")
             

def findBestDays(database, numberofbestdays):
    all_entries = []
    for index in range(database.capacity):
        current = database.table[index]
        while current:
            all_entries.append((current.key, current.value))
            current = current.next

    bestdays = sorted(all_entries, key=lambda x: x[0], reverse=True)[:numberofbestdays]
    print("\n🌟 Top Weather Days Forecast 🌟")
    print("        ✅  Score        |        📅  Date        |        🌡️  Temperature        |        💧  Precipitation        |        📊  Day description")
    print("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

    for key, day in bestdays:
        normalizedkey = "            " + str(key)
        for _ in range (0, 13-len(str(key))):
            normalizedkey = normalizedkey + " "
        print(f"{normalizedkey}|{day}")
    


def changeRatios(ratiotemperature, ratioprecipitation):
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print("🎯 --- Scoring Ratio Adjustment --- 🎯")

    while True:
        print("📋 Choose an option: ")
        print(f"  1️⃣  Change temperature and precipitation weight! Current weights: 🌡️  Temperature = {ratiotemperature} and 💧 Precipitation = {ratioprecipitation})")
        print("  0️⃣  Return to main menu")
        choice = input()

        match choice:
            case "1":
                print(" 🌡️  Enter your Scoring Ratio for temperature: ")
                try:
                    newtemperature = int(input()) # Пробуем преобразовать в int
                except ValueError: # Если не получилось (например, введено "abc")
                    print("⚠️ Error: Input must be positive number")
                    continue
                if newtemperature < 0:
                    print("⚠️ Error: Input must be positive number")
                    continue

                print(" 💧  Enter your Scoring Ratio for Precipitation: ")
                try:
                    newpercipitation = int(input())
                except ValueError:
                    print("⚠️ Error: Input must be positive number")
                    continue
                if newpercipitation < 0:
                    print("⚠️ Error: Input must be positive number")
                    continue

                if newtemperature + newpercipitation != 100:
                    print("⚠️ Error: Ratios need to sum up to 100%")
                else:
                    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                    ratiotemperature, ratioprecipitation = newtemperature, newpercipitation
            case "0":
                return(ratiotemperature, ratioprecipitation)
            case _:
                print("⚠️ Unknown command ⚠️")


if __name__ == "__main__":
    main()
