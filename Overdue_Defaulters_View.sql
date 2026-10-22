USE library_db;

CREATE OR REPLACE VIEW Overdue_Defaulters_View AS
SELECT 
    m.member_id,
    m.register_no,
    m.full_name AS member_name,
    m.department,
    m.phone,
    b.book_id,
    b.title AS book_title,
    br.issue_id,
    br.issue_date,
    br.due_date,
    br.return_date,
    br.status AS borrow_status,
    -- Calculate days overdue dynamically
    CASE 
        WHEN br.return_date IS NULL AND CURRENT_DATE > br.due_date 
            THEN DATEDIFF(CURRENT_DATE, br.due_date)
        WHEN br.return_date > br.due_date 
            THEN DATEDIFF(br.return_date, br.due_date)
        ELSE 0
    END AS days_overdue,
    f.fine_id,
    COALESCE(f.fine_amount, 0.00) AS fine_amount,
    COALESCE(f.payment_status, 'No Fine') AS payment_status
FROM Borrow_Records br
JOIN Members m ON br.member_id = m.member_id
JOIN Books b ON br.book_id = b.book_id
LEFT JOIN Fines f ON br.issue_id = f.issue_id
WHERE (br.return_date IS NULL AND CURRENT_DATE > br.due_date)
   OR (f.payment_status = 'Unpaid');