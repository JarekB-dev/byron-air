import gspread
from google.oauth2.service_account import Credentials
import sys, time
from tabulate import tabulate
import os
import random
from datetime import date, datetime, timedelta


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('byron-air')

LOGO = """

                        Welcome to ByronAir
                        
                                |
                          --====|====--
                                |
                            .-------.
                          .'_________'.
                         ._/_|__|__|_\_.
                        ;'-._       _.-';
   ,--------------------|    `-. .-'    |--------------------,
    ``----..__    ___   ;       '       ;   ___    __..----``
              `"- / \ .._\             /_.. / \-"`
                  \_/    '._        _.'     \_/
                  `"`        ``---``        `"`

"""

EUROPE = """
⢧⠹⡜⢬⠣⡝⡬⢣⡝⢬⢣⡝⢬⢣⡝⡬⢣⡝⢬⠣⡝⢬⠣⡝⢬⠣⡝⢬⢣⠝⣬⠣⡝⣬⠣⡝⣬⢣⡝⢬⢣⠝⡬⢣⠝⡬⢣⠝⡬⢣⠝⡬⢣⡝⢬⢣⡝⢬⢣⡝⣬⢣⡝⢬⠣⡝⣌⢣⠭⣙⢬⣹⡼⠙⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸
⣋⢳⡩⢎⢳⢩⡜⢣⡚⢥⡓⡜⣣⢓⡜⣱⢃⡞⣡⢛⡜⣣⢹⣘⢣⡝⢬⢣⡍⢞⡰⣋⡜⢆⡛⣜⢢⡓⣜⢣⣋⠞⣱⢋⡞⣱⢩⡚⣥⢋⢮⠱⣃⢞⣡⢳⣘⢣⡓⣜⢢⡓⣜⢣⣋⠖⣡⡮⣗⢬⣟⠿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸
⣭⢲⡱⢩⢎⢇⡞⢥⠛⣦⠹⡜⣥⢫⡜⣥⢫⡜⣥⢫⡜⣥⠳⣌⠳⡜⡣⢇⡞⢥⠳⣑⢎⢧⡹⣌⢧⡹⣌⠳⣌⠻⣔⢫⡔⣣⠧⡹⡔⡫⢎⢣⡍⢎⢆⡳⢌⢧⡹⡌⢧⡹⢌⠧⡜⢎⡱⢳⢋⡞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸
⡖⣣⢇⡹⣌⠮⡜⢪⡹⣐⢏⡜⢦⠳⡜⢦⡓⡜⣆⠳⡜⣆⡛⣬⢓⡱⡹⢌⡺⢌⡳⣉⢎⠶⣑⢎⠶⡱⢎⡳⣌⠷⣌⠳⣜⡱⢪⠕⢮⢱⣩⣶⣿⡿⢾⣲⣍⣲⢡⠛⢦⡙⣎⠳⢼⢫⠉⡷⣻⡉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸
⣇⠳⡎⢴⢊⢖⡩⢣⢕⢪⡜⢬⢣⡛⡜⣡⠎⡵⢌⠧⣱⢊⠵⣂⠯⡔⢣⡝⡰⢋⡴⣉⠮⡜⡜⡪⢵⡙⢮⡱⢎⡳⣌⢳⠢⣕⢋⢮⣵⣾⡿⠅⠃⠀⠀⠙⠋⠉⠋⠉⠉⠘⠒⠯⢬⣙⠧⣕⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸
⣎⠳⣍⢲⠩⠦⣍⢣⠞⣢⠞⣡⠧⣙⢬⣱⣾⡶⣍⠞⡤⣋⠼⡑⡞⡸⢅⡎⠵⣉⠖⣥⢚⡬⣱⡙⢦⡙⢦⡙⢮⡱⣌⠧⠳⣌⣾⣿⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠞⠻⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸
⣎⠳⡜⢬⠓⣭⢒⡣⢞⡡⢞⢥⡚⢥⠺⡾⡽⣿⠿⠟⡶⠷⢣⣝⠲⣙⢲⡘⣣⠍⡞⣤⠳⣜⢢⡝⢦⡙⢧⡙⢦⠳⡜⢪⢳⣿⣿⠿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠒⠦⣦⡤⣤⢤⠺⡜⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸
⣎⢳⣉⢮⡙⣤⢣⠝⣦⡙⣎⢦⡙⣎⡱⢷⡛⠀⠀⠀⠀⠀⢸⣯⡱⢩⠖⡱⢥⡚⢵⢢⡛⡴⢣⡚⣥⢛⢦⡙⢮⡱⣍⢣⢓⣾⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡆⡷⠫⠱⠗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸
⡎⢧⠜⣢⠕⠮⡜⣓⢦⡹⠜⣦⢙⠦⣣⢓⡺⣅⣠⣤⠤⣦⠞⢧⣑⠫⡜⢥⠳⣘⢣⠧⡹⣜⢣⡝⢦⣋⠶⣙⠦⣓⢬⢣⣿⠅⠀⠀⠀⠀⠀⢠⣤⢤⡄⠀⠀⠀⠀⠀⠀⠀⠛⠲⠿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸
⡝⢮⡱⢣⢞⡱⡹⠜⣦⢹⡙⢦⣋⠶⣡⢏⡒⢦⠓⡬⢓⡬⡙⣆⠎⡵⡙⣎⠵⣩⢎⡳⡱⢎⡣⢞⡱⢪⡕⣣⢣⢍⠦⣻⠷⠀⠀⠀⠀⠀⠀⣽⡑⣎⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸
⡝⢦⡓⢭⢲⡱⣍⢻⡰⢣⡝⢦⡙⡞⡴⣊⡝⢦⠛⡴⢋⡴⢓⡬⣙⢖⡹⡔⣫⠖⣣⢳⡙⢮⡱⣋⡜⣣⠜⣥⢚⣬⣞⡇⠀⠀⠀⠀⠀⠀⢀⡼⣱⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸
⡝⢦⡙⢮⡱⣚⢬⢣⡝⡱⢎⢧⡹⡜⣥⠳⣜⠪⡝⣔⠫⣔⠫⡴⣩⢚⡴⣙⢦⢛⡴⢣⡝⢦⢳⡱⢎⠵⣩⣦⢿⠟⠛⠁⠀⠀⠀⠀⠠⣰⡟⢭⡋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸
⡝⢦⡙⢦⢳⡩⢎⡇⣞⡱⣋⠶⡱⣍⠶⣹⢰⢫⠜⣆⠯⣔⠫⢖⡥⣋⠶⣩⠖⡭⢒⠧⡜⢎⡵⢚⡬⣺⣾⡻⠁⠀⠀⠀⠀⠀⠀⠀⢸⡳⢌⡣⢧⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸
⡝⢦⡙⢮⢥⠳⣍⠞⡴⢣⡝⣪⠕⣮⠱⣎⡓⢮⡙⢦⠳⣌⡛⣬⠲⣍⠞⣥⢚⡕⣋⣶⣏⡚⡴⢫⠔⣿⠧⡼⠄⠀⠀⠀⠀⠀⠀⠀⠸⣕⢣⣱⢻⣄⡀⠀⣠⡶⢻⣹⠞⠒⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸
⡝⢦⡹⣘⢎⡳⣌⢻⡘⣇⢞⣡⢛⡴⢋⠶⣙⢦⡙⣎⠳⣬⠱⢎⡱⡌⠞⡤⢣⣾⡔⡻⢤⡹⢜⡣⢞⢻⣧⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⣈⣳⡟⢧⠚⣽⡯⠙⠋⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸
⡝⢦⡓⣜⠪⣕⢪⢥⠳⡜⣊⠶⣩⢎⡝⢮⡱⢎⡵⣊⠷⣨⢇⢫⣴⣿⣿⠙⣻⠟⣌⠳⢣⡙⢦⡹⢌⡿⠗⠀⠀⣰⣽⡦⠀⠀⠀⠀⣉⣻⢟⡘⢦⠻⣝⡽⣤⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⡾⢚⠩⡙⢻
⡝⢦⡓⢬⡓⡬⢣⢎⢣⡝⢬⡓⣥⢚⡜⣣⢕⡫⢴⠩⡖⡱⢪⠝⣟⣿⡂⠚⠓⢻⣌⡓⡣⢝⡢⢇⡫⡜⡶⣦⡶⡛⣦⢷⠀⠀⠀⠀⠸⣗⡪⣾⠥⣋⡟⠲⣽⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠓⡄⢣⠑⡨⢹
⡝⢦⡙⢦⣑⢣⠓⣎⡱⠜⢦⡹⡰⣋⠼⣱⢪⡕⢣⡹⢰⢍⣓⡎⣽⣾⣧⣀⡴⡏⢦⡓⡍⠶⣉⠶⡡⢇⢳⢢⣵⡟⣽⢟⣧⠀⠀⠀⢠⣏⢷⡋⣖⣹⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⢪⡑⢌⠰⡁⢆⢹
⡝⢦⣙⠲⡌⢎⡓⢦⡱⢋⠶⣑⢣⡝⢮⡱⢦⡙⢦⣵⢏⡾⠿⠛⢿⣿⣃⣀⠈⢷⢣⡱⢊⡗⣩⠖⣍⢮⢱⢺⡟⢁⣿⣷⣞⡏⢠⡶⢾⡙⢦⢱⢢⡱⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣷⠉⡅⢊⠔⡡⢌⢸
⡹⣆⢇⢹⡈⣇⠹⡆⢷⡉⡾⢁⢷⡸⢇⡸⣆⠹⣶⣏⡀⠀⠀⢀⡾⣾⡿⣁⠀⠸⣆⠷⡉⣶⠱⡾⡈⢾⡸⣈⣿⣾⣏⣷⣸⢿⠹⣿⣆⠹⣆⢷⣶⣿⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢉⢇⡈⠆⡸⢀⠆⣾
⡳⣜⢊⠶⡑⡎⡵⣙⢦⡹⢜⡭⢲⡹⢬⡑⡎⢵⣢⠿⠅⠀⠀⣺⠱⣞⠵⠟⠀⠠⢼⡧⢱⡂⢟⡰⡙⢦⡑⢎⣽⠂⠛⣿⠽⠛⢿⣴⠜⠋⠀⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠚⠶⠚⠴⣈⡼⢿
⡳⣜⠪⣜⡱⢍⠶⣩⠖⣭⢚⡜⣣⢕⡣⡝⡜⣩⠿⣤⠦⡖⢶⣋⣷⠽⠀⠀⠀⠀⠐⠓⢧⡙⢦⢱⣿⡛⠛⠉⠃⠀⠀⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢩⡞⣹
⡳⣌⢳⠸⣜⣊⠧⣓⠞⡴⣋⠼⣱⢪⠕⣎⠵⣃⠞⡤⢛⡌⢧⡘⢭⡷⠴⠂⠀⠀⢀⣴⢯⡘⢦⠏⠛⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠲⢫⡜⣹
⡳⣌⢧⡙⢦⢎⡳⣩⠞⣥⡙⢮⡱⢎⡝⢦⡙⢦⠛⡴⣋⡜⣲⠿⠧⣴⠲⡖⢷⠲⣔⣺⠒⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡴⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠧⣜⣹
⡳⡜⢦⡙⣎⠶⣱⢣⠞⡴⣙⢦⡙⢮⡜⣣⠝⣪⣙⠲⡥⢚⡥⢚⣱⢢⢓⡏⣎⣵⠂⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠾⢿⡥⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢼
⢧⡙⢦⡹⠜⣎⠵⣪⢝⡲⣍⠶⣙⢦⡙⢦⡛⡴⣡⢛⠼⡡⢞⣿⡉⠙⠻⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣷⡤⢀⣠⣤⣿⢍⣞⡼⠅⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣄⣀⠀⣸
⢧⡙⢦⢹⡹⣌⢳⡱⢎⡵⢪⠵⣩⢖⡹⢦⡙⡖⣥⢋⡞⡱⢎⡜⡹⢷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⢩⡛⣽⣋⡈⢈⡽⢺⠭⣹⢰⠲⢤⣠⣒⣒⠫⣉⠛⡍⠰⣉⣝⢿
⢧⡙⡎⢶⠱⣎⠳⣜⢣⠞⣥⢛⡴⢋⡼⣡⢏⡜⢦⡙⠼⡱⣍⢲⡑⡫⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢤⣺⣃⢧⢱⠒⢦⢳⡛⢬⡓⢮⠱⣎⡝⢦⢣⡝⢬⣣⣄⡧⢬⡝⠛⢳⣾
⢧⡹⡜⢬⠳⣌⠳⣌⠧⣋⠶⣩⠖⣭⢲⡱⢎⡜⢦⡙⡥⠳⣌⠧⣜⠱⣪⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡏⡜⢮⡸⣙⢎⡱⢎⠳⣘⢥⢛⡔⣎⢣⢓⡜⣢⠋⠀⠀⠀⠻⠘⡶⣿
⣇⠳⡜⣡⠏⡼⣑⠮⣱⠩⣖⡱⡚⢴⢣⡜⠒⠛⠦⠧⣍⠳⡌⠶⣌⠳⡟⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣻⡽⣷⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢤⠟⣬⢃⠶⣉⢖⡩⡮⠵⠞⠶⠣⠾⠴⠯⠊⠁⠀⠀⠀⠀⠀⠀⠈⢳⣼
⣎⠳⡍⢦⡙⢦⠱⢎⠥⣓⢆⡳⢍⢮⢱⡟⠀⠀⠀⠀⠀⠈⠉⠙⠒⠛⠁⠀⠀⠀⠀⠀⠀⣀⣀⡀⠀⠀⢠⣴⡛⠶⡄⠀⠀⠉⢷⡌⡽⢫⣆⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠿⡹⢤⠫⡜⡜⡲⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣻
⣎⠳⣍⢲⣉⠶⡩⢎⠵⣊⡜⢲⢍⠦⣻⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⢹⡘⢧⠲⡗⢾⠱⣬⡷⢽⣆⠀⠀⠀⠱⡜⡥⢚⡟⢿⠦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣙⣶⣛⡏⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡖⢋⢽
⣎⠳⡜⢲⠌⡶⡙⣬⢓⡼⣘⠣⢞⣸⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⡤⢟⡡⢏⢎⠳⡙⣎⠹⡇⡜⢦⡙⣳⣤⠀⠀⠈⠓⢛⣎⠧⣚⠴⡹⠂⠀⠀⠀⠀⡀⣄⣦⣶⣶⣴⠾⠟⠚⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡔⢋⡟⢡⠊⢼
⣎⢳⣉⢞⡸⣡⠳⡜⡼⢰⠣⡝⣲⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⣇⠳⡸⡌⢵⢊⠮⣱⠙⣆⣯⠟⢹⡆⣓⠦⡩⢏⡻⣤⣄⠀⠀⣩⣚⢶⣙⣄⠀⠀⠀⠘⠷⠿⡓⢾⣛⣧⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⣤⢠⠚⡌⢣⠘⢄⡹⢂⠜⣸
⡎⢧⡜⡸⡔⣣⠳⣩⢜⠣⣏⠲⢥⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣡⠫⡔⣷⢟⡞⢿⢊⡵⢊⡽⣠⢻⠀⢸⡜⢢⣓⡱⢍⡲⢅⢏⣲⡐⠧⣏⢻⡑⠞⡿⣄⠀⠀⠼⣷⢽⡢⢣⢯⢿⣂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⢶⠺⡯⢇⠢⣁⠒⡄⢃⠢⣰⠏⡰⢸
⡝⡲⡜⡱⣜⣡⢛⡴⢋⡵⢪⡕⡺⢆⡤⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡖⢇⡣⢭⡙⢧⡙⢆⡫⢔⠫⣔⢣⠻⢼⡚⠼⡑⣎⡱⠭⡜⢎⣼⣰⡗⣖⡋⢦⡙⢎⡱⢿⣷⠒⠛⣶⡿⣟⣧⡏⢯⣿⣦⣤⣤⡀⢀⡿⣙⢳⠢⣖⢫⣬⢓⡝⣆⣡⠐⡌⠰⣈⡶⠱⡈⠔⣹
⡳⣱⢹⢰⢣⠎⣇⢞⡱⢎⡳⢜⡱⣍⢲⢡⠿⣀⣤⠤⡤⣤⣠⡴⡛⡝⢬⠓⣬⢃⡞⠴⣉⠞⣔⢫⠱⢎⡥⢋⡖⣩⢣⡙⡤⢻⣝⡙⠈⠁⣞⡚⢦⡙⢦⡙⢮⡑⣫⢍⣇⣤⢿⡱⢺⢻⢫⠗⢮⡹⡿⢎⡹⢍⠳⣌⢣⡝⠒⣹⡜⢲⡘⣿⡎⢒⡈⢥⢛⡤⢑⣈⠒⣸
⡇⢧⢫⡜⢣⡛⡬⢎⡵⣋⡜⣣⢳⡘⢎⠦⡟⢙⢬⣓⡜⡤⣃⢎⣕⣮⡡⠟⡒⣓⠚⡓⡉⣌⠲⢓⠋⠞⡰⣻⠊⡍⣱⣻⠒⢧⡸⢌⣛⣦⡞⣜⢢⡝⢦⡙⢦⡹⠔⡮⠴⣉⠟⣭⠷⡌⠮⢝⡦⢟⡱⢎⡲⣩⠳⣌⠧⡹⣍⠳⡸⢅⢾⢽⢌⣂⡜⡃⢆⡝⢪⠡⢩⢹
⣝⣪⣕⣊⣧⣓⣙⣲⣒⣱⣊⣵⣢⣝⡪⣚⣄⣃⣢⣄⣘⣉⣲⣓⣡⣄⣱⣨⣔⣌⣱⣄⣃⣦⣉⣆⣩⣂⣅⣇⣜⣠⣌⣪⣝⣆⣣⣍⣷⣼⣜⣰⣃⣞⣢⣝⣦⣙⣙⣆⣛⣌⣞⣤⣓⣜⣫⣙⣬⣓⣜⣆⣳⣥⣛⣔⣫⣱⣌⣳⣉⣎⣾⢈⡦⣁⣲⢏⣱⣈⣄⣣⣁⣺
"""

