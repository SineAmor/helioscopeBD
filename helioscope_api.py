# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 14:39:31 2021

@author: PeterLiang
"""

import requests
import pandas as pd
import urllib
import zipfile
import io
import itertools
import numpy as np
import pprint

class HelioscopeService:
    def __init__(self):
        self.access_token = "oDBWXKNG0RB3e5XrRKDwhd5cKsDS0Z9Wtj3iWvvohO2v906A"
        self.base_url = "https://www.helioscope.com/api/"
    
    def get_projects(self):
        url = self.base_url + 'projects'
        params = {
            'access_token':self.access_token
            }
        r = requests.get(url, params)
        return (r.json())
    
    def get_design(self, design_id):
        #Design ID is embedded within the simulation
        url = self.base_url + 'designs/{}'.format(design_id)
        params = {
            'access_token':self.access_token
            }
        r = requests.get(url, params)
        return (r.json())
    
    def get_simulation(self, simulation_id):
        #Retrieve the simulation id from the simulated report; number at end of url (Ex: https://www.helioscope.com/projects/1969660/reports/xxxxxxx)
        url = self.base_url + 'simulations/{}'.format(simulation_id)
        params = {
            'access_token':self.access_token
            }
        r = requests.get(url, params)
        return (r.json())
    
    def get_sim_hourly(self, simulation_id):
        params = {
            'access_token':self.access_token}
        url = self.base_url + 'simulations/{}/hourly?'.format(simulation_id)
        #API provides zip file with hourly data for particular simulation ID
        r = requests.get(url, params)
        zf = zipfile.ZipFile(io.BytesIO(r.content))
        #File format structure of the CSV typically inside the zip
        df = pd.read_csv(zf.open("simulation_{}_hourly_data.csv".format(simulation_id)))
        return(df.to_json(orient = 'records'))
    
    def get_sim_hourly_df(self, simulation_id):
        params = {
            'access_token':self.access_token}
        url = self.base_url + 'simulations/{}/hourly?'.format(simulation_id)
        #API provides zip file with hourly data for particular simulation ID
        r = requests.get(url, params)
        zf = zipfile.ZipFile(io.BytesIO(r.content))
        #File format structure of the CSV typically inside the zip
        df = pd.read_csv(zf.open("simulation_{}_hourly_data.csv".format(simulation_id)))
        return(df)
