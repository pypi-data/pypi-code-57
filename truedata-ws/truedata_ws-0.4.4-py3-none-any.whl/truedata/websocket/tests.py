from truedata_ws.websocket.TD import TD
import sys
from time import sleep

import pandas as pd

from colorama import Style, Fore

# Testing connection
td_app = TD(sys.argv[1], sys.argv[2], live_port=8082, historical_port=8092)

# Testing Live data
# td_app.start_live_data(f'BANKNIFTY{sys.argv[3]}FUTbk')
td_app.start_live_data(f'CRUDEOIL-I')
count = 0
while count < 60:
    print(td_app.live_data[2000].__dict__)
    sleep(1)
    count = count + 1

# Testing malformed historical contracts
hist_data_0 = td_app.get_historic_data(f'BANKNIFTY99ZYXFUT')

# Testing historical data
hist_data_1 = td_app.get_historic_data(f'BANKNIFTY{sys.argv[3]}FUT')
hist_data_2 = td_app.get_historic_data(f'BANKNIFTY{sys.argv[3]}FUT', duration='3 D')
hist_data_3 = td_app.get_historic_data(f'BANKNIFTY{sys.argv[3]}FUT', duration='3 D', bar_size='15 mins')
hist_data_4 = td_app.get_historic_data(f'BANKNIFTY{sys.argv[3]}FUT', bar_size='30 mins')

print(f'{Style.BRIGHT}{Fore.GREEN}HISTDATA 1...{Style.RESET_ALL}')
for hist_point in hist_data_1:
    print(hist_point)
print(f'{Style.BRIGHT}{Fore.GREEN}HISTDATA 2...{Style.RESET_ALL}')
for hist_point in hist_data_2:
    print(hist_point)
print(f'{Style.BRIGHT}{Fore.GREEN}HISTDATA 3...{Style.RESET_ALL}')
for hist_point in hist_data_3:
    print(hist_point)
print(f'{Style.BRIGHT}{Fore.GREEN}HISTDATA 4...{Style.RESET_ALL}')
for hist_point in hist_data_4:
    print(hist_point)

# Testing conversion to pandas dataframe
df = pd.DataFrame(hist_data_1)
