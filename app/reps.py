import xml.etree.ElementTree as ET
import pandas as pd
import requests

ROOT = 'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs'

# example report: https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2024/20024769.pdf
# ROOT/year/doc_id.pdf
# 8 digit id
# 20025107 doc id -> valid pdf
# 7 digit id
# 8220177 doc id -> hand delivered - scanned pdf

# Parse the XML file
tree = ET.parse('data/2024FD.xml')  # Replace 'your_file.xml' with the actual filename
root = tree.getroot()

pdfs = []

# Iterate over each member element in the XML
for member in root.findall('Member'):
    filing_type = member.find('FilingType').text
    
    if filing_type == 'P':
        # Extract relevant data
        prefix = member.find('Prefix').text or ''
        last_name = member.find('Last').text or ''
        first_name = member.find('First').text or ''
        suffix = member.find('Suffix').text or ''
        state_dst = member.find('StateDst').text or ''
        year = member.find('Year').text or ''
        filing_date = member.find('FilingDate').text or ''
        doc_id = member.find('DocID').text or ''
        
        # Construct the URL for the document PDF
        pdf_url = f'{ROOT}/{year}/{doc_id}.pdf'
        # Check if the DocID is 8 digits (valid PDF) or 7 digits (scanned PDF)
        if len(doc_id) == 8:
            # Check if the PDF URL is valid
            response = requests.head(pdf_url)
            if response.status_code == 200:
                print(f'[VALID] PDF found for {first_name} {last_name} at {pdf_url}')
                pdfs.append({
                    'Prefix': prefix,
                    'LastName': last_name,
                    'FirstName': first_name,
                    'Suffix': suffix,
                    'StateDst': state_dst,
                    'Year': year,
                    'FilingDate': filing_date,
                    'DocID': doc_id,
                    'PDF_URL': pdf_url,
                    'PDF_Status': 'Valid'
                })
            else:
                print(f'[INVALID] PDF not found for {first_name} {last_name} at {pdf_url}')
        elif len(doc_id) == 7:
            print(f'[SCANNED] Scanned PDF for {first_name} {last_name} at {pdf_url}')
            pdfs.append({
                'Prefix': prefix,
                'LastName': last_name,
                'FirstName': first_name,
                'Suffix': suffix,
                'StateDst': state_dst,
                'Year': year,
                'FilingDate': filing_date,
                'DocID': doc_id,
                'PDF_URL': pdf_url,
                'PDF_Status': 'Scanned'
            })
      

# Convert the list to a DataFrame
df = pd.DataFrame(pdfs)

# Save the DataFrame to a CSV file
df.to_csv('output/filtered_members.csv', index=False)

print("Filtered members saved to 'output/filtered_members.csv'")