PRAGMA foreign_keys = ON;
CREATE TABLE members (
 id INTEGER PRIMARY KEY,
 name TEXT NOT NULL,
 email TEXT NOT NULL UNIQUE
);
CREATE TABLE books (
 id INTEGER PRIMARY KEY,
 title TEXT NOT NULL,
 author TEXT NOT NULL
);
-- Chaque ligne représente un exemplaire physique empruntable.
CREATE TABLE copies (
 id INTEGER PRIMARY KEY,
 book_id INTEGER NOT NULL REFERENCES books(id)
);
CREATE TABLE loans (
 id INTEGER PRIMARY KEY,
 copy_id INTEGER NOT NULL REFERENCES copies(id),
 member_id INTEGER NOT NULL REFERENCES members(id),
 borrowed_on TEXT NOT NULL,
 due_on TEXT NOT NULL,
 returned_on TEXT,
 CHECK(due_on >= borrowed_on),
 CHECK(returned_on IS NULL OR returned_on >= borrowed_on)
);
CREATE UNIQUE INDEX one_open_loan_per_copy ON loans(copy_id) WHERE returned_on IS NULL;
CREATE INDEX loans_member ON loans(member_id);
