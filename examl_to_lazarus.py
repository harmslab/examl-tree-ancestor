#!/usr/bin/env python3
__description__ = \
"""
Hacked together program that rips the exact model used by examl out of examl
output and spits out in paml format.  alpha shape parameter is sent to standard
out.
"""
__author__ = "Michael J. Harms"
__date__ = "2015-07-09"
__usage__ = "examl_to_lazarus.py examl_model_output [final_paml_file]"

import sys

AA_LIST = ["A","R","N","D","C","Q","E","G","H","I",
           "L","K","M","F","P","S","T","W","Y","V"]

def floatCheck(value,line):
    """
    Verify a string value can be read as a float.
    """

    try:
        float(value)
    except ValueError:
        err = "mangled file.  line:\n\n{:s}\n\n".format(line)
        raise ValueError(err)

def readExamlModel(model_file):
    """
    Read and parse the model file that gets dumped out of examl.
    """   
 
    f = open(model_file,'r')
    lines = f.readlines()
    f.close()

    alpha = None
  
    pi = {} 
    transitions = {}
    for i in range(len(AA_LIST)):
        pi[AA_LIST[i]] = None
        for j in range(len(AA_LIST)):
            transitions["{:s}{:s}".format(AA_LIST[i],AA_LIST[j])] = None

    for l in lines:

        # skip blank lines
        if l.strip() == "":
            continue

        col = l.split()

        if col[0] == "alpha:":
            floatCheck(col[1],l)
            alpha = col[1].strip()

        if col[0] == "rate":
            tran_f = col[1] + col[3][0]
            tran_r = col[3][0] + col[1]
            
            # resplit on ":" because N (for some reason) has space after it
            value = l.split(":")[1].strip()
            floatCheck(value,l)
            transitions[tran_f] = value
            transitions[tran_r] = value

        if col[0] == "freq":
            key = col[1].split("(")[1].split(")")[0].strip()

            # resplit on ":" because N (for some reason) has space after it
            value = l.split(":")[1].strip()
            floatCheck(value,l)
            pi[key] = value

    return alpha, pi, transitions

def writeLazarusInput(alpha,pi,transitions,output_file="examl-matrix-used.dat"):
    """
    Create paml output given an alpha shape parameter, pi and a transition
    matrix.
    """
  
    paml_out = [] 
    for i in range(1,len(AA_LIST)):
        for j in range(i):
            key = "{:s}{:s}".format(AA_LIST[i],AA_LIST[j])
            paml_out.append(transitions[key])
            paml_out.append(" ")
        paml_out.append("\n")
   
    paml_out.append("\n")

    for aa in AA_LIST:
        paml_out.append(pi[aa])
        paml_out.append(" ")

    paml_out.append("\n")

    f = open(output_file,"w")
    f.write("".join(paml_out))
    f.close()

    print(alpha)


def main(argv=None):
    """
    Parse command line and run.
    """

    if argv == None:
        argv = sys.argv[1:]

    try:
        examl_model_file = argv[0]
    except IndexError:
        err = "incorrect arguments. usage:\n\n{:s}\n\n".format(__usage__)
        raise IndexError(err)

    try:
        paml_output_file = argv[1]
    except IndexError:
        paml_output_file = "examl-matrix-used.dat"

    alpha, pi, transitions = readExamlModel(examl_model_file)
    writeLazarusInput(alpha,pi,transitions,output_file=paml_output_file)

if __name__ == "__main__":
    main()
