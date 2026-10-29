"""Démonstration reproductible sur une base SQLite en mémoire."""
from pathlib import Path
import sqlite3

def database():
    db=sqlite3.connect(':memory:')
    db.row_factory=sqlite3.Row
    folder=Path(__file__).parent
    for file in ['schema.sql','seed.sql']:
        db.executescript((folder/file).read_text(encoding='utf-8'))
    return db

if __name__=='__main__':
    with database() as db:
        queries=(Path(__file__).with_name('queries.sql')).read_text(encoding='utf-8')
        for number,query in enumerate(queries.split(';'),1):
            if query.strip():
                print(f'\nRequête {number}')
                for row in db.execute(query):print(dict(row))
