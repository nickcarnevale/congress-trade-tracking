import xml.etree.ElementTree as ET
import pandas as pd

ROOT = 'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs'

# Parse the XML file
tree = ET.parse('data/2024FD.xml')  # Replace 'your_file.xml' with the actual filename
root = tree.getroot()

# Initialize a list to store members with FilingType 'P'
filtered_members = []

# Iterate over each Member element in the XML
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
        
        # Append the member information to the list
        filtered_members.append({
            'Prefix': prefix,
            'LastName': last_name,
            'FirstName': first_name,
            'Suffix': suffix,
            'StateDst': state_dst,
            'Year': year,
            'FilingDate': filing_date,
            'DocID': doc_id
        })

# Convert the list to a DataFrame
df = pd.DataFrame(filtered_members)

print(filtered_members)

# Save the DataFrame to a CSV file
df.to_csv('output/filtered_members.csv', index=False)

print("Filtered members saved to 'output/filtered_members.csv'")




