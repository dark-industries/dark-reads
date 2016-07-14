def parse_entry(entry):
    """parse an entry from raw string representation"""
    # eh kinda hacky
    rec, recommenders = entry.rsplit('[', 1)
    rec = rec.strip().strip('<').strip('>')
    recommenders = recommenders[:-1].split(', ')
    return rec, recommenders


def format_entry(rec, reccers):
    """format an entry to raw string representation"""
    return '{rec} [{reccers}]'.format(
        rec=rec,
        reccers=', '.join(reccers))


def load_entries(filename):
    with open(filename, 'r') as f:
        entries = f.readlines()
    return dict(parse_entry(e[2:].strip()) for e in entries)


def save_entries(entries, filename):
    formatted_entries = [format_entry(rec, reccers) for rec, reccers in entries.items()]
    with open(filename, 'w') as db:
        db.write('- {}'.format('\n- '.join(formatted_entries)))