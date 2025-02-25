import os
from flask import Flask
from flask_graphql import GraphQLView
from flask_cors import CORS
from models import db_session
from schema import schema
from services.unit_of_work import UnitOfWork
from dotenv import load_dotenv

# Determine the environment and load the appropriate .env file
env = os.getenv('FLASK_ENV', 'local')  # Default to 'local' if FLASK_ENV is not set

if env == 'production':
    load_dotenv('.env.prod')
elif env == 'development':
    load_dotenv('.env.dev')
else:
    load_dotenv('.env.local')

app = Flask(__name__)
CORS(app, resources={r"/graphql": {"origins": "http://localhost:3000"}})  # Allow only the frontend origin

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # Enable GraphiQL interface
    )
)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.shell_context_processor
def make_shell_context():
    return {'db_session': db_session, 'UnitOfWork': UnitOfWork}

if __name__ == '__main__':
    app.run(debug=(env != 'production'), host='localhost', port=5000)  # Ensure host is set to 'localhost' 