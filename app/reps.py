import xml.etree.ElementTree as ET
import pandas as pd
import requests
import os

ROOT = 'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs'

# example report: https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2024/20024769.pdf
# ROOT/year/doc_id.pdf
# 8 digit id
# 20025107 doc id -> valid pdf
# 7 digit id
# 8220177 doc id -> hand delivered - scanned pdf

def process_xml_file(file_path, existing_df):
    tree = ET.parse(file_path)
    root = tree.getroot()

    pdfs = []

    for member in root.findall('Member'):
        filing_type = member.find('FilingType').text

        if filing_type == 'P':
            prefix = member.find('Prefix').text or ''
            last_name = member.find('Last').text or ''
            first_name = member.find('First').text or ''
            suffix = member.find('Suffix').text or ''
            state_dst = member.find('StateDst').text or ''
            year = member.find('Year').text or ''
            filing_date = member.find('FilingDate').text or ''
            doc_id = member.find('DocID').text or ''

            pdf_url = f'{ROOT}/{year}/{doc_id}.pdf'

            if len(doc_id) == 8:
                response = requests.head(pdf_url)
                pdf_status = 'Valid' if response.status_code == 200 else 'Invalid'
            elif len(doc_id) == 7:
                pdf_status = 'Scanned'
            else:
                continue

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
                'PDF_Status': pdf_status
            })

    if pdfs:
        new_df = pd.DataFrame(pdfs)
        new_df['FilingDate'] = pd.to_datetime(new_df['FilingDate'], format='%m/%d/%Y', errors='coerce')
        existing_df = pd.concat([existing_df, new_df], ignore_index=True)
        existing_df = existing_df.sort_values(by=['LastName', 'FilingDate'], ascending=[True, False])
    
    return existing_df

# Load the initial DataFrame from the CSV file
df = pd.read_csv('data/pre-2024-rep-data.csv')

# Iterate over all XML files in the data directory
for filename in os.listdir('input/'):
    if filename.endswith('.xml'):
        file_path = os.path.join('input/', filename)
        print(f'Processing {file_path}...')
        
        df = process_xml_file(file_path, df)

# Save the sorted DataFrame to a CSV file
df.to_csv('output/filtered_members.csv', index=False)

print("Filtered members saved to 'output/filtered_members.csv'")