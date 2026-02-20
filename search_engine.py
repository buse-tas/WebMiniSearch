from flask import Flask, request, render_template
from query_parser import get_relevant_links
import traceback

# FIX #4: Removed "import pdb" — debug tool should not be in production code

app = Flask(__name__)


# error handler for 500 errors
@app.errorhandler(500)
def internal_error(exception):
    return "<pre>" + traceback.format_exc() + "</pre>"


# initial page
@app.route("/")
def start():
    return render_template('start.html')


@app.route("/search_for_pages")
def search_for_pages():
    query = request.args['search_query']
    search_results = get_relevant_links(query)
    return render_template('search_for_pages.html', found_pages=search_results, search_query=query)
