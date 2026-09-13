"""
excel_reader.py
Reads the finished DCF output straight out of Infosys_DCF_Model.xlsx and
prints a short summary — the "automation on top" layer of the project.

Run locally, after opening the workbook in Excel at least once so the
formulas have cached values (openpyxl can't compute formulas itself):

    pip install openpyxl
    python excel_reader.py
"""

import openpyxl

FILEPATH = "data/Infosys_DCF_Model.xlsx"

# These map to the row numbers in the DCF tab as built by build_model.py.
# If you add/remove rows in Excel, update these to match.
CELLS = {
    "Enterprise Value (₹ Cr)": "B18",
    "Equity Value (₹ Cr)": "B21",
    "Implied Share Price (₹)": "B25",
    "Current Share Price (₹)": "B26",
    "Upside / (Downside)": "B27",
    "Recommendation": "B28",
}


def read_dcf_output(filepath=FILEPATH):
    wb = openpyxl.load_workbook(filepath, data_only=True)  # data_only=True -> cached values, not formula text
    dcf_sheet = wb["DCF"]

    values = {label: dcf_sheet[cell].value for label, cell in CELLS.items()}

    if values["Implied Share Price (₹)"] is None:
        print("No cached values found. Open the workbook in Excel/LibreOffice, let it")
        print("recalculate, save, and re-run this script.")
        return

    print(f"{'Infosys (INFY.NS) — DCF Summary':^45}")
    print("-" * 45)
    print(f"Enterprise Value : ₹{values['Enterprise Value (₹ Cr)']:,.0f} Cr")
    print(f"Equity Value     : ₹{values['Equity Value (₹ Cr)']:,.0f} Cr")
    print(f"Implied Price    : ₹{values['Implied Share Price (₹)']:,.2f}")
    print(f"Current Price    : ₹{values['Current Share Price (₹)']:,.2f}")
    print(f"Upside/Downside  : {values['Upside / (Downside)']:.1%}")
    print(f"Recommendation   : {values['Recommendation']}")


if __name__ == "__main__":
    read_dcf_output()
