import pybitflyer
import datetime
from time import sleep
import sqlite3

# Get date
date = datetime.date.today()
str_date_today = str(date)

# Get Bitcoin data every minute using bitFlyer API
data = []
def bit_flyer_func():
    bid_list = []
    aks_list = []
    bit_flyer_api = pybitflyer.API()
    for i in range(60):
        ticker = bit_flyer_api.ticker(product_code="BTC_JPY")
        bid = ticker["best_bid"]
        ask = ticker["best_ask"]
        print("bid:" + str(bid))
        print("ask:" + str(ask))
        bid_list.append(bid)
        aks_list.append(ask)
        sleep(60)
    print("bid_list:" + str(bid_list))
    print("ask_list:" + str(aks_list))
    data.append(max(bid_list))
    data.append(min(bid_list))
    data.append(max(aks_list))
    data.append(min(aks_list))
    diff_max = int(data[0] - data[2])
    diff_min = int(data[1] - data[3])
    diff_max_min = int(data[0] - data[3])
    data.append(diff_max)
    data.append(diff_min)
    data.append(diff_max_min)
    print("bid_list" + str(bid_list))
    print("ask_list" + str(aks_list))

    # Display the data to be filled in the cell on the console
    result = 0
    while (result < len(data)):
        if result == 0:
            print("bid_max:" + str(data[result]))
        elif result == 1:
            print("bid_min:" + str(data[result]))
        elif result == 2:
            print("ask_max:" + str(data[result]))
        elif result == 3:
            print("ask_min:" + str(data[result]))
        elif result == 4:
            print("diff_max:" + str(data[result]))
        elif result == 5:
            print("diff_min:" + str(data[result]))
        else:
            print("diff_max_min:" + str(data[result]))
        result += 1
    return data

# Operation of sqlite3
def DB_func():
    print(data)
    dbname = "CryptoCoin.db"
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute("CREATE TABLE bitflyer(id INTEGER PRIMARY KEY AUTOINCREMENT, date STRING, bid_max STRING,  bid_min STRING, ask_max STRING, ask_min STRING, diff_max STRING, diff_min  STRING, diff_max_min, STRING)")
    sql = "INSERT INTO bitflyer(date, bid_max, bid_min, ask_max, ask_min, diff_max, diff_min, diff_max_min) values(?,?,?,?,?,?,?,?)"
    data_list = [date, data[0], data[1], data[2], data[3], data[4], data[5], data[6]]
    cur.execute(sql, data_list)
    cur.execute("SELECT * FROM bitflyer")
    print(cur.fetchall())
    conn.commit()
    cur.close()
    conn.close()