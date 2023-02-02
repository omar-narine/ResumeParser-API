from flask import Flask, request, Response, jsonify, Blueprint, current_app
from flask_cors import CORS
from flask_cors import cross_origin

import traceback
import tempfile

parser = Blueprint('parser', __name__, url_prefix='/parser')

@parser.route("/resume-parse", methods=["GET", "POST"])
def resume_parse():
    try:
        print(request.files)
        resume = request.files["resume"]
        resume_contents =  resume.stream.read().decode("utf8")
        print(request.form)
        keyword = request.form["keyword"]
        print(keyword)
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding="utf8") as f:
            f.write(resume_contents)
            resume_file_name = f.name
        
        resume_file = open(resume_file_name, "r", encoding="utf8")
        
        keyword_counter = 0
        text = resume_file.readlines()
        for text_line in text:
            #print(text_line)
            keyword_counter += text_line.lower().count(keyword.lower())         
            
        response = jsonify({"message": keyword_counter})
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
     
        return response 
    
    except :
       traceback.print_exc()
       
       response = jsonify({"message": "ERROR"})
       response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
       return response 
    return response

@parser.route('/parser-health')
def parser_health():
    return jsonify({"status": "OK"})
