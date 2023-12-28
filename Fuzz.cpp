#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

// Function to compute the Levenshtein distance between two strings
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

int main() {
    // Define two strings to compare
    std::string string1 = "Apple Inc";
    std::string string2 = "Apple Computer Inc";

    // Calculate Levenshtein distance
    int distance = levenshteinDistance(string1, string2);

    // Calculate and print the confidence score
    int maxLen = std::max(string1.length(), string2.length());
    int confidence = maxLen > 0 ? (1.0 - static_cast<double>(distance) / maxLen) * 100 : 100;

    std::cout << "Comparing: '" << string1 << "' with '" << string2 << "'\n";
    std::cout << "Confidence: " << confidence << "/100" << std::endl;

    return 0;
}