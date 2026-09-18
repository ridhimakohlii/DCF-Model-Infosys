# Infosys - DCF Valuation Model

A DCF valuation model for Infosys, built primarily in Excel, with Python
automation for data retrieval and output readback. Given a set of
assumptions, the model forecasts 5 years of unlevered free cash flow,
computes WACC via CAPM, discounts everything back, and outputs an implied
share price with a BUY / HOLD / SELL call.

**Result:** Implied price of ₹1,227.91 vs. ₹1,100 market price → 11.6% upside → HOLD recommendation

## What's in this repository

```
dcf-project/
├── data_pull.py             # pulls Infosys financials via yfinance -> data/company_financials.xlsx
├── excel_reader.py          # reads the finished DCF tab and prints a summary
├── data/
│   └── Infosys_DCF_Model.xlsx   # the model itself
└── README.md
```

## The model (`Infosys_DCF_Model.xlsx`)

| Tab | Purpose |
|---|---|
| Instructions | Color legend, what to refresh, what's out of scope |
| Historicals | FY2022–FY2026 actuals (revenue, EBIT, tax, debt, cash, capex) |
| Assumptions | Every input the model uses - the only tab you should edit |
| Forecast | 5-year projection (FY2027–FY2031) of unlevered FCF |
| WACC | Cost of equity (CAPM) + after-tax cost of debt, blended |
| DCF | Discounts FCF, adds terminal value, outputs implied price + call |

**Color convention:** blue = hardcoded input, black = formula, green = link
to another tab, yellow fill = review/refresh before trusting the output.

## Methodology

- **Revenue growth**: fades linearly from a Year-1 rate (near FY26's actual
  growth) down to a Year-5 long-run rate, rather than a single flat number -
  reflects that hyper-growth years don't repeat indefinitely.
- **EBIT margin**: held flat at the 5-year historical average.
- **Unlevered FCF** = NOPAT + D&A − Capex − ΔNWC.
- **WACC**: CAPM for cost of equity (risk-free rate + beta × equity risk
  premium), blended with after-tax cost of debt, weighted by market value of
  equity and debt. Infosys carries very little debt, so WACC is close to
  cost of equity.
- **Terminal value**: Gordon Growth only (`FCF₅ × (1+g) / (WACC − g)`).
- **Recommendation**: upside/downside vs. current price against a ±15%
  threshold (edit in Assumptions).

## Assumptions used and why

| Assumption | Value | Basis |
|---|---|---|
| Revenue growth (Y1 → Y5) | 9% → 7% | Near FY26 actual growth, fading to a long-run IT-services rate |
| EBIT margin | 22.8% | 5-year historical average |
| Tax rate | 27% | ~5-year average effective tax rate |
| Terminal growth | 4% | Proxy for long-run India nominal growth |
| Risk-free rate | 6.9% | India 10Y G-Sec yield - **refresh before real use** |
| Equity risk premium | 6.5% | India country ERP estimate - **refresh before real use** |
| Beta | 0.75 | Approximate - **recompute or refresh before real use** |

## Known limitations (

- **No sensitivity table.** The model outputs one point estimate. A WACC ×
  terminal-growth grid would show how fragile that estimate is - a natural
  v2 addition.
- **Single terminal value method.** Only Gordon Growth; an exit-multiple
  cross-check would catch cases where the two methods disagree sharply.
- **Flat EBIT margin.** A more detailed model would build margins up from
  individual cost lines (S&A, R&D) rather than one blended percentage.
- **D&A and ΔNWC assumptions are placeholders** (marked yellow) - pulled
  approximately, not from the exact cash flow statement breakout. Refresh
  with the precise figures from the annual report before relying on this.
- **Manual refresh.** Historicals are pasted from a Python pull, not
  live-linked - the workbook doesn't update itself.

  ## Output 

```
Infosys (INFY.NS) - DCF Summary
---------------------------------------------
Enterprise Value : ₹503,379 Cr
Equity Value     : ₹508,357 Cr
Implied Price    : ₹1,227.91
Current Price    : ₹1,100.00
Upside/Downside  : 11.6%
Recommendation   : HOLD
```

**Execution Tips**

## How to refresh the data

```bash
pip install yfinance pandas openpyxl
python data_pull.py
```

This writes `data/company_financials.xlsx` with the latest income
statement, balance sheet, cash flow, price, beta, and shares outstanding.
Copy the relevant numbers into the `Historicals` and `Assumptions` tabs of
`Infosys_DCF_Model.xlsx` - the row labels yfinance uses can shift slightly
between pulls, so check them rather than assuming positions match.

## How to read the output from Python

```bash
python excel_reader.py
```

Prints Enterprise Value, Equity Value, Implied Price, Current Price,
Upside/Downside, and the Recommendation straight from the `DCF` tab.
(Open the workbook in Excel/LibreOffice at least once after editing so the
formulas have cached values - `openpyxl` reads cached values, it doesn't
compute formulas itself.)

