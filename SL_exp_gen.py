# -*- coding: utf-8 -*-
"""
Version 1.0

Python script to generate SL word experiments by feeding list of words

Created on Tue Jan 29 18:16:53 2019

@author: JoseAAManzano
"""
import os
import sys
import numpy as np
from random import shuffle

def print_sentence_mbrola(sentence, wordlist=None, pitch = 83.62, addPause=False, pause = 25, vowelDur = 150, consDur = 100):
    """
    Produces list that can be directly copied to Mbroli to save audio string
    Arguments:
        sentence -- long string with words for the experiment
        wordlist -- list of words to count inside the string
        pitch -- add pitch modulation based on Mbroli, default constant 83.62
        addPause -- add pause between words?
        pause -- time for pauses between words (in ms)
        vowelDur -- duration of vowels in stream (in ms)
        consDur -- duration of consonants in stream (in ms)
    """
    def count_words(sentence, wordlist):
        """
        Private method to count words in the sentence and print the count
        """
        for word in wordlist:
            print(word,sentence.count(word))

    ret = ""
    for line in sentence:
        for ch in line:
            if ch in 'aiueo':
                ret += ch.lower() + " {} 0 {}\n".format(vowelDur, pitch)
            else:
                ret += ch.lower() + " {} 0 {}\n".format(consDur, pitch)
        if addPause:
            ret += "_ {}\n".format(pause)
    print('Counting words...')
    if(len(wordlist) > 1):
        count_words("".join(line for line in sentence), wordlist)

    return ret

def create_exact_ml(word_list, reps, out_f):
    '''No consecutive repetitions are allowed'''
    full_list = word_list*reps
    full_len = len(full_list)
    stream = []
    cond = False
    shuffle(full_list)
    while len(stream) != full_len:
        if len(stream) == 0:
            stream.append(full_list.pop(0))
        else:
            while stream[-1] == full_list[0]:
                shuffle(full_list)
                if len(full_list) == 1:
                    cond = True
                    break
            stream.append(full_list.pop(0))
    if cond:
        stream.insert(0,stream.pop())
    return ''.join(stream)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python sl_exp_gen.py <list of words> <reps per word> <output_file>')
        print("Example: python sl_exp_gen.py words.txt 80 exp1.txt")
        sys.exit(1)
    word_file = sys.argv[1]
    word_list = []
    with open(word_file,'r', encoding='utf-8') as f:
        for l in f:
            word_list.append(l.strip())
    reps = int(sys.argv[2])
    out_f = sys.argv[3]
    print('Producing stream...')
    stream = create_exact_ml(word_list,reps,out_f)
    with open(out_f,'w', encoding='utf-8') as f:
        f.write(stream)
    mbroli = print_sentence_mbrola(stream,word_list, vowelDur = 100)
    print('Saving in MBROLA format...')
    with open("MBROLA_{}".format(out_f), 'w') as f2:
        for l in mbroli:
            f2.write(l)
    print('Done!')
