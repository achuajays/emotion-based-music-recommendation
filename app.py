from flask import Flask, render_template, Response, jsonify
import gunicorn
from camera import *

app = Flask(__name__)

headings = ("Name","Album","Artist",'link')
df1 = music_rec()
df1 = df1.head(15)
@app.route('/')
def index():
    print(df1.to_json(orient='records'))
    return render_template('index.html', headings=headings, data=df1)

def gen(camera):
    while True:
        global df1
        frame, df1 = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/t')
def gen_table():
    return df1.to_json(orient='records')

from flask import Flask, render_template, request
from deepface import DeepFace



@app.route('/k')
def inded():
    return render_template('indep.html')

@app.route('/nd', methods=['POST'])
def analyze_attributes():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    # Save the uploaded file
    file_path = 'uploads/' + file.filename
    file.save(file_path)

    # Analyze facial attributes using DeepFace
    result = DeepFace.analyze(file_path)

    # Pass the results to the HTML template
    return render_template('nd.html', result=result)


from flask import Flask, render_template, request
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import webbrowser


# Download the VADER lexicon (if not already downloaded)
nltk.download('vader_lexicon')

def analyze_sentiment(text):
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(text)

    # Classify the sentiment
    if sentiment_scores['compound'] >= 0.05:
        return 'Positive'
    elif sentiment_scores['compound'] <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

@app.route('/nw', methods=['GET', 'POST'])
def inder():
    if request.method == 'POST':
        user_input = request.form['user_input']
        sentiment = analyze_sentiment(user_input)

        if sentiment == 'Positive':
            # Open the YouTube link for happy music
            webbrowser.open("https://www.youtube.com/watch?v=A-bluZKEHiQ")
        elif sentiment == 'Negative':
            # Open the YouTube link for happy music
            webbrowser.open("https://www.youtube.com/watch?v=eRnIks59Pjw")
        elif sentiment == 'Neutral':
            # Open the YouTube link for happy music
            webbrowser.open("https://www.youtube.com/watch?v=zq2pagG8_ok")

        return render_template('n.html', sentiment=sentiment, user_input=user_input)
    else:
        return render_template('n.html', sentiment=None, user_input=None)


from flask import Flask, render_template, request
from deepface import DeepFace
import os


# Ensure the 'uploads' directory exists
if not os.path.exists('uploads'):
    os.makedirs('uploads')

@app.route('/nf')
def indef():
    return render_template('inde.html')

@app.route('/compare', methods=['POST'])
def compare_images():
    # Check if both files are provided
    if 'file1' not in request.files or 'file2' not in request.files:
        return "Please provide two files for comparison."

    file1 = request.files['file1']
    file2 = request.files['file2']

    if file1.filename == '' or file2.filename == '':
        return "Please select two files for comparison."

    # Save the uploaded files
    file1_path = 'uploads/' + file1.filename
    file2_path = 'uploads/' + file2.filename
    file1.save(file1_path)
    file2.save(file2_path)

    # Compare the facial attributes of the two images using DeepFace
    result = DeepFace.verify(file1_path, file2_path)

    # Pass the result to the HTML template
    return render_template('compare.html', result=result)

if __name__ == '__main__':
    app.debug = True
    app.run()


