"""API locale de suivi de candidatures, sans dépendance externe."""
import argparse
import json
import sqlite3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

STATUSES = {"à envoyer", "envoyée", "entretien", "refusée", "acceptée"}

class Store:
    def __init__(self, path):
        self.path = path
        with self.connect() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY,
                company TEXT NOT NULL CHECK(length(company) BETWEEN 1 AND 120),
                role TEXT NOT NULL CHECK(length(role) BETWEEN 1 AND 160),
                status TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)""")

    def connect(self):
        db = sqlite3.connect(self.path)
        db.row_factory = sqlite3.Row
        return db

    def all(self):
        with self.connect() as db:
            return [dict(r) for r in db.execute("SELECT * FROM applications ORDER BY id DESC")]

    def add(self, data):
        if not isinstance(data, dict):
            raise ValueError("Le corps JSON doit être un objet.")
        cleaned = {}
        for field, maximum in [("company", 120), ("role", 160)]:
            value = data.get(field)
            if not isinstance(value, str) or not 1 <= len(value.strip()) <= maximum:
                raise ValueError(f"{field} : texte requis, entre 1 et {maximum} caractères.")
            cleaned[field] = value.strip()
        status = data.get("status", "à envoyer")
        if not isinstance(status, str) or status not in STATUSES:
            raise ValueError("Statut inconnu.")
        with self.connect() as db:
            cursor = db.execute("INSERT INTO applications(company,role,status) VALUES (?,?,?)",
                                (cleaned['company'], cleaned['role'], status))
            return dict(db.execute("SELECT * FROM applications WHERE id=?", (cursor.lastrowid,)).fetchone())

    def status(self, application_id, status):
        if not isinstance(status, str) or status not in STATUSES:
            raise ValueError("Statut inconnu.")
        with self.connect() as db:
            return db.execute("UPDATE applications SET status=? WHERE id=?", (status, application_id)).rowcount

    def remove(self, application_id):
        with self.connect() as db:
            return db.execute("DELETE FROM applications WHERE id=?", (application_id,)).rowcount

def handler_for(store):
    class Handler(BaseHTTPRequestHandler):
        def reply(self, status, data):
            body = json.dumps(data, ensure_ascii=False).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(body)

        def payload(self):
            if self.headers.get_content_type() != "application/json":
                raise ValueError("Content-Type application/json requis.")
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                raise ValueError("Taille de corps invalide.")
            if not 1 <= length <= 16384:
                raise ValueError("Corps requis, limité à 16 Ko.")
            try:
                data = json.loads(self.rfile.read(length))
            except (ValueError, UnicodeDecodeError):
                raise ValueError("JSON invalide.")
            if not isinstance(data, dict):
                raise ValueError("Le corps JSON doit être un objet.")
            return data

        def do_GET(self):
            if urlsplit(self.path).path == "/applications":
                self.reply(200, store.all())
            else:
                self.reply(404, {"error": "Route introuvable."})

        def do_POST(self):
            if urlsplit(self.path).path != "/applications":
                return self.reply(404, {"error": "Route introuvable."})
            try:
                self.reply(201, store.add(self.payload()))
            except ValueError as error:
                self.reply(400, {"error": str(error)})

        def mutate(self, delete=False):
            parts = urlsplit(self.path).path.strip('/').split('/')
            if len(parts) != 2 or parts[0] != 'applications' or not parts[1].isdigit():
                return self.reply(404, {"error": "Route introuvable."})
            try:
                changed = (store.remove(int(parts[1])) if delete else
                           store.status(int(parts[1]), self.payload().get('status')))
                self.reply(200 if changed else 404, {"ok": bool(changed)})
            except ValueError as error:
                self.reply(400, {"error": str(error)})

        def do_PATCH(self):
            self.mutate()

        def do_DELETE(self):
            self.mutate(delete=True)
    return Handler

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', default='stagetrack.sqlite3')
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), handler_for(Store(args.db)))
    print(f'API locale : http://127.0.0.1:{args.port}/applications')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
