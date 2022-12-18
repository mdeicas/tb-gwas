from sklearn import preprocessing
import xgboost as xgb
import argparse

def read_fasta(filename, majors, minors):
    """ Returns a list of sequences in one-hot encoding
        according to major and minors, and also returns their ordering

    Args: 
        filename (str): path to the file
        majors (list): list of major bases
        minors (list): list of minor bases

    Returns: 
        output (list): list of sequences in one-hot encoding
        order (dict): mapping of sequence names to their index in the list
        
    """
    with open(filename, "r") as f:
        output = []
        order = {}
        x = 0
        s = []
        count = 1
        for l in f.readlines():
            l_s = l.strip()
            if l_s[0] == ">":
                # skip the line that begins with ">"
                order[l_s[1:]] = x
                x += 1
                if s == []: continue
                output.append(s)
                s = []
                count = 1
            # keep appending to the current sequence when the line doesn't begin
            # with ">"
            else: 
                for b in l:
                    if count in majors and b == majors[count]:
                        s.append(0)
                        count += 1
                    elif count in minors and b == minors[count]:
                        s.append(1)
                        count += 1

        output.append(s)
        
    return output, order


def get_labels(filename, order):
    """ Returns the phenotype values in corresponding order

    Args: 
        filename (str): path to the file
        order (dict): mapping of sequence names to their index in the list

    Returns: 
        labels (list): list of ordered phenotype values
        
    """
    with open(filename, "r") as f:
        next(f)
        labels = [None] * len(order)
        for l in f.readlines():
            l_s = l.split()
            labels[order[l_s[0]]] = float(l_s[-1])
        return labels

# 
def get_major_minor(filename):
    """ Returns the major and minor bases at each position for a collection of sequences

    Args: 
        filename (str): path to the file

    Returns: 
        majors (list): list of majors at each position
        minors (list): list of minors at each position 
        
    """
    with open(filename, "r") as f:
        next(f)
        majors = {}
        minors = {}
        for l in f.readlines():
            l_s = l.split()
            majors[int(l_s[0])] = l_s[1]
            minors[int(l_s[0])] = l_s[2]
        return majors, minors
                

def main():
    # parse commandline arguments for data files
    parser = argparse.ArgumentParser()
    parser.add_argument('-fm', action="store", dest="fm", type=str) # motifs
    parser.add_argument('-fv', action="store", dest="fv", type=str) # phenotype values
    parser.add_argument('-fi', action="store", dest="fi", type=str) # major/minor base at each position

    args = parser.parse_args()

    # parse major/minor bases, 
    # then use them to process the sequences, 
    # then parse phenotype values, matching them with the sequences.
    majors, minors = get_major_minor(args.fi)
    sequences, order = read_fasta(args.fm, majors, minors)
    labels = get_labels(args.fv, order)

    # put X, y into DMatrix and store it as a binary file for later use
    dmatrix = xgb.DMatrix(sequences, labels, feature_types = "c", enable_categorical = True)
    dmatrix.save_binary("/workdir/dmatrix_bin")

if __name__ == '__main__':
    main()