from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
import jieba
import json


app = Flask(__name__) # reference this file
# /// is relative path, //// is absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)   # initialize database


def generate_tag(sentence):
    with open('static/data/annotation_v2.json', 'r', encoding='gbk') as f:
        mapping = json.load(f)

    sentence = sentence.strip()
    words = jieba.lcut(sentence)
    result = []
    anno_list = []
    other = []
    for word in words:
        found = False
        for key, value in mapping.items():
            value_list = list(set(value.split()))
            if word in value_list:
                result.append('<' + key + '>')
                found = True
                anno_entry = '<'+key+'>' + " = " + "|".join(value_list) + ";"
                anno_list.append(anno_entry)
                break
        if not found:
            result.append('<' + word + '>')
    annotation = '\n'.join(anno_list)
    result = ' '.join(result)

    for word in words:
        found = False
        for key, value in mapping.items():
            value_list = list(set(value.split()))
            if word in value_list:
                other_anno = '<'+key+'>' + " = " + "|".join(value_list) + ";"
                other.append(other_anno)
    other_annotation = '\n'.join(other)

    tag_and_anno = sentence + '\n' + result + '\n' + annotation + '\n' + other_annotation
    return tag_and_anno

class Totag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200000), nullable=False)


    def __repr__(self):
        return '<Sentence %r>' % self.id
# create a index route so that when browse to the url won't just get 404
#  set up routes with the app route decorator

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        global sentence_content
        sentence_content = request.form['content']
        tagged_sentence = generate_tag(sentence_content)
        new_sentence = Totag(content=tagged_sentence)

        try:
            db.session.add(new_sentence)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue tagging your sentence'

    else:
        sentences = Totag.query.order_by(Totag.content).all()
        return render_template('index.html', sentences=sentences)



@app.route('/delete/<int:id>')
def delete(id):
    sentence_to_delete = Totag.query.get_or_404(id)

    try:
        db.session.delete(sentence_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deleting the sentence'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    sentence = Totag.query.get_or_404(id)

    if request.method == 'POST':
        sentence.content = request.form['content']

        try:
            # db.session.add(sentence_content)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your annotation'

    else:
        return render_template('update.html', sentence=sentence)



if __name__ == "__main__":
    app.run(debug=True)
