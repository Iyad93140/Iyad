import importlib.util
import json
from pathlib import Path
import tempfile
import threading
import unittest
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from http.server import ThreadingHTTPServer
spec = importlib.util.spec_from_file_location('stagetrack_app', Path(__file__).with_name('app.py'))
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)

class APIIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = str(Path(self.tmp.name)/'test.sqlite3')
        self.store = app.Store(self.path)
        self.server = ThreadingHTTPServer(('127.0.0.1', 0), app.handler_for(self.store))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.url = f'http://127.0.0.1:{self.server.server_port}'

    def tearDown(self):
        self.server.shutdown(); self.server.server_close(); self.thread.join(); self.tmp.cleanup()

    def call(self, method, path='/applications', data=None):
        body = None if data is None else json.dumps(data).encode()
        request = Request(self.url+path, data=body, method=method, headers={'Content-Type':'application/json'})
        try:
            with urlopen(request, timeout=3) as response:
                return response.status, json.load(response)
        except HTTPError as response:
            return response.code, json.load(response)

    def test_full_lifecycle_and_persistence(self):
        status, item = self.call('POST', data={'company':' Atelier ', 'role':'Stage Python'})
        self.assertEqual(status, 201)
        self.assertEqual(app.Store(self.path).all()[0]['company'], 'Atelier')
        self.assertEqual(self.call('PATCH', f"/applications/{item['id']}", {'status':'entretien'})[0],200)
        self.assertEqual(self.call('GET')[1][0]['status'],'entretien')
        self.assertEqual(self.call('DELETE', f"/applications/{item['id']}")[0],200)
        self.assertEqual(self.call('GET')[1],[])

    def test_validation_and_not_found(self):
        for data in [[], {'company':' ', 'role':'Stage'}, {'company':'A','role':'B','status':[]}]:
            self.assertEqual(self.call('POST',data=data)[0],400)
        self.assertEqual(self.call('PATCH','/applications/999',{'status':'entretien'})[0],404)
        self.assertEqual(self.call('GET','/unknown')[0],404)

    def test_sql_text_is_not_executed(self):
        value="Robert'); DROP TABLE applications;--"
        self.assertEqual(self.call('POST',data={'company':value,'role':'Dev'})[0],201)
        self.assertEqual(self.call('GET')[1][0]['company'],value)

if __name__=='__main__':unittest.main()
