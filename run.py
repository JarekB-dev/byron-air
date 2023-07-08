import gspread
from google.oauth2.service_account import Credentials
import sys, time
from tabulate import tabulate
import os


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


def main():
    """
    to run all functions
    """
    dep_airport = select_airport("departure")
    arr_airport = select_airport("arrival", dep_airport)
    print(dep_airport)
    print(arr_airport)

main_menu()