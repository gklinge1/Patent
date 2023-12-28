import csv
import os

def find_right_most_column(fieldnames, possible_columns):
    # Identify the right-most column from the list of possible columns
    right_most_column = None
    for col in reversed(fieldnames):
        if col in possible_columns:
            right_most_column = col
            break
    return right_most_column

def sort_csv_alphabetically(input_file_path, output_file_path, column_name):
    with open(input_file_path, mode='r', newline='', encoding='utf-8') as file_in:
        reader = csv.DictReader(file_in)
        fieldnames = reader.fieldnames
        first_row = next(reader)
        if column_name not in fieldnames:
            print(f"Column '{column_name}' not found. Skipping this sort method.")
            return  # Skip sorting if the column doesn't exist
        data = [row for row in reader]
    
    # Sort the data by the target column, ignoring case
    data.sort(key=lambda row: row.get(column_name, '').lower())
    
    with open(output_file_path, mode='w', newline='', encoding='utf-8') as file_out:
        writer = csv.DictWriter(file_out, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(first_row)  # Write the unsorted first row
        writer.writerows(data)

# Define the input directory and output directory
input_directory = 'C:/Users/marsh/Patent Tracking/Cleaned'
output_directory = 'C:/Users/marsh/Patent Tracking/Sorted'

# Create subdirectories for each sort type
assignee_output_directory = os.path.join(output_directory, 'assignee')
alphabetical_name_output_directory = os.path.join(output_directory, 'alphabetical_company_name')
assignee_cleaned_output_directory = os.path.join(output_directory, 'assignee_cleaned')
companyname_output_directory = os.path.join(output_directory, 'companyname')  # New subdirectory for companyname
os.makedirs(assignee_output_directory, exist_ok=True)
os.makedirs(alphabetical_name_output_directory, exist_ok=True)
os.makedirs(assignee_cleaned_output_directory, exist_ok=True)
os.makedirs(companyname_output_directory, exist_ok=True)  # Ensure creation of new directory

# Iterate through each CSV file in the input directory
for file_name in os.listdir(input_directory):
    if file_name.lower().endswith('.csv'):
        input_file_path = os.path.join(input_directory, file_name)
        
        # Read fieldnames to determine the right-most 'assignee', 'assignee_cleaned', or 'companyname' column
        with open(input_file_path, mode='r', newline='', encoding='utf-8') as file_in:
            reader = csv.DictReader(file_in)
            right_most_assignee_column = find_right_most_column(reader.fieldnames, ['assignee', 'assignee_cleaned'])
            right_most_companyname_column = find_right_most_column(reader.fieldnames, ['companyname'])
        
        # Sorting by 'assignee' or 'assignee_cleaned'
        if right_most_assignee_column:
            assignee_cleaned_output_file_path = os.path.join(assignee_cleaned_output_directory, file_name)
            print(f"Sorting file by '{right_most_assignee_column}': {file_name}... ", end='')
            sort_csv_alphabetically(input_file_path, assignee_cleaned_output_file_path, right_most_assignee_column)
            print("Done.")
        else:
            print(f"No 'assignee' or 'assignee_cleaned' columns found in: {file_name}. Skipping this file for assignee_cleaned sort.")
        
        # Sorting by 'companyname'
        if right_most_companyname_column:
            companyname_output_file_path = os.path.join(companyname_output_directory, file_name)
            print(f"Sorting file by '{right_most_companyname_column}': {file_name}... ", end='')
            sort_csv_alphabetically(input_file_path, companyname_output_file_path, right_most_companyname_column)
            print("Done.")
        else:
            print(f"No 'companyname' column found in: {file_name}. Skipping this file for companyname sort.")

print("All files have been processed.")




