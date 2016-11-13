import json
import aylien_news_api
import requests
from aylien_news_api.rest import ApiException
from flask import Flask, jsonify

aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-ID'] = '9ba2cd69'
aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-Key'] = 'bdf4becfc24114a0924abb3e231f3649'

# create an instance of the API class
api_instance = aylien_news_api.DefaultApi()
api_response = api_instance.list_stories(source_name = ['CNN','MSNBC'])

articles = []
app = Flask(__name__)

def form_pairs():
    pairs = []
    for article in api_response.stories:
        con_response = api_instance.list_related_stories(source_name = ['Fox News', 'Bloomberg'], story_id = article.id)
        if(con_response is not None and len(con_response.related_stories) > 0):
            pairs.append((article, con_response.related_stories[0]))
    return pairs

def make_json(items):
    articles = []
    for pair in items:
        articles.append(
            {
                'id': pair[0],
                'title': pair[0].title,
                'left_body': pair[0].body,
                'left_author': pair[0].author,
                'left_summary': pair[0].summary,
                'left_sentiment': pair[0].sentiment,
                'left_date': pair[0].published_at,
                'right_title': pair[1].title,
                'right_body': pair[1].body,
                'right_author': pair[1].author,
                'right_summary': pair[1].summary,
                'right_sentiment': pair[1].sentiment,
                'right_date': pair[1].published_at,
                'done': False
            })
    return articles


form_pairs()

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'Articles': make_json(pairs)})

if __name__ == '__main__':
    app.run(debug=True)

"""
for pair in pairs:
    for item in pair:
        print item.title
        print item.source.name
        print "--------------------"
    print ""
"""



