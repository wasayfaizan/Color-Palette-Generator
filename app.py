import openai
from flask import Flask, render_template, request
from dotenv import dotenv_values
import json

config = dotenv_values(".env")

openai.api_key = config["OPENAI_API_KEY"]

app = Flask(__name__,
 template_folder='templates'
)

def get_colors(msg):
    prompt = f"""
    You are a color palette generating assistant that responds to text prompts for color palettes
    You should only generate color palettes that fir the theme, mood, or instructions in the prompt
    The palette should be between 2 and 8 colors.
    
    Q: Convert the following verbal description of a color palette into a list of colors: The Mediterranean Sea 
    A: ["#006699", "#66CCCC", "#F0E68C", "#008000", "#F08080"]
    
    Q: Convert the following verbal description of a color palette into a list of colors: sage, nature, earth
    A: ["#EDF1D6", "#9DC08B", "#609966", "#40513B"]
    
    Desired Format: a JSON array of the hexadecimal color codes 

    Q: Convert the following verbal description of a color palette into a list of colors: {msg}
    A:
    
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        
    )
    
    colors = json.loads(response['choices'][0]['message']['content'])
    return colors


@app.route("/palette", methods=['POST'])
def prompt_to_palette():
    query = request.form.get("query")
    colors = get_colors(query)
    return {"colors": colors}
    


@app.route("/")
def index():
    return render_template("index.html")



if __name__ == '__main__':
    app.run(debug=True)