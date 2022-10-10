from flask import Flask, render_template, url_for
import csv
app = Flask(__name__)

with open('dinosaurs.csv', 'r') as csvfile:
    data = csv.DictReader(csvfile)
    dinosaurs = {row['slug']: {'name':row['name'],'description':row['description'],'image':row['image'],'image-credit':row['source-credit']}for row in data}
    
    print(dinosaurs)

@app.route('/')
@app.route('/dino')
@app.route('/dino/<dino>')
def index(dino=None):
    if dino != None:
        return render_template('dino.html', dinosaurs=dinosaurs)
    else:
        return render_template('index.html', dinosaurs=dinosaurs)
    #make sure dino exists


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/FAQ')
def FAQ():
    return render_template('FAQ.html')

