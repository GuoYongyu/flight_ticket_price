import smtplib
from email.mime.text import MIMEText

from configure import *


class SendMails(object):
    TAG = "SendMails ({departure} to {destination} on {trip_date}): "

    def __init__(self, departure: str, destination: str, trip_date: str):
        logger.info(f"建立邮件发送工作对象：于<{trip_date}>从<{departure}>前往<{destination}>"
                    .format(trip_date=trip_date, departure=departure, destination=destination))

        self.departure_zh, self.departure_en = departure.split(ZH_EN_SPLITER)
        self.destination_zh, self.destination_en = destination.split(ZH_EN_SPLITER)
        self.trip_date = trip_date
        self.TAG = self.TAG.format(
            departure=self.departure_zh, destination=self.destination_zh, trip_date=self.trip_date
        )

        self.message = str()

        for port in EMAIL_SERVER_PORT:
            self.smtp = smtplib.SMTP(host=EMAIL_SERVER_ADDR)
            try:
                self.smtp.connect(host=EMAIL_SERVER_ADDR, port=port)
                self.smtp.ehlo()
                self.smtp.starttls()
                self.smtp.login(user=EMAIL_SENDER_USERNAME, password=EMAIL_SENDER_PASSWORD)
                logger.info(self.TAG + "建立邮件发送服成功")
                break
            except Exception as e:
                logger.error(self.TAG + "建立邮件发送服务时出错：" + str(e))
                self.smtp = None

    def send_mail(self, subject: str, message: str):
        if self.smtp is None:
            logger.error(self.TAG + "由于邮件服务建立失败，无法发送邮件！")
            return
        elif message is None:
            logger.error(self.TAG + "邮件内容为空，发送中止！")
            return
        logger.info(self.TAG + "正在发送邮件...")

        self.message = MIMEText(message, "plain", CODE_FORMAT)
        self.message["From"] = EMAIL_SENDER_USERNAME
        self.message["To"] = ",".join(EMAIL_RECEIVERS_USERNAME)

        if subject is TITLE_PRICE_DOWN:
            self.message["Subject"] = TITLE_PRICE_DOWN + \
                                      TRIP_INFORMATION.format(
                                          departure=self.departure_zh+self.departure_en,
                                          destination=self.destination_zh+self.destination_en,
                                          trip_date=self.trip_date
                                      )
        elif subject is TITLE_PRICE_LOWEST:
            self.message["Subject"] = TITLE_PRICE_LOWEST + \
                                      TRIP_INFORMATION.format(
                                          departure=self.departure_zh+self.departure_en,
                                          destination=self.destination_zh+self.destination_en,
                                          trip_date=self.trip_date
                                      )

        try:
            self.smtp.sendmail(EMAIL_SENDER_USERNAME, EMAIL_RECEIVERS_USERNAME, self.message.as_string())
            logger.info(self.TAG + "邮件发送成功！")
        except Exception as e:
            logger.error(self.TAG + "邮件发送失败：" + str(e))
        finally:
            self.smtp.quit()