def welcome():
	"""
	Print logo.
	"""
	print(LOGO)

def europe_map():
	"""
    Print map of Europe
    """
	print(EUROPE)


# Dictionary will contain all booking information and upload it to the spreadsheet
booking = {'departure': '', 'arrival': '', 'dep_date': '', 'first_pax': '', 'total_number_of_pax': int,
           'time_departure': '', 'time_arrival': '', 'checked_in_bags': '', 'price': '', "reservation_number": ''} 


def typing_print(text, delay=0.02):
	"""
    Typing effect to print statements
    """
	for letter in text:
		sys.stdout.write(letter)
		sys.stdout.flush()
		time.sleep(delay)
		
def typing_input(text, delay=0.02):
	"""
    Typing effect to inputs
    """
	for letter in text:
		sys.stdout.write(letter)
		sys.stdout.flush()
		time.sleep(delay)
	value = input()
	return value

def clear_terminal():
    """
	function to clear terminal
	"""
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    """
    Function displays main menu with option to
    make a booking or retrieve booking
    """

    welcome()

    menu = [
        ["1", "Make a Booking"],
        ["2", "Retrieve Booking"]
    ]

    typing_print(tabulate(menu))
    while True:
        try:
            option = int(
                typing_input("\nPress 1 to Make a Booking or 2 to Retrieve your Booking: \n"))
            if option == 1:
                clear_terminal()
                main()
                break
            elif option == 2:
                clear_terminal()
                print("second option chosen")
                break
            else:
                print("Invalid option, please try again.\n")
        except ValueError:
            print("Invalid option, please try again.\n")


