USE library_db;

INSERT IGNORE INTO Members (member_id, register_no, full_name, department, email, phone) VALUES
(1, 'REG101', 'Aarav Sharma', 'CSE', 'aarav@college.edu', '9876543210'),
(2, 'REG102', 'Diya Patel', 'ECE', 'diya@college.edu', '9876543211'),
(3, 'REG103', 'Rohan Verma', 'MECH', 'rohan@college.edu', '9876543212'),
(4, 'REG104', 'Sneha Reddy', 'CSE', 'sneha@college.edu', '9876543213'),
(5, 'REG105', 'Vikram Nair', 'IT', 'vikram@college.edu', '9876543214'),
(6, 'REG106', 'Ananya Iyer', 'EEE', 'ananya@college.edu', '9876543215'),
(7, 'REG107', 'Karthik Raj', 'CSE', 'karthik@college.edu', '9876543216'),
(8, 'REG108', 'Meera Joshi', 'CIVIL', 'meera@college.edu', '9876543217'),
(9, 'REG109', 'Siddharth Rao', 'IT', 'siddharth@college.edu', '9876543218'),
(10, 'REG110', 'Pooja Menon', 'ECE', 'pooja@college.edu', '9876543219');

INSERT IGNORE INTO Books (book_id, isbn, title, author, category, total_copies, available_copies) VALUES
(1, '978-0073523323', 'Database System Concepts', 'Silberschatz', 'DBMS', 5, 4),
(2, '978-0262033848', 'Introduction to Algorithms', 'Cormen', 'Algorithms', 4, 3),
(3, '978-0133591620', 'Modern Operating Systems', 'Tanenbaum', 'OS', 6, 5),
(4, '978-0132126953', 'Computer Networks', 'Kurose', 'Networking', 5, 4),
(5, '978-0134685991', 'Effective Java', 'Joshua Bloch', 'Programming', 3, 2),
(6, '978-1491950357', 'Designing Data-Intensive Applications', 'Kleppmann', 'DBMS', 4, 4),
(7, '978-0131103627', 'The C Programming Language', 'Kernighan', 'Programming', 8, 7),
(8, '978-0321573513', 'Algorithms', 'Sedgewick', 'Algorithms', 5, 5),
(9, '978-1118063330', 'Operating System Concepts', 'Galvin', 'OS', 6, 6),
(10, '978-0136086208', 'Artificial Intelligence', 'Russell', 'AI', 4, 3);

INSERT INTO Borrow_Records (issue_id, book_id, member_id, issue_date, due_date, return_date, status) VALUES
(1, 1, 1, '2026-09-01', '2026-09-15', '2026-09-20', 'Returned'), 
(2, 2, 2, '2026-09-02', '2026-09-16', '2026-09-22', 'Returned'), -- 6 days late
(3, 3, 3, '2026-09-05', '2026-09-19', '2026-09-25', 'Returned'), -- 6 days late
(4, 4, 4, '2026-09-08', '2026-09-22', '2026-09-24', 'Returned'), -- 2 days late
(5, 5, 5, '2026-09-10', '2026-09-24', '2026-09-30', 'Returned'), -- 6 days late
(6, 6, 6, '2026-09-12', '2026-09-26', '2026-10-01', 'Returned'), -- 5 days late
(7, 7, 7, '2026-09-15', '2026-09-29', '2026-10-04', 'Returned'), -- 5 days late
(8, 8, 8, '2026-09-18', '2026-10-02', '2026-10-10', 'Returned'), -- 8 days late
(9, 9, 9, '2026-09-20', '2026-10-04', '2026-10-07', 'Returned'), -- 3 days late
(10, 10, 10, '2026-09-25', '2026-10-09', '2026-10-14', 'Returned'), -- 5 days late
(11, 1, 2, '2026-10-10', '2026-10-24', NULL, 'Issued'),
(12, 2, 3, '2026-10-12', '2026-10-26', NULL, 'Issued');

-- 10 Sample Records for Fines (Rs 5.00 per overdue day)
INSERT INTO Fines (fine_id, issue_id, fine_amount, payment_status, payment_date) VALUES
(1, 1, 25.00, 'Paid', '2026-09-21'),
(2, 2, 30.00, 'Unpaid', NULL),
(3, 3, 30.00, 'Paid', '2026-09-26'),
(4, 4, 10.00, 'Unpaid', NULL),
(5, 5, 30.00, 'Unpaid', NULL),
(6, 6, 25.00, 'Paid', '2026-10-02'),
(7, 7, 25.00, 'Unpaid', NULL),
(8, 8, 40.00, 'Unpaid', NULL),
(9, 9, 15.00, 'Paid', '2026-10-08'),
(10, 10, 25.00, 'Unpaid', NULL);