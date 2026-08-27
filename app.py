import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Fortune Express Cargo - LR Generator", layout="wide")

DATA_FILE = "lr_database.csv"
PARTY_FILE = "party_database.csv"

# Safely initialize or reset corrupted databases
if os.path.exists(DATA_FILE):
    try:
        df = pd.read_csv(DATA_FILE)
    except Exception:
        os.remove(DATA_FILE)
        df = pd.DataFrame(columns=[
            "LR_No", "Date", "Consignor", "Consignor_GST", "Consignor_Contact", 
            "Consignee", "Consignee_GST", "Consignee_Contact", "From", "To", 
            "Packages", "Goods", "Eway_Bill", "Grand_Total", "Pay_Type"
        ])
        df.to_csv(DATA_FILE, index=False)
else:
    df = pd.DataFrame(columns=[
        "LR_No", "Date", "Consignor", "Consignor_GST", "Consignor_Contact", 
        "Consignee", "Consignee_GST", "Consignee_Contact", "From", "To", 
        "Packages", "Goods", "Eway_Bill", "Grand_Total", "Pay_Type"
    ])
    df.to_csv(DATA_FILE, index=False)

if os.path.exists(PARTY_FILE):
    try:
        df_party = pd.read_csv(PARTY_FILE)
    except Exception:
        os.remove(PARTY_FILE)
        df_party = pd.DataFrame(columns=["Name", "GST", "Contact"])
        df_party.to_csv(PARTY_FILE, index=False)
else:
    df_party = pd.DataFrame(columns=["Name", "GST", "Contact"])
    df_party.to_csv(PARTY_FILE, index=False)

st.title("🚛 FORTUNE EXPRESS CARGO - LR GENERATOR")

next_lr = 100 if df.empty or df["LR_No"].max() < 100 else int(df["LR_No"].max()) + 1

st.subheader("નવી LR એન્ટ્રી કરો (Create New LR)")

consignor_names = df_party["Name"].dropna().unique().tolist() if not df_party.empty else []

with st.form("lr_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        lr_no = st.number_input("LR Number / Docket Number", value=next_lr)
        date = st.date_input("Date", datetime.now(), format="DD/MM/YYYY")
        
        consignor = st.selectbox("Consignor Name (Place of Supply)", options=[""] + consignor_names, index=0)
        if not consignor:
            consignor = st.text_input("Or Type Consignor Name", "")
            
        consignor_gst = st.text_input("Consignor GST", "")
        consignor_contact = st.text_input("Consignor Contact / Pincode", "")
        from_place = st.text_input("From", "ASLALI (AHEM)")
        
    with col2:
        consignee = st.text_input("Consignee Name (Delivery Destination)", "")
        consignee_gst = st.text_input("Consignee GST", "")
        consignee_contact = st.text_input("Consignee Contact", "")
        to_place = st.text_input("To", "")
        instruction = st.text_input("Instruction", "")
        
    st.markdown("---")
    col3, col4 = st.columns(2)
    
    with col3:
        pkg_type = st.text_input("Type of Packaging", "BOX")
        no_pkg = st.text_input("No. of Packages", "1")
        volume = st.text_input("Volume (Inch)", "-")
        goods_desc = st.text_input("Goods Description", "")
        eway_bill = st.text_input("E-Way Bill No.", "")
        inv_no_val_wt = st.text_input("Invoice No. & Value | Weight Details", "")

    with col4:
        st.markdown("<b>Amount & GST Auto-Fill</b>", unsafe_allow_html=True)
        
        grand_total = st.number_input("Enter Grand Total (Total Amount)", value=0.0)
        
        gst_type = st.radio("GST Type", ["CGST + SGST (9% + 9%)", "IGST (18%)"], horizontal=True)
        
        if "CGST" in gst_type:
            total_freight = round(grand_total / 1.18, 2) if grand_total > 0 else 0.0
            cgst = round(total_freight * 0.09, 2)
            sgst = round(grand_total - total_freight - cgst, 2) if grand_total > 0 else 0.0
            igst = 0.0
        else:
            total_freight = round(grand_total / 1.18, 2) if grand_total > 0 else 0.0
            cgst = 0.0
            sgst = 0.0
            igst = round(grand_total - total_freight, 2) if grand_total > 0 else 0.0
            
        basic_freight = total_freight
        value_surcharge = 0.0
        docket_charges = 0.0
        other_charges = 0.0
        oda_charges = 0.0
        surcharges = 0.0
        
        pay_type = st.radio("Payment Status", ["Monthly Billing", "PAID", "TO PAY"], index=2)

    submit = st.form_submit_button("SAVE & GENERATE LR")

if submit:
    formatted_date = date.strftime("%d-%m-%Y")
    new_data = pd.DataFrame([[
        lr_no, formatted_date, consignor, consignor_gst, consignor_contact, 
        consignee, consignee_gst, consignee_contact, from_place, to_place, 
        no_pkg, goods_desc, eway_bill, grand_total, pay_type
    ]], columns=[
        "LR_No", "Date", "Consignor", "Consignor_GST", "Consignor_Contact", 
        "Consignee", "Consignee_GST", "Consignee_Contact", "From", "To", 
        "Packages", "Goods", "Eway_Bill", "Grand_Total", "Pay_Type"
    ])
    new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)

    if consignor and consignor not in consignor_names:
        new_party = pd.DataFrame([[consignor, consignor_gst, consignor_contact]], columns=["Name", "GST", "Contact"])
        new_party.to_csv(PARTY_FILE, mode='a', header=False, index=False)

    st.success(f"✅ LR No. {lr_no} સફળતાપૂર્વક સેવ થઈ ગયું છે!")

    st.session_state['lr_data'] = {
        "lr_no": lr_no, "date": date.strftime("%d-%m-%Y"), "consignor": consignor, "consignor_gst": consignor_gst,
        "consignor_contact": consignor_contact, "consignee": consignee, "consignee_gst": consignee_gst,
        "consignee_contact": consignee_contact, "from": from_place, "to": to_place, "instruction": instruction,
        "pkg_type": pkg_type, "no_pkg": no_pkg, "volume": volume, "goods_desc": goods_desc,
        "eway_bill": eway_bill, "inv_no_val_wt": inv_no_val_wt,
        "basic_freight": basic_freight, "value_surcharge": value_surcharge, "docket_charges": docket_charges,
        "other_charges": other_charges, "oda_charges": oda_charges, "surcharges": surcharges,
        "total_freight": total_freight, "cgst": cgst, "sgst": sgst, "igst": igst, "grand_total": grand_total,
        "pay_type": pay_type
    }

