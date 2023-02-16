"flask app to add rest api layer to dict command line tool"

# pylint: disable=multiple-statements, too-many-branches, too-many-return-statements

import sys
import subprocess
import json
import re
from flask import Flask, request


app = Flask(__name__)

@app.route('/api/dict', methods=['GET', 'POST'])
def translate():
    "service the request for looking up word with dict tool"
    content = request.json

    fd_dict= 'fd-' + two2three(content['source']) + '-' + two2three(content['target'])
    # Call the dict process
    try:
        subproc = subprocess.run( [ 'dict', '-d', fd_dict, content['word'] ], \
                                  capture_output=True, check=True )

    except subprocess.CalledProcessError as dictexcp:

        if dictexcp.returncode == 39:
            return json.dumps({'found': 0, 'error': 'languange/dictionary  not found',\
                    'word': content['word'], 'xlation': content['word']})
        if dictexcp.returncode == 20:
            return json.dumps({'found': 0, 'error': 'word not found',\
                    'word': content['word'], 'xlation': content['word']})
        return json.dumps({'found': 0, 'error': dictexcp.returncode,\
                    'word': content['word'], 'xlation': content['word']})

    lines = subproc.stdout.decode().splitlines()
    copy = lines
    for line in lines:
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
        copy.pop(0)

    # if not found in dictionary, return the original word
    return json.dumps({'found': 0, 'word': content['word'], 'xlation': content['word']})

def two2three(lang):
    "dict tool uses three letter language codes. Every one else uses 2 letter codes"
    langmap = { 'hr': 'hrv',
                'pt': 'por',
                'it': 'ita',
                'pl': 'pol',
                'ga': 'gle',
                'lt': 'lit',
                'ar': 'ara',
                'da': 'dan',
                'hu': 'hun',
                'eo': 'epo',
                'tr': 'tur',
                'sv': 'swe',
                'ja': 'jpn',
                'fi': 'fin',
                'es': 'spa',
                'af': 'afr',
                'sr': 'srp',
                'ku': 'kur',
                'la': 'lat',
                'fr': 'fra',
                'cy': 'cym',
                'nl': 'nld',
                'is': 'isl',
                'sk': 'slk',
                'de': 'deu',
                'cs': 'ces',
                'sw': 'swh',
                'en': 'eng'}
    return langmap[lang]

# check for dict app
try:
    result = subprocess.run(["dict"], capture_output=True, check=True)
except FileNotFoundError:
    print ('rest4dict requires dict process to be loaded. Make sure it is found in the path.',\
            file=sys.stderr)
    sys.exit(127)
except subprocess.CalledProcessError as dictexc:
    print("error code", dictexc.returncode, dictexc.output, file=sys.stderr)

# dict process found
if __name__ == "__main__":
    app.run()
    sys.exit(1)
