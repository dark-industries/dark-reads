# -*- coding: utf-8 -*-
import config
from gittle import Gittle

repo = Gittle(config.REPO, origin_uri=config.REPO_ORIGIN)


def update_repo(db):
    repo.stage(db)
    repo.commit(name='syllabot', email='f@frnsys.com', message='updated syllabus 📚☠')
    repo.push()
