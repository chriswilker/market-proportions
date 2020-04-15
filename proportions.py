import argparse
import yaml
from typing import Dict
import urllib.request
import json
import dateutil.parser


def main() -> None:
    parser = argparse.ArgumentParser(
        description="""Estimate the current market proportions of assets in a
        portfolio. See https://github.com/chriswilker/market-proportions for
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
        portfolio = yaml.safe_load(stream)
        print(output(portfolio), end="")


def output(portfolio: Dict) -> str:
    mps = market_proportions(portfolio)
    out = ""
    for ticker, mp in mps.items():
        out += f'"{ticker}": {mp:.4f}\n'
    return out


def market_proportions(portfolio: Dict) -> Dict:
    mcs = market_caps(portfolio)
    sum_mcs = sum([mcs[ticker] for ticker in mcs.keys()])
    mps = {}
    for ticker in mcs.keys():
        mps[ticker] = mcs[ticker] / sum_mcs
    return mps


def market_caps(portfolio: Dict) -> Dict:
    mcs = {}
    for ticker in portfolio.keys():
        mcs[ticker] = market_cap(
            ticker, portfolio[ticker]["date"], portfolio[ticker]["market cap"]
        )
    return mcs


def market_cap(ticker: str, date: str, market_cap: int) -> float:
    return market_cap * (current_price(ticker) / close_price(ticker, date))


def close_price(ticker: str, date: str) -> float:
    dt = dateutil.parser.parse(date)
    start_unix_ts = int(dt.timestamp())
    # for some reason it works when 6h 30m is added, but not with anything less
    end_unix_ts = start_unix_ts + 23400
    url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={start_unix_ts}&period2={end_unix_ts}&interval=1d&events=history"
    csv_text = urllib.request.urlopen(url).read().decode("utf8")
    for line in csv_text.splitlines():
        if date in line:
            close_price = float(line.split(",")[4])
    return close_price


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
