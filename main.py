import os
import time
from urllib.parse import quote
from datetime import datetime
import yaml 
with open('settings.yml', 'r') as config_file:
    config = yaml.safe_load(config_file)
if not os.path.isdir(config['logsLocation']):
    os.mkdir(config['logsLocation'])
else:
    print('Continuing.')
debugLogFilepath = os.path.join(os.getcwd(),config['logsLocation'])
log_path = os.path.join(debugLogFilepath,config['debug_log_filename'])
clear= open(f'{log_path}{quote(time.asctime())}.txt','w')
clear.write(f'debug_file(date={time.asctime()}) \n')
clx = open(f'{log_path}{quote(time.asctime())}.txt','a')
clx.write( f'grabbed yml info:\n {config}')
try:
    import yfinance as yf
    clx.write('Imported yfinance')
    import yaml
    clx.write('Imported yaml')

    import pandas as pd
    clx.write('Imported pandas')

    from plyer import notification
    clx.write('Imported plyer, notification')

    import matplotlib.pyplot as plt
    clx.write('Imported matplotlib.pyplot')

    from datetime import datetime, timedelta
    clx.write('Imported datetime')

    from tqdm import tqdm
    clx.write('Imported tdqm')

    import tkinter as tk
    clx.write('Imported tkinter')

    from tkinter import filedialog
    clx.write('Imported filedialog,tkinter')

    import openpyxl as xlsx_writer
    clx.write('Imported openpyxl')

    import gradio as gr
    clx.write('Imported gradio')


except ImportError as e:
    clx.write(f'ImportError: {str(e)}')

    
    print('Do you want to install required libraries? y/n')
    if input('y/n').lower() == "y":
        print('Ok! Installing now.')
        try:
            os.system('pip install pyyaml openpyxl matplotlib pandas yfinance tqdm plyer')
        except Exception as e:
            print(f"An error occurred. Retrying different method")
            try:
                os.system('pip3 install pyyaml openpyxl matplotlib pandas yfinance tqdm plyer')
            except Exception as e:
                print(f'An error occurred. No more methods able to try. The error is {e}')
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
debug_log_filename = config.get('debug_log_filename', f'debugLog_{timestamp}.txt')
clear = open(debug_log_filename, 'w')
clear.write(f'debug_file(date={time.asctime()}) \n')
clx = open(debug_log_filename, 'a')
# Fetch percentage filter from configuration or prompt user
try:
    percentage_filter = config['percentage_filter_default'] /100
except ValueError:
    print('Could not find th e percentage from settings.yml.')
    quit()
