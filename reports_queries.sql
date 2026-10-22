SELECT 
    payment_status,
    COUNT(fine_id) AS total_records,
    SUM(fine_amount) AS total_amount,
    ROUND(AVG(fine_amount), 2) AS average_fine
FROM Fines
GROUP BY payment_status;

SELECT 
    m.department,
    COUNT(DISTINCT m.member_id) AS total_defaulters,
    COUNT(f.fine_id) AS total_fines_issued,
    SUM(CASE WHEN f.payment_status = 'Paid' THEN f.fine_amount ELSE 0.00 END) AS fines_collected,
    SUM(CASE WHEN f.payment_status = 'Unpaid' THEN f.fine_amount ELSE 0.00 END) AS fines_pending,
    SUM(f.fine_amount) AS total_fine_incurred
FROM Members m
JOIN Borrow_Records br ON m.member_id = br.member_id
JOIN Fines f ON br.issue_id = f.issue_id
GROUP BY m.department
ORDER BY fines_pending DESC;

SELECT 
    m.register_no,
    m.full_name AS member_name,
    m.department,
    m.phone,
    COUNT(f.fine_id) AS unpaid_books_count,
    SUM(f.fine_amount) AS total_pending_debt
FROM Members m
JOIN Borrow_Records br ON m.member_id = br.member_id
JOIN Fines f ON br.issue_id = f.issue_id
WHERE f.payment_status = 'Unpaid'
GROUP BY m.member_id, m.register_no, m.full_name, m.department, m.phone
ORDER BY total_pending_debt DESC;

SELECT 
    b.category,
    COUNT(br.issue_id) AS times_borrowed,
    COUNT(f.fine_id) AS overdue_instances,
    COALESCE(SUM(f.fine_amount), 0.00) AS total_fines_generated
FROM Books b
LEFT JOIN Borrow_Records br ON b.book_id = br.book_id
LEFT JOIN Fines f ON br.issue_id = f.issue_id
GROUP BY b.category
ORDER BY times_borrowed DESC;

SELECT 
    DATE_FORMAT(payment_date, '%Y-%m') AS collection_month,
    COUNT(fine_id) AS transactions_settled,
    SUM(fine_amount) AS monthly_revenue
FROM Fines
WHERE payment_status = 'Paid' AND payment_date IS NOT NULL
GROUP BY DATE_FORMAT(payment_date, '%Y-%m')
ORDER BY collection_month DESC;