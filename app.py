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
            "Packages", "Goods", "Grand_Total", "Pay_Type"
        ])
        df.to_csv(DATA_FILE, index=False)
else:
    df = pd.DataFrame(columns=[
        "LR_No", "Date", "Consignor", "Consignor_GST", "Consignor_Contact", 
        "Consignee", "Consignee_GST", "Consignee_Contact", "From", "To", 
        "Packages", "Goods", "Grand_Total", "Pay_Type"
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

next_lr = 3901 if df.empty else int(df["LR_No"].max()) + 1

st.subheader("નવી LR એન્ટ્રી કરો (Create New LR)")

consignor_names = df_party["Name"].dropna().unique().tolist() if not df_party.empty else []

with st.form("lr_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        lr_no = st.number_input("LR Number / Docket Number", value=next_lr)
        date = st.date_input("Date", datetime.now())
        
        consignor = st.selectbox("Consignor Name (Place of Supply)", options=[""] + consignor_names, index=0)
        if not consignor:
            consignor = st.text_input("Or Type Consignor Name", "IFFCO - MC CROP SCIENCE PVT LTD")
            
        consignor_gst = st.text_input("Consignor GST", "24AADCI9008G1ZR")
        consignor_contact = st.text_input("Consignor Contact / Pincode", "")
        from_place = st.text_input("From", "Aslali")
        
    with col2:
        consignee = st.text_input("Consignee Name (Delivery Destination)", "VALSAD VIBHAG FARMER")
        consignee_gst = st.text_input("Consignee GST", "")
        consignee_contact = st.text_input("Consignee Contact", "")
        to_place = st.text_input("To", "Valsad")
        instruction = st.text_input("Instruction", "Handle with Care (Pesticides)")
        
    st.markdown("---")
    col3, col4 = st.columns(2)
    
    with col3:
        pkg_type = st.text_input("Type of Packaging", "BOX (Pesticides)")
        no_pkg = st.text_input("No. of Packages", "3 BOXES")
        volume = st.text_input("Volume (Inch)", "-")
        goods_desc = st.text_input("Goods Description", "PESTICIDES")
        inv_no_val_wt = st.text_input("Invoice No. & Value | Weight Details", "")

    with col4:
        st.markdown("<b>Amount & GST Auto-Fill</b>", unsafe_allow_html=True)
        
        # Seedha Grand Total likhne ka option
        grand_total = st.number_input("Enter Grand Total (Total Amount)", value=236.0)
        
        gst_type = st.radio("GST Type", ["CGST + SGST (9% + 9%)", "IGST (18%)"], horizontal=True)
        
        # Automatic Back-calculation for Freight and GST
        if "CGST" in gst_type:
            # Grand Total = Basic Freight + 18% (9% + 9%) => Basic = Grand Total / 1.18
            total_freight = round(grand_total / 1.18, 2)
            cgst = round(total_freight * 0.09, 2)
            sgst = round(grand_total - total_freight - cgst, 2) # Adjustment for rounding match
            igst = 0.0
        else:
            # Grand Total = Basic Freight + 18% IGST => Basic = Grand Total / 1.18
            total_freight = round(grand_total / 1.18, 2)
            cgst = 0.0
            sgst = 0.0
            igst = round(grand_total - total_freight, 2)
            
        basic_freight = total_freight
        value_surcharge = 0.0
        docket_charges = 0.0
        other_charges = 0.0
        oda_charges = 0.0
        surcharges = 0.0
        
        st.info(f"✨ Auto Calculated -> Basic Freight: {basic_freight} | CGST/SGST or IGST automatically adjusted.")
        
        pay_type = st.radio("Payment Status", ["Monthly Billing", "PAID", "TO PAY"], index=1)

    submit = st.form_submit_button("SAVE & GENERATE LR")

if submit:
    new_data = pd.DataFrame([[
        lr_no, str(date), consignor, consignor_gst, consignor_contact, 
        consignee, consignee_gst, consignee_contact, from_place, to_place, 
        no_pkg, goods_desc, grand_total, pay_type
    ]], columns=[
        "LR_No", "Date", "Consignor", "Consignor_GST", "Consignor_Contact", 
        "Consignee", "Consignee_GST", "Consignee_Contact", "From", "To", 
        "Packages", "Goods", "Grand_Total", "Pay_Type"
    ])
    new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)

    if consignor and consignor not in consignor_names:
        new_party = pd.DataFrame([[consignor, consignor_gst, consignor_contact]], columns=["Name", "GST", "Contact"])
        new_party.to_csv(PARTY_FILE, mode='a', header=False, index=False)

    st.success(f"✅ LR No. {lr_no} સફળતાપૂર્વક સેવ થઈ ગયું છે!")

    st.session_state['lr_data'] = {
        "lr_no": lr_no, "date": str(date), "consignor": consignor, "consignor_gst": consignor_gst,
        "consignor_contact": consignor_contact, "consignee": consignee, "consignee_gst": consignee_gst,
        "consignee_contact": consignee_contact, "from": from_place, "to": to_place, "instruction": instruction,
        "pkg_type": pkg_type, "no_pkg": no_pkg, "volume": volume, "goods_desc": goods_desc,
        "inv_no_val_wt": inv_no_val_wt,
        "basic_freight": basic_freight, "value_surcharge": value_surcharge, "docket_charges": docket_charges,
        "other_charges": other_charges, "oda_charges": oda_charges, "surcharges": surcharges,
        "total_freight": total_freight, "cgst": cgst, "sgst": sgst, "igst": igst, "grand_total": grand_total,
        "pay_type": pay_type
    }

if 'lr_data' in st.session_state:
    d = st.session_state['lr_data']

    def get_receipt_html(copy_title):
        paid_mark = "✔" if d['pay_type'] == "PAID" else ""
        topay_mark = "✔" if d['pay_type'] == "TO PAY" else ""
        billing_mark = "✔" if d['pay_type'] == "Monthly Billing" else ""

        return f"""
        <div style="position: relative; margin-bottom: 2px;">
            <div class="copy-box" style="border: 1.5px solid #000; padding: 2px 4px; background: #fff; font-family: Arial, sans-serif; box-sizing: border-box; height: 32.5vh; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="background: #000; color: #fff; text-align: center; font-weight: bold; font-size: 11px; padding: 1px 0;">
                        કાચ, પ્લાસ્ટીક, ફાયબર અથવા લીક્વીડ માલ ડેમેજ અથવા લીક થાય તો તેની જવાબદારી કંપનીની રહેશે નહીં.
                    </div>

                    <table style="width: 100%; border-collapse: collapse; margin-top: 1px;">
                        <tr>
                            <td style="width: 50%; vertical-align: top;">
                                <div style="display: flex; align-items: center; gap: 8px;">
                                    <svg width="50" height="26" viewBox="0 0 60 35" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <rect x="2" y="10" width="30" height="15" fill="#333" />
                                        <path d="M32 14L44 14L50 20L50 25L32 25Z" fill="#333" />
                                        <circle cx="10" cy="26" r="4" fill="#000" stroke="#fff" stroke-width="1.5"/>
                                        <circle cx="24" cy="26" r="4" fill="#000" stroke="#fff" stroke-width="1.5"/>
                                        <circle cx="42" cy="26" r="4" fill="#000" stroke="#fff" stroke-width="1.5"/>
                                        <line x1="6" y1="5" x2="35" y2="5" stroke="#333" stroke-width="2"/>
                                    </svg>
                                    <div>
                                        <div style="font-size: 11px; color: #d32f2f; font-weight: bold; font-style: italic; font-family: 'Times New Roman', serif; line-height: 1;">
                                            Always on Time
                                        </div>
                                        <div style="font-size: 22px; font-weight: 900; font-family: 'Georgia', 'Times New Roman', serif; letter-spacing: 0.5px; line-height: 1.1; white-space: nowrap;">
                                            <span style="color: #d32f2f;">FORTUNE</span> <span style="color: #000;">EXPRESS CARGO</span>
                                        </div>
                                    </div>
                                </div>
                                <div style="font-size: 11px; line-height: 1.15; margin-top: 2px;">
                                    <b>E-mail :</b> fortuneexpresscargo@gmail.com | <b>M. :</b> 9173165886<br>
                                    <b>Add :</b> 15, Bhagwan Estate, Opp. Ekta Hotel Lane, Aslali - 382427
                                </div>
                            </td>
                            <td style="width: 25%; vertical-align: top; text-align: center;">
                                <div style="font-size: 11px; line-height: 1.2; text-align: left; display: inline-block;">
                                    <b>PAN No. :</b> AGVPM3701F<br>
                                    <b>GST No. :</b> 24AGVPM3701F2ZF<br>
                                    <b>SAC No. :</b> 9965
                                </div>
                                <div style="margin-top: 2px;">
                                    <span style="border: 1.5px solid #000; padding: 2px 6px; border-radius: 6px; font-weight: bold; font-size: 11px; background: #fff; display: inline-block;">
                                        {copy_title}
                                    </span>
                                </div>
                            </td>
                            <td style="width: 25%; vertical-align: top; text-align: center;">
                                <div style="border: 1px solid #000; padding: 1px;">
                                    <div style="font-size: 10px; font-weight: bold; color: #333;">DOCKET NUMBER</div>
                                    <div style="font-size: 20px; font-weight: bold; color: #d32f2f; line-height: 1;">{d['lr_no']}</div>
                                    <div style="font-size: 11px;"><b>DATE :</b> {d['date']}</div>
                                </div>
                                <table style="width: 100%; border: 1px solid #000; margin-top: 1px; font-size: 11px; text-align: left; border-collapse: collapse;">
                                    <tr><td style="border: 1px solid #000; padding: 1px 3px;"><b>FROM :</b> {d['from']}</td></tr>
                                    <tr><td style="border: 1px solid #000; padding: 1px 3px;"><b>TO :</b> {d['to']}</td></tr>
                                </table>
                            </td>
                        </tr>
                    </table>

                    <table style="width: 100%; border-collapse: collapse; margin-top: 1px; border: 1px solid #000; font-size: 11.5px;">
                        <tr>
                            <td style="width: 50%; border: 1px solid #000; padding: 3px 5px; vertical-align: top; line-height: 1.25;">
                                <b style="font-size: 11px;">CONSIGNOR DETAILS (PLACE OF SUPPLY)</b><br>
                                <b>NAME :</b> {d['consignor']}<br>
                                <b>GST NO. :</b> {d['consignor_gst']} &nbsp;&nbsp;|&nbsp;&nbsp; <b>CONTACT :</b> {d['consignor_contact']}
                            </td>
                            <td style="width: 50%; border: 1px solid #000; padding: 3px 5px; vertical-align: top; line-height: 1.25;">
                                <b style="font-size: 11px;">CONSIGNEE DETAILS (DELIVERY DESTINATION)</b><br>
                                <b>NAME :</b> {d['consignee']}<br>
                                <b>GST NO. :</b> {d['consignee_gst']} &nbsp;&nbsp;|&nbsp;&nbsp; <b>CONTACT :</b> {d['consignee_contact']}<br>
                                <b>INSTRUCTION :</b> {d['instruction']}
                            </td>
                        </tr>
                    </table>

                    <table style="width: 100%; border-collapse: collapse; margin-top: 1px; border: 1px solid #000; font-size: 10.5px; text-align: center;">
                        <tr style="font-weight: bold; background: #f2f2f2;">
                            <td style="border: 1px solid #000; width: 45%; padding: 1px;" colspan="3">PACKAGE INFORMATION</td>
                            <td style="border: 1px solid #000; width: 31%; padding: 1px;" colspan="2">IN RUPEES (AMOUNT DETAILS)</td>
                            <td style="border: 1px solid #000; width: 8%; font-size: 9px;">Monthly Billing</td>
                            <td style="border: 1px solid #000; width: 8%; font-size: 9px;">PAID</td>
                            <td style="border: 1px solid #000; width: 8%; font-size: 9px;">TO PAY</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #000; padding: 2px; width: 20%;">{d['pkg_type']}</td>
                            <td style="border: 1px solid #000; padding: 2px; width: 15%;">{d['no_pkg']}</td>
                            <td style="border: 1px solid #000; padding: 2px; width: 10%;">{d['volume']}</td>
                            <td style="border: 1px solid #000; text-align: left; padding: 1px 4px;">BASIC FREIGHT</td>
                            <td style="border: 1px solid #000; text-align: right; padding: 1px 4px;">{d['basic_freight']:.2f}</td>
                            <td style="border: 1px solid #000; vertical-align: middle; text-align: center; font-size: 22px; color: #008000; font-weight: 900;" rowspan="11">{billing_mark}</td>
                            <td style="border: 1px solid #000; vertical-align: middle; text-align: center; font-size: 22px; color: #008000; font-weight: 900;" rowspan="11">{paid_mark}</td>
                            <td style="border: 1px solid #000; vertical-align: middle; text-align: center; font-size: 22px; color: #008000; font-weight: 900;" rowspan="11">{topay_mark}</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #000; padding: 2px 5px; text-align: left;" colspan="3" rowspan="10" vertical-align="top">
                                <b>GOODS DESCRIPTION :</b> {d['goods_desc']}<br>
                                <b>NO OF PACKAGES :</b> {d['no_pkg']}
                            </td>
                            <td style="border: 1px solid #000; text-align: left; padding: 1px 4px;">VALUE SURCHARGE (FOV)</td>
                            <td style="border: 1px solid #000; text-align: right; padding: 1px 4px;">{d['value_surcharge']:.2f}</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #000; text-align: left; padding: 1px 4px;">DOCKET CHARGES</td>
                            <td style="border: 1px solid #000; text-align: right; padding: 1px 4px;">{d['docket_charges']:.2f}</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #000; text-align: left; padding: 1px 4px;">OTHER CHARGES</td>
                            <td style="border: 1px solid #000; text-align: right; padding: 1px 4px;">{d['other_charges']:.2f}</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #000; text-align: left; padding: 1px 4px;">ODA CHARGES</td>
                            <td style="border: 1px solid #000; text-align: right; padding: 1px 4px;">{d['oda_charges']:.2f}</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #000; text-align: left; padding: 1px 4px;">SURCHARGES</td>
                            <td style="border: 1px solid #000; text-align: right; padding: 1px 4px;">{d['surcharges']:.2f}</td>
                        </tr>
                        <tr style="font-weight: bold; background: #f9f9f9;">
                            <td style="border: 1px solid #000; text-align: left; padding: 1px 4px;">Total</td>
                            <td style="border: 1px solid #000; text-align: right; padding: 1px 4px;">{d['total_freight']:.2f}</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #000; text-align: left; padding: 1px 4px;">CGST (9%)</td>
                            <td style="border: 1px solid #000; text-align: right; padding: 1px 4px;">{d['cgst']:.2f}</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #000; text-align: left; padding: 1px 4px;">SGST (9%)</td>
                            <td style="border: 1px solid #000; text-align: right; padding: 1px 4px;">{d['sgst']:.2f}</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #000; text-align: left; padding: 1px 4px;">IGST</td>
                            <td style="border: 1px solid #000; text-align: right; padding: 1px 4px;">{d['igst']:.2f}</td>
                        </tr>
                        <tr style="font-weight: bold; background: #eee;">
                            <td style="border: 1px solid #000; text-align: left; padding: 1px 4px;">GRAND TOTAL</td>
                            <td style="border: 1px solid #000; text-align: right; padding: 1px 4px;">{d['grand_total']:.2f}</td>
                        </tr>
                    </table>

                    <div style="border: 1px solid #000; margin-top: 1px; padding: 2px 5px; font-size: 11px;">
                        <b>INVOICE NO. & VALUE | WEIGHT DETAILS :-</b> {d['inv_no_val_wt']}
                    </div>

                    <div style="font-size: 8.5px; margin-top: 1px; text-align: justify; line-height: 1.1; color: #000; font-weight: 600;">
                        (૧) પેક દાગીનામાં રહેલા માલ માટેની પરમીટ સંબંધી અગર ગુનાહિત માલ માટેની જવાબદારી કંપનીની રહેશે નહીં. (૨) આગ, ચોરી, વરસાદ, અકસ્માત, હુલ્લડ, હડતાલ વગેરે અણધાર્યા સંજોગોમાં માલને કોઈપણ નુકશાન થશે તો કંપનીની જવાબદારી રહેશે નહીં. (૩) ગ્રાહક પોતાના માલનું નુકશાન રોકવા માટે વીમો ઉતરાવી લેવો જરૂરી છે. (૪) માલ અંગેની કોઈપણ જાતની ફરીયાદ હોય તો સાત દિવસની અંદર કંપનીને જાણ કરવી. ત્યારબાદ કોઈપણ જાતની કમ્પ્લેન ચાલે નહીં. (૫) કોઈપણ કારણસર ગવર્નમેન્ટ ઓથોરીટી માલ અટકાવશે, જપ્ત કરશે તો કંપની જવાબદાર રહેશે નહીં. (૬) જો ભાડું પહેલેથી ન હોય તો માલ ઉપર લીયન રહેશે. લેનાર કંપની જો માલ લેવાની ના પાડશે તો લાવવા, લઇ જવા અને સ્ટોર કરવાની થઈ લાગશે તે પૂરેપૂરી રકમ ભરપાઈ કરશે માલ ફૂટી કટી આપવાબંધનરહેશે. (૭) અમોએ શરત જે કાંઈ ભરેલી હોય તે વ્યાપારીને બંધનકર્તા રહેશે. (૮) ન્યાયનું કેન્દ્ર વાપી રહેશે. The Company is not responsible for Breakage, Leakage, Damage, Shortage in pack Cartoon/Case/Box/Bags of Goods.
                    </div>
                </div>

                <div style="font-size: 9px; border-top: 1.5px solid #000; padding-top: 2px; margin-top: 1px; line-height: 1.2; font-weight: bold; text-align: justify;">
                    <b>Navsari :-</b> 7089093833 &nbsp;|&nbsp; <b>Valsad :-</b> 7A2B294826 &nbsp;|&nbsp; <b>Vapi :-</b> 9427335518 &nbsp;|&nbsp; <b>Bharuch :-</b> 9427587136 &nbsp;|&nbsp; <b>Ankleshwar :-</b> 9107587136 &nbsp;|&nbsp; <b>Surat :-</b> 8467818918 &nbsp;|&nbsp; <b>Chikhali :-</b> 7089093833 &nbsp;|&nbsp; <b>Sarkhej Amd. :-</b> 9427450535
                </div>
            </div>
            <div style="border-bottom: 1px dashed #000; margin-top: 1px;"></div>
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
                margin: 0mm !important;
            }}
            html, body {{
                height: 100vh !important;
                margin: 0 !important;
                padding: 0 !important;
                overflow: hidden !important;
            }}
            .print-btn-container {{
                display: none !important;
            }}
            .copy-box {{
                height: 32.5vh !important;
                page-break-inside: avoid !important;
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
    st.components.v1.html(full_html, height=1250, scrolling=True)

st.markdown("---")
st.subheader("📊 જુનો બધો ડેટા (Saved LR History)")
if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("No saved records found yet.")
