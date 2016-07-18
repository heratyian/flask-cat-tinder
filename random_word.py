import random

words = [line.strip() for line in open('static/nounlist.txt')]
print(random.choice(words))
