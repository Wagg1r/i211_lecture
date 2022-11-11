from flask import Flask, render_template, request, redirect, url_for
import csv
from os.path import exists
import pymysql
app = Flask(__name__)

app.config.from_pyfile(app.root_path + '/config_defaults.py')

if exists(app.root_path + '/config.py'):
    app.config.from_pyfile(app.root_path + '/config.py')
import database

DINO_PATH = app.root_path + '/dinosaurs.csv'
DINO_KEYS = ['slug', 'name', 'description', 'image', 'image-credit', 'source-url', 'source-credit']

def get_dinos():
    try:
        with open(DINO_PATH, 'r') as csvfile:
            data = csv.DictReader(csvfile)
            dinosaurs = {}
            for dino in data:
                dinosaurs[dino['slug']] = dino
    except Exception as e:
        print(e)
    return dinosaurs

def insert_fact(dino_id, name, fact):
    sql = "INSERT INTO fact (dino_id, name, fact) VALUES (%s,%s,%s)"
    conn = database.get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (dino_id,name,fact))
        conn.commit()

def get_facts(dino_id):
    sql = "select * from fact where dino_id =%s"
    conn = database.get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql,(dino_id))
            return cursor.fetchall()
    

@app.route('/')
@app.route('/dino/')
@app.route('/dino/<dino>')
def index(dino_id=None):
    if dino_id:
        dinosaur = database.get_dino(dino_id)
        facts=database.get_facts(dino_id)
        return render_template('dino.html', dinosaur = dinosaur ,facts=facts)
    else:
        dinosaurs=database.get_dinos()
        return render_template('index.html', dinosaurs=dinosaurs)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/add_dino', methods=['GET', 'POST'])
def add_dino():
    if request.method == 'POST':
        slug = request.form['slug']
        name = request.form['name']
        description = request.form['description']
        image = request.form['image']
        image_credit = request.form['image-credit']
        source_url = request.form['source-url']
        source_credit = request.form['source-credit']
        # Run function to add data for new
        database.insert_dino(slug,name,description,image,image_credit,source_url,source_credit)

        return redirect(url_for('index'))
    else:
        return render_template('add-dino.html')
with open ('faq.csv', 'r') as file:
    questions = csv.reader(file)
    qna = []
    for row in questions:
        qna.append(row)

@app.route('/dino-quiz', methods=['GET','POST'])
def dino_quiz():
    if request.method == 'POST':
        quiz_guesses = {}
        quiz_guesses['Question 1'] = request.form['continents']
        quiz_guesses['Question 2'] = request.form['eggs']
        quiz_guesses['Question 3'] = request.form.getlist('herbivores')
        quiz_guesses['Question 4'] = request.form['extinct']
        print(quiz_guesses)

        quiz_results = {}
        quiz_answers= {
            'Question 1': 'North America',
            'Question 2': 'True',
            'Question 3': ['Stegosaurus', 'Triceratops'],
            'Question 4': 66
        }

        for answer in quiz_answers:
            if quiz_answers[answer] == quiz_guesses[answer]:
                quiz_results[answer] = f"Correct! The answer is {quiz_answers[answer]}"
            else:
                quiz_results[answer] = f"Incorrect! The answer is {quiz_answers[answer]}"

        print(quiz_results)

        return render_template('quiz-results.html', quiz_results=quiz_results)
    else:
        return render_template('dino-quiz.html')


@app.route('/dino/<dino_id>/addfact', methods=['GET','POST'])
def addfact(dino_id):
    dino_id=int(dino_id)
    if request.method == 'POST':
        name = request.form['name']
        fact = request.form['fact']
        database.insert_fact(dino_id, name, fact)
        return redirect(url_for('index',dino_id=dino_id))
    else:
        dino = database.get_dino(dino_id)
        return render_template("add_fact.html",dino=dino)