# Server for TCP interface with outside world
# Created by: Alex Laswell

from flask import Flask, render_template, request
from random import choice
from wtforms import Form, validators, SubmitField, TextField, ValidationError
import os
import subprocess

def valid_response(form, field):
    secret_key = "secret"
    if field.data != secret_key:
        raise ValidationError("That is not the correct answer.")

class ReusableForm(Form):
    """User entry form for challenge/response check"""

    questions = [
        "Where does the car go to sleep?",
        "Mummy, why do your boobies look so sad?",
        "Why is the road there?",
        "Why don’t babies come out of your mouth? It would be a lot easier!",
        "Is Mother Nature married to God?",
        "Why didn’t you call me Dave?",
        "Why can’t I have ketchup with cookies?",
        "Who is this and why?",
        "What is it like to be a girl?",
        "Why can you drink Coke and I can’t?",
        "Who makes eyes?",
        "Why is poo brown if you eat green vegetables?",
        "Why is it Tuesday?",
        "Why does the moon follow us home?",
        "Why don’t dogs walk on two legs like us?",
        "Why do you have blood and bones in your body? I don’t want them, take them out!",
        "Mummy, why does your forehead crease?",
        "How would a monkey eat without a mouth?",
        "Why is water wet?",
        "Where do balloons go?",
        "Why do boys have tails?",
        "But how do you get the pork out of the pig?",
        "How do snails work?",
        "Why is the sun so spicy?",
        "Why is someone stealing my blood?",
        "Why do you have to go to work?",
        "How do the people fit in the TV?",
        "Why don’t frogs eat cheese?",
        "How do we know what’s real?",
        "Why is it raining today?  It’s ‘Sun’day!",
    ]

    # Security question
    answer = TextField(
        choice(questions),
        validators=[
            validators.InputRequired(),
            valid_response,
        ],
    )

    # Submit button
    submit = SubmitField("Enter")

app = Flask(__name__)

@app.route('/status', methods=['GET'])
def status():
    pid = os.popen("pgrep -f 'pugbot.py'").read()
    if len(pid) <= 5:
        return "<h1>The bot is DOWN</h1>"
    else:
        return "<h1>The bot is UP</h1>"

@app.route('/restart', methods=['GET', 'POST'])
def restart():
    # Create form
    form = ReusableForm(request.form)

    # Restart bot on POST -- valid form required
    if request.method == 'POST' and form.validate():
        subprocess.call(['../runBot.sh'])
        return "The bot has been restarted"

    # Send info to index.html
    return render_template('index.html', form=form)

app.run(host='127.0.0.1', port=8000, debug=True)