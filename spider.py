import datetime
import re
import selenium.common.exceptions
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from configure import *


class TripSpider(object):
    TAG = "TripSpider ({departure} to {destination} on {trip_date}): "

    def __init__(self, departure: str, destination: str, trip_date: str, index: int):
        logger.info(f"建立数据获取工作对象：于<{trip_date}>从<{departure}>前往<{destination}>"
                    .format(trip_date=trip_date, departure=departure, destination=destination))

        self.index = str(index)
        self.update_time = time.time()
        self.departure_zh, self.departure_en = departure.split(ZH_EN_SPLITER)
        self.destination_zh, self.destination_en = destination.split(ZH_EN_SPLITER)
        self.trip_date = trip_date
        self.url = data_url.format(
            departure=self.departure_en, destination=self.destination_en, trip_date=self.trip_date)
        self.TAG = self.TAG.format(
            departure=self.departure_zh, destination=self.destination_zh, trip_date=self.trip_date)

        self.chrome_options = webdriver.ChromeOptions()
        # self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(chrome_options=self.chrome_options)

        self.all_airlines = list()
        self.all_airlines_infos = list()

    def get_web_data(self):
        logger.info(self.TAG + "正在获取网页数据...")
        try:
            self.browser.get(self.url)
            WebDriverWait(driver=self.browser, timeout=web_page_waiting).until(
                ec.presence_of_element_located((By.XPATH,
                                                "//*[@id=\"__next\"]/div[2]/div/div[3]/div[3]/div[2]/span/div[1]")))
            self.browser.refresh()
            WebDriverWait(driver=self.browser, timeout=web_page_waiting).until(
                ec.presence_of_element_located((By.XPATH,
                                                "//*[@id=\"__next\"]/div[2]/div/div[3]/div[3]/div[2]/span/div[1]")))

            self.update_time = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")

            for i in range(15):
                self.browser.find_element(by=By.TAG_NAME, value="body").send_keys(Keys.END)
        except Exception as e:
            logger.error(self.TAG + "获取网页数据时遇到错误：" + str(e))

    def extract_all_airlines(self):
        logger.info(self.TAG + "正在提取所有航班...")
        k = 0
        while True:
            k += 1
            xpath = "//*[@id=\"__next\"]/div[2]/div/div[3]/div[3]/div[2]/span/div[k]"
            try:
                airline = self.browser.find_element(by=By.XPATH, value=xpath.replace("k", str(k)))
            except selenium.common.exceptions.NoSuchElementException:
                break

            if "中转组合" in airline.get_attribute("innerHTML"):
                break

            self.all_airlines.append(airline)
        logger.info(self.TAG + f"一共提取到 {k} 躺航班信息。".format(k=str(len(self.all_airlines))))

    def analyze_each_airline(self):
        logger.info(self.TAG + "正在解析每条航班数据...")
        for airline in self.all_airlines:
            airline_html = airline.get_attribute("innerHTML")
            self.all_airlines_infos.append(self.get_airline_infomation(airline_html))

    def get_airline_infomation(self, airline: str) -> dict:
        soup = BeautifulSoup(airline, "html.parser")

        try:
            airline_company = soup.find("span", {"id": re.compile(r"airlineName(.*)")}).text
        except AttributeError:
            airline_company = "获取出错"

        try:
            temp = soup.find("span", {"class": "plane-No"}).text.split(" ")
            airline_name = temp[0]
            plane_type = temp[1]
        except AttributeError:
            airline_name = plane_type = "获取出错"

        try:
            temp = soup.find("div", {"class": "depart-box"}).text
            departure_time = re.search(r"[0-9]+:[0-9]+", temp).group(0)
        except AttributeError:
            departure_time = "获取出错"

        try:
            departure_airport = soup.find("span", {"id": re.compile(r"departureFlightTrain(.*)")}).text
            terminal = soup.find("span", {"class": "terminal ", "id": re.compile(r"departureTerminal(.*)")})
            departure_airport += "" if terminal is None else terminal.text
        except AttributeError:
            departure_airport = "获取出错"

        try:
            transfer_station = soup.find("span", {"id": re.compile(r"flightStop-(.*)")}).text
            transfer_station = transfer_station.replace("m", "分钟")
            transfer_station = transfer_station.replace("h", "小时")
            transfer_station = transfer_station.replace("d", "天")
        except AttributeError:
            transfer_station = "不经停或中转"

        try:
            temp = soup.find("div", {"class": "arrive-box"}).text
            arrival_time = re.search(r"[0-9]+:[0-9]+", temp).group(0)
        except AttributeError:
            arrival_time = "获取出错"

        try:
            destination_airport = soup.find("span", {"id": re.compile(r"arrivalFlightTrain(.*)")}).text
            terminal = soup.find("span", {"class": "terminal ", "id": re.compile(r"departureTerminal(.*)")})
            destination_airport += "" if terminal is None else terminal.text
        except AttributeError:
            destination_airport = "获取出错"

        try:
            cross_days = soup.find("span", {"class": "day", "id": re.compile(r"crossDays(.*)")}).text
        except AttributeError:
            cross_days = "0天"

        departure_time, arrival_time, travel_time = self.calculate_travel_time(
            trip_date=self.trip_date, departure=departure_time, arrival=arrival_time, cross_days=cross_days)

        try:
            ticket_price = soup.find("span", {"class": "price"}).text
        except AttributeError:
            ticket_price = "获取出错"

        airline_info = {
            INDEX: self.index,
            UPDATE_DATETIME: self.update_time,
            DEPARTURE_PLACE: self.departure_zh + "(" + self.departure_en + ")",
            DESTINATION_PLACE: self.destination_zh + "(" + self.destination_en + ")",
            DEPARTURE_DATE: self.trip_date,
            AIRLINE_COMPANY: airline_company,
            AIRLINE_NAME: airline_name,
            PLANE_TYPE: plane_type,
            DEPARTURE_AIRPORT: departure_airport,
            DEPARTURE_TIME: departure_time,
            DESTIMATION_AIRPORT: destination_airport,
            ARRIVAL_TIME: arrival_time,
            TRANSFER_STATION: transfer_station,
            CROSS_DAYS: cross_days,
            TRAVEL_TIME: travel_time,
            TICKET_PRICE: ticket_price
        }
        return airline_info

    def sort_airline_info_on_price(self):
        self.all_airlines_infos = sorted(
            self.all_airlines_infos, key=lambda x: x[TICKET_PRICE], reverse=False)

    def find_preferred_airlines(self) -> list:
        ret = list()
        prefer_up = self.trip_date + " " + PREFERENCE_TIME_FIELD_UP + "00"
        prefer_down = self.trip_date + " " + PREFERENCE_TIME_FIELD_DOWN + ":00"
        for airline in self.all_airlines_infos:
            if prefer_up <= airline[DEPARTURE_TIME] <= prefer_down:
                ret.append(airline)
        return ret

    @staticmethod
    def calculate_travel_time(trip_date: str, departure: str, arrival: str, cross_days: str) -> tuple:
        departure = trip_date + " " + departure + ":00"
        arrival = trip_date + " " + arrival + ":00"
        cross_days = int(re.search(r"[0-9]+", cross_days).group(0))

        time1 = datetime.datetime.strptime(departure, "%Y-%m-%d %H:%M:%S")
        time2 = datetime.datetime.strptime(arrival, "%Y-%m-%d %H:%M:%S")
        time2 += datetime.timedelta(days=cross_days)

        seconds = (time2 - time1).seconds
        minute = int(seconds / 60)
        hour = int(minute / 60)
        minute %= 60
        day = (time2 - time1).days

        traval_time = "" if day == 0 else str(day) + "天"
        traval_time += "" if hour == 0 else str(hour) + "小时"
        traval_time += "" if minute == 0 else str(minute) + "分钟"
        traval_time = "计算出错" if traval_time == "" else traval_time

        return departure, arrival, traval_time

    def main(self):
        self.get_web_data()
        self.extract_all_airlines()
        self.analyze_each_airline()
        self.sort_airline_info_on_price()
        self.browser.quit()
