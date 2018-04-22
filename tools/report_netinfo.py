import os
from email.mime.text import MIMEText
import smtplib
from email.header import Header


DEFAULT_SUBJECT = "Raspberry"
DEFAULT_CONTENT = "No NETWORK_INFO"
# TODO(wangzhh): Modify it to config.
from_addr='raspberry_2018@163.com'
to_addrs=['512171845@qq.com']
password=''
smtp_server='smtp.163.com'


def _get_netinfo():
    cmd='ifconfig'
    m=os.popen(cmd)
    t=m.read()
    m.close()
    return t


class SendMail(object):
    def __init__(self, from_addr, to_addrs, smtp_server,
                 smtp_password=None, subject=None, content=None):

        self.to = to_addrs
        self.subject = subject or DEFAULT_SUBJECT 
        self.content = content or DEFAULT_CONTENT

        self.smtp_server = smtp_server
        self.sender = from_addr
        self.password = smtp_password

	self.connection = None
	self.message = None

	self._get_mail_connect()
	self._generate_message()

    def _get_mail_connect(self):
        self.connection = smtplib.SMTP(smtp_server)
        self.connection.ehlo()
        self.connection.starttls()
        self.connection.ehlo()
        self.connection.login(self.sender, self.password)

    def _log_level(self, loglevel):
        self.connection.set_debuglevel(loglevel)

    def _generate_message(self):
        msg=MIMEText(self.content,'plain','utf-8')
        msg['From'] = 'Raspberry'
        msg['To'] = ','.join(self.to)
        msg['Subject'] = Header('Ip Address Report','utf-8').encode()
        self.message = msg

    def sendmail(self):
        self.connection.sendmail(from_addr, self.to, self.message.as_string())
        self.connection.quit()


if __name__ == '__main__':
    # TODO(wangzhh): Add arguement parsing. 
    net_content = _get_netinfo()
    sender = SendMail(from_addr, to_addrs, smtp_server, password, content=net_content) 
    sender.sendmail()
