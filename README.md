# ExcelStocks
## THIS IS ONLY FOR TESTING/EDUCATIONAL PURPOSES ONLY.
ExcelStocks is a program that generates a list of stocks that conforms to Kristjan Kullamägi's Trading strategies of the following stock rules:

1. There has been an increase of 30-100% or higher in the past 1-3 months.
2. Pull back to test the 10/20/50-day moving average, make narrow adjustments, and form a terminal consolidation pattern. Refer to its stock selection method on the TC2000 platform: 1-Month Gainers: 100*(C/C21-1); 3-Month Gainers: 100*(C/C63-1); 6-Month Gainers: 100*(C/ C126-1).


If you have any errors,please refer to the errors.md file, and if you have a solution,please add on to the errors.md file.

## Installation Guide

first,download this repository by running
`git clone https://github.com/RA86-dev/ExcelStocks1`.
This will download it to ExcelStocks.


1. If this repo is in a .zip or .tar.gz or anything else, please unpack.
2. Open the terminal by right clicking on the folder and clicking open in terminal (ADVANCED: use cd to advance to the location)
3. Run `python3 installer.py`. This will activate a installer that works on Windows,Mac,Linux,etc.
4. After installing the required libraries, run main.py. It should guide you through!

## Sources

The sources for the ExcelStocks are the the following URLS (fetched with pandas)
[Source 1 - Dow Jones Industrial Average](https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average)
[Source 2 - Nasdaq 100](https://en.wikipedia.org/wiki/Nasdaq-100)
[Source 3 - List of S&P 500 Companies](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies)


### Tested Operating Systems:
So far, the operating systems that have been tested:
1. Ubuntu 20.04 LTS (Notifications work)
2. Raspbian 13+ (Notifications don't work)
3. Windows 10/11 (Notifications Work)
5. MacOS 12.7.5 Monterey (Notifications don't work)

