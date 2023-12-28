import csv
import time
from fuzzywuzzy import fuzz, process
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor

def binary_search(data, key, value):
    low, high = 0, len(data) - 1
    while low <= high:
        mid = (low + high) // 2
        if data[mid][key].strip().lower() == value.strip().lower():
            return mid
        elif data[mid][key].strip().lower() < value.strip().lower():
            low = mid + 1
        else:
            high = mid - 1
    return None

def get_marshall_score(name, match, score):
    delta_length = abs(len(name) - len(match))
    return delta_length * score

def plot_matches(matches, total, title):
    """Plot the number of matches made and matches left."""
    plt.bar(['Matches Made', 'Matches Left'], [matches, total - matches])
    plt.xlabel('Category')
    plt.ylabel('Number')
    plt.title(title)
    plt.show()

def fuzzy_match(row, data_to_match, column_name, thread_index, total_threads):
    try:
        if thread_index == (hash(row[column_name]) % total_threads):
            fuzzy_match_result, score = process.extractOne(row[column_name], [x[column_name] for x in data_to_match], scorer=fuzz.token_sort_ratio)
            marshall_score = get_marshall_score(row[column_name], fuzzy_match_result, score)
            return row, fuzzy_match_result, score, marshall_score
    except Exception as e:
        print(f"Error in fuzzy_match: {e}")
        print(f"Row Data: {row}")
    return None 

def match_and_combine_data(
        Uncleaned_Unique_assignees, Cleaned_Unique_assignees,
        UncleanedMatch, CleanedMatch,
        output_csv, unmatched_csv,
        uncleaned_assignee_col, cleaned_assignee_col,
        uncleaned_name_match_col, cleaned_name_match_col):
    
    start_time = time.time()

    # Reading and sorting data
    load_data_start = time.time()
    with open(Uncleaned_Unique_assignees, mode='r', newline='', encoding='utf-8') as file1, \
         open(Cleaned_Unique_assignees, mode='r', newline='', encoding='utf-8') as file2:
        reader1 = csv.DictReader(file1)
        reader2 = csv.DictReader(file2)

        data1_uncleaned = sorted([row for row in reader1], key=lambda x: x[uncleaned_assignee_col].strip().lower())
        data3_cleaned = sorted([row for row in reader2], key=lambda x: x[cleaned_assignee_col].strip().lower())

    with open(UncleanedMatch, mode='r', newline='', encoding='utf-8') as file3, \
         open(CleanedMatch, mode='r', newline='', encoding='utf-8') as file4:
        reader3 = csv.DictReader(file3)
        reader4 = csv.DictReader(file4)

        data2_uncleaned_match = sorted([row for row in reader3], key=lambda x: x[uncleaned_name_match_col].strip().lower())
        data4_cleaned_match = sorted([row for row in reader4], key=lambda x: x[cleaned_name_match_col].strip().lower())

    load_data_end = time.time()
    print(f"Time to load data: {load_data_end - load_data_start:.6f} seconds")

    # Preparing output files
    output_columns = reader1.fieldnames + reader3.fieldnames + ['Match_Type']
    unmatched_columns = reader1.fieldnames + ['Match_Type']
    
    with open(output_csv, mode='w', newline='', encoding='utf-8') as file_out, \
         open(unmatched_csv, mode='w', newline='', encoding='utf-8') as file_unmatched:
        writer = csv.DictWriter(file_out, fieldnames=output_columns)
        writer.writeheader()
        unmatched_writer = csv.DictWriter(file_unmatched, fieldnames=unmatched_columns)
        unmatched_writer.writeheader()

        total_rows = len(data1_uncleaned)
        matches_found = 0
        fuzzy_matches = 0
        non_matches = 0

        # Exact matching for uncleaned data
        exact_match_start = time.time()
        for i, row in enumerate(data1_uncleaned):
            if not row[uncleaned_assignee_col].strip():  # Skip empty or whitespace-only strings
                unmatched_row = {**row, 'Match_Type': 'No Match'}
                unmatched_writer.writerow(unmatched_row)
                non_matches += 1
                continue

            print(f"Processing exact match for row {i+1}/{total_rows}...")
            match_index = binary_search(data2_uncleaned_match, uncleaned_name_match_col, row[uncleaned_assignee_col])

            if match_index is not None:
                combined_row = {**row, **data2_uncleaned_match[match_index], 'Match_Type': 'Uncleaned Exact'}
                writer.writerow(combined_row)
                matches_found += 1
        exact_match_end = time.time()
        print(f"Time for exact matching (uncleaned): {exact_match_end - exact_match_start:.6f} seconds")

        # Plot after all exact matches for uncleaned data
        plot_matches(matches_found, total_rows, 'Exact Matching Progress - Uncleaned')

        # Exact matching for cleaned data
        exact_match_cleaned_start = time.time()
        # ... [Exact matching logic for cleaned data] ...
        exact_match_cleaned_end = time.time()
        print(f"Time for exact matching (cleaned): {exact_match_cleaned_end - exact_match_cleaned_start:.6f} seconds")

        # Plot after all exact matches for cleaned data
        plot_matches(matches_found, total_rows, 'Exact Matching Progress - Cleaned')

        # Multithreaded Fuzzy matching
        fuzzy_match_start = time.time()
        num_threads = 12  # Adjust based on your system
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = []
            for i, row in enumerate(data1_uncleaned):
                if not row[uncleaned_assignee_col].strip():  # Skip empty or whitespace-only strings for fuzzy matching
                    continue
                futures.append(executor.submit(fuzzy_match, row, data2_uncleaned_match, uncleaned_name_match_col, i, num_threads))

            for future in futures:
                result = future.result()
                if result:
                    row, fuzzy_match_result, score, marshall_score = result
                    if marshall_score > 100:
                        fuzzy_match_index = next((index for index, match_row in enumerate(data2_uncleaned_match) if match_row[uncleaned_name_match_col] == fuzzy_match_result), None)
                        combined_row = {**row, **data2_uncleaned_match[fuzzy_match_index], 'Match_Type': 'Fuzzy'}
                        writer.writerow(combined_row)
                        fuzzy_matches += 1
                    else:
                        unmatched_row = {**row, 'Match_Type': 'No Match'}
                        unmatched_writer.writerow(unmatched_row)
                        non_matches += 1
        fuzzy_match_end = time.time()
        print(f"Time for fuzzy matching: {fuzzy_match_end - fuzzy_match_start:.6f} seconds")

        # Final runtime and plot
        total_runtime = time.time() - start_time
        print(f"Total runtime: {total_runtime:.6f} seconds.")
        plot_matches(matches_found + fuzzy_matches, total_rows, 'Final Matching Results')
        print(f"Total matches{matches_found}")
        print(f"Fuzzy Matches: {fuzzy_matches}")

