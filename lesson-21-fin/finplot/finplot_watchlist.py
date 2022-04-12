"""
adapted from https://github.com/highfestiva/finplot/blob/master/finplot/example-snp500.py
"""
import datetime
from time import time
from io import StringIO
import os
import signal
import sys
import numpy as np
import re
# https://stackoverflow.com/questions/56820110/how-can-i-sanitize-a-string-so-that-it-only-contains-only-printable-ascii-chars

from importlib import reload


# from sqlalchemy import create_engine

import psycopg2
from psycopg2 import Error

import pandas as pd
import requests

import yfinance as yf
from yahoofinancials import YahooFinancials
import finplot
from importlib import reload
# https://stackoverflow.com/questions/437589/how-do-i-unload-reload-a-python-module
# workaround issue
# Segmentation fault      (core dumped) python3 $MOM101_HOME/finplot-watchlist.py $*

import db_params
import api_token as gwg

global fa_results


def sanitize(s):
    """Sanitize a string to contain ASCII only"""
    s = s.replace("\t", "    ").replace("'", "")
    return re.sub(r"[^ -~]", "", s)



NUM_OF_DAYS = 400
NUM_OF_MONTHS = 12

MA_FAST = 10
MA_SLOW = 50
MA_LONG = 150
# MACD_FACTOR = 0.2
# TREND_FACTOR = 0.2

RSI_PERIOD = 25

# river/stream band scale-factors
EMA15_SCALE = 1.2
EMA50_SCALE = 5.8


db_kwargs = db_params.get_db_params(
        db_name="gwgdb", 
        db_type="postgresql"
    )

connection = psycopg2.connect(**db_kwargs)


TABLE_NAME = "ticker"

today_str = datetime.datetime.now().strftime('%Y-%m-%d')

color_names = "blue       orange     green      red        purple     brown        pink     black      yellow    light-blue"
colors = [c.strip() for c in color_names.split(" ") if c.strip()]
COLOR_IDX = {}
for i,c in enumerate(colors):
    COLOR_IDX[c] = i


def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Quit...".format(signal))
    exit(0)

signal.signal(signal.SIGINT, keyboardInterruptHandler)
#######################################################

## update crosshair and legend when moving the mouse ##
def update_legend_text(x, y):
    global df
    global symbol
    row = df.loc[df.Date==x]
    # format html with the candle and set legend
    # fmt = '<span style="color:#%s">%%.2f</span>' % ('0bb' if (row.Open<row.Close).all() else 'a00')
    hover_label.setText('%s (%d mon) <br> O:%.2f<br> C:%.2f <br> H:%.2f <br> L:%.2f' % (symbol, NUM_OF_MONTHS, row.Open, row.Close, row.High, row.Low))
    # rawtxt = '<span style="font-size:10px">%%s %%s</span> &nbsp; O:%s<br> C:%s <br> H:%s <br> L:%s' % (fmt, fmt, fmt, fmt)
    # hover_label.setText(rawtxt % (symbol, interval.upper(), row.Open, row.Close, row.High, row.Low))

def update_crosshair_text(x, y, xtext, ytext):
    global df
    ytext = '%s (Close%+.2f)' % (ytext, (y - df.iloc[x].Close))
    return xtext, ytext

def save():
    global file_png
    # # print(__file__)
    # pardir = os.path.dirname(__file__)
    # chart_dir = os.path.join(pardir, "charts", today_str)
    # if not os.path.exists(chart_dir):
    #     os.mkdir(chart_dir)
    # file_png = os.path.join(chart_dir, f"{symbol}_{today_str}.png")
    # print(file_png)
    with open(file_png, 'wb') as f:
        finplot.screenshot(f)



