from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from faicons import icon_svg
from shiny import reactive
from shiny.express import input, render, ui
from shiny.ui import output_ui
from shinywidgets import render_plotly
from stocks import stocks

# Default to the last 6 months
end = pd.Timestamp.now()
start = end - pd.Timedelta(weeks=26)


import requests
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


tickers = ['CHRW', 'ECPG', 'ESLOY', 'KNF', 'NFYEF', 'PWR', 'PPC', 'WTBA', 'WTKWY']

def get_stock_data_direct(ticker, start_date, end_date):
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json',
    }
    interval = "1d"
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?period1={start_date}&period2={end_date}&interval={interval}"

    try:
        resp = requests.get(url, headers=headers)
        data = resp.json()
        result = data['chart']['result'][0]
        timestamps = result['timestamp']
        quote = result['indicators']['quote'][0]
        close_prices = quote.get('close', [])

        if timestamps and close_prices:
            dates = [datetime.datetime.fromtimestamp(ts) for ts in timestamps]
            df = pd.DataFrame({'Close': close_prices}, index=dates)
            return ticker, df
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")

    return ticker, None


def build_stc_index(start_date, end_date):
    stock_data = {}
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_ticker = {
            executor.submit(get_stock_data_direct, ticker, start_date, end_date): ticker
            for ticker in tickers
        }
        for future in as_completed(future_to_ticker):
            ticker, df = future.result()
            if df is not None:
                stock_data[ticker] = df
            time.sleep(0.2)

    if not stock_data:
        return pd.DataFrame()

    all_dates = sorted(set().union(*[df.index for df in stock_data.values()]))
    index_df = pd.DataFrame(index=all_dates)
    for ticker, df in stock_data.items():
        index_df[ticker] = df['Close']

    index_df = index_df.fillna(method='ffill')

    divisor = 0.600234
    index_df['STC_Index'] = index_df.sum(axis=1) / divisor

    return index_df

ui.page_opts(title="Stock explorer", fillable=True)

with ui.sidebar():
    ui.input_date_range("dates", "Select dates", start=start, end=end)


with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("dollar-sign")):
        "Current Price"

        @render.ui
        def price():
            close = get_data()["Close"]
            return f"{close.iloc[-1]:.2f}"

    with ui.value_box(showcase=output_ui("change_icon")):
        "Change"

        @render.ui
        def change():
            return f"${get_change():.2f}"

    with ui.value_box(showcase=icon_svg("percent")):
        "Percent Change"

        @render.ui
        def change_percent():
            return f"{get_change_percent():.2f}%"


with ui.layout_columns(col_widths=[9, 3]):
    with ui.card(full_screen=True):
        ui.card_header("Price history")

        @render_plotly
        def price_history():
            # Get the data and ensure it has a proper DatetimeIndex
            df = get_data()
            
            # The previous code had a redundant df.reset_index() and was trying to use a 'Date' column
            # that was not the DataFrame's index. Plotly works best when the x-axis is a proper
            # DatetimeIndex, which is what we are now returning from get_data().
            fig = go.Figure(
                data=[
                    go.Scatter(
                        x = df.index,  # Use the DataFrame's index directly for the x-axis
                        y = df['Close'],
                        mode="lines",
                        name="STC Index",
                        line={"color": "blue", "dash": "dash"},
                    )
                ]
            )

            df["SMA"] = df["Close"].rolling(window=20).mean()
            fig.add_scatter(
                x=df.index,
                y=df["SMA"],
                mode="lines",
                name="SMA (20)",
                line={"color": "orange", "dash": "dash"},
            )
            
            fig.update_layout(
                hovermode="x unified",
                legend={
                    "orientation": "h",
                    "yanchor": "top",
                    "y": 1,
                    "xanchor": "right",
                    "x": 1,
                },
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            return fig

    with ui.card():
        ui.card_header("Latest data")

        @render.data_frame
        def latest_data():
            x = get_data()
            x.drop('Close', axis=1, inplace=True) #just to remove the close column so that it doesn't show the price of the index twice
            x = x[-1:].T.reset_index() 
            x.columns = ["Category", "Value"]
            x["Value"] = x["Value"].apply(lambda v: f"{v:.1f}")
            return x


ui.include_css(Path(__file__).parent / "styles.css")


@reactive.calc
def get_ticker():
    return yf.Ticker(input.ticker())


@reactive.calc
def get_data():
    # Use the dates from the UI input
    dates = input.dates()
    start_dt = dates[0]
    end_dt = dates[1]

    # Convert dates to epoch timestamps for the API call
    start_epoch = int(pd.Timestamp(start_dt).timestamp())
    end_epoch = int(pd.Timestamp(end_dt).timestamp())

    data = build_stc_index(start_epoch, end_epoch)

    if not data.empty:
        # The index from build_stc_index is already datetime objects.
        # We need to localize and convert the timezone for a proper DatetimeIndex
        data.index = pd.to_datetime(data.index).tz_localize("UTC").tz_convert("America/New_York")
        
        # We also need a 'Close' column for the other functions to work, which is
        # a copy of the calculated 'STC_Index'.
        data['Close'] = data['STC_Index'].copy()

    # The returned dataframe now has a proper DatetimeIndex and a 'Close' column
    return data


@reactive.calc
def get_change():
    close = get_data()["Close"]
    if len(close) < 2:
        return 0.0
    return close.iloc[-1] - close.iloc[-2]


@reactive.calc
def get_change_percent():
    close = get_data()["Close"]
    if len(close) < 2:
        return 0.0
    change = close.iloc[-1] - close.iloc[-2]
    return change / close.iloc[-2] * 100


with ui.hold():

    @render.ui
    def change_icon():
        change = get_change()
        icon = icon_svg("arrow-up" if change >= 0 else "arrow-down")
        icon.add_class(f"text-{('success' if change >= 0 else 'danger')}")
        return icon
