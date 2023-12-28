#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <boost/algorithm/string.hpp>
#include <chrono>
#include "csv.h"

// Include the fuzzy matching functions that were previously defined...
int levenshteinDistance(const std::string &s1, const std::string &s2) {
    const std::size_t len1 = s1.size(), len2 = s2.size();
    std::vector<unsigned int> col(len2 + 1), prevCol(len2 + 1);

    for (unsigned int i = 0; i < prevCol.size(); i++)
        prevCol[i] = i;
    for (unsigned int i = 0; i < len1; i++) {
        col[0] = i + 1;
        for (unsigned int j = 0; j < len2; j++) {
            col[j + 1] = std::min({ 
                prevCol[j + 1] + 1, 
                col[j] + 1, 
                prevCol[j] + (s1[i] == s2[j] ? 0 : 1)
            });
        }
        col.swap(prevCol);
    }
    return prevCol[len2];
}


// Function to calculate the token sort ratio between two strings.
int tokenSortRatio(const std::string &s1, const std::string &s2) {
    std::vector<std::string> tokens1, tokens2;
    boost::split(tokens1, s1, boost::is_any_of(" \t"), boost::token_compress_on);
    boost::split(tokens2, s2, boost::is_any_of(" \t"), boost::token_compress_on);

    std::sort(tokens1.begin(), tokens1.end());
    std::sort(tokens2.begin(), tokens2.end());

    std::string sortedStr1 = boost::join(tokens1, " ");
    std::string sortedStr2 = boost::join(tokens2, " ");

    boost::algorithm::to_lower(sortedStr1);
    boost::algorithm::to_lower(sortedStr2);

    const int maxLen = std::max(sortedStr1.length(), sortedStr2.length());
    if (maxLen == 0) return 100; // Both strings are empty.

    // Levenshtein distance
    int levenshteinDist = levenshteinDistance(sortedStr1, sortedStr2);
    // Ratio as a percentage
    return (1 - (double)levenshteinDist / maxLen) * 100;
}

// Function to find the best match from a list of strings using the token sort ratio.
std::pair<std::string, int> extractOne(const std::string &query, const std::vector<std::string> &choices) {
    int highestScore = 0;
    std::string bestMatch;

    for (const auto &choice : choices) {
        int score = tokenSortRatio(query, choice);
        if (score > highestScore) {
            highestScore = score;
            bestMatch = choice;
        }
    }

    return {bestMatch, highestScore};
}

// Function to perform a binary search on a sorted vector of vectors of strings. Returns the index or -1 if not found
int binary_search(const std::vector<std::vector<std::string>>& data, const std::string& key, int key_col) {
    int low = 0, high = data.size() - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        std::string mid_val = boost::trim_copy(data[mid][key_col]);
        boost::to_lower(mid_val);
        if (mid_val == key) {
            return mid;
        } else if (mid_val < key) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }
    return -1;
}

// Function to calculate a score based on string similarity and length difference. Similar to "get_marshall_score" in Python
int get_marshall_score(const std::string& name, const std::string& match, int score) {
    int delta_length = std::abs(static_cast<int>(name.length() - match.length()));
    int length_penalty = delta_length * 50 / std::max(name.length(), match.length());
    return std::max(score - length_penalty, 0);
}

// Note: The plot_matches function is omitted as C++ doesn't have a direct, simple plotting library like matplotlib in Python.
// Instead, data can be outputted to a file and plotted using an external tool if needed.

