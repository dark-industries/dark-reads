# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import re
import json
import requests
from repo import repo, update_repo
from flask import Blueprint, request
from config import REPO, DB, SLACK_WEBHOOK_URL
from db import load, save

# parses:
# http://google.com this is the title
# http://google.com this is the title ^category
INPUT_RE = re.compile(r'(http[^ ]+) ([^\^]+)(\^(.+))?')


routes = Blueprint('routes', __name__)

@routes.route('/', methods=['POST'])
def index():
    db = os.path.join(REPO, DB)
    try:
        # update repo first
        repo.pull()
        data = load(db)
        name = request.form['user_name']
        link, title, _, category = INPUT_RE.match(request.form['text']).groups()
        title = title.strip()

        # default
        if category is None:
            category = 'hodgepodge'
        category = category.title()

        if category not in data:
            data[category] = {}

        added = False
        if link in data[category]:
            # already exists
            if name not in data[category][link]['recommenders']:
                # add new recommender
                data[category][link]['recommenders'].append(name)
            title = data[category][link]['title']
        else:
            data[category][link] = {
                'title': title,
                'recommenders': [name]
            }
            added = True

        save(data, db)
        update_repo(DB)

        if added:
            resp = '🎉I added {} as "{}", thanks for the recommendation🎉'.format(link, title)
        else:
            resp = '🎉I updated {}, it was already called "{}", thanks for the recommendation🎉'.format(link, title)
        requests.post(SLACK_WEBHOOK_URL, data=json.dumps({
            'text': resp
        }))
        return ''
    except Exception as e:
        requests.post(SLACK_WEBHOOK_URL, data=json.dumps({
            'text': 'uh oh: {}: {}'.format(e.__class__.__name__, str(e))
        }))
        raise
