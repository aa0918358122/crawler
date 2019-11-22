import requests

a = requests.get('https://www.cna.com.tw/list/aipl.aspx')
print(type(a.text))
