from flask import Blueprint, jsonify, request
from file_handler import handle_file_upload, process_file
from ai_agent_handler import setup_and_invoke_agent

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/', methods=['GET'])
def docs():
    return "API"

@main_routes.route('/upload', methods=['POST'])
def upload_file():
    return handle_file_upload(request)

@main_routes.route('/process', methods=['POST'])
def process_query():
    return process_file(request)
