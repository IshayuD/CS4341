import webbrowser
import os
from flask import Flask, jsonify, redirect, render_template

app = Flask(__name__)

def main():
    file_path = 'CS4341_project\pages\home.html'
    webbrowser.open_new_tab('file://' + os.path.realpath(file_path))  # Opens HTML file in new tab

if __name__ == '__main__':
    main()