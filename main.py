"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask

from flask import request
import math

from flask import jsonify
from flask import render_template

from decimal import *

import arrow
import boto3

#usage http://localhost:5000/wilks?bw=75&result=560

app = Flask(__name__)

#database global variables
AWS_region = 'ap-southeast-2'
wilks_dynamoDB_table = 'wilks_logging'

@app.route("/")
def reverse():
    return render_template('input_reverse.html')

@app.route('/reversewilks_api')
def add_numbers():
    bw = request.args.get('bw', 0, type=float)
    wilks = request.args.get('wilks', 0, type=float)
    isMale = request.args.get('isMale', type=str)
    isMetric = request.args.get('isMetric', type=str)
    
    x = bw
    if (isMetric == 'false'):
        x = ( x / 2.204)
    
    if (isMale == 'true'): 
        a = -216.0475144
        b = 16.2606339
        c = -0.002388645
        d = -0.00113732
        e = 0.00000701863
        f = -000.00000001291  
    else:
        a = 594.31747775582
        b = -27.23842536447
        c = 0.82112226871
        d = -0.00930733913
        e = 0.00004731582
        f = -0.00000009054 

    result =  wilks / (500 /( (a)+(b*x)+(c*(x**2))+(d*(x**3))+(e*(x**4))+(f*(x**5))) )
    if (isMetric == 'false'):
        result = ( result * 2.204)

    current_time = arrow.utcnow()
    print('{}'.format(current_time))

    dynamodb = boto3.resource('dynamodb', region_name=AWS_region)
    table = dynamodb.Table(wilks_dynamoDB_table)

    try:
        table.put_item(
            Item={
                'timestamp': '{}'.format(current_time),
                'wilks' : str(wilks),
                'bw' : str(bw),
                'male': str(isMale),
                'total': str(math.ceil(result)),
                'metric' : str(isMetric),
                'function' : 'Reverse',

            },
            ConditionExpression='attribute_not_exists(url_link)'
        )
    except Exception as e:
        print(e)

    return jsonify(result = math.ceil(result))

@app.route('/wilks_api')
def add_numbers1():
    bw = request.args.get('bw', 0, type=float)
    total = request.args.get('total', 0, type=float)
    isMale = request.args.get('isMale', type=str)
    isMetric = request.args.get('isMetric', type=str)

    x = bw


    if (isMetric == 'false'):
        x = ( x / 2.204)
        total = (total / 2.204)

    if (isMale == 'true'): 
        a = -216.0475144
        b = 16.2606339
        c = -0.002388645
        d = -0.00113732
        e = 0.00000701863
        f = -000.00000001291  
    else:
        a = 594.31747775582
        b = -27.23842536447
        c = 0.82112226871
        d = -0.00930733913
        e = 0.00004731582
        f = -0.00000009054

    wilks = total * (500 /( (a)+(b*x)+(c*(x**2))+(d*(x**3))+(e*(x**4))+(f*(x**5))) )

    wilks_round = Decimal(str(wilks))
    wilks_round = wilks_round.quantize(Decimal('0.01'),ROUND_HALF_UP)

    current_time = arrow.utcnow()
    print('{}'.format(current_time))

    dynamodb = boto3.resource('dynamodb', region_name=AWS_region)
    table = dynamodb.Table(wilks_dynamoDB_table)

    try:
        table.put_item(
            Item={
                'timestamp': '{}'.format(current_time),
                'wilks' : str(wilks_round),
                'bw' : str(bw),
                'male': str(isMale),
                'total': str(total),
                'metric' : str(isMetric),
                'function' : 'Forward',

            },
            ConditionExpression='attribute_not_exists(url_link)'
        )
    except Exception as e:
        print(e)

    return jsonify(result = (str(wilks_round)))


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
