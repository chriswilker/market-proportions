import argparse
import yaml
from typing import Dict
import urllib.request
import json


def main() -> None:
    parser = argparse.ArgumentParser(
        description="""Estimate the current market proportions of assets in a
        portfolio. See https://github.com/chriswilker/market_proportions for
        more information.
        """
    )
    parser.add_argument(
        "portfolio_file",
        type=str,
        help="path to a yaml file representing a portfolio",
    )
    args = parser.parse_args()

    with open(args.portfolio_file, "r") as stream:
        try:
            portfolio = yaml.safe_load(stream)
            print(market_proportions_output(portfolio), end="")
        except yaml.YAMLError as e:
            print(e)


def output(portfolio: Dict) -> str:
    mps = market_proportions(portfolio)
    out = ""
    for asset in mps.keys():
        mp = mps[asset]
        market_percent = mp * 100
        out += f"{asset}: {market_percent:.2f}%\n"
    return out


def market_proportions(portfolio: Dict) -> Dict:
    mcs = market_caps(portfolio)
    sum_mcs = sum([mcs[asset] for asset in mcs.keys()])
    mps = {}
    for asset in mcs.keys():
        mps[asset] = mcs[asset] / sum_mcs
    return mps


def market_caps(portfolio: Dict) -> Dict:
    mcs = {}
    for asset in portfolio.keys():
        mcs[asset] = market_cap(portfolio[asset])
    return mcs


def market_cap(asset: Dict) -> float:
    return asset["market cap"] * (
        current_price(asset["ticker"]) / asset["close price"]
    )


def current_price(ticker: str) -> float:
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={ticker}"
    contents = urllib.request.urlopen(url).read()
    response = json.loads(contents)["quoteResponse"]
    error = response["error"]
    if error:
        raise ValueError(f"Response from {url} contains an error:\n{error}")
    else:
        return response["result"][0]["regularMarketPrice"]


if __name__ == "__main__":
    main()
