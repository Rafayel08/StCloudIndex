# # from pathlib import Path

# # import pandas as pd
# # import plotly.graph_objects as go
# # import yfinance as yf
# # from faicons import icon_svg
# # from shiny import reactive
# # from shiny.express import input, render, ui
# # from shiny.ui import output_ui
# # from shinywidgets import render_plotly
# # from stocks import stocks

# # # Default to the last 6 months
# # end = pd.Timestamp.now()
# # start = end - pd.Timedelta(weeks=26)


# # ui.page_opts(title="Stock explorer", fillable=True)

# # with ui.sidebar():
# #     # ui.input_selectize("ticker", "Select Stocks", choices=stocks, selected="AAPL")
# #     ui.input_date_range("dates", "Select dates", start=start, end=end)


# # with ui.layout_column_wrap(fill=False):
# #     with ui.value_box(showcase=icon_svg("dollar-sign")):
# #         "Current Price"

# #         @render.ui
# #         def price():
# #             close = get_data()["Close"]
# #             return f"{close.iloc[-1]:.2f}"

# #     with ui.value_box(showcase=output_ui("change_icon")):
# #         "Change"

# #         @render.ui
# #         def change():
# #             return f"${get_change():.2f}"

# #     with ui.value_box(showcase=icon_svg("percent")):
# #         "Percent Change"

# #         @render.ui
# #         def change_percent():
# #             return f"{get_change_percent():.2f}%"


# # with ui.layout_columns(col_widths=[9, 3]):
# #     with ui.card(full_screen=True):
# #         ui.card_header("Price history")

# #         @render_plotly
# #         def price_history():
# #             # df = get_data().reset_index()
# #             df = yf.Ticker("AAPL").history(period = "1y").reset_index()
# #             fig = go.Figure(
# #                 data=[
# #                     go.Candlestick(
# #                         x=df["Date"],
# #                         open=df["Open"],
# #                         high=df["High"],
# #                         low=df["Low"],
# #                         close=df["Close"],
# #                         increasing_line_color="#44bb70",
# #                         decreasing_line_color="#040548",
# #                         name=input.ticker(),
# #                     )
# #                 ]
# #             )
# #             df["SMA"] = df["Close"].rolling(window=20).mean()
# #             fig.add_scatter(
# #                 x=df["Date"],
# #                 y=df["SMA"],
# #                 mode="lines",
# #                 name="SMA (20)",
# #                 line={"color": "orange", "dash": "dash"},
# #             )
# #             fig.update_layout(
# #                 hovermode="x unified",
# #                 legend={
# #                     "orientation": "h",
# #                     "yanchor": "top",
# #                     "y": 1,
# #                     "xanchor": "right",
# #                     "x": 1,
# #                 },
# #                 paper_bgcolor="rgba(0,0,0,0)",
# #                 plot_bgcolor="rgba(0,0,0,0)",
# #             )
# #             return fig

# #     with ui.card():
# #         ui.card_header("Latest data")

# #         @render.data_frame
# #         def latest_data():
# #             x = get_data()[:1].T.reset_index()
# #             x.columns = ["Category", "Value"]
# #             x["Value"] = x["Value"].apply(lambda v: f"{v:.1f}")
# #             return x


# # ui.include_css(Path(__file__).parent / "styles.css")


# # @reactive.calc
# # def get_ticker():
# #     return yf.Ticker("AAPL")


# # @reactive.calc
# # def get_data():
# #     # dates = input.dates()
# #     return get_ticker().history(period = '1y')


# # @reactive.calc
# # def get_change():
# #     close = get_data()["Close"]
# #     if len(close) < 2:
# #         return 0.0
# #     return close.iloc[-1] - close.iloc[-2]


# # @reactive.calc
# # def get_change_percent():
# #     close = get_data()["Close"]
# #     if len(close) < 2:
# #         return 0.0
# #     change = close.iloc[-1] - close.iloc[-2]
# #     return change / close.iloc[-2] * 100


# # with ui.hold():

# #     @render.ui
# #     def change_icon():
# #         change = get_change()
# #         icon = icon_svg("arrow-up" if change >= 0 else "arrow-down")
# #         icon.add_class(f"text-{('success' if change >= 0 else 'danger')}")
# #         return icon
# from pathlib import Path

# import pandas as pd
# import plotly.graph_objects as go
# import yfinance as yf
# from faicons import icon_svg
# from shiny import reactive
# from shiny.express import input, render, ui
# from shiny.ui import output_ui
# from shinywidgets import render_plotly

# # Default to the last 6 months
# end = pd.Timestamp.now()
# start = end - pd.Timedelta(weeks=26)

# ui.page_opts(title="Stock explorer", fillable=True)

# with ui.sidebar():
#     ui.input_date_range("dates", "Select dates", start=start, end=end)

# with ui.layout_column_wrap(fill=False):
#     with ui.value_box(showcase=icon_svg("dollar-sign")):
#         "Current Price"

#         @render.ui
#         def price():
#             close = get_data()["Close"]
#             return f"{close.iloc[-1]:.2f}"

#     with ui.value_box(showcase=output_ui("change_icon")):
#         "Change"

#         @render.ui
#         def change():
#             return f"${get_change():.2f}"

#     with ui.value_box(showcase=icon_svg("percent")):
#         "Percent Change"

#         @render.ui
#         def change_percent():
#             return f"{get_change_percent():.2f}%"

# with ui.layout_columns(col_widths=[9, 3]):
#     with ui.card(full_screen=True):
#         ui.card_header("Price history")

#         @render_plotly
#         def price_history():
#             df = get_data().reset_index()

