import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Fortune Express Cargo - LR Generator", layout="wide")

DATA_FILE = "lr_database.csv"

if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["LR_No", "Date", "Consignor", "Consignor_GST", "Consignee", "From", "To", "Packages", "Goods", "Freight"])
    df.to_csv(DATA_FILE, index=False)

st.title("🚛 FORTUNE EXPRESS CARGO - LR GENERATOR")

df = pd.read_csv(DATA_FILE)
next_lr = 3294 if df.empty else int(df["LR_No"].max()) + 1

st.subheader("નવી LR એન્ટ્રી કરો (Create New LR)")

with st.form("lr_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        lr_no = st.number_input("LR Number", value=next_lr, disabled=True)
        date = st.date_input("Date", datetime.now())
        consignor = st.text_input("Consignor Name", "IFFCO - MC CROP SCIENCE PVT LTD")
        consignor_gst = st.text_input("Consignor GST", "24AADCI9008G1ZR")
        from_place = st.text_input("From", "Aslali")
        
    with col2:
        consignee = st.text_input("Consignee Name", "VALSAD VIBHAG FARMER")
        to_place = st.text_input("To", "Valsad")
        packages = st.text_input("No. of Packages", "3 BOXES")
        goods = st.text_input("Goods Description", "PESTICIDES")
        freight = st.number_input("Total Freight (GST સાથે)", value=240.00)

    submit = st.form_submit_button("SAVE & PREVIEW LR")

if submit:
    new_data = pd.DataFrame([[lr_no, date, consignor, consignor_gst, consignee, from_place, to_place, packages, goods, freight]], 
                            columns=df.columns)
    new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)
    st.success(f"✅ LR No. {lr_no} સફળતાપૂર્વક સેવ થઈ ગયું છે!")
    
    # Store current entry in session state for printing
    st.session_state['current_lr'] = {
        "lr_no": lr_no, "date": str(date), "consignor": consignor, 
        "consignor_gst": consignor_gst, "consignee": consignee, 
        "from": from_place, "to": to_place, "packages": packages, 
        "goods": goods, "freight": freight
    }

if 'current_lr' in st.session_state:
    data = st.session_state['current_lr']
    st.markdown("---")
    st.subheader(f"📄 LR Copy - No. {data['lr_no']}")
    
    # Simple HTML Slip Format for Web Printing
    html_slip = f"""
    <div id="printableArea" style="border: 2px solid black; padding: 15px; font-family: Arial;">
        <h2 style="text-align: center; margin:0;">FORTUNE EXPRESS CARGO</h2>
        <p style="text-align: center; margin: 2px;">15, Bhagwan Estate, Opp. Ekta Hotel Lane, Aslali - 382427</p>
        <hr>
        <table style="width: 100%;">
            <tr><td><b>LR No:</b> {data['lr_no']}</td><td><b>Date:</b> {data['date']}</td></tr>
            <tr><td><b>From:</b> {data['from']}</td><td><b>To:</b> {data['to']}</td></tr>
            <tr><td><b>Consignor:</b> {data['consignor']} ({data['consignor_gst']})</td><td><b>Consignee:</b> {data['consignee']}</td></tr>
            <tr><td><b>Packages:</b> {data['packages']}</td><td><b>Goods:</b> {data['goods']}</td></tr>
            <tr><td><b>Total Freight:</b> ₹{data['freight']}</td><td><b>Status:</b> PAID</td></tr>
        </table>
    </div>
    """
    st.components.v1.html(html_slip, height=220)
    
    # Print Button Instruction
    st.info("💡 **Print निकालने का तरीका:** कीबोर्ड पर **Ctrl + P** दबाएं और Printer सिलेक्ट करके Print निकाल लें या **Save as PDF** चुन लें।")

st.markdown("---")
st.subheader("📊 જુનો બધો ડેટા (Saved LR History)")
st.dataframe(pd.read_csv(DATA_FILE), use_container_width=True)
