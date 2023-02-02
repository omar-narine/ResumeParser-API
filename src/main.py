from flask import Flask, request, Response, jsonify
from flask_pymongo import PyMongo

from swagger_gen.swagger import Swagger
from dotenv import load_dotenv, find_dotenv

from flask.globals import current_app
import json

from parser.routes import parser

import traceback
import tempfile

app = Flask(__name__)
app.register_blueprint(parser)


swagger = Swagger(
    app=app,
    title='Resume Parser API',
    version="1.0.0",
    description="API Developed to be used in unison with React Resume Parser App",
    contact_email="omarsan786@gmail.com"
    )
swagger.configure()


client_URI = "mongodb+srv://admin:muqijo97ypPPGbVn@resumeparsercluster.hokokmj.mongodb.net/?retryWrites=true&w=majority"
mongodb_client = PyMongo(app, uri=client_URI)
db = mongodb_client.db

@app.route('/')
def main():
    return jsonify({"message": "Hello, World!"})

@app.route('/health')
def health():
    return Response(json.dumps({
        "status" : "OK"
    }), mimetype="application/json")
    
@app.route('/resume/upload', methods=["GET", "POST"])
def upload_to_mongoDB():
    '''
    This route was meant to upload the files to MongoDB so that they can be stored and retrieved later. 
    Processing the files in that manner would be well beyond the scope of my skills so we're going to stick to parsing one file 
    at a time. 
    '''
    
    input_resume = request.files["file"]
    
    # Possible collision scenario if multiple resumes are uploaded with the same name
    mongodb_client.save_file(input_resume.filename, input_resume)
    
    response = jsonify({"message": input_resume.filename})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/resume/retrieve/<file_name>', methods=["GET", 'POST'])
def retrieve_resume(file_name):
    mongodb_client.send_file(file_name)


# This is a testing endpoint to test the functionality of the parser endpoint as I continue to build it out
@app.route("/testing-endpoint", methods=["GET", "POST"])
def test_endpoint():
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
    

@app.route('/parser-health')
def parser_health():
    response = jsonify({"status": "OK"})
    print("Working")
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


# Run app
if __name__ == "__main__":
    app.run()