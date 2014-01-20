#-*- coding:utf8 -*-
#!/usr/bin/python3

import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('inputFile')

args = parser.parse_args()


def get_sentence(conll, actualWord, result=[]):
    result.append(actualWord)
    for word in conll:
        if word[6] == actualWord[0]:
            get_sentence(conll, word, result)
    return result

def get_dependent_words(conll, actualWord):
    result = [actualWord]
    for word in conll:
        if word[6] == actualWord[0]:
            result.append(word)
    return result

def get_dependent_words_without_subst(conll, actualWord):
    result = [actualWord]
    for word in conll:
        if word[6] == actualWord[0] and word[3] != 'subst':
            result.append(word)
    return result    

with open(args.inputFile, 'r') as inputFile:
    conll = []
    line = inputFile.readline()
    while line != '\n':
        conll.append(line[:-1].split('\t'))
        line = inputFile.readline()

    result = None
    for word in conll:
        if word[6] == '0':
            if word[3] == 'verb':
                result = get_sentence(conll, word)
            elif word[3] == 'subst':
                result = get_dependent_words_without_subst(conll, word)
            else:
                predicateCandidates = get_dependent_words(conll, word)
                for candidate in predicateCandidates:
                    if candidate[3] == 'verb':
                        result = get_sentence(conll, candidate)
                        break
                    elif candidate[3] == 'subst':
                        result = get_dependent_words(conll, candidate)

if result != None:
    header = ' '.join([x[1] for x in conll if x in result])

    braces = {
        '()': 0,
        '[]': 0,
        '{}': 0,
        '<>': 0
    }

    startRemove = endRemove = -1
    for i, c in enumerate(header):
        if c == '(':
            braces['()'] += 1
            if braces['()'] == 1:
                startRemove = i
        elif c == ')':
            braces['()'] -= 1
            if braces['()'] == 0:
                endRemove = i

    if startRemove >= 0 and endRemove >= 0:
        header = header[:startRemove] + header[(endRemove + 1):]

    header = re.sub(' *,', ',', header)
    header = re.sub(' *\.', '.', header)

    print(header)

    #TODO:
    # 1. Nawiasy - zrobiłem tylko '(' i ')'
    # 2. Gupie znaki
    # 3. Formatowanie - poprawiłem dla ',' i '.'
    # 4. Zbyt długie zdania
    # 5. Usuniecie drugiego rzeczownikia, kiedy "0" jest podmiotem - zrobione