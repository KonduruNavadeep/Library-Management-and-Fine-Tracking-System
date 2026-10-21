USE library_db;

-- Drop existing procedure and trigger if re-running the script
DROP PROCEDURE IF EXISTS IssueBook;
DROP TRIGGER IF EXISTS AutoCalculateFineOnReturn;

DELIMITER //

-- 1. Stored Procedure: Handle book issue transaction and decrement available copies
CREATE PROCEDURE IssueBook(
    IN p_book_id INT,
    IN p_member_id INT,
    IN p_issue_date DATE,
    IN p_due_date DATE
)
BEGIN
    DECLARE v_avail INT;

    -- Check current available copies for the requested book
    SELECT available_copies INTO v_avail 
    FROM Books 
    WHERE book_id = p_book_id;

    IF v_avail IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Book ID does not exist.';
    ELSEIF v_avail <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No copies currently available for this book.';
    ELSE
        -- Insert the borrow transaction
        INSERT INTO Borrow_Records (book_id, member_id, issue_date, due_date, status)
        VALUES (p_book_id, p_member_id, p_issue_date, p_due_date, 'Issued');

        -- Decrement available_copies by 1
        UPDATE Books
        SET available_copies = available_copies - 1
        WHERE book_id = p_book_id;
    END IF;
END //

-- 2. SQL Trigger: Automatically calculate fine (Rs 5/day) and insert into Fines on late return
CREATE TRIGGER AutoCalculateFineOnReturn
AFTER UPDATE ON Borrow_Records
FOR EACH ROW
BEGIN
    DECLARE v_overdue_days INT;
    DECLARE v_fine_amount DECIMAL(8,2);

    -- Trigger checks if status changed to 'Returned' and return_date is past due_date
    IF NEW.status = 'Returned' AND OLD.status != 'Returned' THEN
        IF NEW.return_date > NEW.due_date THEN
            SET v_overdue_days = DATEDIFF(NEW.return_date, NEW.due_date);
            SET v_fine_amount = v_overdue_days * 5.00;

            INSERT INTO Fines (issue_id, fine_amount, payment_status, payment_date)
            VALUES (NEW.issue_id, v_fine_amount, 'Unpaid', NULL);
        END IF;
    END IF;
END //

DELIMITER ;