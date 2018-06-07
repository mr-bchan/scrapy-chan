from flask import Flask, flash, jsonify, request, render_template, make_response
from flask_cors import CORS
import config
from processor.nlp.collocation import Collocation
import processor.db.helper as helper

print('********************************')
print('Setting up Flask API\n')





collocation = Collocation(helper)

app = Flask(__name__)
CORS(app)

@app.route("/nlp/link/",methods=['GET'])
def get_word_links():
    try:

        text = request.args.get("q")

        print('** /nlp/link **')
        print('** Received text **')
        print(text)
        print('*********************')

        output = collocation.get_links(text)
        response = jsonify({'success': True, 'data': output})
        print(response)

        return response

    except Exception as e:
        print('Error encountered.')
        print(e)

        response = jsonify({'success': False, 'error': str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route("/timeseries/posts/",methods=['GET'])
def get_post_counts():
    try:

        text = request.args.get("q")

        print('** /timeseries/posts **')
        print('** Received text **')
        print(text)
        print('*********************')

        response = []
        csvStrings = ['timestamp,count']

        for x in helper.get_posts_time_aggregated(text):
            response.append(list(x))

        for csvLine in response:
            csvLine[0] = str(csvLine[0])
            csvLine[3] = str(csvLine[3])

            if csvLine[1] < 10:
                csvLine[1] = '0' + str(csvLine[1])
            else:
                csvLine[1] = str(csvLine[1])

            if csvLine[2] < 10:
                csvLine[2] = '0' + str(csvLine[2])
            else:
                csvLine[2] = str(csvLine[2])

            line = [csvLine[0] + '-' + csvLine[1] + '-' + csvLine[2], csvLine[3]]
            csvStrings += [",".join(line)]

        csvStrings =  "\n".join(csvStrings)

        output = make_response(csvStrings)
        output.headers["Content-type"] = "text/csv"

        print(csvStrings)
        return output

    except Exception as e:
        print('Error encountered.')
        print(e)

        response = jsonify({'success': False, 'error': str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route("/timeseries/comments/",methods=['GET' ])
def get_comments_counts():
    try:

        text = request.args.get("q")

        print('** /timeseries/comments **')
        print('** Received text **')
        print(text)
        print('*********************')



        response = []
        csvStrings = ['timestamp,sentiment,count']

        for x in helper.get_comments_time_aggregated(text):
            response.append(list(x))

        for csvLine in response:
            csvLine[0] = str(csvLine[0])
            csvLine[4] = str(csvLine[4])

            if csvLine[1] < 10:
                csvLine[1] = '0' + str(csvLine[1])
            else:
                csvLine[1] = str(csvLine[1])

            if csvLine[2] < 10:
                csvLine[2] = '0' + str(csvLine[2])
            else:
                csvLine[2] = str(csvLine[2])

            line = [csvLine[0] + '-' + csvLine[1] + '-' + csvLine[2], csvLine[3], csvLine[4]]
            csvStrings += [",".join(line)]

        csvStrings =  "\n".join(csvStrings)

        output = make_response(csvStrings)
        output.headers["Content-type"] = "text/csv"

        print(csvStrings)
        return output

    except Exception as e:
        print('Error encountered.')
        print(e)

        response = jsonify({'success': False, 'error': str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')

    return response


if __name__ == "__main__":
    app.run(config.HOST,config.PORT)
