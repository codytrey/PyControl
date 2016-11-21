#! /usr/bin/python

import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, NumericProperty, ObjectProperty

import collections
import json
import requests

try:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
except:
    from urllib3.exceptions import InsecureRequestWarning
    import urllib3

verify_certs = False

import api

Builder.load_string("""
<MenuScreen>:
    username: username
    password: password
    host: host
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            Label:
                text: 'User Name'
            TextInput:
                multiline: False
                id: username
                bind: 'text=on_text'
                write_tab: False
        BoxLayout:
            Label:
                text: 'Password'
            TextInput:
                multiline: False
                password: True
                id: password
                bind: 'text=on_text'
                write_tab: False
        BoxLayout:
            Label:
                text: 'Host'
            TextInput:
                multiline: False
                id: host
                bind: 'text=on_text'
                write_tab: False
        Button:
            text: 'Log In'
            on_press: app.login()
        Button:
            text: 'Quit'
            on_press: quit(0)

<SettingsScreen>:
    BoxLayout:
        Button:
            text: 'My settings button'
        Button:
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'
""")


class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='User Name'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text='Password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)
        self.add_widget(Label(text='Host'))
        self.host = TextInput(multiline=False)
        self.add_widget(self.host)
        self.loginbtn = Button(text='Lon In')
        self.loginbtn.bind()
        self.add_widget(Button(text='Log In'))

    def login(self):
        args = collections.namedtuple('Args', ['host', 'username', 'password'])
        args.host = self.host
        args.username = self.username
        args.password = self.password
        CurrUser = api.user(args)
        CurrUser.login()
        if CurrUser.is_loggedin:
            pass
            # open next view
        else:
            pass
            # show login error


class MenuScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass

# Create the screen manager
sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(SettingsScreen(name='settings'))

class MyApp(App):

    def __init__(self):
        super(MyApp, self).__init__()
        self.username = ""
        self.password = ""
        self.host = ""
        self.is_loggedin = False


    def login(self):
        print(MenuScreen.get_host(self))
        self.username = MenuScreen.get_username(self)
        self.password = MenuScreen.get_password(self)
        self.host = MenuScreen.get_host(self)
        self.baseurl = "https://" + self.host + ":8443/automation-api/"
        print(self.baseurl)
        login_args = collections.namedtuple('Login_Args', ['baseurl', 'username', 'password'])
        auth = login_args(self.baseurl, self.username, self.password)
        if self.username != None and self.password != None and self.host != None:
            api.login(auth)
        else:
            # Missing required input
            pass




    def build(self):
        return sm


if __name__ == '__main__':
    app = MyApp()
    app.run()