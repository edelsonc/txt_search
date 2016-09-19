"""
This script executes a simple text search engine. It takes a search phrase as
and which files in the current working directory to search as input, and ouputs
the number of time that phrase occures in each document.

author: edelsonc
"""
import os
import string


def get_txt_files(directory):
    """This function takes a directory as input and return all of the txt files
    in it.

    Arguments
    ---------
    directory -- a direcoty path (absolute)
    """

    files = os.listdir(directory)
    txt_files = []

    for file in files:
        if '.txt' in file:
            txt_files.append(file)
        else:
            pass
    
    return txt_files

# words was chosen to avoid conflict in namespace with string module
def remove_punc(words):
    """Function that removes punctuation from a string

    Arguments
    ---------
    words -- string to have punctuation removes
    """

    trans = {ord(c): None for c in string.punctuation}
    no_punc = words.translate(trans)

    return no_punc


def remove_stop_words(words, stop_words):
    """Function that removes stop workds from a string

    Arguments
    ---------
    words -- string to have stop words removed
    stop_words -- list of common stop words
    """

    splt_str = words.split()
    result_list = [word for word in splt_str if word.lower() not in stop_words]
    no_stop = ' '.join(result_list)

    return no_stop


def check_numbers(phrase):
    """Functions checks if the given phrase has numbers in it

    Arguments
    ---------
    phrase -- string
    """
    return any(char.isdigit() for char in phrase)


def check_phrase(phrase, file, stop_words):
    """This function checks if the given phrase is in the file

    Arguments
    ---------
    phrase -- search phrase
    file -- .txt file to be searched
    """
    
    # remove stop words and punctuation from phrase and make lower case
    query = remove_stop_words(remove_punc(phrase), stop_words).lower()

    # open and read txt file to be searched
    with open(file, 'r') as f:
        text = f.readlines()

        # loops through each line and check if the phrase is in it
        number_phrase = 0
        for line in text:
            cln_line = remove_stop_words(remove_punc(line), stop_words).lower()

            if query in cln_line:
                number_phrase += 1
            else:
                pass

    return number_phrase

def print_files(files):
    """Function prints a list of files

    Arguments
    --------
    files -- list of files
    """
    for i, file in enumerate(files):
        print("%r) %s" % (i+1, file))


def main():
    """
    Main logic of the script, runs the actual user interface.
    """
    # read all of the stop words from local csv
    stop_words = open('stop_words.csv', 'r').readline().split(',')

    # get user search phrase and make sure it doesn't contain numbers
    while True:
        phrase = input("\nEnter the phrase to search: ")

        if check_numbers(phrase):
            print("Invalid entry; try again")
        else:
            break

    # get the local txt_files in wd
    dir = os.getcwd()
    txt_files = get_txt_files(dir)
    
    # allow user to select to search all or specify files
    print("\nThere are %r .txt files in this directory" % (len(txt_files)))
    search_all = input("Type Y to search all the txt files in the wd: ")

    if search_all.lower() == 'y':  # searching all
        for file in txt_files:
            num = check_phrase(phrase, file, stop_words)
            print("File %s has %r occurences of '%s'" % (file, num, phrase))
    else:  # only check some of the files
        # list all files in wd
        print('\nHere are all the .txt files: ')
        print_files(txt_files)
        
        # ask how many to search
        while True:
            search = int(input("\nHow many files do you want to search in? "))
            if search <= len(txt_files):
                break
            else:
                print("That is too many files.")
        # get the names of the files to search
        search_files = []
        for i in range(search):
            while True:
                srch_file = input('Enter the file name with extension: ')
                if srch_file in txt_files:
                    search_files.append(srch_file)
                    break
                else:  # making sure the file exists
                    print("We can only search in .txt files which exist")
        # check each of the given files
        for file in search_files:
            num = check_phrase(phrase, file, stop_words)
            print("File %s has %r occurences of '%s'" % (file, num, phrase))

    # allow user to search again
    again = input('\nWould you like to search again? Say Y to continue: ')
    if again.lower() == 'y':
        return main()
    else:
        return None


if __name__ == '__main__':
    print("\nHello and welcome to txt search!")
    main()
