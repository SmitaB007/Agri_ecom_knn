from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer,SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from django.core.files.base import ContentFile
from io import BytesIO
import os
from django.conf import settings




def generate_invoice(invoice, buffer=None):
    
    if buffer is None:
        from io import BytesIO
        buffer = BytesIO()

    
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []


    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    normal_style = styles["Normal"]


    elements.append(Paragraph("Sai-Krupa Agrotech", title_style))
    elements.append(Spacer(1, 20))  

   
    invoice_details = f"""
        <b>Order No.:</b> {invoice.order.id}<br/>
        <b>Date:</b> {invoice.created_at.strftime('%Y-%m-%d')}<br/>
        <b>Customer Name:</b> {invoice.user.username}<br/>
        <b>Shipping Address:</b> {invoice.order.Shipping_address}<br/>
        <b>Email:</b> {invoice.user.email}<br/>
        <b>Payment method:</b>{invoice.order.payment_method}<br/>
    """
    elements.append(Paragraph(invoice_details, normal_style))
    elements.append(Spacer(1, 20))  

    
    data = [["Product No.", "Product", "Price"]]
    order_items = invoice.items.all()
   
    for i in order_items:
        data.append([str(i),Paragraph(i.product.name,normal_style),i.product.price])
  
   
    table = Table(data, colWidths=[100, 200, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 1), (-1, -1), 'TOP'),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 20))  # Add spacing

    footer_details = f"""
        <b>Total Amount:</b> ₹{invoice.order.amount_paid:.2f}<br/>
        Thank you for shopping with us.<br/>
        Contact for any queries: saikrupa@agrotech.com
    """
    elements.append(Paragraph(footer_details, normal_style))

    
    doc.build(elements)

   
    buffer.seek(0)
    return buffer





































































# def generate_invoice(invoice):
    
#     file_name = f"invoice_{invoice.invoice_number}.pdf"
#     file_path = os.path.join(settings.MEDIA_ROOT,'invoices',file_name)
#     c = canvas.Canvas(file_path, pagesize=letter)
#     page_width, page_height = letter

  
#     c.setFont("Helvetica-Bold", 20)
#     c.drawCentredString(page_width / 2, page_height - 50, "Sai-Krupa Agrotech")

    
#     c.setFont("Helvetica", 12)
#     c.drawString(50, page_height - 100, "Add:")

    
#     c.drawString(50, page_height - 130, f"Order no.:{invoice.order.id}")
#     c.drawString(300, page_height - 130, f"Date:{invoice.created_at.strftime('%Y-%m-%d')}")


    
#     c.drawString(50, page_height - 160, f"Customer name:{invoice.user.username}")
#     c.drawString(50, page_height - 190, f"Shipping address:{invoice.order.Shipping_address}")

    
#     c.drawString(50, page_height - 220, f"Email:{invoice.user.email}")

#     data = [
#         ["Product no.", "Product", "Price"]
#     ]
#     order_items = invoice.items.filter(user=invoice.user.id)
#     products = [order_item.product for order_item in order_items]
#     for idx, product in enumerate(products, start=1):
#         data.append([str(idx), product.name, f"₹{product.price}"])
        
#     table = Table(data, colWidths=[100, 200, 100, 100])
#     table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#     ]))
#     table.drawOn(c, 50, page_height - 350)

    
#     c.drawString(50, page_height - 400, f"Total amount:{invoice.order.amount_paid}")
#     c.drawString(50, page_height - 430, "Discount:")

   
#     c.drawString(50, page_height - 500, "Thank you for shopping with us.")
#     c.drawString(50, page_height - 520, "Contact for any queries: saikrupa@agrotech.com")

    
#     c.save()
#     return file_name




