import numpy as np
import string

ANSER = 'love'
CHARS = string.ascii_lowercase
# print(CHARS)
char_to_idx = {char: idx for idx, char in enumerate(CHARS)}
print(enumerate(CHARS))
# print(char_to_idx)
# print("==============================================================")
'''a = ['a', 'b', 'c', 'd', 'e']
x = np.array(a)
print(x)
np.random.shuffle(x)
print(x)
print(np.random.permutation(x))'''
'''
one_hot = np.zeros((4, 26))

for i, char in enumerate(ANSER.lower()):
    if char in char_to_idx:
        print(char_to_idx[char], end=" ")
        one_hot[i, char_to_idx[char]] = 1
print("\n", end=" ")
print(one_hot)
'''