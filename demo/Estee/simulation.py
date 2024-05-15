import pandas as pd
from scipy import stats
import random
from datetime import datetime as dt, timedelta
import numpy as np

from typing import Union
def generate_simulation(
    config:dict, 
    sku_ls:list, 
    current_date:str,
    start_date:str,
    history:Union[str, pd.DataFrame], 
    forecast:Union[str, pd.DataFrame], 
    hub_stock:Union[str, pd.DataFrame], 
    week_ls:list,
)->pd.DataFrame:  
    # get data 
    if isinstance(history, str):
        df_history = pd.read_csv(history)
    else:
        df_history = history
    
    if isinstance(forecast, str):
        df_forecast = pd.read_csv(forecast)
    else:
        df_forecast = forecast
        
    if isinstance(hub_stock, str):
        df_hub_stock = pd.read_csv(hub_stock)
    else:
        df_hub_stock = hub_stock
    
    # current hub stock    
    hub_stock = (
        df_hub_stock.query(f"date == '{current_date}'")
        .set_index('sku_name')['hub_stock']
        .to_dict()  
    )

    # calculate allocation and simulate
    df_allocation = pd.DataFrame()

    for sku in sku_ls: 
        channel_plan = config['channel_plan']
        channel_order = sorted(channel_plan, key=lambda x: channel_plan[x]['priority'])
        for channel in channel_order:
            
            current_stock = (
                    df_history
                    .query(f"date == '{current_date}' & sku_name == '{sku}' & channel == '{channel}'")
                    .stock.values[0]
            )
            
            sales_forecast_ls = (
                df_forecast
                .query(f"start_date == '{start_date}' & sku_name == '{sku}' & channel == '{channel}' & week in {week_ls}")
                .sort_values('week')
                .sales_forecast_weekly.to_list()
            )
            
            ttl_sales_forecast = np.sum(sales_forecast_ls)
            
            safety_stock_factor = config['safety_stock_factor'][sku]
            safety_stock = get_safety_stock(sales_forecast_ls , safety_stock_factor)
            
            service_level = config['channel_plan'][channel]['service_level']
            
            allocation_needed = np.ceil(ttl_sales_forecast * service_level) + safety_stock - current_stock
            
            
            allocation = {}
            if allocation_needed < hub_stock[sku]:
                allocation_real = allocation_needed
                hub_stock[sku] -=  allocation_real
                allocation[config['lead_time_hud2channel']] = {'stock_in':allocation_real, 'stock_from':'hub'}
            else:
                allocation_real = hub_stock[sku]
                hub_shortage = allocation_needed - allocation_real
                hub_stock[sku] = 0
                allocation[config['lead_time_hud2channel']] = {'stock_in':allocation_real, 'stock_from':'hub' if allocation_real else ''}
                allocation[config['lead_time_plant2hub']] = {'stock_in':hub_shortage, 'stock_from':'manufacture'} 
            
            df_allocation_ = generate_sales_stock_by_pred_by_week(
                sku, channel, start_date, current_date,timedelta(days=1),4, allocation, sales_forecast_ls, current_stock
            )
            
            df_allocation_['safety_stock'] = safety_stock
            df_allocation_['alert'] = (df_allocation_['stock'] < safety_stock).astype(int)
            
            df_allocation = pd.concat([df_allocation, df_allocation_], axis = 0)
    
    df_allocation['status'] = df_allocation.apply(get_status, axis = 1)
    df_allocation['date'] = pd.to_datetime(df_allocation['date'])

    return df_allocation

def summarize_status(df_allocation):
    df_status = pd.pivot_table(df_allocation, index=['sku_name', 'channel'],columns= 'date' ,values='status', aggfunc=lambda x: ', '.join(x))
    sales_through_breakdown = df_allocation.groupby(['sku_name','channel']).apply(lambda x: x.sales.sum()/(x['stock_in'].sum() + x[x['week']==0].stock) )
    stockout_breakdown = df_allocation.groupby(['sku_name','channel']).apply(lambda x: pd.Series(1 - x.sales.sum()/x.sales_potential_daily.sum(), index = ['stockout']))
    sales_through_breakdown.columns = ['sales_through']
    stockout_breakdown.columns = ['stockout']
    df_status = sales_through_breakdown.join(stockout_breakdown).join(df_status)
    return df_status
    
