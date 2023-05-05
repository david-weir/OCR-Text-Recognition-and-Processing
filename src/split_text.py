import os

def split_txtfile(txtfile, directory):
    path = os.path.dirname(txtfile)
    new_path = os.path.join(path, directory)
    with open(txtfile, 'r') as f:
        words = f.read()
        words_lst = words.split()
        files = []
        chunk = 100
        for c, i in enumerate(range(0, len(words_lst), chunk)):
                with open("{}/part_{}.txt".format(new_path, c+1), "w") as out:
                    out.write(" ".join(words_lst[i:i+chunk]))
                    files.append("{}/part_{}.txt".format(new_path, c+1))

        return files