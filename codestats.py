import sublime
import sublime_plugin
import threading
import urllib.request
import urllib.parse
import os
import re


class CodestatsEvent(sublime_plugin.EventListener):

    count = 0

    def on_modified(self, view):
        self.count += 1
        if self.count > 10:
            thread = CodestatsApiCall(self.count)
            thread.start()
            self.count = 0

class CodestatsApiCall(threading.Thread):
    def __init__(self, count):
        self.count = count
        threading.Thread.__init__(self)

    def run(self):
        path = os.path.dirname(__file__)
        path = re.sub("codestats.py", '', path)
        path = path + "/username.txt"
        try:
            f = open(path)
            line = f.readlines()
            username = re.sub("^\s+|\n|\r|\s+$", '', line[0])
            password = re.sub("^\s+|\n|\r|\s+$", '', line[1])
        except:
            sublime.error_message('Codestats: username file error.')
        try:
            data = urllib.parse.urlencode({'count': self.count, 'password': password}).encode()
            request = urllib.request.Request('http://codestats.pythonanywhere.com/' + username + '/api_call/', data=data)
            resp = urllib.request.urlopen(request)
        except:
            #sublime.error_message('Codestats: connection error.')
            pass
