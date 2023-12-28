#Written by Marshall Doyle on 9/26/2023
import csv
from collections import defaultdict

# Read the data from the input CSV file with UTF-8 encoding
with open('C:/Users/marsh/OneDrive/Desktop/Patent Tracking/cleaned_combined_assignee_September25.csv', 'r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    data = list(reader)  # Convert the reader object to a list to get the total number of rows
    total_rows = len(data)
    company_names = [row[3] for row in data]

# Count the occurrences of each company name
company_name_count = defaultdict(int)
for index, name in enumerate(company_names, 1):  # Start enumeration from 1 for row numbers
    # Calculate and print the current processing percentage
    percentage = (index / total_rows) * 100
    print(f"Processing row {index} of {total_rows} ({percentage:.2f}% completed)")
    
    # Remove commas, ampersands, and periods and convert to lowercase
    cleaned_name = name.replace(',', '').replace('&', '').replace('.', '').lower()
    
    company_name_count[cleaned_name] += 1

# Sort the company name counts by count in descending order
sorted_company_name_count = sorted(company_name_count.items(), key=lambda x: x[1], reverse=True)

# Write the sorted company name counts to a new CSV file with UTF-8 encoding
with open('CompanyNameCount_September25.csv', 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['Company Name', 'Count'])  # Write the header
    writer.writerows(sorted_company_name_count)

print("Company name counts have been written to output_company_names.csv")
