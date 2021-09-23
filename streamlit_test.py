# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 14:13:07 2021

@author: PeterLiang
"""

import streamlit as st
from helioscope_api import HelioscopeService
import pandas as pd

helio_class = HelioscopeService()

st.title("HelioScope Peak Production Hour")
st.markdown('<style>h1{color:#faa501;}</style>', unsafe_allow_html = True)
st.subheader("Find the max hourly PV production of a design as modeled by HelioScope")
st.markdown('<style>h2{color: red;}</style>', unsafe_allow_html = True)
user_input = st.text_input('Enter Helioscope ID for design of interest')
submit = st.button('Run')
if submit:
    sim_id = int(user_input)
    helio_8760_df = helio_class.get_sim_hourly_df(sim_id)
    max_hr_prod = helio_8760_df['grid_power'].max()
    max_hr = helio_8760_df['grid_power'].idxmax()+1
    max_date = pd.Timestamp('2018-01-01') + pd.to_timedelta(max_hr, unit = 'H')
    max_date_str = '{}/{}/XXXX {}:00'.format(max_date.month, max_date.day, max_date.hour)
    helio_design_id = helio_class.get_simulation(sim_id)['design_id']
    helio_design = helio_class.get_design(helio_design_id)
    proj_name = helio_design['project']['name']
    design_img_url = helio_design['render_url']
    design_name = helio_design['description']
    st.markdown('<span style="font-size: 20px; color: rgb(250,165,1)">{}</span>'.format(proj_name), unsafe_allow_html = True)
    st.markdown('<span style="font-size: 15px; color: rgba(250,165,1, 0.5)">*{}*</span>'.format(design_name), unsafe_allow_html = True)
    st.image(design_img_url)
    st.write('Peak hourly production occurs at hour #{} of the year ({})'.format(max_hr, max_date_str))
    st.write('{} kWh'.format(round(max_hr_prod/1000, 2)))
