# Copyright (c) [2025] [Yifu Ding]
import copy
import requests
import json
import common_data
from singleton_meta import SingletonMeta


class CurrencyCache(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.rate_cache = {}
        self.currency_list = []

    def initialize_rates(self):
        url = "https://api.frankfurter.dev/v1/latest?base=" + common_data.BASE_CURRENCY
        try:
            response = requests.get(url)
            response.raise_for_status()  # 检查请求是否成功
            data = response.json()
            self.currency_list = []
            self.currency_list = [key for key, value in data["rates"].items()]
            self.currency_list.append(common_data.BASE_CURRENCY)
            self.currency_list.sort()
            self.rate_cache = {}
            self.rate_cache = copy.deepcopy(data["rates"])
            self.rate_cache[common_data.BASE_CURRENCY] = 1.0
            return True
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            return False
        except json.JSONDecodeError as e:
            print(f"JSON 解析失败: {e}")
            return False
        except Exception as e:
            return False

    def get_rates(self, from_currency, to_currency):
        if from_currency not in self.currency_list or to_currency not in self.currency_list:
            return -1.0
        return self.rate_cache[to_currency] / self.rate_cache[from_currency]

currency_cache = CurrencyCache()
# 获取货币列表
# currencies = get_currencies()
#https://api.frankfurter.dev/v1/latest?base=USD
# # 打印货币列表
# if currencies:
#     for code, name in currencies.items():
#         print(f"{code}: {name}")# Limit the response to specific target currencies.
# /* curl -s https://api.frankfurter.dev/v1/latest?symbols=CHF,GBP */
# {
#   "base": "EUR",
#   "date": "2025-04-15",
#   "rates": {
#     "CHF": 0.9242,
#     "GBP": 0.8557
#   }
# }
# Available currencies
# Get supported currency symbols and their full names.
# /* curl -s https://api.frankfurter.dev/v1/currencies */
# {
#   "AUD": "Australian Dollar",
#   "BGN": "Bulgarian Lev",
#   "BRL": "Brazilian Real",
#   "CAD": "Canadian Dollar",
#   "...": "..."
# }
# Currency Conversion
# Perform currency conversion by fetching the exchange rate and calculating in your code.
# function convert(from, to, amount) {
#   fetch(`https://api.frankfurter.dev/v1/latest?base=${from}&symbols=${to}`)
#     .then((resp) => resp.json())
#     .then((data) => {
#       const convertedAmount = (amount * data.rates[to]).toFixed(2);
#       alert(`${amount} ${from} = ${convertedAmount} ${to}`);
#     });
#   }

# convert("EUR", "USD", 10);