def get_sector_profiles(symbols, connection):
    """
        Get sector,profile info from yfinance for missing symbol in local DB, 
        Add missing info to DB
        Query DB for all symbols, sort by sector,industry
    """

    cursor = connection.cursor()
    symbols_str = gwg.quote_tickers(symbols)
    
    select_sql = f"""select 
        symbol --,sector,industry,website,num_emp,profile 
        from ticker
        where symbol in {symbols_str}
        --order by sector,industry
        ;
    """
    cursor.execute(select_sql)
    query_results = cursor.fetchall()
    symbols_db = [i[0] for i in query_results]
    symbols_new = list(set(symbols).difference(set(symbols_db)))
    print(f"symbols_new = {symbols_new}")

    for symbol in symbols_new:
        sector = industry = website = profile = num_emp = prof_data = None
        try:
            # prof_data = YahooFinancials(symbol).get_stock_profile_data()[symbol]
            prof_data = yf.Ticker(symbol).info
        except Exception as ex:
            print(str(ex))

        if prof_data:
            sector,industry,website, profile, num_emp = \
                prof_data.get("sector", "N/A"), \
                prof_data.get("industry", "N/A"), \
                prof_data.get("website", "N/A"), \
                prof_data.get("longBusinessSummary", "N/A"),\
                prof_data.get("fullTimeEmployees", 0)

            print(f"sector={sector}")
            if profile or sector:
                try:
                    profile=sanitize(profile)
                    insert_query = f""" 
                        INSERT INTO ticker (symbol,sector,industry,website,num_emp,profile) 
                        VALUES ('{symbol}', '{sector}', '{industry}','{website}', {num_emp}, '{profile}')
                        ;
                    """    
                    cursor.execute(insert_query)
                    connection.commit()
                except Exception as ex:
                    print(str(ex))

    select_sql2 = f"""select 
        symbol,sector,industry,website,num_emp,profile 
        from ticker
        where symbol in {symbols_str}
        order by sector,industry,symbol
        ;
    """
    cursor.execute(select_sql2)
    query_results = cursor.fetchall()

    return query_results

