import requests
#from flask import Flask, render_template, jsonify
from flask import Flask, render_template, abort, request, jsonify
from flask import request, redirect, url_for
import codecs
import gensim
import external
from distutils.version import LooseVersion, StrictVersion
from packaging import version


external.app = Flask(__name__)
external.word2vec_model


@external.app.route('/search', methods=['GET', 'POST'])
def search():
    output = []
    if request.method == "POST":
        query = request.values['search'] or ''
        # query = unicode(query, "utf-8")
        # query = query.decode().encode("utf-8")
        query = str(query).lower()
        output = []
        try:
            sim_list = external.word2vec_model.most_similar(query, topn=50)
            #output = external.word2vec_model.most_similar('u' + '\"' + query + '\"', topn=5)
            for wordsimilar in sim_list:
                # output[wordsimilar[0]] = wordsimilar[1]
                output.append(wordsimilar[0] + ' - '+ str(wordsimilar[1]))
                # file = codecs.open("output.txt", "a", "utf-8")
                # file.write(wordsimilar[0] + "\t" + str(wordsimilar[1]) + "\n")
                # file.close()
        except:
            output = 'Not found' + query
    return render_template('search.html', pages = output)

@external.app.route('/viewsearch', methods = ['GET', 'POST'])
def viewanswer():
    


@external.app.route("/home", methods = ['GETS', 'POST'] )
def get_index():
    try:
        
    except Exception as e:
        print(e)
    return render_template('home.html')


if __name__ == "__main__":
    import os
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # download from https://drive.google.com/open?id=0B1GKSX6YCHXlakkzQ2plZVdUUE0
    model = 'data/vnex.model.bin'
    if os.path.isfile(model):
        from packaging import version
        if version.parse(gensim.__version__) >= version.parse("1.0.1"):
            from gensim.models import KeyedVectors
            external.word2vec_model = KeyedVectors.load_word2vec_format(model, binary=True)
        else:
            from gensim.models import Word2Vec
            external.word2vec_model = Word2Vec.load_word2vec_format(model, binary=True)
        external.app.run(port=8089)
    else:
        print("Error")