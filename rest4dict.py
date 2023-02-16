from flask import Flask, request
import sys
import subprocess
import json
import re

app = Flask(__name__)

@app.route('/api/dict', methods=['GET', 'POST'])
def translate():
    content = request.json

    fd_dict= 'fd-' + two2three(content['source']) + '-' + two2three(content['target'])
    # Call the dict process
    subproc = subprocess.run( [ 'dict', '-d', fd_dict, content['word'] ], capture_output=True )

    if subproc.returncode == 39:
        return json.dumps({'found': 0, 'error': 'languange/dictionary  not found',\
                'word': content['word'], 'xlation': content['word']})
    if subproc.returncode == 20:
        return json.dumps({'found': 0, 'error': 'word not found',\
                'word': content['word'], 'xlation': content['word']})

    lines = subproc.stdout.decode().splitlines()
    copy = lines
    for line in lines:
        print ("TP: " , line, file=sys.stderr)
        if content['word'] in line:
            # Why three pops? I don't know and I don't want to think about it. It worked.
            copy.pop(0)
            copy.pop(0)
            copy.pop(0)
            # Join multi-line definitions into one line
            xlation = ','.join(copy)
            # Remove "  1. ", "  2. ", etc from definitions
            xlation = re.sub('  [1-9][.] ', ' ', xlation, count=0, flags=0)
            # remove leading spaces from definition
            xlation = re.sub('^ *', '', xlation, count=0, flags=0)
            print('output: ', xlation, file=sys.stderr)
            return json.dumps({'found': 1, 'word': content['word'],
                               'xlation': xlation})
        else:
            copy.pop(0)

    # if not found in dictionary, return the original word
    return json.dumps({'found': 0, 'word': content['word'], 'xlation': content['word']})

def two2three(lang):
    if lang == 'hr': return 'hrv'
    if lang == 'pt': return 'por'
    if lang == 'it': return 'ita'
    if lang == 'pl': return 'pol'
    if lang == 'ga': return 'gle'
    if lang == 'lt': return 'lit'
    if lang == 'ar': return 'ara'
    if lang == 'da': return 'dan'
    if lang == 'hu': return 'hun'
    if lang == 'eo': return 'epo'
    if lang == 'tr': return 'tur'
    if lang == 'sv': return 'swe'
    if lang == 'ja': return 'jpn'
    if lang == 'fi': return 'fin'
    if lang == 'es': return 'spa'
    if lang == 'af': return 'afr'
    if lang == 'sr': return 'srp'
    if lang == 'ku': return 'kur'
    if lang == 'la': return 'lat'
    if lang == 'fr': return 'fra'
    if lang == 'cy': return 'cym'
    if lang == 'nl': return 'nld'
    if lang == 'is': return 'isl'
    if lang == 'sk': return 'slk'
    if lang == 'de': return 'deu'
    if lang == 'cs': return 'ces'
    if lang == 'sw': return 'swh'
    if lang == 'en': return 'eng'

# check for dict app
try:
    result = subprocess.run(["dict"], capture_output=True)
except FileNotFoundError:
    print ('rest4dict requires dict process to be loaded. Make sure it is found in the path.')
    sys.exit(127)

if result.returncode == 1:
    # dict process found
    if __name__ == "__main__":
        app.run()
        sys.exit(1)