def plt_chart(fa_info, save_chart=False, interactive=False):
    global df
    global symbol
    global file_png
    # load data and convert date

    file_png = ""
    symbol,sector,industry,website,num_emp,profile = fa_info

    return_result = (None, None)
    # end_t = int(time()) 
    # start_t = end_t - NUM_OF_MONTHS*30*24*60*60 # twelve months
    # interval = '1d'
    # url = 'https://query1.finance.yahoo.com/v7/finance/download/%s?period1=%s&period2=%s&interval=%s&events=history' % (symbol, start_t, end_t, interval)
    ## WARN: above url not working 2021-11-14

    try:
        # r = requests.get(url)
        # df = pd.read_csv(StringIO(r.text))
        yticker = yf.Ticker(symbol)
        df = yticker.history(f"{NUM_OF_DAYS}d")
        df.reset_index(inplace=True)    # change index=Date to regular column
        if df.empty:
            print(f"[Warn] symbol {symbol} has no data")
            return return_result

        if df.shape[0] < MA_SLOW:
            print(f"[Warn] symbol {symbol} has fewer than {MA_SLOW} data points")
            return return_result

    except Exception as ex:
        print(f"[Error] failed to download quote from Yahoo finance for {symbol}")
        return return_result

    last_row = df.tail(1)
    last_date = str(last_row['Date'].values[0]).split("T")[0]
    last_close = last_row['Close'].values[0]
    last_high = last_row['High'].values[0]
    last_low = last_row['Low'].values[0]

    df['Date'] = pd.to_datetime(df['Date']).astype('int64') # use finplot's internal representation, which is ns

    log_msg = ""
    if sector:
        title = f"[{symbol}]       {website} - {sector} - {industry}           {last_date}"
        log_msg += title + "\n" + sanitize(profile) 
    else:
        title = f"[{symbol}]           {last_date}"
        log_msg += title
    log_msg += "\n======================================================="

    # Plot Candlesticks, RSI, OBV
    ax,ax_rsi,ax_obv = finplot.create_plot(title, rows=3)

    # Candlestick
    finplot.candlestick_ochl(df[['Date','Open','Close','High','Low']], ax=ax)
    wp = (last_low + last_high + 2*last_close)*0.25
    label = f"{symbol}<br>{last_date}<br>C:{last_close:.2f}<br>W:{wp:.2f}"
    hover_label = finplot.add_legend(label, ax=ax)

    ema15=df.Close.ewm(span=MA_FAST).mean()
    ema50=df.Close.ewm(span=MA_SLOW).mean()
    ema150=df.Close.ewm(span=MA_LONG).mean()

    # calculate range
    h_l_mean5 = (df.High - df.Low).rolling(5).mean()
    h_l_mean25 = (df.High - df.Low).rolling(25).mean()
    ema15_h =  ema15 + 0.5*h_l_mean5 * EMA15_SCALE
    ema15_l =  ema15 - 0.5*h_l_mean5 * EMA15_SCALE
    ema50_h =  ema50 + 0.5*h_l_mean25 * EMA50_SCALE
    ema50_l =  ema50 - 0.5*h_l_mean25 * EMA50_SCALE
    

    # plot stream
    # finplot.plot(w_p, color=COLOR_IDX["blue"], width=1, ax=ax)
    finplot.plot(ema15, color=COLOR_IDX["black"], width=1, ax=ax)
    finplot.plot(ema15_h, color=COLOR_IDX["black"], width=2, ax=ax)
    finplot.plot(ema15_l, color=COLOR_IDX["black"], width=2, ax=ax)

    # plot river
    finplot.plot(ema50, color=COLOR_IDX["green"], width=2, ax=ax)
    finplot.plot(ema50_h, color=COLOR_IDX["green"], width=1, ax=ax)
    finplot.plot(ema50_l, color=COLOR_IDX["green"], width=1, ax=ax)

    # plot big-trend
    finplot.plot(ema150,color=COLOR_IDX["red"], width=2, ax=ax)



    # Macd
    # macd = (ema5-ema50)
    # signal = macd.ewm(span=5).mean()
    # trend = (ema5-ema150)
    # df['trend_signal'] = 2*(trend - signal)

    # finplot.volume_ocv(df[['Date','Open','Close','trend_signal']], colorfunc=finplot.strength_colorfilter, ax=ax_macd)
    # finplot.plot(signal, width=2, color=COLOR_IDX["blue"], ax=ax_macd)
    # finplot.plot(trend, width=2, color=COLOR_IDX["green"], ax=ax_macd)
    # finplot.add_legend("Macd", ax=ax_macd)

    # OBV
    v = df.Volume.copy()
    v[df.Close < df.Close.shift()] = -v
    v[df.Close==df.Close.shift()] = 0
    obv = v.cumsum()
    obv_avg = obv.ewm(span=15).mean()
    finplot.plot(obv, width=2, color=COLOR_IDX["black"], ax=ax_obv)
    finplot.plot(obv_avg, width=1, color=COLOR_IDX["red"], ax=ax_obv)
    finplot.add_band(-0.05, 0.05, ax=ax_obv)
    finplot.add_legend("OBV", ax=ax_obv)

    # OBV histogram
    # df['obv_dif'] = obv - obv_avg
    # finplot.volume_ocv(df[['Date','Open','Close','obv_dif']], colorfunc=finplot.strength_colorfilter, ax=ax_obv_dif)
    # finplot.add_legend("ObvDif", ax=ax_obv_dif)

    # RSI 
    diff = df.Close.diff().values
    gains = diff
    losses = -diff
    with np.errstate(invalid='ignore'):
        gains[(gains<0)|np.isnan(gains)] = 0.0
        losses[(losses<=0)|np.isnan(losses)] = 1e-10 # we don't want divide by zero/NaN
    n = RSI_PERIOD
    m = (n-1) / n
    ni = 1 / n
    g = gains[n] = np.nanmean(gains[:n])
    l = losses[n] = np.nanmean(losses[:n])
    gains[:n] = losses[:n] = np.nan
    for i,v in enumerate(gains[n:],n):
        g = gains[i] = ni*v + m*g
    for i,v in enumerate(losses[n:],n):
        l = losses[i] = ni*v + m*l
    rs = gains / losses
    rsi = 100 - (100/(1+rs))
    finplot.plot(rsi, width=2, color=COLOR_IDX["black"], ax=ax_rsi)
    finplot.add_legend("RSI", ax=ax_rsi)
    finplot.set_y_range(20, 80, ax=ax_rsi)
    finplot.add_band(49, 51, ax=ax_rsi)
    finplot.add_band(65, 70, ax=ax_rsi)
    finplot.add_band(30, 35, ax=ax_rsi)


    # if interactive:
    #     finplot.set_time_inspector(update_legend_text, ax=ax, when='hover')
    #     finplot.add_crosshair_info(update_crosshair_text, ax=ax)

    if save_chart:

        # print(__file__)
        pardir = os.path.dirname(__file__)
        chart_dir = os.path.join(pardir, "charts", today_str)
        if not os.path.exists(chart_dir):
            os.makedirs(chart_dir)
        file_png = os.path.join(chart_dir, f"{symbol}_{today_str}.png")
        # print(file_png)

        finplot.timer_callback(save, 0.5, single_shot=True) # wait some until we're rendered

    # print(chart_info)
    return file_png, log_msg

