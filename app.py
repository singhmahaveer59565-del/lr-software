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

    submit = st.form_submit_button("SAVE & GENERATE ORIGINAL LR")

if submit:
    new_data = pd.DataFrame([[lr_no, str(date), consignor, consignor_gst, consignee, from_place, to_place, packages, goods, freight]], 
                            columns=df.columns)
    new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)
    st.success(f"✅ LR No. {lr_no} સફળતાપૂર્વક સેવ થઈ ગયું છે!")
    
    # Calculate Tax Splits
    base_freight = round(freight / 1.18, 2)
    cgst = round((freight - base_freight) / 2, 2)
    sgst = round(freight - base_freight - cgst, 2)

    st.session_state['lr_html'] = {
        "lr_no": lr_no, "date": str(date), "consignor": consignor, 
        "consignor_gst": consignor_gst, "consignee": consignee, 
        "from": from_place, "to": to_place, "packages": packages, 
        "goods": goods, "freight": freight, "base_freight": base_freight,
        "cgst": cgst, "sgst": sgst
    }

if 'lr_html' in st.session_state:
    d = st.session_state['lr_html']
    
    def get_copy_html(copy_title):
        return f"""
        <div style="border: 2px solid #000; padding: 5px; margin-bottom: 15px; background: #fff; font-family: Arial; font-size: 11px;">
            <div style="background: #000; color: #fff; text-align: center; font-weight: bold; font-size: 10px; padding: 2px 0; margin-bottom: 4px;">
                કાચ, પ્લાસ્ટીક, ફાયબર અથવા લીક્વીડ માલ ડેમેજ અથવા લીક થાય તો તેની જવાબદારી કંપનીની રહેશે નહીં.
            </div>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="width: 50%; vertical-align: top;">
                        <h2 style="margin: 0; font-size: 18px; font-weight: 900;">FORTUNE EXPRESS CARGO</h2>
                        <i style="font-size: 10px;">Always on Time</i><br>
                        <b>E-mail :</b> fortuneexpresscargo@gmail.com | <b>M. :</b> 9173165886<br>
                        <b>Add :</b> 15, Bhagwan Estate, Opp. Ekta Hotel Lane, Aslali - 382427
                    </td>
                    <td style="width: 25%; vertical-align: top; font-size: 10px;">
                        <b>PAN No. :</b> AGVPM3701F<br>
                        <b>GST No. :</b> 24AGVPM3701F2ZF<br>
                        <b>SAC No. :</b> 9965<br><br>
                        <span style="border: 1px solid #000; padding: 2px 5px; background: #eee; font-weight: bold;">{copy_title}</span>
                    </td>
                    <td style="width: 25%; vertical-align: top; text-align: center;">
                        <div style="border: 1.5px solid #000; padding: 3px;">
                            <div style="font-size: 9px; font-weight: bold;">DOCKET NUMBER</div>
                            <div style="font-size: 20px; font-weight: bold; color: #d32f2f;">{d['lr_no']}</div>
                            <div style="font-size: 10px;"><b>DATE :</b> {d['date']}</div>
                        </div>
                        <table style="width: 100%; border: 1px solid #000; margin-top: 3px; font-size: 10px; text-align: left;">
                            <tr><td style="border: 1px solid #000;"><b>FROM:</b> {d['from']}</td></tr>
                            <tr><td style="border: 1px solid #000;"><b>TO:</b> {d['to']}</td></tr>
                        </table>
                    </td>
                </tr>
            </table>

            <table style="width: 100%; border-collapse: collapse; margin-top: 4px; border: 1px solid #000;">
                <tr>
                    <td style="width: 50%; border: 1px solid #000; padding: 4px; vertical-align: top;">
                        <b>CONSIGNOR DETAILS (PLACE OF SUPPLY)</b><br>
                        <b>NAME:</b> {d['consignor']}<br>
                        <b>GST NO.:</b> {d['consignor_gst']}
                    </td>
                    <td style="width: 50%; border: 1px solid #000; padding: 4px; vertical-align: top;">
                        <b>CONSIGNEE DETAILS (DELIVERY DESTINATION)</b><br>
                        <b>NAME:</b> {d['consignee']}<br>
                        <b>INSTRUCTION:</b> Handle with Care ({d['goods']})
                    </td>
                </tr>
            </table>

            <table style="width: 100%; border-collapse: collapse; margin-top: 4px; border: 1px solid #000; font-size: 10px;">
                <tr style="background: #f0f0f0; text-align: center;">
                    <th style="border: 1px solid #000; width: 45%;" colspan="3">PACKAGE INFORMATION</th>
                    <th style="border: 1px solid #000; width: 25%;" colspan="2">IN RUPEES</th>
                    <th style="border: 1px solid #000; width: 10%;">Monthly Billing</th>
                    <th style="border: 1px solid #000; width: 10%;">PAID</th>
                    <th style="border: 1px solid #000; width: 10%;">TO PAY</th>
                </tr>
                <tr>
                    <td style="border: 1px solid #000; text-align: center;"><b>{d['packages']}</b></td>
                    <td style="border: 1px solid #000; text-align: center;"><b>-</b></td>
                    <td style="border: 1px solid #000; text-align: center;"><b>-</b></td>
                    <td style="border: 1px solid #000;">BASIC FREIGHT</td>
                    <td style="border: 1px solid #000; text-align: right;">{d['base_freight']:.2f}</td>
                    <td style="border: 1px solid #000;" rowspan="6"></td>
                    <td style="border: 1px solid #000; text-align: center; font-size: 18px; color: green; font-weight: bold;" rowspan="6">✔</td>
                    <td style="border: 1px solid #000;" rowspan="6"></td>
                </tr>
                <tr>
                    <td style="border: 1px solid #000; padding: 4px;" colspan="3" rowspan="5">
                        <b>GOODS DESCRIPTION:</b> {d['goods']}<br>
                        <b>NO OF PACKAGES:</b> {d['packages']}
                    </td>
                    <td style="border: 1px solid #000;">Total</td>
                    <td style="border: 1px solid #000; text-align: right;"><b>{d['base_freight']:.2f}</b></td>
                </tr>
                <tr><td style="border: 1px solid #000;">CGST (9%)</td><td style="border: 1px solid #000; text-align: right;">{d['cgst']:.2f}</td></tr>
                <tr><td style="border: 1px solid #000;">SGST (9%)</td><td style="border: 1px solid #000; text-align: right;">{d['sgst']:.2f}</td></tr>
                <tr><td style="border: 1px solid #000;">IGST</td><td style="border: 1px solid #000; text-align: right;">0.00</td></tr>
                <tr style="background: #f0f0f0; font-weight: bold;">
                    <td style="border: 1px solid #000;">GRAND TOTAL</td>
                    <td style="border: 1px solid #000; text-align: right;">{d['freight']:.2f}</td>
                </tr>
            </table>

            <div style="font-size: 8px; margin-top: 4px; text-align: justify;">
                (૧) પેક દાગીનામાં રહેલા માલ માટેની પરમીટ સંબંધી અગર ગેરકાયદેસર માલ માટેની જવાબદારી કંપનીની રહેશે નહીં. (૨) આગ, ચોરી, વરસાદ, અકસ્માત વગેરેમાં વીમો ઉતરાવી લેવો. (૩) ૭ દિવસમાં ફરિયાદ કરવી. (૪) વાપી ન્યાયનું કેન્દ્ર રહેશે.
            </div>
        </div>
        """

    full_html = get_copy_html("CONSIGNOR COPY (મોકલનાર કોપી)") + get_copy_html("CONSIGNEE COPY (મેળવનાર કોપી)") + get_copy_html("DRIVER COPY (ગાડી કોપી)")

    st.markdown("---")
    st.components.v1.html(full_html, height=1200, scrolling=True)
    st.info("💡 **Print निकालने के लिए:** अपने कीबोर्ड पर **Ctrl + P** दबाएं!")

st.markdown("---")
st.subheader("📊 જુનો બધો ડેટા (Saved LR History)")
st.dataframe(pd.read_csv(DATA_FILE), use_container_width=True)
