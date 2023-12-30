import sys
import csv
import unicodedata
import re

#remove the words at the beginning of the string 
def standardize_abbreviations(name):
    abbreviations = {
        r"(^| )inc( |$)": " ",
        r"(^| )corporation( |$)": " ",
        r"(^| )ltd( |$)": " ",
        r"(^| )co( |$)": " ",
        r"(^| )company( |$)": " ",
        r"(^| )llc( |$)": " ",
        r"(^| )the( |$)": " ",
        r"(^| )of( |$)": " ",
        r"(^| )kaisha( |$)": " ",
        r"(^| )kabushiki( |$)": " ",
        r"(^| )limited( |$)": " ",
        r"(^| )gmbh( |$)": " ",
        r"(^| )and( |$)": " ",
        r"(^| )ag( |$)": " ",
        r"(^| )incorporated( |$)": " ",
        r"(^| )corp( |$)": " ",
        r"(^| )aktiengesellschaft( |$)": " ",
        r"(^| )lp( |$)": " ",
        r"(^| )sa( |$)": " ",
        r"(^| )as( |$)": " ",
        r"(^| )de( |$)": " ",
        r"(^| )bv( |$)": " ",
        r"(^| )kg( |$)": " ",
        r"(^| )ab( |$)": " ",
        r"(^| )spa( |$)": " ",
        r"(^| )nv( |$)": " ",
        r"(^| )holdings( |$)": " ",
        r"(^| )licensing( |$)": " ",
        r"(^| )i( |$)": " ",
        r"(^| )ip( |$)": " ",
        r"(^| )holding( |$)": " ",
        r"(^| )pty( |$)": " ",
        r"(^| )e( |$)": " ",
        r"(^| )telefonaktiebolaget( |$)": " ",
        r"(^| )du( |$)": " ",
        r"(^| )a/s( |$)": " ",
        r"(^| )koninklijke( |$)": " ",
        r"(^| )oy( |$)": " ",
        r"(^| )et( |$)": " ",
        r"(^| )srl( |$)": " ",
        r"(^| )for( |$)": " ",
        r"(^| )(publ)( |$)": " ",
        r"(^| )a( |$)": " ",
        r"(^| )pte( |$)": " ",
        r"(^| )plc( |$)": " ",
        r"(^| )lm( |$)": " ",
        r"(^| )se( |$)": " ",
        r"(^| )societe( |$)": " ",
        r"(^| )la( |$)": " ",
        r"(^| )l( |$)": " ",
        r"(^| )m( |$)": " ",
        r"(^| )kk( |$)": " ",
        r"(^| )des( |$)": " ",
        r"(^| )r( |$)": " ",
        r"(^| )und( |$)": " ",
        r"(^| )c( |$)": " ",
        r"(^| )gesellschaft( |$)": " ",
        r"(^| )mbh( |$)": " ",
        r"(^| )j( |$)": " ",
        r"(^| )ii( |$)": " ",
        r"(^| )w( |$)": " ",
        r"(^| )der( |$)": " ",
        r"(^| )s( |$)": " ",
        r"(^| )d( |$)": " ",
        r"(^| )b( |$)": " ",
        r"(^| )sarl( |$)": " ",
        r"(^| )anonyme( |$)": " ",
        r"(^| )maschinenfabrik( |$)": " ",
        r"(^| )aktiebolag( |$)": " ",
        r"(^| )g( |$)": " ",
        r"(^| )-( |$)": " ",
        r"(^| )sl( |$)": " ",
        r"(^| )k( |$)": " ",
        r"(^| )kgaa( |$)": " ",
        r"(^| )kommanditgesellschaft( |$)": " ",
        r"(^| )p( |$)": " ",
        r"(^| )t( |$)": " ",
        r"(^| )aktien( |$)": " ",
        r"(^| )ohg( |$)": " ",
        r"(^| )v( |$)": " ",
        r"(^| )llp( |$)": " ",
        r"(^| )oyj( |$)": " ",
        r"(^| )x( |$)": " ",
        r"(^| )societe( |$)": " ",
        r"(^| )bvba( |$)": " ",
        r"(^| )n( |$)": " ",
        r"(^| )anonyme( |$)": " ",
        r"(^| )o( |$)": " ",
        r"(^| )ltda( |$)": " ",
        r"(^| )y( |$)": " ",
        r"(^| )kabushikikaisha( |$)": " ",
        r"(^| )incorporation( |$)": " ",
        r"(^| )publ( |$)": " "
    }
    
    for abbr, full in abbreviations.items():
        name = re.sub(abbr, full, name)

    return name.strip()

