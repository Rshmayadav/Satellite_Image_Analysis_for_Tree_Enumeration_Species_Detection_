import os

import matplotlib.pyplot as plt
import requests
from fpdf import FPDF

# URLs of your two models
url_model_1 = "http://127.0.0.1:5000/upload"  # Flask app 1
url_model_2 = "http://127.0.0.1:5001/upload"  # Flask app 2

# Function to fetch tree count from model API using the uploaded file
def fetch_tree_count(file, url):
    files = {'file': file}
    response = requests.post(url, files=files)
    if response.status_code == 200:
        return response.json().get('tree_count', 0)
    else:
        print(f"Failed to get tree count from {url}")
        return 0

# Function to process image and create PDF report
def generate_report(image_path):
    # Open the image file
    with open(image_path, 'rb') as image_file:
        # Fetch tree counts from both models
        tree_count_model_1 = fetch_tree_count(image_file, url_model_1)
        
        # Reset the file pointer before making the second request
        image_file.seek(0)
        tree_count_model_2 = fetch_tree_count(image_file, url_model_2)

        # Create a pie chart
        labels = ['Model 1 Trees', 'Model 2 Trees']
        sizes = [tree_count_model_1, tree_count_model_2]

        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures that the pie chart is circular.
        pie_chart_path = "tree_count_pie_chart.png"
        plt.savefig(pie_chart_path)
        plt.close()

        # Generate the PDF Report
        pdf = FPDF()

        # Add a page
        pdf.add_page()

        # Title
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(200, 10, txt="Tree Detection Report", ln=True, align='C')

        # Add Tree Counts
        pdf.ln(10)  # Add some vertical space
        pdf.set_font('Arial', '', 12)
        pdf.cell(200, 10, txt=f"Tree Count from Model 1: {tree_count_model_1}", ln=True)
        pdf.cell(200, 10, txt=f"Tree Count from Model 2: {tree_count_model_2}", ln=True)
        pdf.cell(200, 10, txt=f"Total Tree Count: {tree_count_model_1 + tree_count_model_2}", ln=True)

        # Add Pie Chart Image
        if os.path.exists(pie_chart_path):
            pdf.ln(10)  # Add space before the image
            pdf.image(pie_chart_path, x=10, y=None, w=100)  # Position and size the image

        # Save PDF to file
        pdf_output_path = "tree_count_report.pdf"
        pdf.output(pdf_output_path)

        print(f"PDF Report saved as {pdf_output_path}")

# Example usage with an uploaded image (image path to be fetched dynamically from Flask apps)
uploaded_image_path = "R2SP2/static/aerial-view-coconut-palm-trees-plantation_335224-741 (2) (1).avif"  # This will be dynamically replaced
generate_report(uploaded_image_path)
