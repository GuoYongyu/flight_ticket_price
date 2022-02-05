from database import *
from spider import TripSpider


class Analyzer(object):
    TAG = "Analyzer ({departure} to {destination} on {trip_date}): "
    _k = 5

    def __init__(self, departure: str, destination: str, trip_date: str):
        logger.info(f"建立数据分析工作对象：于<{trip_date}>从<{departure}>前往<{destination}>"
                    .format(trip_date=trip_date, departure=departure, destination=destination))

        self.departure_zh, self.departure_en = departure.split(" ")
        self.destination_zh, self.destination_en = destination.split(" ")
        self.trip_date = trip_date
        self.TAG = self.TAG.format(
            departure=self.departure_zh, destination=self.destination_zh, trip_date=self.trip_date)

        self.db_op = DatabaseOperator()
        self.current_index = int()
        self.find_current_index()

        self.first_k_lowest = 5
        self.notification_airlines = set()
        self.email_subject = str()
        self.email_message = str()

    def find_current_index(self):
        sql = "SELECT MAX(`" + INDEX + "`) FROM `" + TABLE_NAME + "`;"
        result = self.db_op.select(sql=sql, log_tag=self.TAG)
        if result is None:
            self.current_index = 1
        else:
            self.current_index = int(result[0]["MAX(`" + INDEX + "`)"]) + 1

    def appear_lowest_price(self, spider: TripSpider):
        logger.info(self.TAG + "正在分析价格是否降至最低水平...")
        sql = "SELECT * " + \
              "FROM `" + TABLE_NAME + "` " + \
              "WHERE `" + DEPARTURE_TIME + "`>=\'" + spider.trip_date + " " + PREFERENCE_TIME_FIELD_UP + "\' " + \
              "AND `" + DEPARTURE_TIME + "`<=\'" + spider.trip_date + " " + PREFERENCE_TIME_FIELD_DOWN + "\' " + \
              "ORDER BY `" + TICKET_PRICE + "` ASC " + \
              "LIMIT " + str(self.first_k_lowest) + " " + \
              "OFFSET 0;"
        results = self.db_op.select(log_tag=self.TAG, sql=sql, fetch_one=False)
        if results is None:
            return True
        for result in results:
            for airline in spider.all_airlines_infos[:self._k]:
                if airline[TICKET_PRICE] < result[TICKET_PRICE]:
                    self.notification_airlines.add(airline)
        return False

    def appear_price_down(self, spider: TripSpider):
        logger.info(self.TAG + "正在分析是否降价...")

        sql = "SELECT * " + \
              "FROM `" + TABLE_NAME + "` " + \
              "WHERE `" + INDEX + "`=(" + \
              "SELECT MAX(`" + INDEX + "`) " + \
              "FROM `" + TABLE_NAME + "`);"
        results = self.db_op.select(log_tag=self.TAG, sql=sql, fetch_one=False)
        if results is None:
            return True
        for result in results:
            for airline in spider.all_airlines_infos[:self._k]:
                if airline[AIRLINE_NAME] == result[AIRLINE_NAME] and airline[TICKET_PRICE] < result[TICKET_PRICE]:
                    self.notification_airlines.add(airline)
        return False

    def organize_email_message(self, title: str):
        if title is TITLE_PRICE_LOWEST:
            message = "当前出现了最低价机票，航班信息为：\n\n"
        elif title is TITLE_PRICE_DOWN:
            message = "当前机票价格发生下降，偏向阶段航班信息为：\n\n"
        else:
            self.email_message = None
            return

        for i, airline in enumerate(self.notification_airlines):
            message += "第" + str(i+1) + "条航班信息：\n"
            message += self.dict_to_str(airline)

        self.email_message = message

    def save_current_airlines(self, spider: TripSpider):
        self.db_op.insert_many(table=TABLE_NAME, log_tag=self.TAG, data_list=spider.all_airlines_infos)

    @staticmethod
    def dict_to_str(info: dict) -> str:
        ret = ""
        for key in info.keys():
            try:
                ret += translator.get(key) + "：" + info.get(key) + "\n"
            except Exception as e:
                logger.error("键值错误：" + str(e))
        return ret + "\n"

    def analyze(self, spider: TripSpider):
        logger.info(self.TAG + "正在分析机票数据...")
        if self.appear_lowest_price(spider=spider):
            self.email_subject = TITLE_PRICE_LOWEST
            self.organize_email_message(TITLE_PRICE_LOWEST)
        elif self.appear_price_down(spider=spider):
            self.email_subject = TITLE_PRICE_DOWN
            self.organize_email_message(TITLE_PRICE_DOWN)
        self.save_current_airlines(spider)
        self.db_op.db.close()
