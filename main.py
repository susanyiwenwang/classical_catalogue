from flask import Flask, render_template, request, redirect, url_for
from openopus import OpenOpus
import random as r


app = Flask(__name__)

open_opus = OpenOpus()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/popular')
def popular():
    return render_template('popular.html')


@app.route('/random', methods=["POST", "GET"])
def random():
    sample = {'title': 'None', 'composer': {'name': 'None', 'epoch': 'None'}}
    sample_img = ""
    return render_template('random.html', epochs=open_opus.epochs, work=sample, img=sample_img, is_result=False)


@app.route('/random/<epoch>', methods=["POST", "GET"])
def random_result(epoch):
    results = open_opus.epoch_random(epoch)
    piece = r.choice(results)
    portrait = open_opus.composer_by_name(piece['composer']['name'])
    return render_template('random.html', epochs=open_opus.epochs, work=piece, img=portrait['portrait'], is_result=True)


@app.route('/composer', methods=["POST", "GET"])
def by_composer():
    if request.method == "POST":
        name = request.form['composer']
        return redirect(url_for('composer_name', name=name))
    return render_template('by_composer.html', is_submit=False)


@app.route('/composer/<name>', methods=["POST", "GET"])
def composer_name(name):
    profile = open_opus.composer_by_name(name.capitalize())
    composer_id = profile['id']
    repertoire = None
    if composer_id:
        repertoire = open_opus.list_keyboard_works(composer_id)
    # exception handling, if composer not there, flash message
    return render_template('by_composer.html', is_submit=True, repertoire=repertoire, profile=profile)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)

