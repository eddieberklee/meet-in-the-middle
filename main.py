#!/usr/bin/python

# Nikita Kouevda, Eddie Lee, Anthony Sutardja
# 2012/10/02

import random
from flask import Flask, render_template, request

# Flask
app = Flask(__name__)

@app.route("/")
def root():
    return "Hello, world!"

if __name__ == "__main__":
    app.run()
