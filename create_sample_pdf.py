from reportlab.pdfgen import canvas

pdf = canvas.Canvas("sample.pdf")

pdf.drawString(100, 750, "Sovereign Agentic AI Workbench")
pdf.drawString(100, 720, "Project Type: AI Agent System")
pdf.drawString(100, 690, "Status: Development")
pdf.drawString(100, 660, "Purpose: Confidential industrial document processing.")

pdf.save()

print("sample.pdf created successfully")