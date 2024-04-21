from flask import Flask
from json_encoder import CustomJSONEncoder

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
