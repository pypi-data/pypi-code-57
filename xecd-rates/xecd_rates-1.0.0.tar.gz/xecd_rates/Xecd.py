import requests
import lxml.html
import datetime

class Xecd(object):

    def __init__(self, options=dict()):
        self.options = dict(
            base_url='https://www.xe.com/currencytables/',
            timeout=None,
            user_agent=None,
            proxies=dict(),
            qs=dict()

        )
        self.options.update(options)

    def _get_html(self, ops):
        self.options.update(ops)
        url = self.options['base_url']
        params = self.options['qs']
        headers = {'User-Agent': self.options['user_agent']}
        proxies = self.options['proxies']
        timeout = self.options['timeout']

        res = requests.get(url=url, params=params, headers=headers, proxies=proxies, timeout=timeout)

        return res.content

    def _parse_html(self, html):
        root = lxml.html.fromstring(html)
        timestamp = root.xpath('//p[@class ="historicalRateTable-date"]/text()')[0]
        _from = root.xpath('//option[@selected ="selected"]/@value')[0]
        table = root.xpath('//table[ @id ="historicalRateTbl"]')[0]

        currency_rates = table.xpath('./tbody/tr/td//text()')
        currency_rates = [currency_rates[i:i + 4] for i in range(0, len(currency_rates), 4)]

        results = dict()
        results['timestamp'] = timestamp
        results['from'] = _from
        results['to'] = [{'quotecurrency': val[0], 'mid': val[2]} for val in currency_rates]

        return results

    def _date_range(self, sdate, edate):
        sdate = datetime.datetime.strptime(sdate, '%Y-%m-%d')
        edate = datetime.datetime.strptime(edate, '%Y-%m-%d')
        delta = edate - sdate
        for date in range(delta.days + 1):
            day = (sdate + datetime.timedelta(days=date)).date()
            yield day

    def _filter_results(self, results, flt):
        if flt == 'all':
            return results

        for i, result in enumerate(results['to']):
            if result['quotecurrency'] == flt:
                results['to'] = [results['to'][i]]
                return results

    def convert_from(self, _from, _to):

        ops = {'qs': {'from': _from, 'date': ''}}
        html = self._get_html(ops)
        results = self._parse_html(html)
        results = self._filter_results(results, _to)

        return results

    def historic_rate(self, _date, _from, _to):
        ops = {'qs': {'from': _from, 'date': _date}}
        html = self._get_html(ops)

        results = self._parse_html(html)
        results = self._filter_results(results, _to)

        return results

    def historic_rate_period(self, sdate, edate, _from, _to):
        results = {}
        results['from'] = _from
        results['to'] = {}

        data_range = self._date_range(sdate, edate)
        for date in data_range:
            result = self.historic_rate(date, _from, _to)
            for currencey in result['to']:
                try:
                    results['to'][currencey['quotecurrency']].append(
                        {'mid': currencey['mid'], 'timestamp': result['timestamp']})
                except:
                    results['to'][currencey['quotecurrency']] = [
                        {'mid': currencey['mid'], 'timestamp': result['timestamp']}]

        return results
