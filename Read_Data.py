import datetime
import pandas as pd
import numpy as np


def read_data(date=None, use_daily=False):
    data_path = 'COVID-19\\'

    jhu_csse_ts_dir_path = data_path + 'csse_covid_19_data\\csse_covid_19_time_series\\'
    jhu_csse_ts_confirmed_name = 'time_series_covid19_confirmed_global.csv'
    jhu_csse_ts_deaths_name = 'time_series_covid19_deaths_global.csv'
    jhu_csse_ts_recovered_name = 'time_series_covid19_recovered_global.csv'

    jhu_csse_daily_data_dir_path = data_path + 'csse_covid_19_data\\csse_covid_19_daily_reports\\'

    if use_daily:
        file_name = date.strftime('%m-%d-%Y') + '.csv'
        jhu_csse_confirmed_today_data_pd = pd.read_csv(jhu_csse_daily_data_dir_path + file_name)

        pd_columns_list = jhu_csse_confirmed_today_data_pd.columns.values.tolist()
        if 'FIPS' in pd_columns_list:
            del jhu_csse_confirmed_today_data_pd['FIPS']
        if 'Admin2' in pd_columns_list:
            del jhu_csse_confirmed_today_data_pd['Admin2']
        if 'Province_State' in pd_columns_list:
            del jhu_csse_confirmed_today_data_pd['Province_State']
        if 'Province/State' in pd_columns_list:
            del jhu_csse_confirmed_today_data_pd['Province/State']
        if 'Last_Update' in pd_columns_list:
            del jhu_csse_confirmed_today_data_pd['Last_Update']
        if 'Lat' in pd_columns_list:
            del jhu_csse_confirmed_today_data_pd['Lat']
        if 'Long_' in pd_columns_list:
            del jhu_csse_confirmed_today_data_pd['Long_']
        if 'Combined_Key' in pd_columns_list:
            del jhu_csse_confirmed_today_data_pd['Combined_Key']
        country_column = None
        if 'Country/Region' in pd_columns_list:
            country_column = 'Country/Region'
        elif 'Country_Region' in pd_columns_list:
            country_column = 'Country_Region'

        world_data_pd = pd.DataFrame()
        countries = jhu_csse_confirmed_today_data_pd[country_column].drop_duplicates()
        for country in countries:
            data = jhu_csse_confirmed_today_data_pd[(jhu_csse_confirmed_today_data_pd[country_column] == country)]
            confirmed = data['Confirmed'].sum()
            deaths = data['Deaths'].sum()
            recovered = data['Recovered'].sum()
            active = 0
            if 'Active' in pd_columns_list:
                active = data['Active'].sum()
            tmp_data = {
                'Country_Region': country,
                'Confirmed': confirmed,
                'Deaths': deaths,
                'Recovered': recovered,
                'Active': active if 'Active' in pd_columns_list else None,
                'Death Rate': deaths / (confirmed if confirmed is not .0 else .1),
                'Recovered Rate': recovered / (confirmed if confirmed is not .0 else .1),
            }
            world_data_pd = world_data_pd.append([tmp_data], ignore_index=True)

        return world_data_pd
    else:
        jhu_csse_confirmed_ts_data_pd = pd.read_csv(jhu_csse_ts_dir_path + jhu_csse_ts_confirmed_name)
        jhu_csse_deths_ts_data_pd = pd.read_csv(jhu_csse_ts_dir_path + jhu_csse_ts_deaths_name)
        jhu_csse_recovered_ts_data_pd = pd.read_csv(jhu_csse_ts_dir_path + jhu_csse_ts_recovered_name)

        del jhu_csse_confirmed_ts_data_pd['Province/State']
        del jhu_csse_confirmed_ts_data_pd['Lat']
        del jhu_csse_confirmed_ts_data_pd['Long']
        del jhu_csse_deths_ts_data_pd['Province/State']
        del jhu_csse_deths_ts_data_pd['Lat']
        del jhu_csse_deths_ts_data_pd['Long']
        del jhu_csse_recovered_ts_data_pd['Province/State']
        del jhu_csse_recovered_ts_data_pd['Lat']
        del jhu_csse_recovered_ts_data_pd['Long']

        world_confirmed_data_pd = pd.DataFrame(columns=jhu_csse_confirmed_ts_data_pd.columns)
        world_deaths_data_pd = pd.DataFrame(columns=jhu_csse_deths_ts_data_pd.columns)
        world_recovered_data_pd = pd.DataFrame(columns=jhu_csse_recovered_ts_data_pd.columns)

        countries = jhu_csse_confirmed_ts_data_pd['Country/Region'].drop_duplicates()

        for country in countries:
            confirmed_data = jhu_csse_confirmed_ts_data_pd[(jhu_csse_confirmed_ts_data_pd['Country/Region'] == country)]
            deaths_data = jhu_csse_deths_ts_data_pd[(jhu_csse_deths_ts_data_pd['Country/Region'] == country)]
            recovered_data = jhu_csse_recovered_ts_data_pd[(jhu_csse_recovered_ts_data_pd['Country/Region'] == country)]

            tmp_data0 = {'Country/Region': country}
            tmp_data1 = {'Country/Region': country}
            tmp_data2 = {'Country/Region': country}

            confirmed_columns = confirmed_data.columns
            confirmed_columns = [x.strip() for x in confirmed_columns if x.strip() != '']
            for i in range(1, len(confirmed_columns)):
                if confirmed_data.shape[0] == 1:
                    tmp_data0[confirmed_columns[i]] = confirmed_data[confirmed_columns[i]].values.tolist()[0]
                else:
                    tmp_data0[confirmed_columns[i]] = confirmed_data[confirmed_columns[i]].sum()

            deaths_columns = deaths_data.columns
            deaths_columns = [x.strip() for x in deaths_columns if x.strip() != '']
            for i in range(1, len(deaths_columns)):
                if deaths_data.shape[0] == 1:
                    tmp_data1[deaths_columns[i]] = deaths_data[deaths_columns[i]].values.tolist()[0]
                else:
                    tmp_data1[deaths_columns[i]] = deaths_data[deaths_columns[i]].sum()

            recovered_columns = recovered_data.columns
            recovered_columns = [x.strip() for x in recovered_columns if x.strip() != '']
            for i in range(1, len(recovered_columns)):
                if recovered_data.shape[0] == 1:
                    tmp_data2[recovered_columns[i]] = recovered_data[recovered_columns[i]].values.tolist()[0]
                else:
                    tmp_data2[recovered_columns[i]] = recovered_data[recovered_columns[i]].sum()

            world_confirmed_data_pd = world_confirmed_data_pd.append([tmp_data0], ignore_index=True)
            world_deaths_data_pd = world_deaths_data_pd.append([tmp_data1], ignore_index=True)
            world_recovered_data_pd = world_recovered_data_pd.append([tmp_data2], ignore_index=True)

        return world_confirmed_data_pd, world_deaths_data_pd, world_recovered_data_pd


def calc_climb_rate(data):
    columns = data.columns
    columns = [x.strip() for x in columns if x.strip() != '']
    weeks_num = (data.shape[1] - 1) // 7
    tmp = [columns[0]]
    tmp += columns[7: weeks_num * 7: 7]

    world_week_climb_rate_pd = pd.DataFrame(columns=tmp)
    for country_idx, country_data in data.iterrows():
        country_climb_rate_dict = {'Country/Region': country_data['Country/Region']}
        last_week_data = country_data.values.tolist()[1]
        for week_idx in range(weeks_num - 1):
            current_week_data = country_data.values.tolist()[1 + week_idx * 7]
            climb_rate = current_week_data / (last_week_data if last_week_data is not 0 else 1)
            last_week_data = current_week_data
            country_climb_rate_dict[columns[7 + week_idx * 7]] = climb_rate
        world_week_climb_rate_pd = world_week_climb_rate_pd.append(country_climb_rate_dict, ignore_index=True)
    return world_week_climb_rate_pd

