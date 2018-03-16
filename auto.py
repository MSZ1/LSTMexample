#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
import numpy as np
import random
import sys

file=codecs.open('juman.txt','r','utf-8')
text = codecs.open('juman.txt','r','utf-8').read().lower()
print('corpus length:', len(text))

LIST=[]
for line in file:
    List=line.split()
    LIST.append(List)
file.close()
l=LIST[0]

chars = sorted(set(l))
print('total chars:', len(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

#sentencesには文ごとに区切ったものが入る
sen=[]
sentences = []
next_chars = []
for i in l:
    if i=="。":
        sen.append("。")
        sentences.append(sen)
        sen=[]
    else:
        sen.append(i)
maxlen=len(max(sentences,key=len))
print('nb sequences:', len(sentences))

print('Vectorization...')
X = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        X[i, t, char_indices[char]] = 1
        number=char_indices[char]
        y[i,number]=1

# build the model: a single LSTM
print('LSTMの作成')
model = Sequential()
model.add(LSTM(128, input_shape=(maxlen, len(chars))))
model.add(Dense(len(chars)))
model.add(Activation('softmax'))

optimizer = RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)

def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

# train the model, output generated text after each iteration
for iteration in range(1, 60):
    print()
    print('-' * 50)
    print('Iteration', iteration)
    model.fit(X, y, batch_size=128,epochs=1)
    start_index = random.randint(0, len(text) - maxlen - 1)

    for diversity in [0.2, 0.5, 1.0, 1.2]:
        print()
        print('----- diversity:', diversity)

        generated = ''
        sentence = l[start_index: start_index + 20]
        for i in sentence:
            generated=generated+str(i)
        print('----- Generating with seed: "' + str(sentence) + '"')
        sys.stdout.write(generated)

        for i in range(20):
            x = np.zeros((1, maxlen, len(chars)))
            for t, char in enumerate(sentence):
                x[0, t, char_indices[char]] = 1.

            preds = model.predict(x, verbose=0)[0]
            next_index = sample(preds, diversity)
            next_char = indices_char[next_index]

            generated += next_char
            sentence.append(next_char)

            sys.stdout.write(next_char)
            sys.stdout.flush()
        print()
