import re
from collections import defaultdict

# parses:
# [this the title](http://google.com)
# [this the title](http://google.com) [rec1, rec2]
ENTRY_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)( \[([^\]]+)\])?')


template = '''
# syllabus

{}
'''


def parse_entry(entry):
    """parse an entry from raw string representation"""
    title, link, _, recommenders = ENTRY_RE.match(entry).groups()
    if recommenders is None:
        recommenders = []
    else:
        recommenders = recommenders.split(', ')
    return title, link, recommenders


def format_entry(link, title, recommenders):
    """format an entry to raw string representation"""
    if recommenders:
        return '[{title}]({link}) [{reccers}]'.format(
            title=title,
            link=link,
            reccers=', '.join(recommenders))
    else:
        return '[{title}]({link})'.format(
            title=title,
            link=link)


def format_category(category, entries):
    # sorry
    formatted_entries = [
        format_entry(link,
                     data['title'],
                     data['recommenders'])
        for link, data in sorted(entries.items())]
    entries ='- {}'.format('\n- '.join(formatted_entries))
    return '## {category}\n{entries}'.format(
        category=category,
        entries=entries)


def load(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    data = defaultdict(dict)
    current_category = ''
    for line in lines:
        line = line.strip()

        if not line:
            continue

        elif line.startswith('##'):
            current_category = line.strip('## ').title()

        elif line.startswith('- '):
            title, link, recommenders = parse_entry(line[2:])
            data[current_category][link] = {
                'title': title,
                'recommenders': recommenders
            }
    return data


def save(data, filename):
    body = '\n\n'.join([
        format_category(name, entries)
        for name, entries in sorted(data.items())])
    with open(filename, 'w') as db:
        db.write(template.format(body).strip())