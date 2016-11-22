#! /usr/bin/python

import kivy
kivy.require('1.9.1') # replace with your current kivy version !

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
import os
import glob

try:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
except:
    from urllib3.exceptions import InsecureRequestWarning
    import urllib3

verify_certs = False

import api
loader_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'loaders', '*Screen.kv')
loader_files = glob.glob(loader_path)
for loader_file in loader_files:
    # print(loader_file)
    Builder.load_file(loader_file)



class LogInScreen(Screen):
    username = ObjectProperty()
    password = ObjectProperty()
    host = ObjectProperty()
    pass


class MonitoringScreen(Screen):
    token = ObjectProperty()
    grid = GridLayout()
    pass


#class SettingsScreen(Screen):
#    pass

class ActiveJobButton(Button):
    jobid = StringProperty('')
    jobname = StringProperty('')
    status = StringProperty('')

class MyApp(App):
    username = ""
    password = ""
    host = ""
    tok = ""
    monitoringscreen = MonitoringScreen(name='MonitoringScreen')
    loginscreen = LogInScreen(name='LogInScreen')

    def build(self):
        # Create the screen manager
        self.sm = ScreenManager()
        #self.loginscreen = LogInScreen(name='LogInScreen')
        self.sm.add_widget(self.loginscreen)
        #self.monitoringscreen = MonitoringScreen(name='MonitoringScreen')
        self.sm.add_widget(self.monitoringscreen)
        return self.sm

    def login(self):
        self.username = self.loginscreen.username.text
        self.password = self.loginscreen.password.text
        self.host = self.loginscreen.host.text
        login_args = collections.namedtuple('login_args',['username','password','host'])
        args = login_args(self.username,self.password,self.host)
        self.tok = api.login(args)
        self.refresh_monitoring()
        self.sm.current = 'MonitoringScreen'
        pass


    def logout(self):
        logout_args = collections.namedtuple('logout_args',['token','username','host'])
        args = logout_args(self.tok,self.username,self.host)
        self.tok = ''
        self.password = ''
        self.sm.current = 'LogInScreen'
        api.logout(args)

    def refresh_monitoring(self):
        login_args = collections.namedtuple('login_args', ['username', 'token', 'host'])
        args = login_args(self.username, self.tok, self.host)
        json = api.list_jobs(args)
        self.monitoringscreen.grid.clear_widgets()
        for job in json:
            print(job['jobId'])
            self.monitoringscreen.grid.add_widget(ActiveJobButton(jobid=job['jobId'], jobname=job['name'],status=job['status'],name=job['jobId']))



if __name__ == '__main__':
    app = MyApp()
    app.run()