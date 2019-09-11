import requests as req
import logging
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('..') / '.env'
load_dotenv(env_path)
CONSUMER_KEY= os.getenv("CONSUMER_KEY")
REDIRECT_URI = os.getenv("REDIRECT_URI")


class Pocket:

    def __init__(self):
        self.consumer_key = CONSUMER_KEY
        self.redirect_uri = REDIRECT_URI
        self.code = ""
        self.user_data= ""


    def get_app_request_token(self):

        url = "https://getpocket.com/v3/oauth/request"
        r_ = req.post(url, params= {'consumer_key': self.consumer_key,'redirect_uri': self.redirect_uri}, headers={'Content-Type':'application/json; charset=UTF8', 'X-Accept': 'application/json'})
        try:
            self.code = r_.json()['code']

        except Exception as e:
            logging.exception("Error when getting code : \n {}".format(e))

        return self.code

    def get_user_access_token(self):

        url = "https://getpocket.com/v3/oauth/authorize"
        self.user_data = dict()
        request_token = self.code
        if request_token:
            r = req.post(url,params={'consumer_key': self.consumer_key,'code': request_token}, headers={'Content-Type':'application/json', 'X-Accept': 'application/json'})
            try:
                self.user_data = r.json()
            except Exception as e:
                logging.exception("Error when getting access token: \n {}".format(e))

        return self.user_data

    def get_user_content(self):
        url = "https://getpocket.com/v3/get"
        data = dict()
        consumer_key = self.consumer_key
        if self.user_data:
            access_token = self.user_data['access_token']
            r = req.post(url,params={'consumer_key': consumer_key, 'access_token': access_token}, headers={'Content-Type':'application/json', 'X-Accept': 'application/json'})
            try:
                content_data = [value for key, value in r.json()['list'].items()]
                data = {'username': self.user_data['username'], 'content': content_data}
                

            except Exception as e:
                logging.exception("Error when getting access token: \n {}".format(e))

        return data
