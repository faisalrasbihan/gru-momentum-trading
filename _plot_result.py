test_date = df_test[input_timesteps+output_timesteps:].index
res = pd.DataFrame(test_date)
res['pred'] = test_pred
res = res.set_index(['Date'])

res['position'] = 'Hold'
res.loc[res['pred'] > 0.9,'position'] = 'Buy'
res.loc[res['pred'] < -0.8,'position'] = 'Sell'

res = df_test.merge(res, how='inner', left_index=True, right_index=True).copy()

test_returns = dp.generate_returns(res)

def plot_returns(df):
    fig, ax = plt.subplots(3, 1, sharex=True, figsize=[16, 12])

    # Closing price chart
    sns.lineplot(data=df['Close'], ax=ax[0])
    ax[0].set_ylabel('Closing Price')
    last_closing_price = df['Close'][-1]
    first_closing_price = df['Close'][0]
    ax[0].axhline(last_closing_price, ls='--',linewidth=1, color='m')
    ax[0].axhline(first_closing_price, ls='--',linewidth=1, color='m')
    buys = df.loc[df.position == 'Buy'] # mark buy transactions
    sells = df.loc[df.position == 'Sell'] # mark sell transactions
    ax[0].plot(buys.index, df['Close'].loc[buys.index], '.', markersize=8, color='g', label='buy')
    ax[0].plot(sells.index, df['Close'].loc[sells.index], '.', markersize=8, color='r', label='sell')
    ax[0].annotate((last_closing_price).round(2),xy=(1,last_closing_price),xycoords=('axes fraction','data'),ha='left',va='center',color='black')
    ax[0].annotate((first_closing_price).round(2),xy=(1,first_closing_price),xycoords=('axes fraction','data'),ha='left',va='center',color='black')
    ax[0].grid(True)

    # Price change chart
    sns.lineplot(data=df[['price_change','pred']], ax=ax[1])
    ax[1].set_ylabel('{}D Price Change (%)'.format(3))
    ax[1].grid(True)

    # Portfolio value
    sns.lineplot(data=df['value'], ax=ax[2])
    ax[2].set_ylabel('Portfolio Value')
    last_value = df['value'][-1]
    ax[2].axhline(last_value, ls='--',linewidth=1, color='m')
    ax[2].annotate((last_value/10000000).round(2),xy=(1,last_value),xycoords=('axes fraction','data'),ha='left',va='center',color='black')
    ax[2].grid(True)

plot_returns(test_returns)

test_returns.groupby(['position']).mean()

    test_returns.groupby(['position']).mean()[['Close','Open','High','Low']]