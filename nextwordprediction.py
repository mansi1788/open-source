import tensorflow as tf
from tensorflow.python.keras.models import Sequential
from keras.layers import * from keras.models import *
from keras.layers import Dense,LSTM,Embedding from
keras.preprocessing.text import Tokenizer from
keras_preprocessing.sequence import pad_sequences
import numpy as np import regex as re def
file_to_sentence_list(file_path): with
open(file_path, 'r') as file:
text = file.read()
sentences = [sentence.strip() for sentence in re.split(
r'(?<=[.!?])\s+', text) if
sentence.strip()] return sentences file_path =
'pizza.txt'
text_data = file_to_sentence_list(file_path)
tokenizer = Tokenizer()
tokenizer.fit_on_texts(text_data)
total_words = len(tokenizer.word_index) + 1
input_sequences = [] for line in text_data:
token_list = tokenizer.texts_to_sequences([line])[0]
for i in range(1, len(token_list)):
n_gram_sequence = token_list[:i+1]
input_sequences.append(n_gram_sequence)
max_sequence_len = max([len(seq) for seq in input_sequences]) input_sequences
= np.array(pad_sequences(
input_sequences, maxlen=max_sequence_len, padding='pre'))
X, y = input_sequences[:, :-1], input_sequences[:, -1] y =
tf.keras.utils.to_categorical(y, num_classes=total_words)
# Define the model model
= Sequential()
model.add(Embedding(total_words, 10,
input_length=max_sequence_len-1))
model.add(LSTM(128))
model.add(Dense(total_words, activation='softmax'))
model.compile(loss='categorical_crossentropy',
optimizer='adam',
metrics=['accuracy']) model.fit(X, y, epochs=500, verbose=1)
seed_text = "Pizza have different "
next_words = 5 for _ in
range(next_words):
token_list = tokenizer.texts_to_sequences([seed_text])[0]
token_list = pad_sequences(
[token_list], maxlen=max_sequence_len-1, padding='pre')
predicted_probs = model.predict(token_list)
predicted_word = tokenizer.index_word[np.argmax(predicted_probs)]
seed_text += " " + predicted_word
print("Next predicted words:", seed_text)
