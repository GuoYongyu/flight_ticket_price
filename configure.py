import logging


# code format
CODE_FORMAT = "UTF-8"
ZH_EN_SPLITER = " "

# log settings
LOG_FORMAT = '%(asctime)s - %(thread)d - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

# url and web settings
data_url = "https://flights.ctrip.com/online/list/oneway-{departure}-{destination}?_=1&depdate={trip_date}"
web_page_waiting = 30  # 30 sec
scan_gap_seconds = 30 * 60  # 30 min

# data to be obtained
INDEX = "index"
UPDATE_DATETIME = "update_datetime"
DEPARTURE_PLACE = "departure_place"
DESTINATION_PLACE = "destination_place"
DEPARTURE_DATE = "departure_date"
AIRLINE_COMPANY = "airline_company"
AIRLINE_NAME = "airline_name"
PLANE_TYPE = "plane_type"
DEPARTURE_TIME = "departure_time"
DEPARTURE_AIRPORT = "departure_airport"
ARRIVAL_TIME = "arrival_time"
DESTIMATION_AIRPORT = "destination_airport"
TRANSFER_STATION = "transfer_station"
CROSS_DAYS = "cross_days"
TRAVEL_TIME = "travel_time"
TICKET_PRICE = "ticket_price"
translator = {
    UPDATE_DATETIME: "数据更新时间",
    DEPARTURE_PLACE: "出发地",
    DESTINATION_PLACE: "目的地",
    DEPARTURE_DATE: "出发日期",
    AIRLINE_COMPANY: "航空公司",
    AIRLINE_NAME: "航班号",
    PLANE_TYPE: "机型",
    DEPARTURE_TIME: "预计起飞时间",
    DEPARTURE_AIRPORT: "起飞机场",
    ARRIVAL_TIME: "预计到达时间",
    DESTIMATION_AIRPORT: "降落机场",
    TRANSFER_STATION: "中转站",
    CROSS_DAYS: "跨越天数",
    TRAVEL_TIME: "预计飞行用时",
    TICKET_PRICE: "机票价格"
}

# database's settings
DATABASE_NAME = "airline_tickets"
DATABASE_HOST = "localhost"
DATABASE_USER = "root"
DATABASE_PASSWORD = "******"
DATABASE_PORT = 3306
DATABASE_CHARSET = "utf8"

# records table's settings
TABLE_NAME = "flight_price_records"

# email settings
EMAIL_SERVER_ADDR = "smtp.***.com"
EMAIL_SERVER_PORT = [0, ]
EMAIL_SENDER_USERNAME = "******@***.com"
EMAIL_SENDER_PASSWORD = "******"
EMAIL_RECEIVERS_USERNAME = ["******@***.com"]
TRIP_INFORMATION = "{trip_date}从{departure}到{destination}"
TITLE_PRICE_DOWN = "<机票降价提醒>"
CONTENT_PRICE_DOWN = "的机票价格相较前期有所下降，具体如下：\n"
TITLE_PRICE_LOWEST = "<低价机票提醒>"
CONTENT_PRICE_LOWEST = "的机票价格已经降至低于目前数据库中已有数据的最低水平，具体如下：\n"

# references
PREFERENCE_TIME_FIELD_UP = "10:00"
PREFERENCE_TIME_FIELD_DOWN = "14:00"