// Main matching and combining data function
void match_and_combine_data(
    const std::string& uncleaned_csv_path, const std::string& cleaned_csv_path,
    const std::string& uncleaned_match_csv_path, const std::string& cleaned_match_csv_path,
    const std::string& output_csv_path, const std::string& unmatched_csv_path,
    const std::string& uncleaned_column, const std::string& cleaned_column
) {
    // Start processing time
    auto start_time = std::chrono::high_resolution_clock::now();

    // Read and sort the data (using Fast C++ CSV Parser)
    io::CSVReader<2> uncleaned_reader(uncleaned_csv_path); // Adjust number of columns based on your CSV
    uncleaned_reader.read_header(io::ignore_extra_column, uncleaned_column, cleaned_column);

    io::CSVReader<2> cleaned_reader(cleaned_csv_path); // Adjust number of columns based on your CSV
    cleaned_reader.read_header(io::ignore_extra_column, uncleaned_column, cleaned_column);

    io::CSVReader<2> uncleaned_match_reader(uncleaned_match_csv_path); // Adjust number of columns based on your CSV
    uncleaned_match_reader.read_header(io::ignore_extra_column, uncleaned_column, cleaned_column);

    io::CSVReader<2> cleaned_match_reader(cleaned_match_csv_path); // Adjust number of columns based on your CSV
    cleaned_match_reader.read_header(io::ignore_extra_column, uncleaned_column, cleaned_column);

    std::vector<std::vector<std::string>> uncleaned_data, cleaned_data;
    std::vector<std::vector<std::string>> uncleaned_match_data, cleaned_match_data;
    std::vector<std::string> row; // Temporary vector to hold the read row.

    while (uncleaned_reader.read_row(row)) {
        // Assuming first column is uncleaned and second is cleaned
        uncleaned_data.push_back({row[0], row[1]});
    }
    while (cleaned_reader.read_row(row)) {
        cleaned_data.push_back({row[0], row[1]});
    }
    while (uncleaned_match_reader.read_row(row)) {
        uncleaned_match_data.push_back({row[0], row[1]});
    }
    while (cleaned_match_reader.read_row(row)) {
        cleaned_match_data.push_back({row[0], row[1]});
    }

    std::ofstream output_file(output_csv_path);
    std::ofstream unmatched_file(unmatched_csv_path);

    // Output CSV headers
    output_file << "UncleanedName,CleanedName,MatchType\n";
    unmatched_file << "UncleanedName,CleanedName,MatchType\n";

    // Exact matching for uncleaned data
    for (const auto& uncleaned_row : uncleaned_data) {
        std::string uncleaned_name = boost::trim_copy(uncleaned_row[0]);
        boost::to_lower(uncleaned_name);

        int match_index = binary_search(uncleaned_match_data, uncleaned_name, 0);
        if (match_index != -1) {
            output_file << uncleaned_row[0] << "," << uncleaned_row[1] << ",Uncleaned Exact\n";
        } else {
            // If no exact match found, perform fuzzy matching using tokenSortRatio and extractOne
            int highest_score = 0;
            std::pair<std::string, int> best_match;
            for (const auto& match_row : uncleaned_match_data) {
                int score = tokenSortRatio(uncleaned_name, boost::trim_copy(match_row[0]));
                if (score > highest_score) {
                    highest_score = score;
                    best_match = {match_row[0], score};
                }
            }
            int marshall_score = get_marshall_score(uncleaned_name, best_match.first, highest_score);
            if (marshall_score > 80) { // Assuming threshold is 80, adjust as needed
                output_file << uncleaned_row[0] << "," << uncleaned_row[1] << ",Fuzzy\n";
            } else {
                unmatched_file << uncleaned_row[0] << "," << uncleaned_row[1] << ",No Match\n";
            }
        }
    }

    // Additional logic for cleaned data can be added similarly

    // End processing time and display total runtime
    auto end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> runtime = end_time - start_time;
    std::cout << "Total runtime: " << runtime.count() << " seconds.\n";
}

int main() {
    // Example usage
    const std::string Uncleaned_Unique_assignees = "C:/Users/marsh/Patent Tracking/Sorted/Sorted_unique_assignee/Unique_Assignee_sorted_by_Uncleaned.csv";
    const std::string Cleaned_Unique_assignees = "C:/Users/marsh/Patent Tracking/Sorted/Sorted_unique_assignee/Unique_Assignee_sorted_by_Cleaned.csv";
    const std::string UncleanedMatch = "C:/Users/marsh/Patent Tracking/Sorted/Sorted_crsp_permo/CSRP_Permco_Sorted_by_UnCleaned.csv";
    const std::string CleanedMatch = "C:/Users/marsh/Patent Tracking/Sorted/Sorted_crsp_permo/CSRP_Permco_Sorted_by_Cleaned.csv";
    const std::string output_csv = "TestMatcher_December.csv";
    const std::string unmatched_csv = "unmatched_data_December.csv";
    const std::string uncleaned_assignee_col = "UncleanedAssignee";
    const std::string cleaned_assignee_col = "CleanedAssignee";
    const std::string uncleaned_name_match_col = "company_name";
    const std::string cleaned_name_to_match_col = "Cleaned_Companmy_Name";

    match_and_combine_data(
        Uncleaned_Unique_assignees, Cleaned_Unique_assignees,
        UncleanedMatch, CleanedMatch,
        output_csv, unmatched_csv,
        uncleaned_assignee_col, cleaned_assignee_col
    );

    return 0;
}