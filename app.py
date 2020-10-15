import random
import requests
import json
from flask import Flask



def getWords(path):   
    words = open(path, "rb").readlines()
    pairs = []
    for w in words:
        pairs.append(w.split("\\"))
    words_dict = dict(pairs)

    nouns = []
    verbs = []
    adjectives = []

    for w, t in words_dict.iteritems():
        if "N" in t:
            nouns.append(w)
        if "V" in t:
            verbs.append(w)
        if "A" in t:
            adjectives.append(w)

    return {
        "nouns": nouns,
        "verbs": verbs,
        "adjectives": adjectives
    }

def rw(d, t):
    if t == "N":
        return random.choice(d["nouns"])
    if t == "V":
        return random.choice(d["verbs"])
    if t == "A":
        return random.choice(d["adjectives"])


def rws(d, ts):
    result = ""
    for t in ts:
        result += rw(d, t) + " "
    return result[:-1]

def getImage(q):
    url = "https://api.cognitive.microsoft.com/bing/v7.0/images/search?mkt=en-us&q=" + q
    headers = { "ocp-apim-subscription-key" : "" }
    return requests.get(url, headers=headers).json()["value"][0]["thumbnailUrl"]

d = getWords("mobypos.txt")

app = Flask(__name__)

@app.route('/')
def hello_world():
    rws2 = [rw(d, "N"), rw(d, "N"), rw(d, "N")]
    imgs = [ getImage(rws2[0]), getImage(rws2[1]), getImage(rws2[2]) ]
    colors = ["#adccff", "#b7fff9", "#c6b5ff", "#ffccfb", "#e8ffcc", "#ffe4cc"]

    html = """
        <html>
            <head>
                <style>
                    body {{
                        background-color: {randomColor}
                    }}
                    .images {{
                        padding: 1em;
                    }}
                    img {{
                        max-height: 22vw;
                        max-width: 29%;
                        padding: 1em;
                    }}
                </style>
            </head>
            <body>
                {rws2[0]} {rws2[1]} {rws2[2]} 
                <div class="images">
                    <img src="{img1}"> 
                    <img src="{img2}">
                    <img src="{img3}">
                </div>
            </body>
        </html>
    """.format(randomColor=random.choice(colors), rws2=rws2, img1=imgs[0], img2=imgs[1], img3=imgs[2])

    return html

