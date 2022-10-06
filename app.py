from flask import Flask, render_template, url_for
import csv
app = Flask(__name__)

with open('dinosaurs.csv', 'r') as csvfile:
    data = csv.DictReader(csvfile)
    for row in data:
        dinosaurs = {row['slug']: {'name':row['name'],'description':row['description'],'image':row['image'],'image-credit':row['source-credit']}}
    
    print(dinosaurs)

@app.route('/')
def index():
    return render_template('index.html', name="Thomas", dinosaurs = dinosaurs)

@app.route('/about')
def about():
    return render_template('about.html')

# @app.route('/dino/<dino>')
# def index(dino=None):
#     return render_template('index.html', dinosaurs=dinosaurs)