def plt_chart_obv_roc(fa_info, save_chart=False, interactive=False):
    global df
    global symbol
    global file_png
    # load data and convert date

    file_png = ""
    symbol,sector,industry,website,num_emp,profile = fa_info

    return_result = (None, None)
    end_t = int(time()) 
    start_t = end_t - NUM_OF_MONTHS*30*24*60*60 # twelve months
    interval = '1d'
    url = 'https://query1.finance.yahoo.com/v7/finance/download/%s?period1=%s&period2=%s&interval=%s&events=history' % (symbol, start_t, end_t, interval)

    try:
        r = requests.get(url)
        df = pd.read_csv(StringIO(r.text))
        if df.empty:
            print(f"[Warn] symbol {symbol} has no data")
            return return_result

        if df.shape[0] < MA_SLOW:
            print(f"[Warn] symbol {symbol} has fewer than {MA_SLOW} data points")
            return return_result

    except Exception as ex:
        print(f"[Error] failed to download quote from Yahoo finance for {symbol}")
        return return_result

    last_date = str(df.tail(1)['Date'].values[0]).split("T")[0]

    df['Date'] = pd.to_datetime(df['Date']).astype('int64') # use finplot's internal representation, which is ns

    log_msg = ""
    if sector:
        title = f"[{symbol}]       {website} - {sector} - {industry}           {last_date}"
        log_msg += title + "\n" + sanitize(profile) 
    else:
        title = f"[{symbol}]           {last_date}"
        log_msg += title
    log_msg += "\n======================================================="

    ax,\
        ax_obv,\
        ax_obv_dif,\
        ax_roc1,\
        ax_roc2 = finplot.create_plot(title, rows=5)

    # Candlestick
    finplot.candlestick_ochl(df[['Date','Open','Close','High','Low']], ax=ax)
    hover_label = finplot.add_legend(symbol, ax=ax)
    ema5=df.Close.ewm(span=5).mean()
    ema15=df.Close.ewm(span=MA_FAST).mean()
    ema50=df.Close.ewm(span=MA_SLOW).mean()
    ema150=df.Close.ewm(span=MA_LONG).mean()
    finplot.plot(ema15, color=COLOR_IDX["blue"], width=2, ax=ax)
    finplot.plot(ema50, color=COLOR_IDX["green"], width=2, ax=ax)
    finplot.plot(ema150,color=COLOR_IDX["red"], width=2, ax=ax)

    # Macd
    macd = (ema5-ema50)
    signal = macd.ewm(span=5).mean()
    trend = (ema5-ema150)
    df['trend_signal'] = 2*(trend - signal)

    # finplot.volume_ocv(df[['Date','Open','Close','trend_signal']], colorfunc=finplot.strength_colorfilter, ax=ax_macd)
    # finplot.plot(signal, width=2, color=COLOR_IDX["blue"], ax=ax_macd)
    # finplot.plot(trend, width=2, color=COLOR_IDX["green"], ax=ax_macd)
    # finplot.add_legend("Macd", ax=ax_macd)

    # OBV
    v = df.Volume.copy()
    v[df.Close < df.Close.shift()] = -v
    v[df.Close==df.Close.shift()] = 0
    obv = v.cumsum()
    obv_avg = obv.ewm(span=15).mean()
    finplot.plot(obv, width=2, color=COLOR_IDX["black"], ax=ax_obv)
    finplot.plot(obv_avg, width=2, color=COLOR_IDX["red"], ax=ax_obv)
    finplot.add_band(-0.05, 0.05, ax=ax_obv)
    finplot.add_legend("Obv", ax=ax_obv)

    # OBV histogram
    df['obv_dif'] = obv - obv_avg
    finplot.volume_ocv(df[['Date','Open','Close','obv_dif']], colorfunc=finplot.strength_colorfilter, ax=ax_obv_dif)
    finplot.add_legend("ObvDif", ax=ax_obv_dif)

    # EMA50 ROC
    df['ema50_roc'] = ema50 - ema50.shift() 
    finplot.volume_ocv(df[['Date','Open','Close','ema50_roc']], colorfunc=finplot.strength_colorfilter, ax=ax_roc1)
    finplot.add_legend("Roc50", ax=ax_roc1)

    # EMA150 ROC
    df['ema150_roc'] = ema150 - ema150.shift() 
    finplot.volume_ocv(df[['Date','Open','Close','ema150_roc']], colorfunc=finplot.strength_colorfilter, ax=ax_roc2)
    finplot.add_legend("Roc150", ax=ax_roc2)

    # if interactive:
    #     finplot.set_time_inspector(update_legend_text, ax=ax, when='hover')
    #     finplot.add_crosshair_info(update_crosshair_text, ax=ax)

    if save_chart:

        # print(__file__)
        pardir = os.path.dirname(__file__)
        chart_dir = os.path.join(pardir, "charts", today_str)
        if not os.path.exists(chart_dir):
            os.mkdir(chart_dir)
        file_png = os.path.join(chart_dir, f"{symbol}_{today_str}.png")
        # print(file_png)

        finplot.timer_callback(save, 0.5, single_shot=True) # wait some until we're rendered

    # print(chart_info)
    return file_png, log_msg


