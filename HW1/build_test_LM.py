#!/usr/bin/python
from __future__ import division
import math
import re
import nltk
import sys
import getopt


# returns array of four characters of input string
def get_four_char_array(string):
    array = []
    for i in range(0, len(string) - 3):
        array.append((string[i], string[i + 1], string[i + 2], string[i + 3]))
    return array


def build_LM(in_file):
    """
    build language models for each label
    each line in in_file contains a label and an URL separated by a tab(\t)
    """
    print 'building language models...'
    # This is an empty method
    # Pls implement your code in below
    LMs = {'malaysian': {}, 'indonesian': {}, 'tamil': {}}
    malay_LM = LMs['malaysian']
    indon_LM = LMs['indonesian']
    tamil_LM = LMs['tamil']

    FD = open(in_file, 'r')

    lines = FD.read()
    lines_array = lines.replace('\r', ' ').split('\n')
    lines_array.pop(len(lines_array) - 1)

    for line in lines_array:
        line_array = line.split(' ', 1)
        lang = line_array[0]
        text = line_array[1]
        current_LM = LMs[lang]
        four_char_array = get_four_char_array(text)

        for four_char in four_char_array:
            if four_char not in current_LM:
                # performs add one smoothing
                malay_LM[four_char] = 1
                indon_LM[four_char] = 1
                tamil_LM[four_char] = 1
            current_LM[four_char] += 1

    # calculates ratio of set frequency over total frequency
    # for all sets in each of the three LMs
    for LM in LMs.values():
        count = 0
        for freq_value in LM.values():
            count += freq_value
        for four_char_key in LM.keys():
            LM[four_char_key] /= count
    return LMs

    FD.close()


def test_LM(in_file, out_file, LM):
    """
    test the language models on new URLs
    each line of in_file contains an URL
    you should print the most Countable label for each URL into out_file
    """
    print "testing language models..."
    # This is an empty method
    # Pls implement your code in below
    malay_LM = LM['malaysian']
    indon_LM = LM['indonesian']
    tamil_LM = LM['tamil']

    FD_in = open(in_file, 'r')
    FD_out = open(out_file, 'w')

    lines = FD_in.read()
    lines_array = lines.replace('\r', ' ').split('\n')
    lines_array.pop(len(lines_array) - 1)

    for line in lines_array:
        malay_count = 1
        indon_count = 1
        tamil_count = 1

        total_count = 0
        miss_count = 0

        four_char_array = get_four_char_array(line)

        for four_char in four_char_array:
            # key in malayLM = key in all LMs due to add one smoothing
            if four_char in malay_LM:
                malay_count += math.log10(malay_LM[four_char])
                indon_count += math.log10(indon_LM[four_char])
                tamil_count += math.log10(tamil_LM[four_char])
            else:
                miss_count += 1
            total_count += 1

        if (miss_count / total_count > 0.7):
            FD_out.write("other " + line + "\n")
        elif malay_count > indon_count and malay_count > tamil_count:
            FD_out.write("malaysian " + line + "\n")
        elif indon_count > malay_count and indon_count > tamil_count:
            FD_out.write("indonesian " + line + "\n")
        else:
            FD_out.write("tamil " + line + "\n")

    FD_in.close()
    FD_out.close()


def usage():
    print "usage: " + sys.argv[0] + " -b input-file-for-building-LM -t input-file-for-testing-LM -o output-file"

input_file_b = input_file_t = output_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'b:t:o:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-b':
        input_file_b = a
    elif o == '-t':
        input_file_t = a
    elif o == '-o':
        output_file = a
    else:
        assert False, "unhandled option"
if input_file_b == None or input_file_t == None or output_file == None:
    usage()
    sys.exit(2)

LM = build_LM(input_file_b)
test_LM(input_file_t, output_file, LM)
