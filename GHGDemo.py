import sqlite3
import json
#import pandas as pd

#connect to database
conn = sqlite3.connect('Battery_Value_Chain.db')
#create a cursor
c = conn.cursor()

# create mineral value chain tables
table1 = """CREATE TABLE Nickel(
            Name TEXT,
            Type TEXT,
            Headquarters TEXT,
            Total_GHG_Emissions INTEGER,
            Energy_Use INTEGER,
            Water_Use INTEGER,
            Production_Volume INTEGER
            )"""
c.execute("DROP TABLE IF EXISTS Nickel;")
c.execute(table1)

# add value chain operators into the Nickel table
operators = [
                ('Vale', 'Mining', 'Brazil', 575300000, 165800000000, 148000000, 208000),
                ('Norilsk Nickel', 'Mining', 'Russia', 9900000, 18501000, 1344000000, 228700),
                ('Glencore', 'Mining', 'Switzerland', 2900000, 33000000, 116000000, 120600),
                ('Anglo American', 'Mining', 'UK', 17700000, 86500000, 209155000, 42600),
                ('South32', 'Mining', 'Australia', 139500000, 176000000, 45724000, 41100),
                ('Sumitomo Metal Mining', 'Mining', 'Japan', 2807000, 32052000, 619000, 12000),
                ('Western Areas', 'Mining', 'Australia', 66105, 552414, None, 23208),
                ('Lundin Mining', 'Mining', 'Canada', 946203, 10738795, 34702540, 13494),
                ('Terraframe', 'Mining', 'Finland', 231214, 2302000, 4500000, 27468),
                ('BHP', 'Mining', 'Australia', 990000, 149000000, 353000, 87400),
                ('Zhejiang Huayou Cobalt', 'Mining', 'China', 26156693, 4418609, 8196570, 21144)
            ]
c.executemany("INSERT INTO Nickel VALUES (?,?,?,?,?,?,?)", operators)

#commit our command
conn.commit()
#close our connection
conn.close()

# Convert SQL database into JSON format
db_local = 'Battery_Value_Chain.db'
connie = sqlite3.connect(db_local)
c = connie.cursor()

#select company data
sql_query = "SELECT * FROM Nickel;"
c.execute(sql_query)
company_details = c.fetchall()

#select column headers
sql_query = "SELECT Name FROM PRAGMA_TABLE_INFO('Nickel');"
c.execute(sql_query)
headers = c.fetchall()
headers = [i[0] for i in headers]

company_dict = {}

#iterate through each company in company_details
for company in company_details:
    company_indiv = dict(zip(headers[1:], company[1:]))
    company_dict[company[0]] = company_indiv

with open('ValueChainList.json', 'w') as json_output:
    json.dump({'company': company_dict}, json_output)