def select_airport(direction, locked=None):
    """
    function will pull list of Countries from spreedsheet
    worksheets and depending on choice will print list of
    airports in that country
    """
    global booking
    clear_terminal()
    europe_map()

    while True:
        try:
            sheet_names = [s.title for s in SHEET.worksheets()[1:]]
            for index, item in enumerate(sheet_names):
                print(index + 1, item.capitalize())
            print("\n")
            selection = int(
                typing_input(f"Please choose your Country of {direction.capitalize()}:"))
            clear_terminal()
            if sheet_names[selection - 1]:
                chosen_country_airports = SHEET.worksheet(
                    sheet_names[selection - 1]).get_all_values()[1:]

                for airport in chosen_country_airports:
                    print(*airport)
                chosen_airport = int(
                    input(f"Please choose your Airport of {direction.capitalize()}: \n"))

                airport_to_add = chosen_country_airports[chosen_airport - 1][1]
                booking[direction] = airport_to_add

                if (locked):
                    if (locked == airport_to_add):
                        print(
                            "Arrival Airport must be different than Departure Airport. Please try again.\n")
                        return select_airport(direction, locked)

                return airport_to_add
            else:
                print("Please select correct Airport.\n")
        except ValueError:
            print("Please enter correct Airport.\n")
        except IndexError:
            print("Please enter correct Value.\n")


