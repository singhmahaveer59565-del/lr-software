import os
import pandas as pd
import streamlit as st
from datetime import datetime
from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

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
        consignor = st.text_input("Consignor Name", "IFFCO - MC CROP SCIENCE PVT LTD")
        consignor_gst = st.text_input("Consignor GST", "24AADCI9008G1ZR")
        consignor_contact = st.text_input("Consignor Contact", "")
        from_place = st.text_input("From", "Aslali")
        
    with col2:
        consignee = st.text_input("Consignee Name", "VALSAD VIBHAG FARMER")
        consignee_gst = st.text_input("Consignee GST / Contact", "")
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

    submit = st.form_submit_button("SAVE & GENERATE PERFECT PDF LR")

def generate_pdf_bytes(d):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=15, rightMargin=15,
        topMargin=15, bottomMargin=15
    )
    
    styles = getSampleStyleSheet()

    style_disclaimer = ParagraphStyle('Disc', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=6.5, leading=8, textColor=colors.white, alignment=1)
    style_header_contact = ParagraphStyle('HContact', parent=styles['Normal'], fontName='Helvetica', fontSize=7, leading=9, textColor=colors.black)
    style_address = ParagraphStyle('Address', parent=styles['Normal'], fontName='Helvetica', fontSize=7, leading=9, textColor=colors.black)
    style_docket_box = ParagraphStyle('DBox', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=10, alignment=1)
    style_docket_num = ParagraphStyle('DNum', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=13, leading=14, textColor=colors.HexColor('#C00000'), alignment=1)
    style_party_body = ParagraphStyle('PBody', parent=styles['Normal'], fontName='Helvetica', fontSize=7, leading=9, textColor=colors.black)
    style_tbl_hdr = ParagraphStyle('THdr', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=6.5, leading=8, alignment=1)
    style_tbl_cell = ParagraphStyle('TCell', parent=styles['Normal'], fontName='Helvetica', fontSize=6.5, leading=8, alignment=1)
    style_tbl_cell_left = ParagraphStyle('TCellL', parent=styles['Normal'], fontName='Helvetica', fontSize=6.5, leading=8, alignment=0)
    style_tbl_cell_right = ParagraphStyle('TCellR', parent=styles['Normal'], fontName='Helvetica', fontSize=6.5, leading=8, alignment=2)
    style_handwritten = ParagraphStyle('HW', parent=styles['Normal'], fontName='Times-BoldItalic', fontSize=13, leading=14, textColor=colors.HexColor('#002060'), alignment=1)
    style_guqrati_terms = ParagraphStyle('GTerms', parent=styles['Normal'], fontName='Helvetica', fontSize=5.5, leading=7, textColor=colors.HexColor('#222222'))
    style_sign = ParagraphStyle('Sign', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=6.5, leading=8)

    def build_copy_block(copy_title):
        block_elements = []
        
        banner_p = Paragraph("કાચ, પ્લાસ્ટીક, ફાયબર અથવા લીક્વીડ માલ ડેમેજ અથવા લીક થાય તો તેની જવાબદારી કંપનીની રહેશે નહીં.", style_disclaimer)
        t_banner = Table([[banner_p]], colWidths=[550])
        t_banner.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.black),
            ('TOPPADDING', (0,0), (-1,-1), 1.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ]))
        
        copy_tag_p = Paragraph(f"<b>{copy_title}</b>", ParagraphStyle('Tag', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7, alignment=2))
        t_tag = Table([[copy_tag_p]], colWidths=[550])
        t_tag.setStyle(TableStyle([('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 1)]))
        
        c1_html = Paragraph(f"<b><font size=12>FORTUNE EXPRESS CARGO</font></b><br/><font size=7 color='#333333'><i>Always on Time</i></font><br/><font size=6.5><b>E-mail :</b> fortuneexpresscargo@gmail.com<br/><b>M. :</b> 9173165886</font>", style_header_contact)
        c2_html = Paragraph("<b>FORTUNE EXPRESS CARGO</b><br/>15, Bhagwan Estate, Opp. Ekta Hotel Lane, Aslali - 382427<br/><b>PAN:</b> AGVPM3701F | <b>GST:</b> 24AGVPM3701F2ZF<br/><b>SAC No. :</b> 9965", style_address)
        
        docket_table_data = [
            [Paragraph("DOCKET NUMBER", style_docket_box)],
            [Paragraph(str(d['lr_no']), style_docket_num)],
            [Paragraph(f"<b>DATE:</b> {d['date']}", ParagraphStyle('DD', parent=styles['Normal'], fontName='Helvetica', fontSize=7, alignment=1))],
            [Paragraph(f"<b>FROM:</b> {d['from']}", ParagraphStyle('DF', parent=styles['Normal'], fontName='Helvetica', fontSize=6.5))],
            [Paragraph(f"<b>TO:</b> {d['to']}", ParagraphStyle('DT', parent=styles['Normal'], fontName='Helvetica', fontSize=6.5))]
        ]
        t_docket = Table(docket_table_data, colWidths=[110])
        t_docket.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
            ('TOPPADDING', (0,0), (-1,-1), 1), ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ]))
        
        t_header = Table([[c1_html, c2_html, t_docket]], colWidths=[240, 195, 115])
        t_header.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 2)]))
        
        party_data = [
            [
                Paragraph(f"<b>CONSIGNOR DETAILS (PLACE OF SUPPLY)</b><br/>NAME: {d['consignor']}<br/>GST NO.: {d['consignor_gst']} | CONTACT: {d.get('consignor_contact', '')}", style_party_body),
                Paragraph(f"<b>CONSIGNEE DETAILS (DELIVERY DESTINATION)</b><br/>NAME: {d['consignee']}<br/>GST NO.: {d.get('consignee_gst', '')} | INSTRUCTION: {d['instruction']}", style_party_body)
            ]
        ]
        t_party = Table(party_data, colWidths=[275, 275])
        t_party.setStyle(TableStyle([('BOX', (0,0), (-1,-1), 1, colors.black), ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black), ('TOPPADDING', (0,0), (-1,-1), 2), ('BOTTOMPADDING', (0,0), (-1,-1), 2)]))
        
        paid_pen = Paragraph("<i><b>✓ Paid</b></i>", style_handwritten) if d['pay_type'] == 'PAID' else Paragraph("", style_handwritten)
        topay_pen = Paragraph("<i><b>✓ To Pay</b></i>", style_handwritten) if d['pay_type'] == 'TO PAY' else Paragraph("", style_handwritten)
        bill_pen = Paragraph("<i><b>✓ Billing</b></i>", style_handwritten) if d['pay_type'] == 'Monthly Billing' else Paragraph("", style_handwritten)

        main_tbl_data = [
            [Paragraph("PACKAGE INFORMATION", style_tbl_hdr), "", "", "", Paragraph("IN RUPEES", style_tbl_hdr), "", Paragraph("Monthly Billing", style_tbl_hdr), Paragraph("PAID", style_tbl_hdr), Paragraph("TO PAY", style_tbl_hdr)],
            [Paragraph("TYPE OF PKG", style_tbl_hdr), Paragraph("NO OF PKG", style_tbl_hdr), Paragraph("VOLUME", style_tbl_hdr), Paragraph("TOTAL PKG", style_tbl_hdr), Paragraph("BASIC FREIGHT", style_tbl_cell_left), Paragraph(f"{d['basic_freight']:.2f}", style_tbl_cell_right), bill_pen, paid_pen, topay_pen],
            [Paragraph(str(d['pkg_type']), style_tbl_cell), Paragraph(str(d['no_pkg']), style_tbl_cell), Paragraph(str(d['volume']), style_tbl_cell), Paragraph(str(d['total_pkg']), style_tbl_cell), Paragraph("VAL. SURCHARGE/DOCKET", style_tbl_cell_left), Paragraph(f"{(d['val_surcharge']+d['docket_chg']):.2f}", style_tbl_cell_right), "", "", ""],
            [Paragraph("INVOICE DETAILS", style_tbl_hdr), "", "", "", Paragraph("OTHER/ODA/SURCHARGE", style_tbl_cell_left), Paragraph(f"{(d['other_chg']+d['oda_chg']+d['surcharges']):.2f}", style_tbl_cell_right), "", "", ""],
            [Paragraph(f"INV: {d['inv_no']}", style_tbl_cell_left), Paragraph(f"VAL: {d['inv_val']}", style_tbl_cell_left), Paragraph(f"ACT WT: {d['act_wt']}", style_tbl_cell_left), Paragraph(f"CHG WT: {d['chg_wt']}", style_tbl_cell_left), Paragraph(f"CGST ({d['cgst']}) / SGST ({d['sgst']})", style_tbl_cell_left), Paragraph(f"{(d['cgst']+d['sgst']):.2f}", style_tbl_cell_right), "", "", ""],
            [Paragraph("BRANCH PHONES: Navsari: 8000537847 | Valsad: 6351700152 | Vapi: 9427335518 | Ankleshwar: 9978811411 | Surat: 8467818918 | Sarkhej: 9427450535 | Madhupura: 9173165886 | Narol: 9427450535", style_tbl_cell_left), "", "", "", Paragraph("IGST", style_tbl_cell_left), Paragraph(f"{d['igst']:.2f}", style_tbl_cell_right), "", "", ""],
            ["", "", "", "", Paragraph("GRAND TOTAL", style_tbl_hdr), Paragraph(f"{d['grand_total']:.2f}", style_tbl_hdr), "", "", ""]
        ]
        
        t_main = Table(main_tbl_data, colWidths=[45, 45, 45, 55, 120, 50, 60, 65, 65])
        t_main.setStyle(TableStyle([
            ('SPAN', (0,0), (3,0)), ('SPAN', (4,0), (5,0)), ('SPAN', (0,3), (3,3)), ('SPAN', (0,5), (3,6)),
            ('SPAN', (6,1), (6,6)), ('SPAN', (7,1), (7,6)), ('SPAN', (8,1), (8,6)),
            ('BOX', (0,0), (-1,-1), 1, colors.black), ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
            ('BACKGROUND', (0,0), (5,0), colors.HexColor('#E0E0E0')), ('BACKGROUND', (4,6), (5,6), colors.HexColor('#E0E0E0')),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('TOPPADDING', (0,0), (-1,-1), 1), ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ]))
        
        terms_p = Paragraph("""(૧) પેક દાગીનામાં રહેલા માલ માટેની બીલ અથવા પરમીટ કે E-way bill ની સંપૂર્ણ જવાબદારી ગ્રાહકની રહેશે. (૨) આગ, ચોરી, વરસાદ, અકસ્માત, હુલ્લડ વગેરે અણધાર્યા સંજોગોમાં માલને કોઈપણ નુકશાન થશે તો કંપનીની જવાબદારી રહેશે નહીં. (૩) માલ અંગેની કોઈપણ જાતની ફરીયાદ હશે તો ૧૦ દિવસની અંદર શરુ કરવી. (૪) કોઈપણ કારાણસર ગવર્નમેન્ટ ઓથોરીટી માલ અટકાવશે, જપ્ત કરશે તો કંપની જવાબદાર રહેશે નહીં. (૬) ન્યાયનું ક્ષેત્ર વાપી રહેશે.""", style_guqrati_terms)
        
        t_sign = Table([[Paragraph("CUSTOMER SIGN: _______________________", style_sign), Paragraph("<b>For, Fortune Express Cargo</b>", ParagraphStyle('RS', parent=style_sign, alignment=2))]], colWidths=[275, 275])
        t_sign.setStyle(TableStyle([('TOPPADDING', (0,0), (-1,-1), 2), ('BOTTOMPADDING', (0,0), (-1,-1), 1)]))
        
        bottom_bar_p = Paragraph("કોઈ પણ માલ ૧૦ દિવસ માં છોડાવવામાં નહીં આવે તો ડેમરેજ ચાર્જ લગાવવામાં આવશે. જે પાર્ટીની જવાબદારી રહેશે.", style_disclaimer)
        t_bottom_bar = Table([[bottom_bar_p]], colWidths=[550])
        t_bottom_bar.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.black), ('TOPPADDING', (0,0), (-1,-1), 1.5), ('BOTTOMPADDING', (0,0), (-1,-1), 1.5)]))
        
        cut_line_p = Paragraph("✂️ -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------", ParagraphStyle('CL', parent=styles['Normal'], fontName='Helvetica', fontSize=6, alignment=1, textColor=colors.HexColor('#666666')))
        
        block_elements.extend([t_tag, t_banner, Spacer(1, 2), t_header, Spacer(1, 2), t_party, Spacer(1, 2), t_main, Spacer(1, 2), terms_p, Spacer(1, 2), t_sign, Spacer(1, 1), t_bottom_bar, Spacer(1, 3), cut_line_p, Spacer(1, 4)])
        return block_elements

    story = []
    story.extend(build_copy_block("CONSIGNOR COPY"))
    story.extend(build_copy_block("CONSIGNEE COPY"))
    story.extend(build_copy_block("DRIVER COPY"))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