def remove_company_suffix(name):
    # Define suffix patterns and their conditions
    suffixes = {
        r"(^| )mfg( |$)": " manufacturing ",
        r"(^| )tech( |$)": " technology ",
        r"(^| )lab(s)?( |$)": " laboratories ",
        r"(^| )intl( |$)": " international ",
        r"(^| )inst( |$)": " institute ",
        r"(^| )assn( |$)": " association ",
    }

    for suffix, replacement in suffixes.items():
        name = re.sub(suffix, replacement, name)
        
    return name.strip()

def remove_international_terms(name):
    terms = [
        " a g",
        " l p",
        " s a",
        " a s",
        " a b",
        " b v",
        " k g",
        " n v",
        " s p a",
        " s a r l",
        " s r l",
        " k k",
        " s l",
        " c a"
    ]
    for term in terms:
        if name.endswith(term):
            name = name[:-len(term)]
    return name.strip()

def Light_abbreviations(name):
    abbreviations = {
        r"(^| )inc( |$)": " ",
        r"(^| )corporation( |$)": " ",
        r"(^| )ltd( |$)": " ",
        r"(^| )co( |$)": " ",
        r"(^| )company( |$)": " ",
        r"(^| )llc( |$)": " ",
        r"(^| )the( |$)": " ",
        r"(^| )of( |$)": " ",
        r"(^| )kaisha( |$)": " ",
        r"(^| )kabushiki( |$)": " ",
        r"(^| )limited( |$)": " ",
        r"(^| )gmbh( |$)": " ",
        r"(^| )and( |$)": " ",
        r"(^| )ag( |$)": " ",
        r"(^| )incorporated( |$)": " ",
        r"(^| )corp( |$)": " ",
        r"(^| )aktiengesellschaft( |$)": " ",
        r"(^| )lp( |$)": " ",
        r"(^| )sa( |$)": " ",
        r"(^| )as( |$)": " ",
        r"(^| )de( |$)": " ",
        r"(^| )bv( |$)": " ",
        r"(^| )kg( |$)": " ",
        r"(^| )ab( |$)": " ",
        r"(^| )spa( |$)": " ",
        r"(^| )nv( |$)": " ",
        r"(^| )holdings( |$)": " ",
        r"(^| )licensing( |$)": " ",
        r"(^| )ip( |$)": " ",
        r"(^| )holding( |$)": " ",
        r"(^| )pty( |$)": " ",
        r"(^| )telefonaktiebolaget( |$)": " ",
        r"(^| )du( |$)": " ",
        r"(^| )koninklijke( |$)": " ",
        r"(^| )oy( |$)": " ",
        r"(^| )et( |$)": " ",
        r"(^| )srl( |$)": " ",
        r"(^| )for( |$)": " ",
        r"(^| )(publ)( |$)": " ",
        r"(^| )pte( |$)": " ",
        r"(^| )plc( |$)": " ",
        r"(^| )lm( |$)": " ",
        r"(^| )se( |$)": " ",
        r"(^| )societe( |$)": " ",
        r"(^| )la( |$)": " ",
        r"(^| )kk( |$)": " ",
        r"(^| )des( |$)": " ",
        r"(^| )und( |$)": " ",
        r"(^| )gesellschaft( |$)": " ",
        r"(^| )mbh( |$)": " ",
        r"(^| )der( |$)": " ",
        r"(^| )sarl( |$)": " ",
        r"(^| )anonyme( |$)": " ",
        r"(^| )maschinenfabrik( |$)": " ",
        r"(^| )aktiebolag( |$)": " ",
        r"(^| )sl( |$)": " ",
        r"(^| )kgaa( |$)": " ",
        r"(^| )kommanditgesellschaft( |$)": " ",
        r"(^| )aktien( |$)": " ",
        r"(^| )ohg( |$)": " ",
        r"(^| )llp( |$)": " ",
        r"(^| )oyj( |$)": " ",
        r"(^| )societe( |$)": " ",
        r"(^| )bvba( |$)": " ",
        r"(^| )anonyme( |$)": " ",
        r"(^| )ltda( |$)": " ",
        r"(^| )kabushikikaisha( |$)": " ",
        r"(^| )incorporation( |$)": " ",
        r"(^| )publ( |$)": " "
    }
    
    for abbr, full in abbreviations.items():
        name = re.sub(abbr, full, name)

    return name.strip()