def date_of_departure():
    """
    Function enable user to set date of departure. Date must be in the future and error is being 
    handled by except ValueError
    """
    clear_terminal()
    print(
        f"Departure Airport: {booking['departure'].upper()}, Arrival Airport: {booking['arrival'].upper()}")
    while True:
        try:
            date_component = input(
                "Please Enter departure date in DD/MM/YYYY format: \n")
            dep_date = datetime.strptime(date_component, "%d/%m/%Y").date()
            current_date = datetime.now().date()
            if dep_date < current_date:
                print("Please provide date in the future.\n")
                continue
            booking['dep_date'] = dep_date.strftime('%d/%B/%Y')
            clear_terminal()
            choose_flight()
            break
        except ValueError:
            print("Please provide correct date in DD/MM/YYYY format.\n")

def generate_random_time(start_time_str, end_time_str, hours_to_add):
    """
    Function generates random time for departure and random time for arrival,
    but with additionaal 2 hours added
    """
    start_time = datetime.strptime(start_time_str, '%H:%M').time()
    end_time = datetime.strptime(end_time_str, '%H:%M').time()
    time_range = (end_time.hour - start_time.hour) * 60 + \
        (end_time.minute - start_time.minute)
    random_minutes = random.randint(0, time_range)
    random_time = datetime.combine(
        datetime.today(), start_time) + timedelta(minutes=random_minutes)
    random_time += timedelta(hours=hours_to_add)
    return random_time.strftime("%H:%M")

