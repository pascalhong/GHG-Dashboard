import pandas as pd

file = "GHG_Template_Sanitized_Fictional.xlsx"

tabs = [
    "🔌Electricity",
    "⛽Fuels",
    "🚛Freight",
    "✈️Business Travel",
    "🗑️Waste"
]

dfs = []

for tab in tabs:
    df = pd.read_excel(file, sheet_name=tab)
    df["Source"] = tab  # wichtig!
    dfs.append(df)

master_df = pd.concat(dfs, ignore_index=True)

# speichern
master_df.to_excel("master_data.xlsx", index=False)

print(master_df.head())