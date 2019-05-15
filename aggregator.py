# -----------------------------------------------------------------------------
# Name:        aggregator.py
# Purpose:     implement a simple general purpose aggregator
#
# Author:      Russell Yang
# -----------------------------------------------------------------------------
"""
Implement a simple general purpose aggregator

Usage: aggregator.py filename topic
filename: input file that contains a list of the online sources (urls).
topic:  topic to be researched and reported on
"""

import urllib.request # Import request module in urllib
import urllib.error   # Import error module in urllib
import re
import sys

def parameters_are_valid():
    """
    Checks if the number of parameters entered at the terminal is valid

    Returns:
    true if the number of parameters is 3, false otherwise (boolean)
    """
    # The only accepted number of command line arguments is 3: they are
    # aggregator.py, the filename, and the topic
    if len(sys.argv) != 3:
        # Issue error message if invalid number of command line arguments
        print("Error: invalid number of arguments")
        print("Usage: aggregator.py filename topic")
        return False
    else:
        return True

def write_to_out(result_list, topic):
    """
    Creates an output file for in the form of topicsummary with the results

    Parameters
    result_list (list): a list representing all the results
    topic: the topic given by the user
    """
    # Use formatted string to make the topic-specific output file name
    out_filename = f"{topic}summary.txt"

    # Using the with...as construct to open an output file in write mode
    with open(out_filename, "w", encoding="utf-8") as out_file:
        # For every list in the result_list
        for list in result_list:
            # The first element in the list is the url
            url = list[0]
            # The second element in the list is a list of references to
            # the topic
            mentions = list[1]
            # Write the url and a new line to the output file
            out_file.write(url + "\n")
            # Iterate over all the references
            for each_mention in mentions:
                # Write each reference and new line
                out_file.write(each_mention + "\n")
            # Write out 70 lines of dashes to separate the different urls
            out_file.write("---------------------------------------" +
                           "-------------------------------\n")

def get_comm_line_args():
    """
    Gets the command line arguments passed by the user

    Returns: a tuple with the filename and topic put by user into terminal
    """
    filename = sys.argv[1] # The 2nd command line argument is the filename
    topic = sys.argv[2]    # The 3rd command line argument is the topic
    return filename, topic # Return both as a tuple

def analyze_urls(filename, topic):
    """
    Analyzes the urls in the file with urls to find matches

    Parameters:
    filename (string): the name of the file which contains urls to search
    topic (string): the topic the user puts into the terminal (Ex: art)
    Returns:
    result_list (list): a list representing all the results of the search.
    see below for more information about how the result_list stores the results
    """
    # Initialize an empty list. Note that I store my urls and references
    # in a sort of strange way. Each element in result_list is a list of two
    # elements, the first element being the url, and the second element
    # being a list of all the references to the url
    result_list = []

    # Using the with...as construct to open the file in read mode
    with open(filename, "r", encoding="utf-8") as files:
            # Iterate over each line (each is a url)
            for line in files:
                # Use the try ... except construct
                try:
                    # Try to open each url
                    with urllib.request.urlopen(line) as url_file:
                        # Read the page
                        page = url_file.read()
                        # Decode the page
                        decoded_page = page.decode("UTF-8")
                        # Regex expression to find the places which open
                        # with a > then have some stuff, then the topic, then
                        # close with a <
                        pattern = fr">[^<]*\b{topic}\b.*?<"

                        # Use the findall method from re to find all of the
                        # occurrences of pattern in decoded_page as a list
                        # The flags are IGNORECASE and DOTALL
                        my_list = re.findall(pattern, decoded_page,
                                             re.IGNORECASE | re.DOTALL)

                        # If my_list is not empty
                        if my_list:
                            # Slice off the the closing and opening angle
                            # brackets using a list comprehension
                            new_list = [word[1:-1] for word in my_list]
                            # Append a new list of two elements to result_list,
                            # where the first element of the list is the url,
                            # and the second element of the list is the list of
                            # references
                            result_list.append([line, new_list])
                # One possible error is the urllib.error.URLError
                except urllib.error.URLError as url_err: # Catch the error
                    # Print a message, url, and the error
                    print("Error opening url:", line, url_err)
                # Another possible error is the UnicodeDecodeError
                except UnicodeDecodeError as dec_err: # Catch the error
                    # Print a message, and url
                    print("Error decoding url:", line)
                    # Print the error
                    print(dec_err)
                # Except all other errors
                except:
                    pass
    # Return the result_list
    return result_list

def main():
    # If there aren't the right number of parameters
    if not parameters_are_valid():
        # Exit the main method
        return
    # Get filename, topic as tuple
    filename, topic = get_comm_line_args()
    # Call analyze_urls to find references for each of the urls for topic
    result_list = analyze_urls(filename, topic)
    # Call write_to_out to write our findings to an output file
    write_to_out(result_list, topic)

if __name__ == '__main__':
    main()