def clear_terminal():
    """
    Clears the terminal screen.
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def get_tickers():
    """
    Downloads S&P 500, NASDAQ-100, and DJIA ticker symbols from Wikipedia and returns them.
    """
    sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    nasdaq_url = 'https://en.wikipedia.org/wiki/NASDAQ-100'
    djia_url = 'https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average'

    sp500_table = pd.read_html(sp500_url, header=0)[0]
    nasdaq_table = pd.read_html(nasdaq_url, header=0)[4]
    djia_table = pd.read_html(djia_url, header=0)[1]

    # Debugging: print the column names to find the correct one
    print("S&P 500 columns:", sp500_table.columns)
    print("NASDAQ columns:", nasdaq_table.columns)
    print("DJIA columns:", djia_table.columns)

    sp500_tickers = sp500_table['Symbol'].tolist()
    # Adjust based on the actual column name for NASDAQ tickers
    nasdaq_tickers = nasdaq_table['Ticker'].tolist()
    djia_tickers = djia_table['Symbol'].tolist()
    return list(set(sp500_tickers + nasdaq_tickers + djia_tickers))
def show_notification(title,message,app_name,timeout=10):
    notification.notify(
        title=f"{title}",
        message=f"{message}",
        app_name=f"{app_name}",
        timeout=timeout
    )
def fetch_stock_data(ticker):
    """
    Fetches and processes stock data for a given ticker symbol.
    """
    end_date = datetime.today()
    start_date = end_date - timedelta(days=180)
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    
    if stock_data.empty:
        return pd.DataFrame()
    
    stock_data['MA10'] = stock_data['Close'].rolling(window=10).mean()
    stock_data['MA20'] = stock_data['Close'].rolling(window=20).mean()
    stock_data['MA50'] = stock_data['Close'].rolling(window=50).mean()
    stock_data['1M_Gain'] = 100 * (stock_data['Close'] / stock_data['Close'].shift(21) - 1)
    stock_data['3M_Gain'] = 100 * (stock_data['Close'] / stock_data['Close'].shift(63) - 1)
    stock_data['6M_Gain'] = 100 * (stock_data['Close'] / stock_data['Close'].shift(126) - 1)
    
    # Apply the first rule: increased 30% or more
    # also convert stock_data['1M/3M/6M_gain'] into percentage,on line 73/74
    filtered_data = stock_data[
        ((stock_data['1M_Gain'] >= 30)) |
        ((stock_data['3M_Gain'] >= 30)) 
    ]
    # Apply the second rule
    filtered_data = filtered_data[
        (filtered_data['Close'] < filtered_data['MA10'] * 1 + percentage_filter) & (filtered_data['Close'] > filtered_data['MA10'] * 1 - percentage_filter) &
        (filtered_data['Close'] < filtered_data['MA20'] * 1 + percentage_filter) & (filtered_data['Close'] > filtered_data['MA20'] * 1 - percentage_filter) &
        (filtered_data['Close'] < filtered_data['MA50'] * 1 + percentage_filter) & (filtered_data['Close'] > filtered_data['MA50'] * 1 - percentage_filter)
    ]
    
    if filtered_data.empty:
        return pd.DataFrame()
    
    filtered_data['Ticker'] = ticker
    filtered_data.reset_index(inplace=True)
    filtered_data = filtered_data[['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'MA10', 'MA20', 'MA50', '1M_Gain', '3M_Gain', '6M_Gain', 'Ticker']]
    
    return filtered_data

def main():
    tickers = get_tickers()
    all_filtered_data = pd.DataFrame()
    
    for ticker in tqdm(tickers, desc="Processing tickers", leave=True, ncols=100):
        filtered_data = fetch_stock_data(ticker)
        all_filtered_data = pd.concat([all_filtered_data, filtered_data])
        clear_terminal()
    
    if not all_filtered_data.empty:
        root = tk.Tk()
        root.title('Background dialog for filename UI')
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            all_filtered_data.to_excel(file_path, index=False)
            print(f"Data saved to {file_path}")
            show_notification("ExcelStocks","Program sucessfully found the stocks that match the criteria.","bg_da")
        else:
            print("Save operation canceled.")
        root.destroy()
        return file_path
    else:
        print("No data to save.")
        print('This means that no results match the needed criteria of:')
        print(f'{(1 - percentage_filter) * 100}% to {(1 + percentage_filter) * 100}% of the base_value for average')
        print(f"and does not follow the rules of Kristjan Kullamagi's Trading strategy.")
def show_filedialog():
    root = tk.Tk()
    root.title('Background dialog for filename UI')
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    root.destroy()
    return file_path
def repeat_main(file_path):
    tickers = get_tickers()
    all_filtered_data = pd.DataFrame()
    
    for ticker in tqdm(tickers, desc="Processing tickers", leave=True, ncols=100):
        filtered_data = fetch_stock_data(ticker)
        all_filtered_data = pd.concat([all_filtered_data, filtered_data])
        clear_terminal()
     
    if not all_filtered_data.empty:
        
        if file_path:
            all_filtered_data.to_excel(file_path, index=False)
            print(f"Data saved to {file_path}")
            show_notification("ExcelStocks","Program sucessfully found the stocks that match the criteria.","bg_da")
        else:
            print("Save operation canceled.")

    else:
        print("No data to save.")
        print('This means that no results match the needed criteria of:')
        print(f'{(1 - percentage_filter) * 100}% to {(1 + percentage_filter) * 100}% of the base_value for average')
        print(f"and does not follow the rules of Kristjan Kullamagi's Trading strategy.")
    
def gradio_live_server(file_path):
    
    # Function to read and display the Excel file
    def show_excel(file_path):
        df = pd.read_excel(file_path)
        return df


    # Create a Gradio interface
    iface = gr.Interface(
        fn=lambda: show_excel(file_path),
        inputs=[],
        outputs=gr.Dataframe(),
        live=False,
        title="Excel File Viewer",
        description="This app displays the contents of an Excel file."
    )

    # Launch the server
    iface.launch()
    return 200
if not config['repeat'] == True:
    
    file_path= main()
    try:
        
        print('Host a server to read the xlsx file?')
        inputf = input('y/n')
        if inputf.lower() == "y":
            if not file_path:
                print('Error! There is no data to display.')
                KeyboardInterrupt('There is no data to display.')
            else:

                gradio_live_server(file_path)
        else:
            quit()
    except Exception as c:
        clx.write(f'Exception in main: {c}')
elif config['repeat'] == True:
    if not config['usefilepath']:
        fp = show_filedialog()
    else:
        fp = config['repeatfileLocation']
    while True:
        print('Press Ctrl+C (on windows, and linux), Control+C on mac')
        repeat_main(fp)

else:
    print('Error! The settings.yml file does not include anything about the repeated amount of time, in repeatLocation.')
