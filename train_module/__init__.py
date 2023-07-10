import nltk
nltk.download('punkt')
#from nltk.stem.lancaster import LancasterStemmer
#stemmer = LancasterStemmer()
import numpy
from . import train
import random
import json
import pickle
from time import sleep
import os


link = "intents.json"

with open(link) as file:
    data = json.load(file)

try:
    with open(link, "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []
    for intent in data ["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [w.lower() for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [w for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)


        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)


    training = numpy.array(training)
    output = numpy.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)


model = train.neural_net(training,output)

try :
    if os.path.exists("checkpoint") and os.path.exists("model.tflearn.index"):
        model.load("model.tflearn")
    else:
        raise FileNotFoundError
except FileNotFoundError:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [word.lower() for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)

def process(message):
    inp = message
    results = model.predict([bag_of_words(inp, words)])[0]
    results_index = numpy.argmax(results)
    tag = labels[results_index]
    if results[results_index] > 0.6:
        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']
        sleep(2)
        Bot = random.choice(responses)
        return(Bot)
    else:
        sleep(1)
        return(random.choice(["ma fhamtch","t9der twade7 liya?","chno ka tgol?"]))

