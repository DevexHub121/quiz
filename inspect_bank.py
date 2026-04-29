import pandas as pd
import os

FILE = 'data/Question Bank.xlsx'

def inspect_bank():
    if not os.path.exists(FILE):
        print(f"File not found: {FILE}")
        return
        
    xls = pd.ExcelFile(FILE)
    print(f"Sheets: {xls.sheet_names}")
    
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet)
        print(f"\n--- Sheet: {sheet} ---")
        print(f"Columns: {df.columns.tolist()}")
        print(f"Rows: {len(df)}")
        if not df.empty:
            print("First row sample:")
            print(df.iloc[0].to_dict())

if __name__ == "__main__":
    inspect_bank()
