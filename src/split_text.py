import os

# function to split text file into smaller text files
def split_txtfile(txtfile, directory):
    path = os.path.dirname(txtfile)
    new_path = os.path.join(path, directory)
    with open(txtfile, 'r') as f:
        words = f.read()
        words_lst = words.split() # split the txt file into words
        files = [] # array of file paths
        chunk = 100 # split into smaller 100 word txt files
        for c, i in enumerate(range(0, len(words_lst), chunk)):
                with open("{}/part_{}.txt".format(new_path, c+1), "w") as out:
                    out.write(" ".join(words_lst[i:i+chunk])) # write 100 words into new file
                    files.append("{}/part_{}.txt".format(new_path, c+1))

        return files