# Random times depending on chosen flight
early = generate_random_time('06:00', '08:00', hours_to_add=0)
early_arr = generate_random_time("08:00", "10:00", hours_to_add=2)
midday = generate_random_time("14:00", "16:00", hours_to_add=0)
midday_arr = generate_random_time(
    "16:00", "18:00", hours_to_add=2)
late = generate_random_time("18:00", "20:00", hours_to_add=0)
late_arr = generate_random_time("20:00", "22:00", hours_to_add=2)

def generate_flight_price(min, max):
    """
    Function generates random price for the ticket
    """
    random_price = random.uniform(min, max)
    return random_price

# Different random prices depending on the chosen flight.
currency_symbol = "€"
price_1 = generate_flight_price(100, 200)
price_2 = generate_flight_price(100, 200)
price_3 = generate_flight_price(100, 200)
flight_cost = booking["price"]

def format_currency(value, currency_symbol):
    """
    Print flight price with currency attached
    """
    amount = f"{currency_symbol}{value:.2f}"
    return amount

def choose_flight():
    """
    Function enables user to choose 1 out of 3 randomly generated flights.
    Departure and arrival has already been selected before.
    Time and price is being generated randoomly."""
    global booking
    choose = [
        ["Selection", "Departure Airport", "Dep Time",
            "Arr Time", "Arrival Airport", "Price"],
        ["1", booking['departure'], early, early_arr,
            booking['arrival'], format_currency(price_1, currency_symbol)],
        ["2", booking['departure'], midday, midday_arr,
            booking['arrival'], format_currency(price_2, currency_symbol)],
        ["3", booking['departure'],  late, late_arr, booking['arrival'], format_currency(price_3, currency_symbol)]]
    print(tabulate(choose, headers='firstrow', tablefmt='grid'))
    while True:
        try:
            flight = int(input("Please choose an available flight by Selection number: \n"))
            
            if flight in (1, 2, 3):
                booking["time_departure"] = [early, midday, late][flight-1]
                booking["time_arrival"] = [early_arr, midday_arr, late_arr][flight-1]
                booking["price"] = [price_1, price_2, price_3][flight-1]
                passenger_name()
                break
            else:
                print("Please choose a correct flight from the list..\n")
        except ValueError:
            print("Please choose a correct flight from the list..\n")