#             fig = go.Figure(
#                 data=[
#                     go.Candlestick(
#                         x=df["Date"],
#                         open=df["Open"],
#                         high=df["High"],
#                         low=df["Low"],
#                         close=df["Close"],
#                         increasing_line_color="#44bb70",
#                         decreasing_line_color="#040548",
#                         name="AAPL",  # Hard-coded to AAPL
#                     )
#                 ]
#             )

#             # 20-day SMA
#             df["SMA"] = df["Close"].rolling(window=20).mean()
#             fig.add_scatter(
#                 x=df["Date"],
#                 y=df["SMA"],
#                 mode="lines",
#                 name="SMA (20)",
#                 line={"color": "orange", "dash": "dash"},
#             )

#             fig.update_layout(
#                 hovermode="x unified",
#                 legend={
#                     "orientation": "h",
#                     "yanchor": "top",
#                     "y": 1,
#                     "xanchor": "right",
#                     "x": 1,
#                 },
#                 paper_bgcolor="rgba(0,0,0,0)",
#                 plot_bgcolor="rgba(0,0,0,0)",
#             )
#             return fig

#     with ui.card():
#         ui.card_header("Latest data")

#         @render.data_frame
#         def latest_data():
#             x = get_data()[:1].T.reset_index()
#             x.columns = ["Category", "Value"]
#             x["Value"] = x["Value"].apply(lambda v: f"{v:.1f}")
#             return x

# ui.include_css(Path(__file__).parent / "styles.css")

# @reactive.calc
# def get_ticker():
#     return yf.Ticker("AAPL")  # Hard-coded AAPL

# @reactive.calc
# def get_data():
#     start, end = input.dates()
#     return get_ticker().history(start=start, end=end)

# @reactive.calc
# def get_change():
#     close = get_data()["Close"]
#     if len(close) < 2:
#         return 0.0
#     return close.iloc[-1] - close.iloc[-2]

# @reactive.calc
# def get_change_percent():
#     close = get_data()["Close"]
#     if len(close) < 2:
#         return 0.0
#     change = close.iloc[-1] - close.iloc[-2]
#     return change / close.iloc[-2] * 100

# with ui.hold():
#     @render.ui
#     def change_icon():
#         change = get_change()
#         icon = icon_svg("arrow-up" if change >= 0 else "arrow-down")
#         icon.add_class(f"text-{('success' if change >= 0 else 'danger')}")
#         return icon

from pathlib import Path
import requests
import pandas as pd
import datetime
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import plotly.graph_objects as go

from faicons import icon_svg
from shiny import reactive
from shiny.express import input, render, ui
from shiny.ui import output_ui
from shinywidgets import render_plotly

#-------------------------------------------------------------------------------
# St. Cloud Stock Price Index (STC_Index)
#-------------------------------------------------------------------------------

# Define ticker symbols
tickers = ['CHRW', 'ECPG', 'ESLOY', 'KNF', 'NFYEF', 'PWR', 'PPC', 'WTBA', 'WTKWY']

# Direct Yahoo API fetcher
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


#-------------------------------------------------------------------------------
# Shiny UI + Server
#-------------------------------------------------------------------------------

end = pd.Timestamp.now()
start = end - pd.Timedelta(weeks=26)

ui.page_opts(title="St. Cloud Stock Price Index", fillable=True)

with ui.sidebar():
    ui.input_date_range("dates", "Select dates", start=start, end=end)

with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("dollar-sign")):
        "Current Index Value"

        @render.ui
        def price():
            close = get_data()["STC_Index"]
            return f"{close.iloc[-1]:.2f}"

    with ui.value_box(showcase=output_ui("change_icon")):
        "Change"

        @render.ui
        def change():
            return f"{get_change():.2f}"

    with ui.value_box(showcase=icon_svg("percent")):
        "Percent Change"

        @render.ui
        def change_percent():
            return f"{get_change_percent():.2f}%"

with ui.layout_columns(col_widths=[9, 3]):
    with ui.card(full_screen=True):
        ui.card_header("Index history")
 

        @render_plotly
        def price_history():
            df = get_data().reset_index()
            df['index'] = pd.to_datetime(df['index'])
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=df["index"],
                    y=df["STC_Index"],
                    mode="lines",
                    name="STC Index",
                    line=dict(color="blue")
                )
            )

            # 20-day SMA
            df["SMA"] = df["STC_Index"].rolling(window=20).mean()
            fig.add_trace(
                go.Scatter(
                    x=df["index"],
                    y=df["SMA"],
                    mode="lines",
                    name="SMA (20)",
                    line=dict(color="orange", dash="dash")
                )
            )

            fig.update_layout(
                hovermode="x unified",
                legend={"orientation": "h", "yanchor": "top", "y": 1, "xanchor": "right", "x": 1},
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )


            # print(df["index"])

            return fig

    with ui.card():
        ui.card_header("Latest data")

        @render.data_frame
        def latest_data():
            x = get_data()[:1].T.reset_index()
            x.columns = ["Category", "Value"]
            x["Value"] = x["Value"].apply(lambda v: f"{v:.1f}")
            return x


ui.include_css(Path(__file__).parent / "styles.css")

@reactive.calc
def get_data():
    start_dt, end_dt = input.dates()
    start_epoch = int(pd.Timestamp(start_dt).timestamp())
    end_epoch = int(pd.Timestamp(end_dt).timestamp())
    return build_stc_index(start_epoch, end_epoch)

@reactive.calc
def get_change():
    close = get_data()["STC_Index"]
    if len(close) < 2:
        return 0.0
    return close.iloc[-1] - close.iloc[-2]

@reactive.calc
def get_change_percent():
    close = get_data()["STC_Index"]
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


