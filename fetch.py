import urllib.request
import json
import re

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


for fundSymbol in ("VUSXX", "VMRXX", "VMFXX"):
    print(fundSymbol, getVanguardMutualFundYield(fundSymbol))

print("Wealthfront", getWealthfrontAPY())