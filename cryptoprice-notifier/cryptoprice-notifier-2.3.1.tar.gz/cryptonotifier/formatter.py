# Function to format the Crypto Price Response for different destinations
def response_formatter(crypto_logs, event, curr):
    rows = []
    curr = curr.upper()

    # Currency Symbol Formatter
    symbol = '₹'
    if curr == 'INR':
        symbol = '₹'
    elif curr == 'EUR':
        symbol = '€'
    elif curr == 'USD':
        symbol = '$'
    elif curr == 'GBP':
        symbol = '£'

    if(event == 'telegram'):
        for crypto_value in crypto_logs:
            date = crypto_value['date'].strftime('%d.%m.%Y %H:%M')
            value = crypto_value['crypto_current_price']
            row = '{}: {} <b>{}</b>'.format(date, symbol, value)
            rows.append(row)
        data = '<br>'.join(rows)
        data += '<br><br>Happy Earning'
        return data
    else:
        for crypto_value in crypto_logs:
            date = crypto_value['date'].strftime('%d.%m.%Y %H:%M')
            value = crypto_value['crypto_current_price']
            row = '{}: {} {}'.format(date, symbol, value)
            rows.append(row)
        data = '\n'.join(rows)
        data += '\n\nHappy Earning'
        return data
