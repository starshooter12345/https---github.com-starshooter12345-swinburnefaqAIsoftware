import openai
from flask import Flask, request, jsonify
from transformers import pipeline
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the OpenAI API key and zero-shot classification pipeline
openai.api_key = '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'
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def is_relevant(question):
    """ Check if the question is relevant to Swinburne University. """
    relevant_keywords = [
    "Swinburne", "University", "Admission", "Application", "Scholarship",
    "Tuition", "Financial Aid", "Academic Calendar", "Classes", "Registration",
    "Housing", "Campus", "Health", "Transportation", "Student ID", "Library",
    "Study Spaces", "Gym", "Sports", "Clubs", "Events", "Career", "Internships",
    "Visa", "Orientation", "Accommodations", "Credits", "Study Abroad", "Transcripts",
    "Online Courses", "Technology Resources", "Plagiarism", "Complaint", "Major/Minor",
    "Tutoring", "Alumni", "Networking", "Diploma", "Mentoring", "Diversity", "LGBTQ+",
    "Mental Health", "Safety", "Sustainability", "Indigenous Support", "Cultural Events",
    "Spiritual Resources", "Leave of Absence", "Gap Year", "Research", "Innovation",
    "Entrepreneurship", "Art and Design", "Film and Media", "Exhibitions"
    ]
    return any(keyword.lower() in question.lower() for keyword in relevant_keywords)
    return True


def ask_chat_model(question, model_id):
    """Send a question to the OpenAI chat model and return the response within university context."""
    try:
        university_context = "You are a helpful assistant knowledgeable about Swinburne University's facilities, services, and academic programs."
        response = openai.ChatCompletion.create(
            model=model_id,
            messages=[{"role": "system", "content": university_context},
                      {"role": "user", "content": question}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Sorry, I couldn't process your request at the moment."


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    question = data.get("question", "")
    model_id = 'ft:gpt-3.5-turbo-0125:personal::9E5EM4b8'  # Use a fine-tuned model or a capable general model
    
    if is_relevant(question):
        answer = ask_chat_model(question, model_id)
    else:
        answer = "Please ask a question related to Swinburne University."
    
    return jsonify({"response": answer})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
