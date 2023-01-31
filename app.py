from flask import Flask, jsonify
from views import AdsView
from errors import ApiException
from database import create_base


create_base()
app = Flask('app')

@app.errorhandler(ApiException)
def error_handler(error: ApiException):
    response = jsonify(
        {
            'status': 'error',
            'message': error.message
        }
    )
    response.status_code = error.status_code
    return response


app.add_url_rule('/ads/<int:id>', view_func=AdsView.as_view('ads'), methods={'GET', 'PATCH', 'DELETE'})
app.add_url_rule('/ads/', view_func=AdsView.as_view('ads_create'), methods={'POST'})
app.run()
