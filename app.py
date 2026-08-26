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
next_lr = 3901 if df.empty else int(df["LR_No"].max()) + 1

st.subheader("નવી LR એન્ટ્રી કરો (Create New LR)")

with st.form("lr_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        lr_no = st.number_input("LR Number / Docket Number", value=next_lr)
        date = st.date_input("Date", datetime.now())
        consignor = st.text_input("Consignor Name (Place of Supply)", "IFFCO - MC CROP SCIENCE PVT LTD")
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
        basic_freight = st.number_input("Basic Freight", value=200.39)
        val_surcharge = st.number_input("Value Surcharge (FOV)", value=0.0)
        docket_chg = st.number_input("Docket Charges", value=0.0)
        other_chg = st.number_input("Other Charges", value=0.0)
        oda_chg = st.number_input("ODA Charges", value=0.0)
        surcharges = st.number_input("Surcharges", value=0.0)
        tax_type = st.selectbox("GST Type", ["SGST/CGST (18%)", "IGST (18%)", "None"])
        pay_type = st.radio("Payment Status", ["Monthly Billing", "PAID", "TO PAY"], index=1)

    submit = st.form_submit_button("SAVE & GENERATE LR")

if submit:
    subtotal = basic_freight + val_surcharge + docket_chg + other_chg + oda_chg + surcharges
    
    if tax_type == "SGST/CGST (18%)":
        cgst = round(subtotal * 0.09, 2)
        sgst = round(subtotal * 0.09, 2)
        igst = 0.0
    elif tax_type == "IGST (18%)":
        cgst = 0.0
        sgst = 0.0
        igst = round(subtotal * 0.18, 2)
    else:
        cgst = sgst = igst = 0.0
        
    grand_total = round(subtotal + cgst + sgst + igst, 2)

    new_data = pd.DataFrame([[lr_no, str(date), consignor, consignor_gst, consignee, from_place, to_place, no_pkg, pkg_type, grand_total]], 
                            columns=df.columns)
    new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)
    st.success(f"✅ LR No. {lr_no} સફળતાપૂર્વક સેવ થઈ ગયું છે!")

    st.session_state['lr_data'] = {
        "lr_no": lr_no, "date": str(date), "consignor": consignor, "consignor_gst": consignor_gst,
        "consignor_contact": consignor_contact, "consignee": consignee, "consignee_gst": consignee_gst,
        "consignee_contact": consignee_contact, "from": from_place, "to": to_place, "instruction": instruction,
        "pkg_type": pkg_type, "no_pkg": no_pkg, "volume": volume, "goods_desc": goods_desc,
        "inv_no_val_wt": inv_no_val_wt,
        "basic_freight": basic_freight, "val_surcharge": val_surcharge, "docket_chg": docket_chg,
        "other_chg": other_chg, "oda_chg": oda_chg, "surcharges": surcharges,
        "subtotal": subtotal, "cgst": cgst, "sgst": sgst, "igst": igst, "grand_total": grand_total,
        "pay_type": pay_type
    }

