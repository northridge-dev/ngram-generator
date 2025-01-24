import os

with open("train/great_gatsby.txt", "r") as file:
    text = file.read()


def train_trigrams(text):
    global trigram_list

    wordlist = text.replace('\n', ' ').split(' ')
    trigram_list = []
    for i in range(len(wordlist) - 2):
        one_trigram = [wordlist[i],wordlist[i+1],wordlist[i+2]]
        trigram_list.append(one_trigram)

    return trigram_list

train_trigrams(text)

print('\n\n\n\nwe doin trigrams now boyyy\n')
word1 = input("Enter first word   ->")
word2 = input("Enter second word   ->")

final_list = []

for i in range(len(trigram_list)):
    if trigram_list[i][0] == word1:
        if trigram_list[i][1] == word2:
            final_list.append(trigram_list[i][2])

os.system('clear')

print(final_list)
        