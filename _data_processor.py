import pandas
import numpy as np
import math

def generate_targets(df, ma_period, chg_period, threshold_buy, threshold_sell):
    # Add moving average
    df['moving_average'] = df['Close'].rolling(window=ma_period).mean()
    # Add price change 
    df['price_change'] = (df['moving_average'].shift(-chg_period) - df['moving_average']) / df['moving_average']
    df['price_change'] = df['price_change']  * 100
    # Remove NaN value
    df = df[:-chg_period] # remove NaN value from price changes
    df = df[ma_period:] # remove NaN value from moving averages
    # Add Buy, Sell and Hold Position
    df['position'] = 'Hold'
    df.loc[df['price_change'] >= threshold_buy,'position'] = 'Buy'
    df.loc[df['price_change'] <= threshold_sell,'position'] = 'Sell'
    return df

def generate_returns(df):
    temp = df.copy()
    temp['cash'] = 10000000
    temp['quantity'] = 0
    temp['equity'] = 0
    prev_pos = None
    prev_cash = 10000000
    prev_quantity, prev_equity = (0, 0)
    for i, row in temp.iterrows():
        if (row['position'] == 'Buy') and (prev_pos != 'Buy'):
            prev_pos = row['position']
            quantity = math.floor(prev_cash/row['Close'])
            temp.at[i,'cash'] = prev_cash - quantity*row['Close']
            temp.at[i,'quantity'] += quantity
            temp.at[i,'equity'] = quantity * row['Close']
            prev_cash = temp.at[i,'cash']
            prev_quantity = temp.at[i,'quantity']
            prev_equity = temp.at[i,'equity']
        elif (row['position'] == 'Sell') and (prev_pos == 'Buy'):
            prev_pos = row['position']
            temp.at[i,'cash'] = prev_quantity * row['Close'] + prev_cash
            temp.at[i,'quantity'] = 0
            temp.at[i,'equity'] = 0
            prev_cash = temp.at[i,'cash']
            prev_quantity = temp.at[i,'quantity']
            prev_equity = temp.at[i,'equity']
        else:
            temp.at[i,'cash'] = prev_cash
            temp.at[i,'quantity'] = prev_quantity
            temp.at[i,'equity'] = prev_quantity * row['Close']
    temp['value'] = temp['cash'] + temp['equity']
    return temp

def volume_transformation(data, ma_period, exponential_avg=False, log_scaled=True, offset=0):
    if exponential_avg:
        ma = data.ewm(span=ma_period, adjust=False).mean()
    else:
        ma = data.rolling(window=ma_period).mean()
    if log_scaled:
        ma = np.log(ma)
    return ma

def momentum_transformation(data, target_variables, ma_span=1, normalized=False):
    if normalized:
        return 100*(data[target_variables] - data[target_variables].rolling(window=ma_span).mean())/data[target_variables].rolling(window=ma_span).mean()
    else:
        return (data[target_variables] - data[target_variables].rolling(window=ma_span).mean())
    
def momentum_scaled(data, target_variables, ma_span=1):
    return (data[target_variables] - data[target_variables].rolling(window=ma_span).mean())/data[target_variables]

def timeseries_transformation(data, 
                            ma_span=1, 
                            exponential_avg=False, 
                            log_scaled=False, 
                            offset=0):
    if exponential_avg:
        ma = data.ewm(span=ma_span, adjust=False).mean()
    else:
        ma = data.rolling(window=ma_span).mean()
    if log_scaled:
        ma = np.log(ma)
    return ma + offset
    
def generate_batch(data, input_timesteps, output_timesteps,input_variables, output_variables):
    '''
    Inputs a dataframe with desired sequence length and target name
    Yield a generator of training data from filename on given list of cols split for train/test
    outputs Sequence of data with corresponding target
    '''
    X, y = list(), list()
    target = data[output_variables].values
    data = data[input_variables].values
    # Iterate 
    for i in range(len(data) - (input_timesteps + output_timesteps) + 1):
        end_seq_x = i + input_timesteps
        end_seq_y = end_seq_x + output_timesteps
        # Input sequence starts from i to (i + input_timesteps - 1)
        seq_x = data[i:end_seq_x]
        # Target sequence starts after end of input sequence to end_ix + output_timesteps
        seq_y = target[end_seq_x:end_seq_y]
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)