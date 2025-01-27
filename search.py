import os
import argparse
import difflib #To caclulate the word distance (Levenshtein distance).

from typing import List, Tuple

def highlight(text: str, intervals: List[Tuple[int, int]]) -> str:
    intervals.sort() # Sorts by first index
    result: List[str] = []
    index = 0
    for interval in intervals:
        while index < interval[0]:
            result.append(text[index])
            index += 1
        
        while index <= interval[1]:
            result.append(f'\033[91m{text[index]}\033[0m')
            index += 1
    
    return "".join(result) + text[index:]
    

def search_files(directory, search_term: str, search_names_only=False, exact=False, recursive=True, match_rate=0) -> None:
    results: List[Tuple[str, int, list[str]]] = []
    
    if recursive:
        iterable = os.walk(directory)  # Use os.walk for recursive search
    else:
        iterable = [(directory, [], os.listdir(directory))] #only search top level


    for root, _, files in iterable:
        for full_path in files:
            full_path = os.path.normpath(os.path.join(root, full_path)) 
            found_lines = [] #store results for this file.
            total_count = 0

            #Search File Name
            if result := dst_search_text(full_path, search_term, match_rate):
              found_lines.append(f"Found in filename ({len(result):<3}): {highlight(full_path, result)}") #filename always shows even when only one instance of the work is found in content.
              total_count += len(result)

            # Search File Content
            if not search_names_only:
              try:
                  with open(full_path, 'r', encoding='utf-8') as f:
                      for line_number, line in enumerate(f, 1):
                          if result := dst_search_text(line, search_term, match_rate):
                              found_lines.append(f"Found in content ({len(result):<3}): Line [{line_number:<3}]: ${highlight(line, result)}$")
                              total_count += len(result)
              except (IOError, UnicodeDecodeError):
                  print(f"Error reading or decoding file: {full_path}. Skipping.")


            if found_lines:  # Add file results only if matches found
              results.append((full_path, total_count, found_lines)) #(name, count, [list of strings of where the word was found]) #Number of result in content, not including the "found in filename"


    #Sort Results: by relevance, then by filepath:
    #(name, count, [list of strings of where the word was found])
    results.sort(key=lambda x: (
        -(1 if x[2] and x[2][0].startswith("Found in filename") else 0),  # filename matches get higher priority with a negative number, 
        -x[1], # Then sort by the negative count (so more matches will go to top), # Number of matches in content (negative for descending order)
        x[2][0].lower() # Then sort alphabetically by file path
    ))
    
    if len(results) == 0:
        print(f"No results found in directory: {directory}")

    for full_path, count, found_lines in results:
        # Print formatted output:
        print(f"{full_path} ({count if count!=0 else 'no'} matches in content):")

        # Print content matches with indentation if there are any:
        if count>0:
            for result_string in found_lines:
                print(f"\t{result_string}")
            print() #newline to seperate paragraphs

        else:
            print()
                  
def dst_search_text(text: str, search_term: str, match_rate: int) -> List[Tuple[int, int]]:
    """
    Helper function for search logic in text
    Reutns the intervals where the match was found so it can be highlighted
    """
    search_term = search_term.lower()
    
    if match_rate == 0:
        matches = []
        i = 0
        while i <= len(text) - len(search_term):
            match = str.find(text[i:], search_term)  # Match at each position
            if match != -1:
                matches.append((i + match, i + match + len(search_term) - 1)) # Store start and end of match
                i += match + 1
            else:
                break
        return matches
    
    # else
    matches = []
    window_gen = ([text[i:i + len(search_term)] for i in range(len(text) - len(search_term) + 1)])
    for interval, window in window_gen:
        if difflib.SequenceMatcher(None, window, search_term).ratio() >= (1 - match_rate * 0.01):
            matches.append(interval)
    
    return matches
  


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for a word or phrase in files.")
    parser.add_argument("directory", help="Directory to search.")
    parser.add_argument("search_term", help="Word or phrase to search for.")
    parser.add_argument("-n", "--names_only", action="store_true", help="Search file names only.")
    parser.add_argument("-r", "--recursive", action="store_false", help="Disable recursive search (default: recursive).")
    parser.add_argument("-m", "--match_rate", type=int, default=0, help="Set matching tolerance %")

    args = parser.parse_args()

    print("Parsed Arguments:")
    for arg_name, arg_value in vars(args).items():
        print(f"  {arg_name}: <{arg_value}>")
    print("\n") #newline for better readability.
  
    search_files(args.directory, args.search_term, args.names_only, args.exact, args.recursive, args.match_rate)