if submit:
    subtotal = basic_freight + val_surcharge + docket_chg + other_chg + oda_chg + surcharges
    cgst = round(subtotal * 0.09, 2) if tax_type == "SGST/CGST (18%)" else 0.0
    sgst = round(subtotal * 0.09, 2) if tax_type == "SGST/CGST (18%)" else 0.0
    igst = round(subtotal * 0.18, 2) if tax_type == "IGST (18%)" else 0.0
    grand_total = round(subtotal + cgst + sgst + igst, 2)

    data_dict = {
        "lr_no": lr_no, "date": str(date), "consignor": consignor, "consignor_gst": consignor_gst,
        "consignor_contact": consignor_contact, "consignee": consignee, "consignee_gst": consignee_gst,
        "from": from_place, "to": to_place, "instruction": instruction, "pkg_type": pkg_type,
        "no_pkg": no_pkg, "volume": volume, "total_pkg": total_pkg, "inv_no": inv_no, "inv_val": inv_val,
        "act_wt": act_wt, "chg_wt": chg_wt, "basic_freight": basic_freight, "val_surcharge": val_surcharge,
        "docket_chg": docket_chg, "other_chg": other_chg, "oda_chg": oda_chg, "surcharges": surcharges,
        "cgst": cgst, "sgst": sgst, "igst": igst, "grand_total": grand_total, "pay_type": pay_type
    }
    
    pdf_out = generate_pdf_bytes(data_dict)
    st.download_button(
        label="📄 DOWNLOAD 100% PERFECT PDF (ALL 3 COPIES ON 1 PAGE)",
        data=pdf_out,
        file_name=f"Fortune_LR_{lr_no}.pdf",
        mime="application/pdf"
    )
