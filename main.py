import gspread
from oauth2client.service_account import ServiceAccountCredentials
import schedule
import time
import sys
sys.path.append("..")
from scraping_db import bit_flyer_func, DB_func, str_date_today

# Periodic execution function
def job():
    date_today = str_date_today
    coin_data = bit_flyer_func()
    DB_func()
    print("Jop start")

    # Get Google API information
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name("Json file name that can be obtained by Google API", scope)
    gc = gspread.authorize(credentials)
    SPREADSHEET_KEY = "SPREADSHEET_KEY"

    # Get information on Google Sheets
    wks = gc.open("Google sheet sheet file name").sheet1
    values_row_list = wks.row_values(1)
    values_col_list = wks.col_values(1)
    values_col_num = len(values_col_list)
    values_col_num = values_col_num + 1

    # Enter the acquired data in the cell
    wks.batch_update([{
        'range': "A" + str(values_col_num) + ":" + "B" + str(values_col_num),
        'values': [[date_today, "BTC"]]
    }])
    wks.batch_update([{
        'range': "C" + str(values_col_num) + ":" + "D" + str(values_col_num),
        'values': [[coin_data[0], coin_data[1]]],
    }])
    wks.batch_update([{
        'range': "E" + str(values_col_num) + ":" + "F" + str(values_col_num),
        'values': [[coin_data[2], coin_data[3]]],
    }])
    wks.batch_update([{
        'range': "G" + str(values_col_num) + ":" + "H" + str(values_col_num),
        'values': [[coin_data[4], coin_data[5]]],
    }])
    wks.update_acell("I" + str(values_col_num), str(coin_data[6]))

    # Display result of the cell value on the console
    result = 0
    while (result < len(values_row_list)):
        if result == 0:
            print(wks.acell("A" + str(values_col_num)))
        elif result == 1:
            print(wks.acell("B" + str(values_col_num)))
        elif result == 2:
            print(wks.acell("C" + str(values_col_num)))
        elif result == 3:
            print(wks.acell("D" + str(values_col_num)))
        elif result == 4:
            print(wks.acell("E" + str(values_col_num)))
        elif result == 5:
            print(wks.acell("F" + str(values_col_num)))
        elif result == 6:
            print(wks.acell("G" + str(values_col_num)))
        elif result == 7:
            print(wks.acell("H" + str(values_col_num)))
        else:
            print(wks.acell("I" + str(values_col_num)))
        result += 1

# Periodic execution time setting
schedule.every(3).hours.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)