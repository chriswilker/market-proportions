## Introduction
This is a script that estimates the current market proportions of assets
in a portfolio. These assets need to be tracked by stocks or ETFs and to
have a known market capitalization at some prior date.

For example, the total US stock market is tracked by multiple ETFs, and
its market capitalization is periodically published by index providers.

## Getting started
Install pyyaml and git clone the repository. Requires Python 3.6.

```sh
pip3 install pyyaml
git clone git@github.com:chriswilker/market-proportions.git
cd market-proportions
```

## Use
Give the path to a portfolio yaml file as an argument. The market
proportions of the assets in the portfolio will be displayed. In this
case, the relative sizes of the US and non-US stock markets are
displayed.

```console
$ python3 proportions.py example-portfolios/world-stock-market.yml
us stocks: 61.91%
non-us stocks: 38.09%
```

Run `python3 proportions.py -h` to get help.

## Creating a portfolio yaml file
The yaml file should be structured like this:

```yaml
"us stocks":
  "date": "2017-07-31"
  "market cap": 25089806
  "ticker": "VTSAX"
"non-us stocks":
  "date": "2017-07-31"
  "market cap": 20585441
  "ticker": "VTIAX"
```

You can give the assets whatever names you want. In this case, the
assets are named "us stocks" and "non-us stocks".

"date" is the date at which the market capitalization was measured. It
should be formatted in ISO 8601 format (YYYY-MM-DD).

"market cap" is the market capitalization of the asset at the date.
The units don't matter, as long as they are consistent with the units
for the market capitalizations of your other assets.

"ticker" is the ticker of the stock or ETF that tracks the asset.
For example, the ticker VTSAX represents the Vanguard Total Stock
Market Index ETF, which tracks the US stock market.
