import random
import requests
import json
from flask import Flask, render_template

def getDict(path):   
    pairs = []

    for w in open(path, encoding="ISO-8859-1").readlines():
        pairs.append(w.split("\\"))

    words_dict = dict(pairs)

    nouns = []
    verbs = []
    adjectives = []
    adverbs = []

    for w, t in words_dict.items():
        if "N" in t:
            nouns.append(w)
        if "V" in t:
            verbs.append(w)
        if "A" in t:
            adjectives.append(w)
        if "v" in t:
            adverbs.append(w)

    return {
        "nouns": nouns,
        "verbs": verbs,
        "adjectives": adjectives,
        "adverbs": adverbs
    }

def rw(d, ts):
    result = ""

    for t in ts:
      if t == "N":
          result += random.choice(d["nouns"]) + ","
      if t == "V":
          result += random.choice(d["verbs"]) + ","
      if t == "A":
          result += random.choice(d["adjectives"]) + ","
      if t == "v":
          result += random.choice(d["adverbs"]) + ","

    return result

def getImage(q):
    url = "https://api.cognitive.microsoft.com/bing/v7.0/images/search?mkt=en-us&q=" + q
    key = "" # from azure portal
    headers = { "ocp-apim-subscription-key" : key }
    return requests.get(url, headers=headers).json()["value"][0]["thumbnailUrl"]

d = getDict("mobypos.txt")
colors = ["#adccff", "#b7fff9", "#c6b5ff", "#ffccfb", "#e8ffcc", "#ffe4cc"]

app = Flask(__name__)

@app.route('/')
def main():
    words = rw(d, "NNN").split(",")
    imgs = [getImage(words[0]), getImage(words[1]), getImage(words[2])]

    return render_template("index.html", randomColor=random.choice(colors), words=words, img1=imgs[0], img2=imgs[1], img3=imgs[2])

@app.route('/<word1>/<word2>/<word3>')
def words(word1, word2, word3):
    imgs = [getImage(word1), getImage(word2), getImage(word3)]
    return render_template("index.html", randomColor=random.choice(colors), words=[word1, word2, word3], img1=imgs[0], img2=imgs[1], img3=imgs[2])


@app.route('/example/<num>')
def example(num):
    return render_template("examples/example{num}.html".format(num=num))
