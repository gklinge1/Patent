#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <chrono>
#include "csv.h"

// Trims whitespace from the start and end of a string
std::string trim(const std::string& str) {
    auto start = std::find_if_not(str.begin(), str.end(), ::isspace);
    auto end = std::find_if_not(str.rbegin(), str.rend(), ::isspace).base();
    return (start < end) ? std::string(start, end) : std::string();
}

// Converts a string to lowercase
std::string to_lower(const std::string& str) {
    std::string lower_str;
    std::transform(str.begin(), str.end(), std::back_inserter(lower_str),
                   [](unsigned char c) { return std::tolower(c, std::locale()); });
    return lower_str;
}

// Function to perform a binary search on a sorted vector of vectors of strings. 
// Returns the index or -1 if not found
// Function to perform a binary search on a sorted vector of strings.
int binary_search(const std::vector<std::string>& data, const std::string& key) {
    int low = 0, high = data.size() - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (data[mid] == key) {
            return mid;
        } else if (data[mid] < key) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }
    return -1;
}

// Main matching and combining data function
void match_and_combine_data(
    const std::string& uncleaned_csv_path,
    const std::string& cleaned_csv_path,
    const std::string& uncleaned_match_csv_path,
    const std::string& cleaned_match_csv_path,
    const std::string& output_matched_csv_path,
    const std::string& output_unmatched_csv_path,
    const std::string& uncleaned_name_match_col,
    const std::string& cleaned_name_match_col
) {
    auto start_time = std::chrono::high_resolution_clock::now();

    // Initialize CSV readers for both datasets
    io::CSVReader<2> uncleaned_reader(uncleaned_csv_path);
    io::CSVReader<2> cleaned_reader(cleaned_csv_path);
    uncleaned_reader.read_header(io::ignore_extra_column, uncleaned_name_match_col, cleaned_name_match_col);
    cleaned_reader.read_header(io::ignore_extra_column, uncleaned_name_match_col, cleaned_name_match_col);

    std::vector<std::string> uncleaned_data, cleaned_data;
    std::string uncleaned, cleaned;

    // Read data from both datasets
    while (uncleaned_reader.read_row(uncleaned, cleaned)) {
        uncleaned_data.push_back(uncleaned);
    }
    while (cleaned_reader.read_row(uncleaned, cleaned)) {
        cleaned_data.push_back(cleaned);
    }

    std::ofstream output_matched_file(output_matched_csv_path);
    std::ofstream output_unmatched_file(output_unmatched_csv_path);

    // Write the headers for the matched and unmatched files
    output_matched_file << uncleaned_name_match_col << "," << cleaned_name_match_col << "\n";
    output_unmatched_file << uncleaned_name_match_col << "," << cleaned_name_match_col << "\n";

    // Exact match of "company name" to "assignee"
    for (const auto& name : uncleaned_data) {
        int match_index = binary_search(uncleaned_data, name);
        if (match_index != -1) {
            output_matched_file << name << "\n";
            std::cout << "Exact 'uncleaned' match found: " << name << std::endl;
        } else {
            output_unmatched_file << name << "\n";
        }
    }

    // Exact match of "cleaned company name" to "cleaned assignee"
    for (const auto& name : cleaned_data) {
        int match_index = binary_search(cleaned_data, name);
        if (match_index != -1) {
            output_matched_file << name << "\n";
            std::cout << "Exact 'cleaned' match found: " << name << std::endl;
        } else {
            output_unmatched_file << name << "\n";
        }
    }

    auto end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end_time - start_time;
    std::cout << "Total runtime: " << elapsed.count() << " seconds." << std::endl;
}

int main() {
    // File paths and column names as parameters
    std::string uncleaned_csv_path = "C:/Users/marsh/Patent Tracking/Sorted/Sorted_unique_assignee/Unique_Assignee_sorted_by_Uncleaned.csv";
    std::string cleaned_csv_path = "C:/Users/marsh/Patent Tracking/Sorted/Sorted_unique_assignee/Unique_Assignee_sorted_by_Cleaned.csv";
    std::string uncleaned_match_csv_path = "C:/Users/marsh/Patent Tracking/Sorted/Sorted_crsp_permo/CSRP_Permco_Sorted_by_UnCleaned.csv";
    std::string cleaned_match_csv_path = "C:/Users/marsh/Patent Tracking/Sorted/Sorted_crsp_permo/CSRP_Permco_Sorted_by_Cleaned.csv";
    std::string output_matched_csv_path = "C:/Users/marsh/Patent Tracking/TestMatcher_December.csv";
    std::string output_unmatched_csv_path = "C:/Users/marsh/Patent Tracking/unmatched_data_December.csv";
    std::string uncleaned_column = "assignee";  // Column with the uncleaned unique assignee in alphabetical order
    std::string cleaned_column = "assignee_cleaned"; // Column with the Cleaned unique assignee in alphabetical order
    std::string uncleaned_name_match_col = "company_name"; // Column with the uncleaned company name in alphabetical order
    std::string cleaned_name_match_col = "Cleaned_company_name"; // Column with the Cleaned company name in alphabetical order

    // Begin matching process
    match_and_combine_data(
        uncleaned_csv_path,
        cleaned_csv_path,
        uncleaned_match_csv_path,
        cleaned_match_csv_path,
        output_matched_csv_path,
        output_unmatched_csv_path,
        uncleaned_name_match_col,
        cleaned_name_match_col
    );

    return 0;
}