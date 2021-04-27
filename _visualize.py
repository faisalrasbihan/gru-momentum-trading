import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as mpatches

def display_confusion_matrix(conf_matrix, reverse_ylabel=False, reverse_xlabel=False):
    labels = ['Negatives','Positives']
    sns.heatmap(conf_matrix, 
                annot=True, 
                cmap="Blues",
                fmt="d",vmin=0, 
                annot_kws={"size": 20}, 
                xticklabels = labels[::-1] if reverse_xlabel else labels, 
                yticklabels= labels[::-1] if reverse_ylabel else labels)
    plt.xlabel('Predicted Values', fontsize = 12) # x-axis label with fontsize 15
    plt.ylabel('Actual Values', fontsize = 12) # y-axis label with fontsize 15
    plt.show()

def plot_returns(df, ma_period, chg_period, threshold_buy, threshold_sell):
    fig, ax = plt.subplots(4, 1, sharex=True, figsize=[16, 12])
    
    # Closing price chart
    sns.lineplot(data=df['Close'], ax=ax[0])
    ax[0].set_ylabel('Closing Price')
    last_closing_price = df['Close'][-1]
    ax[0].axhline(last_closing_price, ls='--',linewidth=1, color='m')
    ax[0].annotate((last_closing_price).round(2),xy=(1,last_closing_price),xycoords=('axes fraction','data'),ha='left',va='center',color='black')
    ax[0].grid(True)
    
    # Moving average chart
    sns.lineplot(data=df['moving_average'], ax=ax[1])
    ax[1].set_ylabel('MA - {}'.format(ma_period))
    buys = df.loc[df.position == 'Buy'] # mark buy transactions
    sells = df.loc[df.position == 'Sell'] # mark sell transactions
    ax[1].plot(buys.index, df['moving_average'].loc[buys.index], '.', markersize=4, color='g', label='buy')
    ax[1].plot(sells.index, df['moving_average'].loc[sells.index], '.', markersize=4, color='r', label='sell')
    ax[1].grid(True)
    
    # Price change chart
    sns.lineplot(data=df['price_change'], ax=ax[2])
    ax[2].set_ylabel('{}D Price Change (%)'.format(chg_period))
    ax[2].axhline(threshold_buy, ls='--',linewidth=1, color='m')
    ax[2].axhline(threshold_sell, ls='--',linewidth=1, color='m')
    ax[2].annotate(threshold_buy,xy=(1,threshold_buy),xycoords=('axes fraction','data'),ha='left',va='center',color='black')
    ax[2].annotate(threshold_sell,xy=(1,threshold_sell),xycoords=('axes fraction','data'),ha='left',va='center',color='black')
    ax[2].grid(True)
    
    # Portfolio value
    sns.lineplot(data=df['value'], ax=ax[3])
    ax[3].set_ylabel('Portfolio Value')
    last_value = df['value'][-1]
    ax[3].axhline(last_value, ls='--',linewidth=1, color='m')
    ax[3].annotate((last_value/10000000).round(2),xy=(1,last_value),xycoords=('axes fraction','data'),ha='left',va='center',color='black')
    ax[3].grid(True)    
    
def tsplot(y, lags=None, figsize=(15, 10), style='bmh'):
    if not isinstance(y, pd.Series):
        y = pd.Series(y)
    with plt.style.context(style):    
        fig = plt.figure(figsize=figsize)
        #mpl.rcParams['font.family'] = 'Ubuntu Mono'
        layout = (3, 2)
        ts_ax = plt.subplot2grid(layout, (0, 0), colspan=2)
        acf_ax = plt.subplot2grid(layout, (1, 0))
        pacf_ax = plt.subplot2grid(layout, (1, 1))
        qq_ax = plt.subplot2grid(layout, (2, 0))
        pp_ax = plt.subplot2grid(layout, (2, 1))
        
        y.plot(ax=ts_ax)
        ts_ax.set_title('Time Series Analysis Plots')
        smt.graphics.plot_acf(y, lags=lags, ax=acf_ax, alpha=0.05)
        smt.graphics.plot_pacf(y, lags=lags, ax=pacf_ax, alpha=0.05)
        sm.qqplot(y, line='s', ax=qq_ax)
        qq_ax.set_title('QQ Plot')        
        scs.probplot(y, sparams=(y.mean(), y.std()), plot=pp_ax)

        plt.tight_layout()
    return

