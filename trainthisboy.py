import os
import random

with open("train/great_gatsby.txt", "r") as file:
    text = file.read()

print('\n\nwe doin n-grams now boyyy\n')
grammy = input("Enter a word/phrase\n-> ")
grammy_list = grammy.split(' ')
n = len(grammy_list)

def train_ngrams(text):
    global ngram_list
    global n
    global wordlist

    wordlist = text.replace('\n', ' ').split(' ')
    ngram_list = []
    for i in range(len(wordlist) - n):
        one_ngram = []
        for g in range(n):
            one_ngram.append(wordlist[i+g])
        ngram_list.append(one_ngram)

    return ngram_list

train_ngrams(text)
sentence_list = []

for l in range(len(grammy_list)):
    sentence_list.append(grammy_list[l])

for p in range(100):
    final_list = []
    for f in range(len(ngram_list)):
        similarity = 0
        for u in range(n):
            if grammy_list[u] == ngram_list[f][u]:
                similarity += 1
        if similarity == n:
            final_list.append(ngram_list[f+1][n-1])
    sentence_list.append(random.choice(final_list))
    grammy_list = [sentence_list[p+1],sentence_list[p+2]]


sentence = ' '.join(sentence_list)
print(sentence)

def get_frequency():
    frequency_dict = {}
    for word in final_list:
        if word in frequency_dict:
            frequency_dict[word] += 1
        else:
            frequency_dict[word] = 1
    return frequency_dict

freq_list = get_frequency()