def ttl_sales_through_rate(df_allocation):
    current_stock = df_allocation.query('week == 0').stock.sum()
    stock_allocating = df_allocation.stock_in.sum()

    sales_simulated = df_allocation.sales.sum()
    sales_forecast =  df_allocation.sales_potential_daily.sum()

    current_stock, stock_allocating, sales_simulated, sales_forecast

    sale_through_rate = sales_simulated/(current_stock + stock_allocating)

    return sale_through_rate


def ttl_sales_shortage_rate(df_allocation):
    return 1 - df_allocation.sales.sum() / df_allocation.sales_potential_daily.sum()



# TS generator 
def daily_ts_generator(start_date: str, period_unit:timedelta, n:int=None, end_date:str = None):
    
    start_date = dt.strptime(start_date, '%Y-%m-%d')
    ts_idx_ls = [start_date]
    
    if n: 
        for i in range(1, n):
            start_date += period_unit
            ts_idx_ls.append(start_date)
    if end_date:
        while start_date<end_date:
            start_date += period_unit
            ts_idx_ls.append(start_date)
    
    return ts_idx_ls

# def generate_forecast(start_date, weeks, sales_dist, sales_dist_arg = {}, ):
#     # weeks_ls = daily_ts_generator('2023-01-15', timedelta(weeks=1), 4)
#     sales_week_ls = stat_generate(weeks, sales_dist, **sales_dist_arg)
    
#     df_forecast = pd.DataFrame() 
    
#     df_forecast['week'] = [i+1 for i in range(weeks)]
#     df_forecast['sales_forecast_weekly'] = sales_week_ls
#     df_forecast['start_date'] = start_date
#     return df_forecast
            
def generate_sales_stock_by_pred_by_week(
    sku_name, 
    channel_name, 
    start_date, 
    current_date,
    period_unit,
    weeks,
    stock_allocation, 
    sales_week_ls,
    current_stock = 0, 
):
    date_ls = daily_ts_generator(start_date, period_unit, 7 * weeks)
    week_ls = [np.ceil((i+1)/7) for i in range(weeks*7)]
    stock_in_ls = [stock_allocation[i]['stock_in'] if i in stock_allocation.keys() else 0 for i in range(weeks * 7 ) ]
    stock_from_ls = [stock_allocation[i]['stock_from'] if i in stock_allocation.keys() else '' for i in range(weeks * 7 ) ]

    sales_daily_ls = [sw/7  for sw in sales_week_ls for _ in range(7)]
    
    sales_week_ls =  [sw  for sw in sales_week_ls for _ in range(7)]
    
    stock_left_ls = []
    sales_acc_ls = [] 
    current_stock_ = current_stock
    for si, sales_acc in zip(stock_in_ls, sales_daily_ls):
        current_stock = current_stock +  si
        actual_sales = sales_acc if current_stock > sales_acc else  current_stock
        current_stock = max(current_stock - sales_acc, 0)
        stock_left_ls.append(current_stock)
        sales_acc_ls.append(actual_sales)
        
    df_generated = pd.DataFrame() 

    df_generated['sku_name'] = [sku_name] * len(date_ls)
    df_generated['channel'] = [channel_name] * len(date_ls)
    df_generated['date'] =  date_ls
    df_generated['week'] =  week_ls
    df_generated['stock_in'] = stock_in_ls
    df_generated['stock_from'] = stock_from_ls
    df_generated['stock'] =  stock_left_ls
    df_generated['sales_potential_weekly'] = sales_week_ls
    df_generated['sales_potential_daily'] = sales_daily_ls
    df_generated['sales'] = sales_acc_ls
    
    df_generated = pd.concat([pd.DataFrame({'sku_name' : [sku_name], 'channel':[channel_name], 'date':[current_date], 'week':[0],'stock_in':[0],'stock_from':[''], 'stock':[current_stock_]}), df_generated],axis=0)
    
    return df_generated

def get_safety_stock(weekly_forecast, factor):
    safety_stock = np.sum(weekly_forecast) / len(weekly_forecast) / 7 * factor   
    return np.ceil(safety_stock)

def get_status(x):
    status = 'full'
    if x['alert'] == 1:
        status = 'risk'
    if x['stock'] < x['safety_stock']/2:
        status = 'near stockout' 
    if x['sales'] < x['sales_potential_daily']:
        status = 'stockout'
    if x['stock_from'] == 'hub':
        status = 'hub' 
    if x['stock_from'] == 'manufacture':
        status = 'manufacture'
    
    return status

def status_select(x):
    if 'stockout' in x:
        return 'stockout'
    if 'risk' in x:
        return 'risk'
    return 'full'