if 'lr_data' in st.session_state:
    d = st.session_state['lr_data']

    def get_receipt_html(copy_title):
        paid_mark = "✔" if d['pay_type'] == "PAID" else ""
        topay_mark = "✔" if d['pay_type'] == "TO PAY" else ""
        billing_mark = "✔" if d['pay_type'] == "Monthly Billing" else ""

        return f"""
        <div style="position: relative; margin-bottom: 4px;">
            <div class="copy-box" style="border: 1.5px solid #000; padding: 4px 6px; background: #fff; font-family: Arial, sans-serif; box-sizing: border-box; height: 32vh; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <!-- Top Warning Bar -->
                    <div style="background: #000; color: #fff; text-align: center; font-weight: bold; font-size: 10px; padding: 1px 0; margin-bottom: 2px;">
                        કાચ, પ્લાસ્ટીક, ફાયબર અથવા લીક્વીડ માલ ડેમેજ અથવા લીક થાય તો તેની જવાબદારી કંપનીની રહેશે નહીં.
                    </div>

                    <!-- Header Table -->
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="width: 48%; vertical-align: top;">
                                <div style="font-size: 9px; color: #d32f2f; font-weight: bold; font-style: italic; font-family: 'Times New Roman', serif;">
                                    Always on Time
                                </div>
                                <div style="font-size: 17px; font-weight: 900; font-family: 'Arial Black', Impact, sans-serif; line-height: 1.1; white-space: nowrap;">
                                    <span style="color: #d32f2f;">FORTUNE</span> <span style="color: #000;">EXPRESS CARGO</span>
                                </div>
                                <div style="font-size: 9.5px; line-height: 1.2; margin-top: 2px;">
                                    <b>E-mail :</b> fortuneexpresscargo@gmail.com<br>
                                    <b>M. :</b> 9173165886<br>
                                    <b>Add :</b> 15, Bhagwan Estate, Opp. Ekta Hotel Lane, Aslali - 382427
                                </div>
                            </td>
                            <td style="width: 27%; vertical-align: top; text-align: center;">
                                <div style="font-size: 9.5px; line-height: 1.25; text-align: left; display: inline-block;">
                                    <b>PAN No. :</b> AGVPM3701F<br>
                                    <b>GST No. :</b> 24AGVPM3701F2ZF<br>
                                    <b>SAC No. :</b> 9965
                                </div>
                                <div style="margin-top: 3px;">
                                    <span style="border: 1.5px solid #000; padding: 2px 8px; border-radius: 10px; font-weight: bold; font-size: 10px; background: #fff; display: inline-block;">
                                        {copy_title}
                                    </span>
                                </div>
                            </td>
                            <td style="width: 25%; vertical-align: top; text-align: center;">
                                <div style="border: 1px solid #000; padding: 2px;">
                                    <div style="font-size: 8.5px; font-weight: bold; color: #333;">DOCKET NUMBER</div>
                                    <div style="font-size: 17px; font-weight: bold; color: #d32f2f; line-height: 1;">{d['lr_no']}</div>
                                    <div style="font-size: 9.5px;"><b>DATE :</b> {d['date']}</div>
                                </div>
                                <table style="width: 100%; border: 1px solid #000; margin-top: 2px; font-size: 9.5px; text-align: left; border-collapse: collapse;">
                                    <tr><td style="border: 1px solid #000; padding: 1px 3px;"><b>FROM :</b> {d['from']}</td></tr>
                                    <tr><td style="border: 1px solid #000; padding: 1px 3px;"><b>TO :</b> {d['to']}</td></tr>
                                </table>
                            </td>
                        </tr>
                    </table>

                    <!-- Consignor & Consignee Table -->
                    <table style="width: 100%; border-collapse: collapse; margin-top: 2px; border: 1px solid #000; font-size: 9.5px;">
                        <tr>
                            <td style="width: 50%; border: 1px solid #000; padding: 2px 4px; vertical-align: top; line-height: 1.2;">
                                <b>CONSIGNOR DETAILS (PLACE OF SUPPLY)</b><br>
                                NAME : {d['consignor']}<br>
                                GST NO. : {d['consignor_gst']}<br>
                                CONTACT NO. : {d['consignor_contact']}
                            </td>
                            <td style="width: 50%; border: 1px solid #000; padding: 2px 4px; vertical-align: top; line-height: 1.2;">
                                <b>CONSIGNEE DETAILS (DELIVERY DESTINATION)</b><br>
                                NAME : {d['consignee']}<br>
                                GST NO. : {d['consignee_gst']}<br>
                                CONTACT NO. : {d['consignee_contact']}<br>
                                INSTRUCTION : {d['instruction']}
                            </td>
                        </tr>
                    </table>

                    <!-- Package & Payment Details Grid -->
                    <table style="width: 100%; border-collapse: collapse; margin-top: 2px; border: 1px solid #000; font-size: 9.5px; text-align: center;">
                        <tr style="font-weight: bold; background: #f2f2f2;">
                            <td style="border: 1px solid #000; width: 45%; padding: 1px;" colspan="3">PACKAGE INFORMATION</td>
                            <td style="border: 1px solid #000; width: 25%; padding: 1px;" colspan="2">IN RUPEES</td>
                            <td style="border: 1px solid #000; width: 10%;">Monthly Billing</td>
                            <td style="border: 1px solid #000; width: 10%;">PAID</td>
                            <td style="border: 1px solid #000; width: 10%;">TO PAY</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #000; padding: 1px; width: 20%;">{d['pkg_type']}</td>
                            <td style="border: 1px solid #000; padding: 1px; width: 15%;">{d['no_pkg']}</td>
                            <td style="border: 1px solid #000; padding: 1px; width: 10%;">{d['volume']}</td>
                            <td style="border: 1px solid #000; text-align: left; padding: 1px 3px;">BASIC FREIGHT</td>
                            <td style="border: 1px solid #000; text-align: right; padding: 1px 3px;">{d['basic_freight']:.2f}</td>
                            <td style="border: 1px solid #000; vertical-align: middle; text-align: center; font-size: 26px; color: #008000; font-weight: 900;" rowspan="11">{billing_mark}</td>
                            <td style="border: 1px solid #000; vertical-align: middle; text-align: center; font-size: 26px; color: #008000; font-weight: 900;" rowspan="11">{paid_mark}</td>
                            <td style="border: 1px solid #000; vertical-align: middle; text-align: center; font-size: 26px; color: #008000; font-weight: 900;" rowspan="11">{topay_mark}</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #000; padding: 2px; text-align: left;" colspan="3" rowspan="10" vertical-align="top">
                                <b>GOODS DESCRIPTION :</b> {d['goods_desc']}<br>
                                <b>NO OF PACKAGES :</b> {d['no_pkg']}
                            </td>
                            <td style="border: 1px solid #000; text-align: left; padding: 0px 3px;">VALUE SURCHARGE (FOV)</td>
                            <td style="border: 1px solid #000; text-align: right; padding: 0px 3px;">{d['val_surcharge']:.2f}</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #000; text-align: left; padding: 0px 3px;">DOCKET CHARGES</td>
                            <td style="border: 1px solid #000; text-align: right; padding: 0px 3px;">{d['docket_chg']:.2f}</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #000; text-align: left; padding: 0px 3px;">OTHER CHARGES</td>
                            <td style="border: 1px solid #000; text-align: right; padding: 0px 3px;">{d['other_chg']:.2f}</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #000; text-align: left; padding: 0px 3px;">ODA CHARGES</td>
                            <td style="border: 1px solid #000; text-align: right; padding: 0px 3px;">{d['oda_chg']:.2f}</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #000; text-align: left; padding: 0px 3px;">SURCHARGES</td>
                            <td style="border: 1px solid #000; text-align: right; padding: 0px 3px;">{d['surcharges']:.2f}</td>
                        </tr>
                        <tr style="font-weight: bold; background: #f9f9f9;">
                            <td style="border: 1px solid #000; text-align: left; padding: 0px 3px;">Total</td>
                            <td style="border: 1px solid #000; text-align: right; padding: 0px 3px;">{d['subtotal']:.2f}</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #000; text-align: left; padding: 0px 3px;">CGST (9%)</td>
                            <td style="border: 1px solid #000; text-align: right; padding: 0px 3px;">{d['cgst']:.2f}</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #000; text-align: left; padding: 0px 3px;">SGST (9%)</td>
                            <td style="border: 1px solid #000; text-align: right; padding: 0px 3px;">{d['sgst']:.2f}</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #000; text-align: left; padding: 0px 3px;">IGST</td>
                            <td style="border: 1px solid #000; text-align: right; padding: 0px 3px;">{d['igst']:.2f}</td>
                        </tr>
                        <tr style="font-weight: bold; background: #eee;">
                            <td style="border: 1px solid #000; text-align: left; padding: 1px 3px;">GRAND TOTAL</td>
                            <td style="border: 1px solid #000; text-align: right; padding: 1px 3px;">{d['grand_total']:.2f}</td>
                        </tr>
                    </table>

                    <!-- Invoice Details Row -->
                    <div style="border: 1px solid #000; margin-top: 2px; padding: 1px 3px; font-size: 9px;">
                        <b>INVOICE NO. & VALUE | WEIGHT DETAILS :-</b> {d['inv_no_val_wt']}
                    </div>

                    <!-- Terms & Conditions Gujarati Text -->
                    <div style="font-size: 7.5px; margin-top: 2px; text-align: justify; line-height: 1.1; color: #111;">
                        (૧) પેક દાગીનામાં રહેલા માલ માટેની બીલ અથવા પરમીટ કે E-way bill ની સંપૂર્ણ જવાબદારી ગ્રાહકની રહેશે. (૨) આગ, ચોરી, વરસાદ, અકસ્માત, હુલ્લડ વગેરે અણધાર્યા સંજોગોમાં માલને કોઈપણ નુકશાન થશે તો કંપનીની જવાબદારી રહેશે નહીં. (૩) માલ અંગેની કોઈપણ જાતની ફરીયાદ હશે તો ૧૦ દિવસની અંદર શરુ કરવી. (૪) કોઈપણ કારાણસર ગવર્નમેન્ટ ઓથોરીટી માલ અટકાવશે, જપ્ત કરશે તો કંપની જવાબદાર રહેશે નહીં. The Company is not responsible for Breakage, Leakage, Damage, Shortage in pack Cantoos/Cases/Boxes/Bags of Goods.
                    </div>
                </div>

                <!-- Footer Branch Phones -->
                <div style="font-size: 8.5px; border-top: 1.5px solid #000; padding-top: 2px; margin-top: 1px; line-height: 1.2; font-weight: bold;">
                    <b>Navsari :</b> 70B9093833 | <b>Valsad :</b> 7A2B294826 | <b>Vapi :</b> 9427335518 | <b>Bharuch :</b> 9427587136 | <b>Ankleshwar :</b> 9107587136 | <b>Surat :</b> 8467818918 | <b>Chikhali :</b> 70B9093834 | <b>Sarkhej Amd. :</b> 9427450535
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
                height: 32vh !important;
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
st.dataframe(pd.read_csv(DATA_FILE), use_container_width=True)
