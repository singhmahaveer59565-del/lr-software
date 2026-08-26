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
        consignor_pincode = st.text_input("Consignor Pincode / Contact", "")
        from_place = st.text_input("From", "Aslali")
        
    with col2:
        consignee = st.text_input("Consignee Name (Delivery Destination)", "VALSAD VIBHAG FARMER")
        consignee_gst = st.text_input("Consignee GST / Contact", "")
        consignee_pincode = st.text_input("Consignee Pincode", "")
        to_place = st.text_input("To", "Valsad")
        instruction = st.text_input("Instruction", "Handle with Care")
        
    st.markdown("---")
    col3, col4 = st.columns(2)
    
    with col3:
        pkg_type = st.text_input("Type of Packaging", "BOXES")
        no_pkg = st.text_input("No. of Packages", "3")
        volume = st.text_input("Volume (Inch)", "-")
        total_pkg = st.text_input("Total Packages", "3 BOXES")
        inv_no = st.text_input("Invoice Number", "")
        inv_val = st.text_input("Invoice Value", "")
        act_wt = st.text_input("Actual Weight", "")
        chg_wt = st.text_input("Charged Weight", "")

    with col4:
        basic_freight = st.number_input("Basic Freight", value=203.39)
        val_surcharge = st.number_input("Value Surcharge (FOV)", value=0.0)
        docket_chg = st.number_input("Docket Charges", value=0.0)
        other_chg = st.number_input("Other Charges", value=0.0)
        oda_chg = st.number_input("ODA Charges", value=0.0)
        surcharges = st.number_input("Surcharges", value=0.0)
        tax_type = st.selectbox("GST Type", ["SGST/CGST (18%)", "IGST (18%)", "None"])
        pay_type = st.radio("Payment Status", ["Monthly Billing", "PAID", "TO PAY"], index=1)

    submit = st.form_submit_button("SAVE & GENERATE ORIGINAL BILL LR")

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

    new_data = pd.DataFrame([[lr_no, str(date), consignor, consignor_gst, consignee, from_place, to_place, total_pkg, pkg_type, grand_total]], 
                            columns=df.columns)
    new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)
    st.success(f"✅ LR No. {lr_no} સફળતાપૂર્વક સેવ થઈ ગયું છે!")

    st.session_state['lr_data'] = {
        "lr_no": lr_no, "date": str(date), "consignor": consignor, "consignor_gst": consignor_gst,
        "consignor_pincode": consignor_pincode, "consignee": consignee, "consignee_gst": consignee_gst,
        "consignee_pincode": consignee_pincode, "from": from_place, "to": to_place, "instruction": instruction,
        "pkg_type": pkg_type, "no_pkg": no_pkg, "volume": volume, "total_pkg": total_pkg,
        "inv_no": inv_no, "inv_val": inv_val, "act_wt": act_wt, "chg_wt": chg_wt,
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
        <div class="copy-box" style="border: 2px solid #000; padding: 6px; margin-bottom: 8px; background: #fff; font-family: Arial, sans-serif; font-size: 10.5px; box-sizing: border-box; height: 32.5vh; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div style="float: right; font-weight: bold; font-size: 10px; border: 1.5px solid #000; padding: 1px 6px; background: #e0e0e0;">{copy_title}</div>
                
                <div style="background: #000; color: #fff; text-align: center; font-weight: bold; font-size: 9.5px; padding: 2px 0; margin-bottom: 4px;">
                    કાચ, પ્લાસ્ટીક, ફાયબર અથવા લીક્વીડ માલ ડેમેજ અથવા લીક થાય તો તેની જવાબદારી કંપનીની રહેશે નહીં.
                </div>

                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="width: 42%; vertical-align: top;">
                            <h3 style="margin: 0; font-size: 16px; font-weight: 900; line-height: 1.1;">FORTUNE EXPRESS CARGO</h3>
                            <i style="font-size: 9.5px;">Always on Time</i><br>
                            <b>E-mail :</b> fortuneexpresscargo@gmail.com<br>
                            <b>M. :</b> 9173165886
                        </td>
                        <td style="width: 33%; vertical-align: top; font-size: 9.5px; line-height: 1.2;">
                            <b>FORTUNE EXPRESS CARGO</b><br>
                            15, Bhagwan Estate, Opp. Ekta Hotel Lane, Aslali - 382427<br>
                            <b>PAN:</b> AGVPM3701F | <b>GST:</b> 24AGVPM3701F2ZF<br>
                            <b>SAC No. :</b> 9965
                        </td>
                        <td style="width: 25%; vertical-align: top; text-align: center;">
                            <div style="border: 1.5px solid #000; padding: 2px;">
                                <span style="font-size: 8.5px; font-weight: bold;">DOCKET NUMBER</span>
                                <div style="font-size: 18px; font-weight: bold; color: #d32f2f; line-height: 1;">{d['lr_no']}</div>
                                <div style="font-size: 9.5px;"><b>DATE:</b> {d['date']}</div>
                            </div>
                            <table style="width: 100%; border: 1px solid #000; margin-top: 2px; font-size: 9.5px; text-align: left;">
                                <tr><td style="border: 1px solid #000; padding: 1px 3px;"><b>FROM:</b> {d['from']}</td></tr>
                                <tr><td style="border: 1px solid #000; padding: 1px 3px;"><b>TO:</b> {d['to']}</td></tr>
                            </table>
                        </td>
                    </tr>
                </table>

                <table style="width: 100%; border-collapse: collapse; margin-top: 4px; border: 1.5px solid #000; font-size: 9.5px;">
                    <tr>
                        <td style="width: 50%; border: 1px solid #000; padding: 3px; vertical-align: top;">
                            <b>CONSIGNOR DETAILS (PLACE OF SUPPLY)</b><br>
                            NAME: {d['consignor']}<br>
                            GST NO.: {d['consignor_gst']} | CONTACT: {d['consignor_pincode']}
                        </td>
                        <td style="width: 50%; border: 1px solid #000; padding: 3px; vertical-align: top;">
                            <b>CONSIGNEE DETAILS (DELIVERY DESTINATION)</b><br>
                            NAME: {d['consignee']}<br>
                            GST NO.: {d['consignee_gst']} | INSTRUCTION: {d['instruction']}
                        </td>
                    </tr>
                </table>

                <table style="width: 100%; border-collapse: collapse; margin-top: 4px; border: 1.5px solid #000; font-size: 9px; text-align: center;">
                    <tr style="background: #e0e0e0; font-weight: bold;">
                        <td style="border: 1px solid #000; width: 35%; padding: 2px;" colspan="4">PACKAGE INFORMATION</td>
                        <td style="border: 1px solid #000; width: 25%; padding: 2px;" colspan="2">IN RUPEES</td>
                        <td style="border: 1px solid #000; width: 13.3%;">Monthly Billing</td>
                        <td style="border: 1px solid #000; width: 13.3%;">PAID</td>
                        <td style="border: 1px solid #000; width: 13.4%;">TO PAY</td>
                    </tr>
                    <tr style="font-weight: bold;">
                        <td style="border: 1px solid #000; padding: 2px;">TYPE OF PKG</td>
                        <td style="border: 1px solid #000; padding: 2px;">NO OF PKG</td>
                        <td style="border: 1px solid #000; padding: 2px;">VOLUME</td>
                        <td style="border: 1px solid #000; padding: 2px;">TOTAL PKG</td>
                        <td style="border: 1px solid #000; text-align: left; padding: 2px;">BASIC FREIGHT</td>
                        <td style="border: 1px solid #000; text-align: right; padding: 2px;">{d['basic_freight']:.2f}</td>
                        <td style="border: 1px solid #000; font-size: 15px;" rowspan="7">{billing_mark}</td>
                        <td style="border: 1px solid #000; font-size: 15px; color: green;" rowspan="7">{paid_mark}</td>
                        <td style="border: 1px solid #000; font-size: 15px; color: red;" rowspan="7">{topay_mark}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #000; padding: 2px;">{d['pkg_type']}</td>
                        <td style="border: 1px solid #000; padding: 2px;">{d['no_pkg']}</td>
                        <td style="border: 1px solid #000; padding: 2px;">{d['volume']}</td>
                        <td style="border: 1px solid #000; padding: 2px;">{d['total_pkg']}</td>
                        <td style="border: 1px solid #000; text-align: left; padding: 2px;">VAL. SURCHARGE/DOCKET</td>
                        <td style="border: 1px solid #000; text-align: right; padding: 2px;">{(d['val_surcharge'] + d['docket_chg']):.2f}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #000; font-weight: bold; padding: 2px;" colspan="4">INVOICE DETAILS</td>
                        <td style="border: 1px solid #000; text-align: left; padding: 2px;">OTHER/ODA/SURCHARGE</td>
                        <td style="border: 1px solid #000; text-align: right; padding: 2px;">{(d['other_chg'] + d['oda_chg'] + d['surcharges']):.2f}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #000; padding: 2px;">INV: {d['inv_no']}</td>
                        <td style="border: 1px solid #000; padding: 2px;">VAL: {d['inv_val']}</td>
                        <td style="border: 1px solid #000; padding: 2px;">ACT WT: {d['act_wt']}</td>
                        <td style="border: 1px solid #000; padding: 2px;">CHG WT: {d['chg_wt']}</td>
                        <td style="border: 1px solid #000; text-align: left; padding: 2px;">CGST ({d['cgst']}) / SGST ({d['sgst']})</td>
                        <td style="border: 1px solid #000; text-align: right; padding: 2px;">{(d['cgst'] + d['sgst']):.2f}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #000; font-size: 7.5px; text-align: left; padding: 2px;" colspan="4" rowspan="3">
                            <b>BRANCH PHONES:</b> Navsari: 8000537847 | Valsad: 6351700152 | Vapi: 9427335518 | Ankleshwar: 9978811411 | Surat: 8467818918 | Sarkhej: 9427450535 | Madhupura: 9173165886 | Narol: 9427450535
                        </td>
                        <td style="border: 1px solid #000; text-align: left; padding: 2px;">IGST</td>
                        <td style="border: 1px solid #000; text-align: right; padding: 2px;">{d['igst']:.2f}</td>
                    </tr>
                    <tr style="font-weight: bold; background: #e0e0e0;">
                        <td style="border: 1px solid #000; text-align: left; padding: 2px;">GRAND TOTAL</td>
                        <td style="border: 1px solid #000; text-align: right; padding: 2px;">{d['grand_total']:.2f}</td>
                    </tr>
                </table>

                <div style="font-size: 7.5px; margin-top: 3px; text-align: justify; line-height: 1.1;">
                    (૧) પેક દાગીનામાં રહેલા માલ માટેની બીલ અથવા પરમીટ કે E-way bill ની સંપૂર્ણ જવાબદારી ગ્રાહકની રહેશે. (૨) આગ, ચોરી, વરસાદ, અકસ્માત, હુલ્લડ વગેરે અણધાર્યા સંજોગોમાં માલને કોઈપણ નુકશાન થશે તો કંપનીની જવાબદારી રહેશે નહીં. (૩) માલ અંગેની કોઈપણ જાતની ફરીયાદ હશે તો ૧૦ દિવસની અંદર શરુ કરવી. (૪) કોઈપણ કારાણસર ગવર્નમેન્ટ ઓથોરીટી માલ અટકાવશે, જપ્ત કરશે તો કંપની જવાબદાર રહેશે નહીં. (૬) ન્યાયનું ક્ષેત્ર વાપી રહેશે.
                </div>
            </div>

            <div>
                <table style="width: 100%; margin-top: 3px; font-size: 8.5px;">
                    <tr>
                        <td style="width: 60%;">CUSTOMER SIGN: _______________________</td>
                        <td style="width: 40%; text-align: right;"><b>For, Fortune Express Cargo</b></td>
                    </tr>
                </table>
                
                <div style="background: #000; color: #fff; text-align: center; font-weight: bold; font-size: 9px; margin-top: 2px; padding: 2px 0;">
                    કોઈ પણ માલ ૧૦ દિવસ માં છોડાવવામાં નહીં આવે તો ડેમરેજ ચાર્જ લગાવવામાં આવશે. જે પાર્ટીની જવાબદારી રહેશે.
                </div>
            </div>
        </div>
        """

    full_html = f"""
    <style>
        @media print {{
            @page {{
                size: A4 portrait;
                margin: 2mm 5mm 2mm 5mm;
            }}
            html, body {{
                height: 100%;
                margin: 0 !important;
                padding: 0 !important;
                overflow: hidden;
            }}
            .print-btn {{
                display: none !important;
            }}
            .copy-box {{
                height: 32.5vh !important;
                page-break-inside: avoid !important;
            }}
        }}
    </style>
    <div style="text-align: center; margin-bottom: 10px;" class="print-btn">
        <button onclick="window.print()" style="background-color: #008CBA; color: white; padding: 10px 20px; border: none; font-size: 15px; font-weight: bold; border-radius: 5px; cursor: pointer;">
            🖨️ PRINT ALL 3 COPIES (FULL A4 PAGE)
        </button>
    </div>
    {get_receipt_html("CONSIGNOR COPY")}
    {get_receipt_html("CONSIGNEE COPY")}
    {get_receipt_html("DRIVER COPY")}
    """

    st.markdown("---")
    st.components.v1.html(full_html, height=1400, scrolling=True)

st.markdown("---")
st.subheader("📊 જુનો બધો ડેટા (Saved LR History)")
st.dataframe(pd.read_csv(DATA_FILE), use_container_width=True)
