import logging
import os

from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create console handler and set level to DEBUG
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add formatter to ch
ch.setFormatter(formatter)

# Add ch to logger
logger.addHandler(ch)


@app.route("/generate_tags", methods=["POST"])
def tags_controller():
    data = request.json
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You will be provided with a block of text, and your task is to extract a list of tags from it, a minimum of 2 a maximum of 6. The tags should be preferrably single words. Also, the output should be a comma separated list of tags."
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
    logger.debug("Output message: %s", output_message)
    lines = output_message.content.split('\n')  # Split content by newline character

    tags = []
    for line in lines:
        # Extract tags from each line and append to the tags list
        tags.extend([tag.strip().rstrip(',') for tag in line.split()])

    return jsonify({'output': tags})


if __name__ == '__main__':
    app.run(debug=True)
