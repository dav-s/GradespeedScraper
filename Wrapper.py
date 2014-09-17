from bs4 import *
import mechanize
from stringcode import decode_string, encode_string


class Wrapper():

    def __init__(self, url):
        self.br = mechanize.Browser()
        self.start_url = url
        self.logged_in = False

        self.br.set_handle_robots(False)
        self.br.open(url)

    def login(self, username, password):
        self.br.select_form("Form1")
        self.br["txtUserName"] = username
        self.br["txtPassword"] = password
        self.br.submit()
        self.logged_in = True

    def get_available_students(self):
        if not self.logged_in:
            raise Exception
        pass