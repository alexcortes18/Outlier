from gensim import models
import pandas as pd
import numpy as np
import nlpaug.augmenter.word as naw
import nltk

from tensorflow.keras.preprocessing.text import Tokenizer
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# Download w2v first: https://code.google.com/archive/p/word2vec/

w2v_model = models.KeyedVectors.load_word2vec_format('public_data/GoogleNews-vectors-negative300.bin.gz', binary=True)


def loadData(path):
    ngram = []
    _class = []
    with open(path) as f:
        for line in f.readlines():
            line = line.strip("\n").split("\t")
            ngram.append(line[0])
            _class.append(int(line[1]))
    return pd.DataFrame({"phrase":ngram,"class":_class})
train = loadData("public_data/train.tsv")
test = loadData("public_data/test.tsv")

positive = train[train['class']==1].reset_index(drop=True)
negative = train[train['class']==0].reset_index(drop=True)
ratio = len(negative)/len(positive)
print("Ratio:", ratio)

aug = naw.SynonymAug(aug_src='wordnet', model_path=None, name='Synonym_Aug', aug_min=1, aug_max=10, aug_p=0.3, lang='eng',
                     stopwords=None, tokenizer=None, reverse_tokenizer=None, stopwords_regex=None, force_reload=False,
                     verbose=0)

new_phrases = []
number_of_replications = 30

for i, phrase_to_translate in enumerate(list(positive.phrase)):
    for i in range(number_of_replications):
        aug_phrase = aug.augment(phrase_to_translate)
        number_words = len(nltk.word_tokenize(aug_phrase[0]))
        if aug_phrase not in new_phrases and aug_phrase != phrase_to_translate and number_words <= 5:
            new_phrases.append(aug_phrase)
            
new_phrases = list(np.concatenate(new_phrases))
new_phrases_df = pd.DataFrame()
new_phrases_df['phrase'] = new_phrases[:]
new_phrases_df['class'] = 1

all_positives = pd.concat([positive, new_phrases_df], ignore_index=True, sort=False)
n = len(all_positives)
negative_fraction = negative.sample(n= n, random_state = 42, ignore_index=True)
print("Number of positive data for 'positive' class: ", len(all_positives))
print("Number of positive data for 'negative' class: ", len(negative_fraction))

training_dataset = pd.concat([all_positives, negative_fraction], ignore_index=True, sort=False)
training_dataset = training_dataset.sample(frac = 1, random_state = 42, ignore_index=True)
training_dataset.to_csv('training_dataset',index=False)

training_dataset_test = pd.read_csv('training_dataset')

tok = Tokenizer()
tok.fit_on_texts(pd.concat([training_dataset,test],ignore_index=True)['phrase'])
vocab_size = len(tok.word_index) + 1
train_encoded_phrase = tok.texts_to_sequences(training_dataset['phrase'])
test_encoded_phrase = tok.texts_to_sequences(test['phrase'])

max_word_len = 5 
X_train = pad_sequences(train_encoded_phrase, maxlen=max_word_len, padding = 'post')
X_test = pad_sequences(test_encoded_phrase, maxlen=max_word_len, padding = 'post')

y_train = to_categorical(training_dataset['class'])
y_test = to_categorical(test['class'])

X_train,X_val,y_train,y_val = train_test_split(X_train,y_train,test_size=0.20,random_state=42)

embedding_matrix = np.zeros((vocab_size, 300))
for key, i in tok.word_index.items():
    try:
        vector = w2v_model[key]
    except:
        vector = None
    if vector is not None:
        embedding_matrix[i] = w2v_model[key]
        
# Classification:
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense , Flatten , Embedding, LSTM, LSTM, ReLU, Dropout
from tensorflow.keras.initializers import Constant
from tensorflow.keras.layers import ReLU
from tensorflow.keras.layers import Dropout
from tensorflow.keras.optimizers import RMSprop
import tensorflow as tf

model=Sequential()
model.add(Embedding(input_dim=(vocab_size),output_dim=300,input_length=5,embeddings_initializer=Constant(embedding_matrix)))
#model.add(LSTM(64,return_sequences=True))
model.add(LSTM(64,return_sequences=False))
model.add(Flatten())
model.add(Dense(2,activation='sigmoid'))

model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
my_callbacks = [
    tf.keras.callbacks.EarlyStopping(patience=2),
    tf.keras.callbacks.ModelCheckpoint(filepath='model.{epoch:02d}-{val_loss:.2f}.h5'),
    tf.keras.callbacks.TensorBoard(log_dir='./logs'),
]
model.fit(X_train,y_train,validation_data=(X_val,y_val),epochs = 12, batch_size = 256, callbacks = my_callbacks)

accuracy = model.evaluate(X_test,y_test)
print("Final accuracy score: ", accuracy[1])


