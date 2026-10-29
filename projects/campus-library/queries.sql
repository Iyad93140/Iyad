-- 1. Exemplaires actuellement disponibles, y compris les livres jamais empruntés.
SELECT b.title, COUNT(*) AS available_copies
FROM copies c JOIN books b ON b.id=c.book_id
WHERE NOT EXISTS (SELECT 1 FROM loans l WHERE l.copy_id=c.id AND l.returned_on IS NULL)
GROUP BY b.id ORDER BY b.title;

-- 2. Retards à une date de référence reproductible.
SELECT m.name, b.title, l.due_on
FROM loans l JOIN members m ON m.id=l.member_id
JOIN copies c ON c.id=l.copy_id JOIN books b ON b.id=c.book_id
WHERE l.returned_on IS NULL AND l.due_on < '2026-10-29'
ORDER BY l.due_on;

-- 3. Nombre d’emprunts par membre, y compris ceux sans emprunt.
SELECT m.name, COUNT(l.id) AS loan_count
FROM members m LEFT JOIN loans l ON l.member_id=m.id
GROUP BY m.id ORDER BY loan_count DESC,m.name;
