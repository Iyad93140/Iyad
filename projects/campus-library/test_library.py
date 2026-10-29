import importlib.util
from pathlib import Path
import sqlite3
import unittest
spec=importlib.util.spec_from_file_location('library_demo',Path(__file__).with_name('demo.py'))
demo=importlib.util.module_from_spec(spec);spec.loader.exec_module(demo)
class LibraryTests(unittest.TestCase):
    def setUp(self):self.db=demo.database()
    def tearDown(self):self.db.close()
    def test_reports(self):
        queries=Path(__file__).with_name('queries.sql').read_text().split(';')
        results=[list(self.db.execute(q)) for q in queries if q.strip()]
        self.assertEqual([(r['title'],r['available_copies']) for r in results[0]], [('Algorithmes',1),('Apprendre SQL',1)])
        self.assertEqual([r['name'] for r in results[1]],['Amina'])
        self.assertEqual([(r['name'],r['loan_count']) for r in results[2]],[('Amina',2),('Hugo',1),('Lina',0)])
    def test_prevent_double_loan_then_allow_after_return(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("INSERT INTO loans VALUES(4,1,2,'2026-10-29','2026-11-12',NULL)")
        self.db.execute("UPDATE loans SET returned_on='2026-10-29' WHERE id=1")
        self.db.execute("INSERT INTO loans VALUES(4,1,2,'2026-10-29','2026-11-12',NULL)")
    def test_foreign_keys_and_dates(self):
        for statement in ["INSERT INTO copies VALUES(9,999)","INSERT INTO loans VALUES(9,4,1,'2026-10-29','2026-10-01',NULL)"]:
            with self.assertRaises(sqlite3.IntegrityError):self.db.execute(statement)
if __name__=='__main__':unittest.main()