def generate_html(file_csv, file_png, i):  
    """generate a html file in $MOM101_HOME/research folder

    Args:
        file_csv - watchlist filename
        file_png - 

    Return:
        None    
    """
    global fa_results
    global df_symbol, fa_dict


    if i:
        html_mode = "a"
    else:
        html_mode = "w"
    root_dir = os.environ['MOM101_HOME']
    file_png_path = f"file://{root_dir}/{file_png}"

    filename, _ = os.path.splitext(os.path.basename(file_csv))
    file_html = os.path.join(root_dir, "research", f"{filename}.html")
    with open(file_html, html_mode) as f:
        # create a summary table at the top
        if i == 0:
            table_str = f"""
            <h3><a name=summary>Summary</a></h3>

            <table border="ipx">
            <tr><th>Symbol</th>
                <th>Sector</th>
                <th>Industry</th>
                <th>URL</th>
                <th>#Employees</th>
                <th>Score</th>
                </tr>
            """
            for idx in df_symbol.index:
                symbol = df_symbol.loc[idx, "Ticker"]
                score  = df_symbol.loc[idx, "HQM Score"]

                symbol,sector,industry,website,num_emp,profile = \
                    fa_dict.get(symbol, [symbol,"N/A","N/A","N/A",0,"N/A"])

                table_str += f"""
                    <tr><td><a href="#{symbol}">{symbol}</a></td>
                        <td>{sector}</td>
                        <td>{industry}</td>
                        <td><a href={website}>{website}</a></td>
                        <td>{num_emp}</td>
                        <td>{score:.1f}</td>
                        </tr>
                """

            table_str += "</table>"
            f.write(table_str)

        symbol = df_symbol.loc[i, "Ticker"]
        symbol,sector,industry,website,num_emp,profile = \
            fa_dict.get(symbol, [symbol,"N/A","N/A","N/A",0,"N/A"])

        html_str = f"""
            <h3><a name="{symbol}" href="https://finviz.com/quote.ashx?t={symbol}">{symbol}</a> </h3>
            <table>
            <tr><td> <img src={file_png_path} width=1200> </td></tr>
        """
        if sector:
            html_str += f"""
                <tr><td> <b>URL:  </b> <a href={website}> {website}</a> - <b>Sector: </b>{sector} - <b>Industry: </b> {industry} - <b>Employes: </b> {num_emp}   </td></tr>
                <tr><td> <b>Profile: </b> {profile}  </td></tr>
            """
        html_str += "</table>  <a href=#summary> [Summary] </a>"
        f.write(html_str)

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            for file_csv in sys.argv[1:]:
                try:
                    df_symbol = pd.read_csv(file_csv)[['Ticker','HQM Score']]
                except:
                    df_symbol = pd.DataFrame(gwg.read_ticker(file_csv), columns=['Ticker'])
                    df_symbol["HQM Score"] = 0

                symbols = df_symbol['Ticker'].tolist()
                num_symbols = len(symbols)
                print(f"symbols={symbols}")

                fa_dict = {}
                fa_results = get_sector_profiles(symbols, connection)
                for row in fa_results:
                    fa_dict[row[0]] = row

                for i in df_symbol.index:

                    # not working: still has core dump
                    # if not i % 5:
                    #     finplot = reload(finplot)

                    # reload module
                    # not working: still has core dump
                    # if not i % 20 and 'finplot' in sys.modules:  
                    #     del sys.modules["finplot"]
                    #     del finplot
                    #     import finplot

                    print(f"\n==========   {i+1} / {num_symbols}   =========================\n")
                    symbol = df_symbol.loc[i, "Ticker"]
                    fa_info = fa_dict.get(symbol, [symbol,"N/A","N/A","N/A",0,"N/A"])
                    file_png, log_msg = plt_chart(fa_info, save_chart=True, interactive=False)

                    if file_png:
                        print(log_msg)
                        generate_html(file_csv, file_png, i)

                    finplot.show()


    except KeyboardInterrupt:
        sys.exit()
