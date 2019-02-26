import os 
import json
import time
import pprint

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

# for avoiding throttling the email server 
import threading

config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
with open(config_path, 'r') as f:
    CONFIG = json.load(f)

def get_emailer():
    return Emailer()

class Emailer(object):
    def __init__(self, host='gmail'):
        self._host_map = {
            'gmail': ('smtp.gmail.com', 587),
            'ntu': ('mail.ntu.edu.tw', 587)
        }

        self.is_alive = True

        self.server     = None
        self.message    = None

        self._rest_timer = 10
        self._rest_count = 10
        self._count = 0

        self._connect(CONFIG['GOOGLE']['ACCOUNTS']['user'], CONFIG['GOOGLE']['ACCOUNTS']['password'], host)
    
    def _overwatch(self):
        """
        Sounds like a cool name for a monitoring function tbh
        """
        accumulated_time = 0

        while self.is_alive:
            prev_count = self._count
            time.sleep(1)

            if (self._count - prev_count) == 0:
                # idle
                #print('adding acc time')
                accumulated_time += 1
            else:
                #print('resetting acc time')
                # currently sending emails
                accumulated_time = 0
            
            if accumulated_time >= 10:
                #print('Resetting _count...')
                self._count = 0
                accumulated_time = 0

        # Not printed when thread is stopped due to some unknown reason
        # If someone knows the reason behind this behavior, please email b04901118@ntu.edu.tw
        print('Overwatch stopped.')

    def _connect(self, user, pwd, host):
        if isinstance(host, str):
            try:
                host = self._host_map[host]
            except KeyError:
                raise KeyError(f'"{host}" not in host map. Please pass host explictly.')
        elif not isinstance(host, tuple):
            raise TypeError('Unknown host type')
        
        server = smtplib.SMTP(*host)
        server.set_debuglevel(False)

        server.ehlo()
        if server.has_extn('STARTTLS'):
            server.starttls()
            server.ehlo()
        server.login(user, pwd)
        print('Connected to SMTP server\n')

        self.server = server 
        overwatch = threading.Thread(target=self._overwatch, args=())
        overwatch.daemon = True
        overwatch.start()
    
    def set_message(self, mail_path):
        with open(mail_path, 'r') as f:
            msg = f.read()
        
        if self.message is not None:
            print('#'*30)
            print('Overwritting original message: ')
            print(self.message)
            print('\n')
            print('with new message:')
            print(msg)
            print('\n')

            for i in range(5, 0, -1):
                print(f'Countdown {i}')
                time.sleep(1)
        else:
            self.message = msg
            print('Message set to:')
            print(self.message)
            print('\n')
    
    def send(self, sender, receiver, subject=''):
        if self._count < 10:
            self.__not_safe_send(sender, receiver, subject)
        else:
            print('Reached send rate limit. Resting for 10 seconds...')
            time.sleep(10)
            print('Re-sending...')
            self.__not_safe_send(sender, receiver, subject)
        self._count += 1

    def __not_safe_send(self, sender, receiver, subject):
        if not subject:
            raise ValueError('WARNING: sending email without subject line.\nIf sending without subject is intended, set subject parameter to " ".')
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = receiver
        msg.preamble = 'Multipart message\n'
        
        body = MIMEText(self.message)
        msg.attach(body)

        self.server.sendmail(msg['From'], msg['To'], msg.as_string())
        print(f'Sent mail from {sender} to {receiver}')
    
    def set_rest_timer(self, t):
        """
        Warning: Setting this too low may result in being restricted from sending
        emails for a short time period
        """
        self._rest_timer = t
    
    def set_rest_count(self, n):
        """
        Sets the number of emails to be sent before resting
        """
        self._rest_count = n

    def __del__(self):
        if self.server is not None:
            self.server.quit()
            print('Disconnecting from server...')
            self.is_alive = False

            time.sleep(1)
