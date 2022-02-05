import threading

from analyze import *
from spider import *
from sendmails import *


class NewTask(threading.Thread):
    def __init__(self, departure: str, destination: str, trip_date: str):
        super().__init__()
        self.mail_sender = SendMails(
            departure=departure, destination=destination, trip_date=trip_date)

        self.analyzer = Analyzer(
            departure=departure, destination=destination, trip_date=trip_date)

        self.spider = TripSpider(
            departure=departure, destination=destination, trip_date=trip_date, index=self.analyzer.current_index)

    def run(self):
        self.spider.main()
        # self.analyzer.analyze(self.spider)
        # self.mail_sender.send_mail(subject=self.analyzer.email_subject, message=self.analyzer.email_message)
