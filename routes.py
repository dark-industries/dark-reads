import os
import json
import requests
from repo import repo, update_repo
from flask import Blueprint, request
from config import REPO, DB, SLACK_WEBHOOK_URL
from db import load_entries, save_entries


routes = Blueprint('routes', __name__)

@routes.route('/', methods=['POST'])
def index():
    db = os.path.join(REPO, DB)
    try:
        # update repo first
        repo.pull()
        entries = load_entries(db)
        name = request.form['user_name']
        link_or_title = request.form['text']

        added = False
        if link_or_title in entries:
            # already exists
            if name not in entries[link_or_title]:
                # add new recommender
                entries[link_or_title].append(name)
        else:
            entries[link_or_title] = [name]
            added = True

        save_entries(entries, db)
        update_repo(DB)

        if added:
            resp = 'I added {}'.format(link_or_title)
        else:
            resp = 'I updated {}'.format(link_or_title)
        requests.post(SLACK_WEBHOOK_URL, data=json.dumps({
            'text': resp
        }))
        return ''
    except Exception as e:
        requests.post(SLACK_WEBHOOK_URL, data=json.dumps({
            'text': 'uh oh: {}'.format(str(e))
        }))
        raise
