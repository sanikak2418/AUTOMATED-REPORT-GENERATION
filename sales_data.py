import pandas as pd
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch

# Step 1: Read Data
df = pd.read_csv("sales_data.csv")

# Step 2: Basic Analysis
df["Sales"] = df["Quantity"] * df["Price"]
total_sales = df["Sales"].sum()
average_sales = df["Sales"].mean()

# Group by Product instead of Department
department_sales = df.groupby("Product")["Sales"].sum()

# Step 3: Create Chart
plt.figure()
department_sales.plot(kind='bar')
plt.title("Product-wise Sales")
plt.xlabel("Product")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig("sales_chart.png")
plt.close()

# Step 4: Create PDF
pdf = SimpleDocTemplate("Sales_Report.pdf")
elements = []

styles = getSampleStyleSheet()
elements.append(Paragraph("<b>Sales Report</b>", styles["Title"]))
elements.append(Spacer(1, 0.5 * inch))

elements.append(Paragraph(f"Total Sales: ₹{total_sales}", styles["Normal"]))
elements.append(Paragraph(f"Average Sales: ₹{average_sales:.2f}", styles["Normal"]))
elements.append(Spacer(1, 0.5 * inch))

# Add Table
table_data = [df.columns.tolist()] + df.values.tolist()
table = Table(table_data)

table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))

elements.append(table)
elements.append(Spacer(1, 0.5 * inch))

# Add Chart Image
elements.append(Image("sales_chart.png", width=4*inch, height=3*inch))

pdf.build(elements)

print("Report Generated Successfully!")
