# 航班价格获取

## 项目目的

从网页中爬取某一日从某地到其他某地的数据，例如：

<center>20**年**月**日从**地方到达**地方的航班信息</center>

爬取的信息包括：

```json
{
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
```

然后对本次爬取到的数据，选取偏好时间段的数据，例如每日出发时间在10:00至14:00间的航班数据，与数据库中已有的数据做比较并判断发送什么样的通知邮件到预定的邮箱：

- 选取数据库中机票价格最小的前k条数据，与之比较，对比当前数据的价格是否比历史最低价还要低，若是，那么发送<低价通知>到邮箱。
- 选取数据库中前一次更新数据时的所有机票信息，与之比较，对比当前的价格是否比上次的价格低，若是，那么发送<降价通知>到邮箱。

每次保存数据到数据库时，会获得一个index值，用于标识本次数据获取，index的规则如下例：

- 若前次获取时index值为$i$，那么此次获取则为$i+1$。

## 文件说明

- configure.py：配置文件，主要存储了静态常量，包括数据库的表名、列名，固定的数据值等。
- database.py：数据库连接文件，连接本地MySQL数据库，并往数据库中增、删、查数据。
- analyze.py：根据本次获取的机票数据，分析发送什么类型的邮件，<降价通知>和<低价通知>。
- spider.py：爬取网页上的机票数据。
- sendmails.py：发送邮件到目标邮箱，用于通知用户。
- newtask.py：新建线程任务，可以用于在main中创建多个线程爬取多个不同航班。
- main.py：main函数所在文件，新建NewTask对象。
- sql.sql：创建数据库和表的SQL语句。