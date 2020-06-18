# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytse_client', 'pytse_client.data', 'pytse_client.examples']

package_data = \
{'': ['*'], 'pytse_client.examples': ['tickers_data/*']}

install_requires = \
['pandas', 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'pytse-client',
    'version': '0.3.1',
    'description': 'tehran stock exchange(TSE) client in python',
    'long_description': '# pyTSEClient (python tse client)\n&rlm;\nبا استفاده از این پکیج میتونید به دیتای بازار بورس تهران در پایتون دسترسی داشته باشید.\n&rlm;\n\n&rlm;\nهدف حل مشکلات گرفتن اطلاعات بروز از سایت بازار بورس تهران هست.\n&rlm;\n\n## قابلیت ها\n * دریافت اطلاعات روز های معاملاتی هر سهم و قابلیت ذخیره سازی\n * قابلیت گرفتن اطلاعات یک سهام مانند گروه سهام و اطلاعات معاملات حقیقی و حقوقی\n * دریافت اطلاعات فاندامنتال یک نماد شامل(eps, p/e ,حجم مبنا)\n\n## نصب \n```bash\npip install pytse-client \n```\n\n## نحوه استفاده\n### دانلود سابقه سهم ها\nبا استفاده از این تابع میتوان سابقه سهام هارو دریافت کرد و هم اون رو ذخیره و هم توی کد استفاده کرد\n```python\nimport pytse_client as tse\ntickers = tse.download(symbols="all", write_to_csv=True)\ntickers["ولملت"] # history\n\n            date     open     high  ...     volume  count    close\n0     2009-02-18   1050.0   1050.0  ...  330851245    800   1050.0\n1     2009-02-21   1051.0   1076.0  ...  335334212   6457   1057.0\n2     2009-02-22   1065.0   1074.0  ...    8435464    603   1055.0\n3     2009-02-23   1066.0   1067.0  ...    8570222    937   1060.0\n4     2009-02-25   1061.0   1064.0  ...    7434309    616   1060.0\n...          ...      ...      ...  ...        ...    ...      ...\n2323  2020-04-14   9322.0   9551.0  ...  105551315  13536   9400.0\n2324  2020-04-15   9410.0   9815.0  ...  201457026  11322   9815.0\n2325  2020-04-18  10283.0  10283.0  ...  142377245   8929  10283.0\n2326  2020-04-19  10797.0  10797.0  ...  292985635  22208  10380.0\n2327  2020-04-20  10600.0  11268.0  ...  295590437  16313  11268.0\n```\nسابقه سهم توی فایلی با اسم سهم نوشته میشه `write_to_csv=True` همچنین با گذاشتن\n\nاست `Dataframe` سابقه سهم در قالب\n\n\nبرای دانلود سابقه یک یا چند سهم کافی هست اسم اون ها به تابع داده بشه:\n```python\nimport pytse_client as tse\ntse.download(symbols="وبملت", write_to_csv=True)\ntse.download(symbols=["وبملت", "ولملت"], write_to_csv=True)\n```\n\n### Ticker ماژول\n&rlm;\nاین ماژول برای کار با دیتای یک سهم خاص هست و با گرفتن نماد اطلاعات موجود رو میده\n\n\nبرای مثال:\n&rlm;\n```python\nimport pytse_client as tse\n\ntse.download(symbols="وبملت", write_to_csv=True)  # optional\nticker = tse.Ticker("وبملت")\nprint(ticker.history)  # سابقه قیمت سهم\nprint(ticker.client_types)  # حقیقی حقوقی\nprint(ticker.title)  # نام شرکت\nبانك ملت (وبملت)\nprint(ticker.url)  # آدرس صفحه سهم\nhttp://tsetmc.com/Loader.aspx?ParTree=151311&i=778253364357513\nprint(ticker.group_name)  # نام گروه\nبانكها و موسسات اعتباري\nprint(ticker.eps)  # eps\n2725.0\nprint(ticker.p_e_ratio)  # P/E\n6.1478899082568805\nprint(ticker.group_p_e_ratio)  # group P/E\n18.0\nprint(ticker.base_volume)  # حجم مبنا\n7322431.0\nprint(ticker.last_price)  # آخرین معامله\n17316\nprint(ticker.adj_close)  # قیمت پایانی\n16753\n```\nبرای استفاده لازم نیست حتما تابع دانلود صدا زده بشه.\nاگر این کد رو بدون دانلود کردن سهم  استفاده کنید خودش اطلاعات سهم رو از سایت میگیره،\nاما اگر قبل از اون از دانلود استفاده کرده باشید\nبه جای گرفتن از اینترنت اطلاعات رو از روی فایل میخونه که سریع تر هست\n##### نکته\n&rlm;\nطبق تجربه\u200c ای که داشتم چون گاهی اوقات سایت بورس مدت زیادی طول میکشه تا اطلاعات رو بفرسته یا بعضی مواقع نمیفرسته بهتر هست که اول تابع دانلود رو استفاده کنید برای سهم هایی که لازم هست و بعد با دیتای اون ها کار کنید.\n&rlm;\n\n#### اطلاعات حقیقی و حقوقی\nاطلاعات خرید و فروش حقیقی و حقوقی سهام رو میشه از طریق `ticker.client_types` گرفت این اطلاعات یه DataFrame شامل اطلاعات موجود در تب حقیقی حقوقی(تب بنفشی که در این [صفحه](http://www.tsetmc.com/Loader.aspx?ParTree=151311&i=778253364357513) هست) سهم هست:\n```\ndate : تاریخ \nindividual_buy_count : تعداد معاملات خرید حقیقی\ncorporate_buy_count : تعداد معلاملات خرید حقوقی\nindividual_sell_count : تعداد معاملات فروش حقیقی\ncorporate_sell_count : تعداد معلاملات فروش حقوقی\nindividual_buy_vol : حجم خرید حقیقی\ncorporate_buy_vol : حجم خرید حقوقی\nindividual_sell_vol : حجم فروش حقیقی\ncorporate_sell_value : حجم فروش حقوقی\nindividual_buy_mean_price : قیمت میانگین خرید حقیقی\nindividual_sell_mean_price : قیمت میانگین فروش حقیقی\ncorporate_buy_mean_price : قیمت میانگین خرید حقوقی\ncorporate_sell_mean_price : قیمت میانگین فروش حقوقی\nindividual_ownership_change : تغییر مالکیت حقوقی به حقیقی\n```\n\n\n#### &rlm; پکیج های مورد نیاز: &rlm; \n* [Pandas](https://github.com/pydata/pandas)\n* [Requests](http://docs.python-requests.org/en/master/)\n#### &rlm; الهام گرفته از: &rlm; \n* tehran_stocks: https://github.com/ghodsizadeh/tehran-stocks\n* yfinance: https://github.com/ranaroussi/yfinance\n',
    'author': 'glyphack',
    'author_email': 'sh.hooshyari@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
