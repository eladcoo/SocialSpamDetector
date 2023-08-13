import os
import re
from collections import defaultdict
import chardet

from BE.basicGraph import createConnections

list_of_spam_words = {}
def load_spam_words():
    with open('../resources/spam-words.txt','r') as file:
        for line in file:
            line = line.strip()
            list_of_spam_words[line] = True


# Get the list of all files and directories
def extract_from_dir(path):

    # Create base graph and graph to be sketched
    base_graph = defaultdict(list)
    num_of_invalid_files = 0
    if not list_of_spam_words:
        load_spam_words()

    # Add nodes and edges to base graph
    for path, subdirs, files in os.walk(path):
        for name in files:
            try:
                file_name = os.path.join(path, name)
                with open(file_name, 'rb') as file:
                    data = file.read()
                    encoding = chardet.detect(data)['encoding']

                with open(file_name, 'r', encoding=encoding) as file:
                    from_addresses = []
                    to_addresses = []
                    is_spam = False
                    for line in file:
                        line = line.rstrip()  # remove '\n' at end of line
                        # check if line contains any spam words
                        for word in line.split():
                            if word in list_of_spam_words:
                                is_spam = True

                        if "@" not in line:
                            continue
                        if "From:" in line and line.index("From:") == 0:
                            from_addresses = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", line)
                        if "To:" in line and line.index("To:") == 0:
                            to_addresses = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", line)

                    createConnections(base_graph, from_addresses, to_addresses, is_spam)
            except:
                print("invalid file:", name)
                num_of_invalid_files += 1
    print("num_of_invalid_files: ", num_of_invalid_files)
    return base_graph

