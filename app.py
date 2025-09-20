import os
import json
from flask import Flask, jsonify, request
from groq import Groq
import serverless_wsgi
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize Groq client using API key from .env
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Categories
categories = [
    "Banking", "Books", "Clothes", "College Admissions", "Cooking",
    "Elementary Education", "Middle School Education", "High School Education", "University Education",
    "Employment", "Finance", "Food", "Gardening", "Homelessness", "Housing", "Jobs", "Investing",
    "Matrimonial", "Brain Medical", "Depression Medical", "Eye Medical", "Hand Medical",
    "Head Medical", "Leg Medical", "Rental", "School", "Shopping",
    "Baseball Sports", "Basketball Sports", "Cricket Sports", "Handball Sports",
    "Jogging Sports", "Hockey Sports", "Running Sports", "Tennis Sports",
    "Stocks", "Travel", "Tourism"
]

# Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "API is running"})

@app.route('/predict_categories', methods=['POST'])
def predict_categories_api():
    data = request.get_json()
    subject = data.get("subject")
    description = data.get("description")

    if not subject or not description:
        return jsonify({"error": "Subject and description are required"}), 400

    try:
        predicted_categories = predict_categories(subject, description)
        response = jsonify(predicted_categories)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate_answer', methods=['POST'])
def generate_answer_api():
    data = request.get_json()
    category = data.get("category")
    subject = data.get("subject")
    question = data.get("description")

    if not category or not subject or not question:
        return jsonify({"error": "Category, subject, and description are required"}), 400

    try:
        answer = chat_with_llama(category, subject, question)
        response = jsonify(answer)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def predict_categories(subject, description):
    prompt = f"""
You are a zero-shot text classifier that classifies user input into exactly three categories from the predefined list below. Respond ONLY with a comma-separated list of categories. Do not include any additional text or explanations.

Categories: {", ".join(categories)}

User Input:
Subject: {subject}
Description: {description}

Output (comma-separated categories):
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        top_p=0.3
    )

    raw_output = response.choices[0].message.content.strip()
    parts = [category.strip() for category in raw_output.split(",")]
    valid_categories = [category for category in parts if category in categories]
    return valid_categories[:3]

# Category prompts dictionary (only a few examples shown; you can add the rest)
category_prompts = {
    "Banking": "You are a meticulous and trustworthy banking advisor at Saayam. Answer this question carefully:",
    "Books": "You are a well-read literary guide at Saayam. Share your perspective:",
    "Clothes": "You are a fashion stylist at Saayam. Offer friendly and practical advice:",
    "College Admissions": "You are a dedicated admissions mentor at Saayam. Provide supportive guidance:",
    "Cooking": "You are a cheerful culinary expert at Saayam. Help this user with friendly advice:",
    # Add remaining categories as in your previous code
}

def chat_with_llama(category, subject, description):
    role_prompt = category_prompts.get(
        category,
        "You are a helpful expert from Saayam. Answer the question clearly and kindly:"
    )

    full_prompt = f"{role_prompt}\n\nSubject: {subject}\nQuestion: {description}"

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()

def lambda_handler(event, context):
    if "path" in event:
        event["path"] = event["path"].replace("/dev/genai/v0.0.1", "")
    return serverless_wsgi.handle_request(app, event, context)