if 'lr_data' in st.session_state:
    d = st.session_state['lr_data']

    def get_receipt_html(copy_title):
        paid_mark = "✔" if d['pay_type'] == "PAID" else "<span style='font-family: cursive; font-size: 13px; color: #444;'>❌</span>"
        topay_mark = "✔" if d['pay_type'] == "TO PAY" else "<span style='font-family: cursive; font-size: 13px; color: #444;'>❌</span>"
        billing_mark = "✔" if d['pay_type'] == "Monthly Billing" else "<span style='font-family: cursive; font-size: 13px; color: #444;'>❌</span>"

        return f"""
        <div class="copy-box" style="border: 1px solid #000; padding: 2px 4px; background: #fff; font-family: Arial, sans-serif; box-sizing: border-box; width: 100%; max-width: 800px; margin: 0 auto 1.5mm auto; page-break-inside: avoid; break-inside: avoid;">
            <div>
                <div style="background: #000; color: #fff; text-align: center; font-weight: bold; font-size: 8px; padding: 1px 0; margin-bottom: 1.5px;">
                    કાચ, પ્લાસ્ટીક, ફાયબર અથવા લીક્વીડ માલ ડેમેજ અથવા લીક થાય તો તેની જવાબદારી કંપનીની રહેશે નહીં.
                </div>

                <table style="width: 100%; border-collapse: collapse; table-layout: fixed;">
                    <tr>
                        <td style="width: 46%; vertical-align: top; padding-right: 4px; overflow: hidden;">
                            <div style="font-size: 9px; color: #d32f2f; font-weight: bold; font-style: italic; font-family: 'Times New Roman', serif; line-height: 1;">
                                Always on Time
                            </div>
                            <div style="font-size: 16px; font-weight: 900; font-family: 'Georgia', serif; line-height: 1.1; white-space: nowrap; overflow: hidden;">
                                <span style="color: #d32f2f;">FORTUNE</span> <span style="color: #000;">EXPRESS CARGO</span>
                            </div>
                            <div style="font-size: 7px; line-height: 1.05; margin-top: 1.5px; text-transform: uppercase;">
                                <b>E-MAIL :</b> FORTUNEEXPRESSCARGO@GMAIL.COM | <b style="color:#d32f2f; font-size:8px;">M.: 9173165886</b><br>
                                <b>ADD :</b> 15, BHAGWAN ESTATE, OPP. EKTA HOTEL LANE, ASLALI - 382427
                            </div>
                        </td>
                        <td style="width: 27%; vertical-align: top; text-align: center; padding: 0 2px;">
                            <div style="font-size: 7px; line-height: 1.05; text-align: left; display: inline-block; text-transform: uppercase;">
                                <b>PAN NO. :</b> AGVPM3701F<br>
                                <b>GST NO. :</b> 24AGVPM3701F2ZF<br>
                                <b>SAC NO. :</b> 9965
                            </div>
                            <div style="margin-top: 1.5px;">
                                <span style="border: 1px solid #000; padding: 1px 3px; border-radius: 2px; font-weight: bold; font-size: 7.5px; background: #fff; display: inline-block;">
                                    {copy_title}
                                </span>
                            </div>
                        </td>
                        <td style="width: 27%; vertical-align: top; text-align: center;">
                            <div style="border: 1px solid #000; padding: 1.5px;">
                                <div style="font-size: 6.5px; font-weight: bold; color: #333;">DOCKET NUMBER</div>
                                <div style="font-size: 13px; font-weight: bold; color: #d32f2f; line-height: 1.1;">{d['lr_no']}</div>
                                <div style="font-size: 7.5px;"><b>DATE :</b> {d['date']}</div>
                            </div>
                            <table style="width: 100%; border: 1px solid #000; margin-top: 1.5px; font-size: 7.5px; text-align: left; border-collapse: collapse;">
                                <tr><td style="border: 1px solid #000; padding: 1px 2px;"><b>FROM :</b> {d['from']}</td></tr>
                                <tr><td style="border: 1px solid #000; padding: 1px 2px;"><b>TO :</b> {d['to']}</td></tr>
                            </table>
                        </td>
                    </tr>
                </table>

                <table style="width: 100%; border-collapse: collapse; margin-top: 1.5px; border: 1px solid #000; font-size: 8px; table-layout: fixed;">
                    <tr>
                        <td style="width: 50%; border: 1px solid #000; padding: 2px 3px; vertical-align: top; line-height: 1.1; word-break: break-word;">
                            <b style="font-size: 7.5px;">CONSIGNOR DETAILS (PLACE OF SUPPLY)</b><br>
                            <b>NAME :</b> {d['consignor']}<br>
                            <b>GST NO. :</b> {d['consignor_gst']} &nbsp;|&nbsp; <b>CONTACT :</b> {d['consignor_contact']}
                        </td>
                        <td style="width: 50%; border: 1px solid #000; padding: 2px 3px; vertical-align: top; line-height: 1.1; word-break: break-word;">
                            <b style="font-size: 7.5px;">CONSIGNEE DETAILS (DELIVERY DESTINATION)</b><br>
                            <b>NAME :</b> {d['consignee']}<br>
                            <b>GST NO. :</b> {d['consignee_gst']} &nbsp;|&nbsp; <b>CONTACT :</b> {d['consignee_contact']}<br>
                            <b>INSTRUCTION :</b> {d['instruction']}
                        </td>
                    </tr>
                </table>

                <table style="width: 100%; border-collapse: collapse; margin-top: 1.5px; border: 1px solid #000; font-size: 7.5px; text-align: center; table-layout: fixed;">
                    <tr style="font-weight: bold; background: #f2f2f2;">
                        <td style="border: 1px solid #000; width: 45%; padding: 1px;" colspan="3">PACKAGE INFORMATION</td>
                        <td style="border: 1px solid #000; width: 31%; padding: 1px;" colspan="2">IN RUPEES (AMOUNT DETAILS)</td>
                        <td style="border: 1px solid #000; width: 8%; font-size: 6px;">Monthly Billing</td>
                        <td style="border: 1px solid #000; width: 8%; font-size: 6px;">PAID</td>
                        <td style="border: 1px solid #000; width: 8%; font-size: 6px;">TO PAY</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #000; padding: 1px; width: 18%;">{d['pkg_type']}</td>
                        <td style="border: 1px solid #000; padding: 1px; width: 15%;">{d['no_pkg']}</td>
                        <td style="border: 1px solid #000; padding: 1px; width: 12%;">{d['volume']}</td>
                        <td style="border: 1px solid #000; text-align: left; padding: 1px 3px; width: 19%;">BASIC FREIGHT</td>
                        <td style="border: 1px solid #000; text-align: right; padding: 1px 3px; width: 12%;">{d['basic_freight']:.2f}</td>
                        <td style="border: 1px solid #000; vertical-align: middle; text-align: center; font-size: 12px; font-weight: bold;" rowspan="11">{billing_mark}</td>
                        <td style="border: 1px solid #000; vertical-align: middle; text-align: center; font-size: 12px; font-weight: bold;" rowspan="11">{paid_mark}</td>
                        <td style="border: 1px solid #000; vertical-align: middle; text-align: center; font-size: 12px; font-weight: bold;" rowspan="11">{topay_mark}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #000; padding: 2px 3px; text-align: left; word-break: break-word;" colspan="3" rowspan="10" vertical-align="top">
                            <b>GOODS DESCRIPTION :</b> {d['goods_desc']}<br>
                            <b>NO OF PACKAGES :</b> {d['no_pkg']} &nbsp;|&nbsp; <b>E-WAY BILL NO. :</b> {d['eway_bill']}
                        </td>
                        <td style="border: 1px solid #000; text-align: left; padding: 1px 3px;">VALUE SURCHARGE (FOV)</td>
                        <td style="border: 1px solid #000; text-align: right; padding: 1px 3px;">{d['value_surcharge']:.2f}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #000; text-align: left; padding: 1px 3px;">DOCKET CHARGES</td>
                        <td style="border: 1px solid #000; text-align: right; padding: 1px 3px;">{d['docket_charges']:.2f}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #000; text-align: left; padding: 1px 3px;">OTHER CHARGES</td>
                        <td style="border: 1px solid #000; text-align: right; padding: 1px 3px;">{d['other_charges']:.2f}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #000; text-align: left; padding: 1px 3px;">ODA CHARGES</td>
                        <td style="border: 1px solid #000; text-align: right; padding: 1px 3px;">{d['oda_charges']:.2f}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #000; text-align: left; padding: 1px 3px;">SURCHARGES</td>
                        <td style="border: 1px solid #000; text-align: right; padding: 1px 3px;">{d['surcharges']:.2f}</td>
                    </tr>
                    <tr style="font-weight: bold; background: #f9f9f9;">
                        <td style="border: 1px solid #000; text-align: left; padding: 1px 3px;">Total</td>
                        <td style="border: 1px solid #000; text-align: right; padding: 1px 3px;">{d['total_freight']:.2f}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #000; text-align: left; padding: 1px 3px;">CGST (9%)</td>
                        <td style="border: 1px solid #000; text-align: right; padding: 1px 3px;">{d['cgst']:.2f}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #000; text-align: left; padding: 1px 3px;">SGST (9%)</td>
                        <td style="border: 1px solid #000; text-align: right; padding: 1px 3px;">{d['sgst']:.2f}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #000; text-align: left; padding: 1px 3px;">IGST</td>
                        <td style="border: 1px solid #000; text-align: right; padding: 1px 3px;">{d['igst']:.2f}</td>
                    </tr>
                    <tr style="font-weight: bold; background: #eee;">
                        <td style="border: 1px solid #000; text-align: left; padding: 1px 3px;">GRAND TOTAL</td>
                        <td style="border: 1px solid #000; text-align: right; padding: 1px 3px;">{d['grand_total']:.2f}</td>
                    </tr>
                </table>

                <div style="border: 1px solid #000; margin-top: 1.5px; padding: 1px 3px; font-size: 7.5px; word-break: break-word;">
                    <b>INVOICE NO. & VALUE | WEIGHT DETAILS :-</b> {d['inv_no_val_wt']}
                </div>

                <div style="font-size: 7px; margin-top: 2px; text-align: justify; line-height: 1.15; color: #000; font-weight: 600;">
                    (૧) પેક દાગીનામાં રહેલા માલ માટેની પરમીટ સંબંધી અગર ગુનાહિત માલ માટેની જવાબદારી કંપનીની રહેશે નહીં. (૨) આગ, ચોરી, વરસાદ, અકસ્માત, હુલ્લડ, હડતાલ વગેરે અણધાર્યા સંજોગોમાં માલને કોઈપણ નુકશાન થશે તો કંપનીની જવાબદારી રહેશે નહીં. (૩) ગ્રાહક પોતાના માલનું નુકશાન રોકવા માટે વીમો ઉતરાવી લેવો જરૂરી છે. (૪) માલ અંગેની કોઈપણ જાતની ફરીયાદ હોય તો સાત દિવસની અંદર કંપનીને જાણ કરવી. ત્યારબાદ કોઈપણ જાતની કમ્પ્લેન ચાલે નહીં. (૫) કોઈપણ કારણસર ગવર્નમેન્ટ ઓથોરીટી માલ અટકાવશે, જપ્ત કરશે તો કંપની જવાબદાર રહેશે નહીં. (૬) જો ભાડું પહેલેથી ન હોય તો માલ ઉપર લીયન રહેશે. લેનાર કંપની જો માલ લેવાની ના પાડશે તો લાવવા, લઇ જવા અને સ્ટોર કરવાની થઈ લાગશે તે પૂરેપૂરી રકમ ભરપાઈ કરશે માલ ફૂટી કટી આપવાબંધનરહેશે. (૭) અમોએ શરત જે કાંઈ ભરેલી હોય તે વ્યાપારીને બંધનકર્તા રહેશે. (૮) ન્યાયનું કેન્દ્ર વાપી રહેશે. The Company is not responsible for Breakage, Leakage, Damage, Shortage in pack Cartoon/Case/Box/Bags of Goods.
                </div>
            </div>

            <div style="font-size: 6.5px; border-top: 1px solid #000; padding-top: 1px; margin-top: 1.5px; line-height: 1; font-weight: bold; text-align: justify;">
                Navsari :- 8000537847 &nbsp;|&nbsp; Valsad :- 6351700152 &nbsp;|&nbsp; Vapi :- 9427335518 &nbsp;|&nbsp; Ankleshwar :- 9978811411 &nbsp;|&nbsp; Surat :- 8467818918 &nbsp;|&nbsp; Sarkhej Ahm. :- 9427450535 &nbsp;|&nbsp; Madhupura :- 9173165886 &nbsp;|&nbsp; Narol :- 9427450535
            </div>
        </div>
        """

    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        @media print {{
            @page {{
                size: A4 portrait;
                margin: 2mm !important;
            }}
            html, body {{
                width: 100% !important;
                margin: 0 !important;
                padding: 0 !important;
            }}
            .print-btn-container {{
                display: none !important;
            }}
            .copy-box {{
                margin-bottom: 1mm !important;
                page-break-inside: avoid !important;
                break-inside: avoid !important;
                border: 1px solid #000 !important;
            }}
        }}
    </style>
    </head>
    <body style="margin:0; padding:0; background:#fff;">
        <div style="text-align: center; margin-bottom: 10px; display: flex; justify-content: center; gap: 12px;" class="print-btn-container">
            <button onclick="window.print()" style="background-color: #007bff; color: white; padding: 10px 20px; border: none; font-size: 14px; font-weight: bold; border-radius: 4px; cursor: pointer;">
                🖨️ PRINT ALL 3 COPIES
            </button>
            <button onclick="window.print()" style="background-color: #28a745; color: white; padding: 10px 20px; border: none; font-size: 14px; font-weight: bold; border-radius: 4px; cursor: pointer;">
                📥 DOWNLOAD PDF (SAVE AS PDF)
            </button>
        </div>
        <div>
            {get_receipt_html("CONSIGNOR COPY (કોન્સાઈનર કોપી)")}
            {get_receipt_html("CONSIGNEE COPY (કોન્સાઈની કોપી)")}
            {get_receipt_html("DRIVER COPY (ડ્રાઈવર કોપી)")}
        </div>
    </body>
    </html>
    """

    st.markdown("---")
    st.components.v1.html(full_html, height=1150, scrolling=True)

st.markdown("---")
st.subheader("📊 જુનો બધો ડેટા (Saved LR History & Backup)")
if not df.empty:
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download All LR Data (Excel Backup)",
        data=csv_data,
        file_name=f"fortune_lr_backup_{datetime.now().strftime('%d-%m-%Y')}.csv",
        mime="text/csv",
    )
    st.dataframe(df, use_container_width=True)
else:
    st.info("No saved records found yet.")