def passenger_name():
    """
    Function have to input main passenger name that must
    contain at least first and last name. Both parts of the name 
    are being capitalized by title()
    """
    clear_terminal()
    print(booking)
    while True:
        try:
            name = input(
                "Please enter First and Last Name of main Passenger:\n")
            parts = name.split()
            if len(parts) < 2:
                print("Please provide Full Name")
                continue
            if any(element.isdigit() for element in name):
                print("Name and Last name should not contain numbers\n")
                continue
            else:
                first_name = parts[0].capitalize()
                last_name = parts[1].capitalize()
                full_name = ' '.join([first_name, last_name])
                booking["first_pax"] = full_name
                total_amount_of_pax()
                break
        except ValueError:
            print("Name and Last name should not contain numbers\n")

def total_amount_of_pax():
    """
    function add total amount of passengers to
    booking dictionary
    """
    pax_amount =int(input("Please provide total amount of Passengers in the Reservation: \n"))
    booking["total_number_of_pax"] = pax_amount
    price = booking["price"]
    total_price = pax_amount * price
    booking["price"] = total_price

def main():
    """
    to run all functions
    """
    dep_airport = select_airport("departure")
    arr_airport = select_airport("arrival", dep_airport)
    print(dep_airport)
    print(arr_airport)

main_menu()