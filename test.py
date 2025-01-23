from main_old import textbreaker

training_texts = ['./train/great_gatsby.txt']
with open(training_texts[0], 'r') as file:
    text = file.read()


input = '''He didn't say any more, but we've always been unusually communicative in a reserved way, and I understood that he meant a great deal more than that. In consequence, I'm inclined to reserve all judgements, a habit that has opened up many curious natures to me and also made me the victim of not a few veteran bores.'''
input = "The Mr. dog barked at the squirrel, that ran up the tree. Why did the dog bark? I TOLD YOU! Sorry."

output =  textbreaker(text)
print(output[:3])