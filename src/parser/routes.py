from flask import Flask, request, Response, jsonify, Blueprint, current_app
from flask_cors import CORS
from flask_cors import cross_origin

parser = Blueprint('parser', __name__, url_prefix='/parser')

@parser.route("/resume-parse", methods=["GET"])
def resume_parse():
    resume = request.files("file")
    keyword = request.form["keyword"]
    
    resume_file = open(resume, "r", encoding="utf8")
    
    keyword_counter = 0
    text = resume_file.readline()
    
    for text_line in text:
        keyword_counter += text_line.count(keyword)
        
    # return jsonify({"message": keyword_counter})
    
    response = jsonify({'some': 'data'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@parser.route('/parser-health')
def parser_health():
    return jsonify({"status": "OK"})