# Example usage
Uncleaned_Unique_assignees = 'C:/Users/marsh/Patent Tracking/Sorted/Sorted_unique_assignee/Unique_Assignee_sorted_by_Uncleaned.csv' #CSV with unique assignee sorted by uncleaned name
Cleaned_Unique_assignees = 'C:/Users/marsh/Patent Tracking/Sorted/Sorted_unique_assignee/Unique_Assignee_sorted_by_Cleaned.csv' #CSV with unique assignee sorted by cleaned name
UncleanedMatch = 'C:/Users/marsh/Patent Tracking/Sorted/Sorted_crsp_permo/CSRP_Permco_Sorted_by_UnCleaned.csv' #CSV sorted alphabetically by uncleaned name
CleanedMatch = 'C:/Users/marsh/Patent Tracking/Sorted/Sorted_crsp_permo/CSRP_Permco_Sorted_by_Cleaned.csv' #CSV sorted alphabetically by cleaned name
output_csv = 'TestMatcher_December.csv'
unmatched_csv = 'unmatched_data_December.csv'
uncleaned_assignee_col = 'assignee'  # Column with the uncleaned unique assignee in alphabetical order
cleaned_assignee_col = 'assignee_cleaned'     # Column with the Cleaned unique assignee in alphabetical order
uncleaned_name_match_col = 'company_name'  # Column with the uncleaned company name in alphabetical order
cleaned_name_match_col = 'Cleaned_company_name'      # Column with the Cleaned compnany name in alphabetical order

match_and_combine_data(
    Uncleaned_Unique_assignees, Cleaned_Unique_assignees,
    UncleanedMatch, CleanedMatch,
    output_csv, unmatched_csv,
    uncleaned_assignee_col, cleaned_assignee_col,
    uncleaned_name_match_col, cleaned_name_match_col
)
