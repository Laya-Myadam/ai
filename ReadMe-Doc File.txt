This is a Flask API using Groq LLM in order to classify and generate answers specific to categories.

This API will help us classify the user queries and convert them to predefined categories and thus generate detailed answers related to the category, subject and the description of the question asked.

It is built on Flask API, Integrated with GROQ LLM(Large Language Model)

Main features:
Predict upto 3 different categories for a question asked.
With the help of GROQ LLM generating the category specific answers
Covers various domains like finance, health, education etc
API key is managed via a .env file for the safety purpose.

Installation steps:

git clone https://github.com/saayam-for-all/ai
cd ai

creating a virtual environment
python -m venv venv
.\venv\Scripts\activate

Installing the dependencies
pip install -r requirements.txt
pip install flask groq serverless-wsgi python-dotenv

Adding groq api key in .env file

set FLASK_APP=app.py
set FLASK_ENV=development
flask run

Check the API End points using Get and Post(PostMan)

Future improvemnets:
1. we can further add authentication for secure API access
2. Add error tracking and logging.
Make the categories as dynamic and allow user to add more categories.