import json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

def post(url, data):
    req = Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type':'application/json'})
    try:
        with urlopen(req, timeout=10) as resp:
            return resp.read().decode('utf-8')
    except HTTPError as e:
        return e.read().decode('utf-8')
    except URLError as e:
        return str(e)

url = 'http://127.0.0.1:5000/api/generate'
idea = 'A lonely lighthouse keeper discovers a secret message in a bottle.'
for mode in ['screenplay','characters','plan']:
    out = post(url, {'idea': idea, 'mode': mode, 'temperature': 0.5, 'max_tokens': 300})
    print('MODE:', mode)
    try:
        j = json.loads(out)
        print(j.get('output','(no output)')[:600])
    except Exception:
        print('RESPONSE:', out[:600])
    print('\n' + '-'*60 + '\n')
