from flask import Flask, request, Response, jsonify
from flask_pymongo import PyMongo

from swagger_gen.swagger import Swagger
from dotenv import load_dotenv, find_dotenv

from flask.globals import current_app
import json

from parser.routes import parser

app = Flask(__name__)


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
    
    return jsonify({"message": input_resume.filename})


@app.route('/resume/retrieve/<file_name>', methods=["GET", 'POST'])
def retrieve_resume(file_name):
    mongodb_client.send_file(file_name)
    

@app.route("/resume-parse", methods = ["GET", "POST"])
def resume_parse():
    print("This is working")
    
    try:
        resume = request.files["file"]
        resume_contents = resume.read()
        keyword = request.form["keyword"]
    except KeyError:
        return jsonify({"error": "Missing 'file' or 'keyword' in request"}), 400
    
    #resume = request.files["file"]
    #resume_contents = resume.read()
    #keyword = request.form["keyword"]
 
    resume_file = open(resume_contents, "r", encoding="utf8")
 
    keyword_counter = 0
    text = resume_file.readline()
    
    print("This is still working")
    
    for text_line in text:
        keyword_counter += text_line.count(keyword)
     
    print(keyword_counter)    
    # return jsonify({"message": keyword_counter})
    
    response = jsonify({"status": "OK"})
    response.headers.add('Access-Control-Allow-Origin', '*')
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