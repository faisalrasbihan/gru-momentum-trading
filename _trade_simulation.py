import pandas as pd
import numpy as np
import math

def simulate_position(df, buy_thresh, sell_thresh, buy_fee=0, sell_fee=0, closing_price_name='Close', consecutive_buy_thresh = 0, consecutive_sell_thresh = 0):
    temp = df.copy()
    # Mark position
    temp['buy_threshold'] = buy_thresh
    temp['sell_threshold'] = sell_thresh
    temp['position'] = 'Hold'
    temp.loc[temp['pred'] > buy_thresh,'position'] = 'Buy' # Buy action
    temp.loc[temp['pred'] < sell_thresh,'position'] = 'Sell' # Sell action
    # Simulate portfolio value
    temp['cash'] = 10000000
    temp['quantity'] = 0
    temp['equity'] = 0
    temp['trade_no'] = 0
    prev_pos = None
    prev_cash = 10000000
    prev_quantity, prev_equity = (0, 0)
    # Trade Count
    trade_count = 1
    consecutive_buys = 0
    consecutive_sells = 0
    for i, row in temp.iterrows():
        if (row['position'] == 'Buy') and (prev_pos != 'Buy') and (consecutive_buys >= consecutive_buy_thresh):
            temp.loc[i:,'trade_no'] = trade_count
            consecutive_buys = 1
            consecutive_sells = 0
            # Update position
            prev_pos = row['position']
            quantity = math.floor(prev_cash/row[closing_price_name])
            fee = quantity * row[closing_price_name] * buy_fee
            temp.at[i,'cash'] = prev_cash - (quantity*row[closing_price_name]) - fee
            temp.at[i,'quantity'] += quantity
            temp.at[i,'equity'] = quantity * row[closing_price_name]
            prev_cash = temp.at[i,'cash']
            prev_quantity = temp.at[i,'quantity']
            prev_equity = temp.at[i,'equity']
        elif (row['position'] == 'Sell') and (prev_pos == 'Buy') and (consecutive_sells >= consecutive_sell_thresh):
            temp.loc[i:,'trade_no'] = trade_count
            trade_count = trade_count + 1
            consecutive_sells = 1
            consecutive_buys = 0
            # Update position
            prev_pos = row['position']
            fee = prev_quantity * row[closing_price_name] * sell_fee
            temp.at[i,'cash'] = prev_quantity * row[closing_price_name] + prev_cash - fee
            temp.at[i,'quantity'] = 0
            temp.at[i,'equity'] = 0
            prev_cash = temp.at[i,'cash']
            prev_quantity = temp.at[i,'quantity']
            prev_equity = temp.at[i,'equity']
        elif (row['position'] == 'Buy') and (prev_pos == 'Buy'):
            consecutive_sells = 0
            consecutive_buys = consecutive_buys + 1
            # Update position
            temp.at[i,'cash'] = prev_cash
            temp.at[i,'quantity'] = prev_quantity
            temp.at[i,'equity'] = prev_quantity * row[closing_price_name]
        elif (row['position'] == 'Sell') and (prev_pos == 'Sell'):
            consecutive_buys = 0
            consecutive_sells = consecutive_sells + 1
            # Update position
            temp.at[i,'cash'] = prev_cash
            temp.at[i,'quantity'] = prev_quantity
            temp.at[i,'equity'] = prev_quantity * row[closing_price_name]
        else:
            consecutive_buys = 0
            consecutive_sells = 0
            # Update position
            temp.at[i,'cash'] = prev_cash
            temp.at[i,'quantity'] = prev_quantity
            temp.at[i,'equity'] = prev_quantity * row[closing_price_name]
    temp['value'] = temp['cash'] + temp['equity']
    return temp

def simulate_categorical_position(df, closing_price_name='Close', consecutive_buy_thresh = 0, consecutive_sell_thresh = 0):
    temp = df.copy()
    # Mark position
#     temp['position'] = 'Hold'
#     temp.loc[temp['pred'] == 2,'position'] = 'Buy' # Buy action
#     temp.loc[temp['pred'] == 0,'position'] = 'Sell' # Sell action
    # Simulate portfolio value
    temp['cash'] = 10000000
    temp['quantity'] = 0
    temp['equity'] = 0
    temp['trade_no'] = 0
    prev_pos = None
    prev_cash = 10000000
    prev_quantity, prev_equity = (0, 0)
    # Trade Count
    trade_count = 1
    consecutive_buys = 0
    consecutive_sells = 0
    for i, row in temp.iterrows():
        if (row['position'] == 'Buy') and (prev_pos != 'Buy') and (consecutive_buys >= consecutive_buy_thresh):
            temp.loc[i:,'trade_no'] = trade_count
            consecutive_buys = 1
            consecutive_sells = 0
            # Update position
            prev_pos = row['position']
            quantity = math.floor(prev_cash/row[closing_price_name])
            temp.at[i,'cash'] = prev_cash - quantity*row[closing_price_name]
            temp.at[i,'quantity'] += quantity
            temp.at[i,'equity'] = quantity * row[closing_price_name]
            prev_cash = temp.at[i,'cash']
            prev_quantity = temp.at[i,'quantity']
            prev_equity = temp.at[i,'equity']
        elif (row['position'] == 'Sell') and (prev_pos == 'Buy') and (consecutive_sells >= consecutive_sell_thresh):
            temp.loc[i:,'trade_no'] = trade_count
            trade_count = trade_count + 1
            consecutive_sells = 1
            consecutive_buys = 0
            # Update position
            prev_pos = row['position']
            temp.at[i,'cash'] = prev_quantity * row[closing_price_name] + prev_cash
            temp.at[i,'quantity'] = 0
            temp.at[i,'equity'] = 0
            prev_cash = temp.at[i,'cash']
            prev_quantity = temp.at[i,'quantity']
            prev_equity = temp.at[i,'equity']
        elif (row['position'] == 'Buy') and (prev_pos == 'Buy'):
            consecutive_sells = 0
            consecutive_buys = consecutive_buys + 1
            # Update position
            temp.at[i,'cash'] = prev_cash
            temp.at[i,'quantity'] = prev_quantity
            temp.at[i,'equity'] = prev_quantity * row[closing_price_name]
        elif (row['position'] == 'Sell') and (prev_pos == 'Sell'):
            consecutive_buys = 0
            consecutive_sells = consecutive_sells + 1
            # Update position
            temp.at[i,'cash'] = prev_cash
            temp.at[i,'quantity'] = prev_quantity
            temp.at[i,'equity'] = prev_quantity * row[closing_price_name]
        else:
            consecutive_buys = 0
            consecutive_sells = 0
            # Update position
            temp.at[i,'cash'] = prev_cash
            temp.at[i,'quantity'] = prev_quantity
            temp.at[i,'equity'] = prev_quantity * row[closing_price_name]
    temp['value'] = temp['cash'] + temp['equity']
    return temp

def trade_summary(df):
    return {
        'start_date': df.index.min(),
        'end_date': df.index.max(),
        'days_count': len(df),
        'buy_threshold': df['buy_threshold'][0],
        'sell_threshold': df['sell_threshold'][0],
        'buy_and_hold_return': df.Close[-1]/df.Close[0],
        'simulated_return': df['value'].iloc[-1]/(10**7),
        'excess_return': df['value'].iloc[-1]/(10**7) - df.Close[-1]/df.Close[0],
        'maximum_drawdown': df['value'].min()/(10**7),
        'trade_pairs': df.trade_no[-1],
        'profits_per_trade': (df['value'].iloc[-1]/(10**7)) / df.trade_no[-1]
    }