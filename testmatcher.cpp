#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>
#include <chrono>
#include "csv.h"

// Levenshtein Distance Function
int levenshteinDistance(const std::string &s1, const std::string &s2) {
    const size_t len1 = s1.size(), len2 = s2.size();
    std::vector<unsigned int> col(len2 + 1), prevCol(len2 + 1);

    for (unsigned int i = 0; i < prevCol.size(); i++)
        prevCol[i] = i;
    for (unsigned int i = 0; i < len1; i++) {
        col[0] = i + 1;
        for (unsigned int j = 0; j < len2; j++) {
            col[j + 1] = std::min({prevCol[j + 1] + 1, col[j] + 1, prevCol[j] + (s1[i] == s2[j] ? 0 : 1)});
        }
        col.swap(prevCol);
    }
    return prevCol[len2];
}

// Function to calculate the token sort ratio between two strings.
int tokenSortRatio(const std::string &s1, const std::string &s2) {
    const int maxLen = std::max(s1.length(), s2.length());
    if (maxLen == 0) return 100; // Both strings are empty.

    // Levenshtein distance
    int levenshteinDist = levenshteinDistance(s1, s2);
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

// Function to perform a binary search on a sorted vector of vectors of strings.
int binary_search(const std::vector<std::vector<std::string>>& data, const std::string& key, int key_col) {
    int low = 0, high = data.size() - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (data[mid][key_col] == key) {
            return mid;
        } else if (data[mid][key_col] < key) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }
    return -1;
}

// Function to calculate a score based on string similarity and length difference.
int get_marshall_score(const std::string& name, const std::string& match, int score) {
    int delta_length = std::abs(static_cast<int>(name.length() - match.length()));
    int length_penalty = delta_length * 50 / std::max(name.length(), match.length());
    return std::max(score - length_penalty, 0);
}

// Main matching and combining data function
void match_and_combine_data(
    const std::string& uncleaned_csv_path, const std::string& cleaned_csv_path,
    const std::string& uncleaned_match_csv_path, const std::string& cleaned_match_csv_path,
    const std::string& output_csv_path, const std::string& unmatched_csv_path,
    const std::string& uncleaned_column, const std::string& cleaned_column
) {
    auto start_time = std::chrono::high_resolution_clock::now();

    io::CSVReader<2> uncleaned_reader(uncleaned_csv_path);
    uncleaned_reader.read_header(io::ignore_extra_column, uncleaned_column, cleaned_column);

    io::CSVReader<2> cleaned_reader(cleaned_csv_path);
    cleaned_reader.read_header(io::ignore_extra_column, uncleaned_column, cleaned_column);

    io::CSVReader<2> uncleaned_match_reader(uncleaned_match_csv_path);
    uncleaned_match_reader.read_header(io::ignore_extra_column, uncleaned_column, cleaned_column);

    io::CSVReader<2> cleaned_match_reader(cleaned_match_csv_path);
    cleaned_match_reader.read_header(io::ignore_extra_column, uncleaned_column, cleaned_column);

    std::vector<std::vector<std::string>> uncleaned_data, cleaned_data;
    std::vector<std::vector<std::string>> uncleaned_match_data, cleaned_match_data;
    std::vector<std::string> row;

    while (uncleaned_reader.read_row(row)) {
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

    output_file << "UncleanedName,CleanedName,MatchType\n";
    unmatched_file << "UncleanedName,CleanedName,MatchType\n";

    for (const auto& uncleaned_row : uncleaned_data) {
        int match_index = binary_search(uncleaned_match_data, uncleaned_row[0], 0);
        if (match_index != -1) {
            output_file << uncleaned_row[0] << "," << uncleaned_row[1] << ",Uncleaned Exact\n";
        } else {
            auto best_match = extractOne(uncleaned_row[0], uncleaned_match_data);
            int marshall_score = get_marshall_score(uncleaned_row[0], best_match.first, best_match.second);
            if (marshall_score > 80) {
                output_file << uncleaned_row[0] << "," << uncleaned_row[1] << ",Fuzzy\n";
            } else {
                unmatched_file << uncleaned_row[0] << "," << uncleaned_row[1] << ",No Match\n";
            }
        }
    }

    auto end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> runtime = end_time - start_time;
    std::cout << "Total runtime: " << runtime.count() << " seconds.\n";
}

int main() {
    const std::string Uncleaned_Unique_assignees = "Uncleaned_Unique_assignees.csv";
    const std::string Cleaned_Unique_assignees = "Cleaned_Unique_assignees.csv";
    const std::string UncleanedMatch = "UncleanedMatch.csv";
    const std::string CleanedMatch = "CleanedMatch.csv";
    const std::string output_csv = "TestMatcher_December.csv";
    const std::string unmatched_csv = "unmatched_data_December.csv";
    const std::string uncleaned_assignee_col = "UncleanedAssignee";
    const std::string cleaned_assignee_col = "CleanedAssignee";

    match_and_combine_data(
        Uncleaned_Unique_assignees, Cleaned_Unique_assignees,
        UncleanedMatch, CleanedMatch,
        output_csv, unmatched_csv,
        uncleaned_assignee_col, cleaned_assignee_col
    );

    return 0;
}
