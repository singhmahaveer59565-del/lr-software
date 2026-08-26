import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Fortune Express Cargo - LR Generator", layout="wide")

# File to store data
DATA_FILE = "lr_database.csv"

if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["LR_No", "Date", "Consignor", "Consignor_GST", "Consignee", "From", "To", "Packages", "Goods", "Freight"])
    df.to_csv(DATA_FILE, index=False)

st.title("🚛 FORTUNE EXPRESS CARGO - LR GENERATOR")

# Load existing data to calculate next LR number
df = pd.read_csv(DATA_FILE)
next_lr = 3294 if df.empty else int(df["LR_No"].max()) + 1

st.subheader("નવી LR એન્ટ્રી કરો (Create New LR)")

with st.form("lr_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        lr_no = st.number_input("LR Number", value=next_lr, disabled=True)
        date = st.date_input("Date", datetime.now())
        consignor = st.text_input("Consignor Name (મોકલનાર)", "IFFCO - MC CROP SCIENCE PVT LTD")
        consignor_gst = st.text_input("Consignor GST", "24AADCI9008G1ZR")
        from_place = st.text_input("From (ક્યાંથી)", "Aslali")
        
    with col2:
        consignee = st.text_input("Consignee Name (મેળવનાર)", "VALSAD VIBHAG FARMER")
        to_place = st.text_input("To (ક્યાં સુધી)", "Valsad")
        packages = st.text_input("No. of Packages", "3 BOXES")
        goods = st.text_input("Goods Description", "PESTICIDES")
        freight = st.number_input("Total Freight (GST સાથે)", value=240.00)

    submit = st.form_submit_button("SAVE & GENERATE LR")

if submit:
    new_data = pd.DataFrame([[lr_no, date, consignor, consignor_gst, consignee, from_place, to_place, packages, goods, freight]], 
                            columns=df.columns)
    new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)
    st.success(f"✅ LR No. {lr_no} સફળતાપૂર્વક સેવ થઈ ગયું છે!")

st.markdown("---")
st.subheader("📊 જુનો બધો ડેટા (Saved LR History)")
st.dataframe(pd.read_csv(DATA_FILE), use_container_width=True)