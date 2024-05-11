import os

from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)


@app.route("/generate_tags", methods=["POST"])
def tags_controller():
    data = request.json
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You will be provided with a block of text, and your task is to extract a list of tags from it, a minimum of 2 a maximum of 6."
            },
            {
                "role": "user",
                "content": data["text"]
            }
        ],
        temperature=0.5,
        max_tokens=64,
        top_p=1
    )
    completion = response.choices[0]
    output_message = completion.message
    tags = output_message.content.split('\n')[1:]  # Extracting tags from the content
    formatted_output = "\n".join(tags)

    return jsonify({'output': formatted_output})


if __name__ == '__main__':
    app.run(debug=True)

