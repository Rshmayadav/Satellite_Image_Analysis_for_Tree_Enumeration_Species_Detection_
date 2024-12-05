# import os
# from datetime import datetime

# import matplotlib.pyplot as plt
# from fpdf import FPDF

# # Paths to the count files
# count_file_1 = 'static/tree_count_model_1.txt'
# count_file_2 = 'static/tree_count_model_2.txt'

# # Function to create a pie chart
# def create_pie_chart(counts, labels, output_file):
#     plt.figure(figsize=(6, 6))
#     plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=140)
#     plt.title('Tree Count Distribution')
#     plt.savefig(output_file, transparent=True)  # Save with a transparent background
#     plt.close()

# # Create the PDF report with a background image
# class PDF(FPDF):
#     def header(self):
#         # Add a background image to the entire page
#         self.image(background_img_path, x=0, y=0, w=210, h=297)  # A4 size page in mm

#     def footer(self):
#         # Optional: You can add a page number or footer here if needed
#         pass

# # Background image path
# background_img_path = 'static/beautiful.jpg'  # Make sure this file exists

# # Create an instance of the PDF class
# pdf = PDF()

# # Add a new page with the background image
# pdf.add_page()

# # Set font
# pdf.set_font("Arial", size=12)

# # Add title
# pdf.cell(200, 10, txt="Tree Counting Report", ln=True, align='C')

# # Add tree counts from Model 1
# with open(count_file_1, 'r') as file:
#     count_1 = file.read()
# pdf.multi_cell(0, 10, txt=f"Total tree count: {count_1.split(': ')[1]}")

# # Add tree counts from Model 2
# with open(count_file_2, 'r') as file:
#     count_2 = file.read()
# pdf.multi_cell(0, 10, txt=f"Species count: {count_2.split(': ')[1]}")

# # Create pie chart
# pie_chart_path = 'static/pie_chart.png'
# create_pie_chart([int(count_1.split(': ')[1]), int(count_2.split(': ')[1])], ['Model 1', 'Model 2'], pie_chart_path)

# # Add pie chart to the same page
# pdf.image(pie_chart_path, x=15, y=100, w=180)

# # Save the PDF to the Downloads folder with a unique name
# downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')

# # Generate a unique filename using a timestamp
# timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
# pdf_filename = f'tree_count_report_{timestamp}.pdf'
# pdf_output_path = os.path.join(downloads_folder, pdf_filename)

# pdf.output(pdf_output_path)

# print(f"Report generated and saved to {pdf_output_path}")
def generate_report(count_1, count_2):
    report_path = 'static/tree_count_report.pdf'
    pie_chart_path = 'static/pie_chart.png'
    histogram_path = 'static/histogram.png'

    # Create a text file for the report
    with open('static/tree_count_report.txt', 'w') as file:
        file.write(f"Total Tree Count: {count_1}\n")
        file.write(f"Species Tree Count: {count_2}\n")

    # Calculate other tree count
    other_trees = int(count_1) - int(count_2)

    # Generate pie chart
    plt.figure()
    plt.pie([int(count_2), other_trees], labels=['Species Trees', 'Other Trees'], autopct='%1.1f%%')
    plt.title("Tree Count Distribution")
    plt.savefig(pie_chart_path)
    plt.close()

    # Generate histogram
    plt.figure()
    plt.hist([int(count_2), other_trees], bins=[0, int(count_2) + 1, other_trees + 1], edgecolor='black')
    plt.title("Tree Count Histogram")
    plt.xlabel("Tree Count")
    plt.ylabel("Frequency")
    plt.savefig(histogram_path)
    plt.close()

    # Generate PDF report
    pdf = FPDF()
    
    # First page
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt="Tree Detection Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font('Arial', '', 12)
    pdf.cell(200, 10, txt=f"Total Tree Count: {count_1}", ln=True)
    pdf.cell(200, 10, txt=f"Species Tree Count: {count_2}", ln=True)
    pdf.cell(200, 10, txt=f"Other Tree Count: {other_trees}", ln=True)
    
    # Second page
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(200, 10, txt="Visualizations", ln=True, align='C')
    
    pdf.ln(10)
    if os.path.exists(pie_chart_path):
        pdf.image(pie_chart_path, x=10, y=None, w=180)
    
    pdf.ln(10)
    if os.path.exists(histogram_path):
        pdf.image(histogram_path, x=10, y=None, w=180)
    
    pdf.output(report_path)

    print(f"PDF Report saved as {report_path}")
