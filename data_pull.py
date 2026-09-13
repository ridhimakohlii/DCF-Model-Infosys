"""
data_pull.py
Pulls Infosys (NSE: INFY) financial statements via yfinance and saves them
to an Excel file so you can refresh the Historicals/Assumptions tabs of
Infosys_DCF_Model.xlsx with current numbers.

Run locally (this needs internet access to Yahoo Finance, which the sandbox
that built this template does not have):

    pip install yfinance pandas openpyxl
    python data_pull.py
"""

import yfinance as yf
import pandas as pd

# Use the NSE-listed ticker so figures come back in INR (crores/absolute rupees),
# matching the Excel model. INFY (no suffix) is the NYSE ADR and reports in USD —
# don't mix the two without converting.
TICKER = "INFY.NS"


def get_financials(ticker):
    company = yf.Ticker(ticker)

    income_stmt = company.financials       # annual, most recent ~4 years
    balance_sheet = company.balance_sheet
    cash_flow = company.cashflow

    info = company.info
    current_price = info.get("currentPrice")
    shares_out = info.get("sharesOutstanding")
    beta = info.get("beta")
    market_cap = info.get("marketCap")

    return income_stmt, balance_sheet, cash_flow, current_price, shares_out, beta, market_cap


def save_to_excel(ticker):
    income_stmt, balance_sheet, cash_flow, price, shares, beta, mcap = get_financials(ticker)

    with pd.ExcelWriter("data/company_financials.xlsx") as writer:
        income_stmt.to_excel(writer, sheet_name="Income Statement")
        balance_sheet.to_excel(writer, sheet_name="Balance Sheet")
        cash_flow.to_excel(writer, sheet_name="Cash Flow")

        summary = pd.DataFrame({
            "Metric": ["Current Price (INR)", "Shares Outstanding", "Beta", "Market Cap (INR)"],
            "Value": [price, shares, beta, mcap],
        })
        summary.to_excel(writer, sheet_name="Summary", index=False)

    print(f"Saved data for {ticker} to data/company_financials.xlsx")
    print("\nQuick check — copy these into Assumptions tab (yellow cells):")
    print(f"  Current share price : {price}")
    print(f"  Beta                : {beta}")
    print(f"  Shares outstanding  : {shares}")
    print(f"  Market cap          : {mcap}")
    print("\nNote: row labels from yfinance (e.g. 'Total Revenue', 'EBIT', 'Total Debt')")
    print("can shift slightly between refreshes — open the file and confirm the")
    print("label before pasting a number into Historicals.")


if __name__ == "__main__":
    save_to_excel(TICKER)
