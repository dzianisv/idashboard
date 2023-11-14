#!/usr/bin/env python3

import urllib.request
from bs4 import BeautifulSoup
import json
import re
import dataclasses


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15'
}
class requests   :
    @dataclasses.dataclass
    class Response:
        status_code: int
        text: str

    @staticmethod
    def get(url):
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request) as response:
            print(response.read())
            data = json.loads(response.read().decode())
            return Response(status_code=response.status, text=data)

def getVanguardMutualFundYield(symbol: str) -> float:
    url = f'https://investor.vanguard.com/investment-products/mutual-funds/profile/api/{symbol}/price'

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        yeild = float(data["currentPrice"]["yield"]["yieldPct"])
        return yeild

def getWealthfrontAPY() -> float:
    url =  "https://www.wealthfront.com/cash"

    with urllib.request.urlopen(url) as response:
        m = re.search(r"(\d+\.\d+)\% APY", response.read().decode('utf8'))
        if m:
            apy = float(m[1])
            if 0 < apy < 100:
                return apy

    return None

def guessAPY(url='https://www.ufbdirect.com/'):
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    # This is a basic method, which assumes that APY might be in a format like "x.xx% APY".
    # The exact logic might need to be adjusted based on the structure and content of the webpage.
    potential_matches = soup.find_all(text=True)
    for match in potential_matches:
        if ' APY' in match and '%' in match:
            return match.strip()

    return None

def getFidelityMutualFundAPY(url):
    apySelector = '#summary-card-container > div:nth-child(6) > div > portfolio-data-template > div > div > div > div:nth-child(1) > p.portfolio-data--ind-value.ng-binding.ng-scope'
    nameSelector = 'body > div.mfl-app.ng-scope > div > div > div > header-template > div.data-card.no-padding > div.header-container > div.header-container--search.header-search--width-5 > div.header-container--search-info.RETAIL > div:nth-child(1) > h1'

    with urllib.request.urlopen(url) as response:
        html_content = response.read()


    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Use the CSS selector to find the desired element and extract its text content
    apy = soup.select_one(apySelector).text
    name = soup.slect_one(nameSelector).text
    return name, apy


for fundSymbol in ("VUSXX", "VMRXX", "VMFXX"):
    print(fundSymbol, getVanguardMutualFundYield(fundSymbol))

# print(getFidelityMutualFundAPY('https://fundresearch.fidelity.com/mutual-funds/summary/316341304'))

print("Wealthfront", getWealthfrontAPY())
#print("UFB Direct", guessAPY())
