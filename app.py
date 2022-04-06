from flask import Flask, request
import werkzeug
import cv2
import numpy as np
import os

app = Flask(__name__)

@app.route("/test")
def test():
    print("Working")
    return "Working"





if __name__ == '__main__':
    app.run(debug=True)
