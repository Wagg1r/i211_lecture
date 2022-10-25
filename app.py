from flask import Flask, render_template, request, redirect, url_for
import csv
app = Flask(__name__)

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

@app.route('/')
@app.route('/dino/')
@app.route('/dino/<dino>')
def index(dino=None):
    dinosaurs = get_dinos()

    print(dino)
    if dino and dino in dinosaurs.keys():
        dinosaur = dinosaurs[dino]
        return render_template('dino.html', dinosaur = dinosaur)
    else:
        return render_template('index.html', dinosaurs=dinosaurs)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/add_dino', methods=['GET', 'POST'])
def add_dino():
    if request.method == 'POST':
        dinosaurs = get_dinos()
        new_dino = {}
        new_dino['slug'] = request.form['slug']
        new_dino['name'] = request.form['name']
        new_dino['description'] = request.form['description']
        new_dino['image'] = request.form['image']
        new_dino['image-credit'] = request.form['image-credit']
        new_dino['source-url'] = request.form['source-url']
        new_dino['source-credit'] = request.form['source-credit']

        dinosaurs[request.form['slug']] = new_dino

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