def corp_phrase(name):
    pattern = r'(a corp|corp of|corporation of|a delaware).*'
    return re.sub(pattern, '', name, flags=re.IGNORECASE)

# Main function to clean and standardize company names

def clean_name(name):
    # Convert name to lowercase
    name = name.lower()\
    # Normalize non-ASCII characters to ASCII\
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode()\
    #removes the corp of and other phrases
    name = corp_phrase(name)\
    # Remove extra spaces from name\
    name = ' '.join(name.split())\
    # Retain only alphanumeric characters and certain punctuation\
    name = ''.join(e for e in name if e.isalnum() or e in '&-() ')\
    # Replace dashes with spaces\
    name = name.replace("-", " ")\
    # Replace & with spaces\
    name = name.replace(" & ", " ")\
    # Strip\
    name = name.strip()\
    # Standardize abbreviations\
    name = Light_abbreviations(name)\
    # Remove company suffixes\
    name = remove_company_suffix(name)
    #Removing non alphanumeric
    name = remove_non_alphanumeric(name)
    #Remove the international terms
    name = remove_international_terms(name)
    #Removing spaces
    name = remove_spaces(name)
    # Remove single letters that stand alone
    #name = re.sub(r'\b[a-z]\b', '', name)
    return name

def remove_non_alphanumeric(name):
    return re.sub(r'[^a-zA-Z0-9 ]', ' ', name)

def remove_spaces(name):
    return name.replace(" ", "")

"""
Column Letter to Index Reference:
A: 0
B: 1
C: 2
D: 3
E: 4
F: 5
G: 6
H: 7
I: 8
J: 9
K: 10
L: 11
M: 12
"""
# Read arguments from the command line
input_file = sys.argv[1]
output_file = sys.argv[2]
COLUMN_TO_READ = int(sys.argv[3])
COLUMN_TO_COPY_TO = int(sys.argv[4])

unique_names = []
full_data = []

with open(input_file, 'r', encoding='utf-8') as infile:
    csv_reader = csv.reader(infile)
    total_rows = sum(1 for row in csv.reader(open(input_file, 'r', encoding='utf-8')))
    infile.seek(0)
    for i, row in enumerate(csv_reader, 1):
        if len(row) >= COLUMN_TO_READ:
            original_name = row[COLUMN_TO_READ]
            cleaned_name = clean_name(original_name)
            unique_names.append(cleaned_name)
            print(f"Row {i} ({(i / total_rows) * 100:.2f}% complete): {original_name}")
            row.insert(COLUMN_TO_COPY_TO, cleaned_name)
            full_data.append(row)

with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    csv_writer = csv.writer(outfile)
    for row in full_data:
        csv_writer.writerow(row)

print(f"Data with cleaned names as a new column has been saved to {output_file}")