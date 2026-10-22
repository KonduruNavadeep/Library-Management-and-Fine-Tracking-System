-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: library_db
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `library_db`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `library_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `library_db`;

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `books` (
  `book_id` int NOT NULL AUTO_INCREMENT,
  `isbn` varchar(20) NOT NULL,
  `title` varchar(150) NOT NULL,
  `author` varchar(100) NOT NULL,
  `category` varchar(50) NOT NULL,
  `total_copies` int NOT NULL,
  `available_copies` int NOT NULL,
  PRIMARY KEY (`book_id`),
  UNIQUE KEY `isbn` (`isbn`),
  CONSTRAINT `books_chk_1` CHECK ((`total_copies` >= 0)),
  CONSTRAINT `books_chk_2` CHECK ((`available_copies` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books`
--

LOCK TABLES `books` WRITE;
/*!40000 ALTER TABLE `books` DISABLE KEYS */;
INSERT INTO `books` VALUES (1,'978-0073523323','Database System Concepts','Silberschatz','DBMS',5,3),(2,'978-0262033848','Introduction to Algorithms','Cormen','Algorithms',4,3),(3,'978-0133591620','Modern Operating Systems','Tanenbaum','OS',6,5),(4,'978-0132126953','Computer Networks','Kurose','Networking',5,4),(5,'978-0134685991','Effective Java','Joshua Bloch','Programming',3,1),(6,'978-1491950357','Designing Data-Intensive Applications','Kleppmann','DBMS',4,4),(7,'978-0131103627','The C Programming Language','Kernighan','Programming',8,7),(8,'978-0321573513','Algorithms','Sedgewick','Algorithms',5,5),(9,'978-1118063330','Operating System Concepts','Galvin','OS',6,6),(10,'978-0136086208','Artificial Intelligence','Russell','AI',4,3);
/*!40000 ALTER TABLE `books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `borrow_records`
--

DROP TABLE IF EXISTS `borrow_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `borrow_records` (
  `issue_id` int NOT NULL AUTO_INCREMENT,
  `book_id` int NOT NULL,
  `member_id` int NOT NULL,
  `issue_date` date NOT NULL,
  `due_date` date NOT NULL,
  `return_date` date DEFAULT NULL,
  `status` varchar(20) DEFAULT 'Issued',
  PRIMARY KEY (`issue_id`),
  KEY `book_id` (`book_id`),
  KEY `member_id` (`member_id`),
  CONSTRAINT `borrow_records_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `books` (`book_id`) ON DELETE CASCADE,
  CONSTRAINT `borrow_records_ibfk_2` FOREIGN KEY (`member_id`) REFERENCES `members` (`member_id`) ON DELETE CASCADE,
  CONSTRAINT `borrow_records_chk_1` CHECK ((`status` in (_utf8mb4'Issued',_utf8mb4'Returned'))),
  CONSTRAINT `borrow_records_chk_2` CHECK ((`due_date` >= `issue_date`))
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `borrow_records`
--

LOCK TABLES `borrow_records` WRITE;
/*!40000 ALTER TABLE `borrow_records` DISABLE KEYS */;
INSERT INTO `borrow_records` VALUES (1,1,1,'2026-09-01','2026-09-15','2026-09-20','Returned'),(2,2,2,'2026-09-02','2026-09-16','2026-09-22','Returned'),(3,3,3,'2026-09-05','2026-09-19','2026-09-25','Returned'),(4,4,4,'2026-09-08','2026-09-22','2026-09-24','Returned'),(5,5,5,'2026-09-10','2026-09-24','2026-09-30','Returned'),(6,6,6,'2026-09-12','2026-09-26','2026-10-01','Returned'),(7,7,7,'2026-09-15','2026-09-29','2026-10-04','Returned'),(8,8,8,'2026-09-18','2026-10-02','2026-10-10','Returned'),(9,9,9,'2026-09-20','2026-10-04','2026-10-07','Returned'),(10,10,10,'2026-09-25','2026-10-09','2026-10-14','Returned'),(11,1,2,'2026-10-10','2026-10-24',NULL,'Issued'),(12,2,3,'2026-10-12','2026-10-26',NULL,'Issued'),(13,1,2,'2026-10-21','2026-11-04',NULL,'Issued'),(14,1,1,'2026-10-21','2026-11-04','2026-10-22','Returned'),(15,5,5,'2026-10-21','2026-11-04',NULL,'Issued'),(16,5,1,'2026-10-21','2026-11-20','2026-10-22','Returned'),(17,1,1,'2026-10-22','2026-11-21','2026-10-22','Returned'),(18,10,5,'2026-09-21','2026-10-20','2026-10-22','Returned');
/*!40000 ALTER TABLE `borrow_records` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `AutoCalculateFineOnReturn` AFTER UPDATE ON `borrow_records` FOR EACH ROW BEGIN
    DECLARE v_overdue_days INT;
    DECLARE v_fine_amount DECIMAL(8,2);

    
    IF NEW.status = 'Returned' AND OLD.status != 'Returned' THEN
        IF NEW.return_date > NEW.due_date THEN
            SET v_overdue_days = DATEDIFF(NEW.return_date, NEW.due_date);
            SET v_fine_amount = v_overdue_days * 5.00;

            INSERT INTO Fines (issue_id, fine_amount, payment_status, payment_date)
            VALUES (NEW.issue_id, v_fine_amount, 'Unpaid', NULL);
        END IF;
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `fines`
--

DROP TABLE IF EXISTS `fines`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fines` (
  `fine_id` int NOT NULL AUTO_INCREMENT,
  `issue_id` int NOT NULL,
  `fine_amount` decimal(8,2) NOT NULL,
  `payment_status` varchar(20) DEFAULT 'Unpaid',
  `payment_date` date DEFAULT NULL,
  PRIMARY KEY (`fine_id`),
  KEY `issue_id` (`issue_id`),
  CONSTRAINT `fines_ibfk_1` FOREIGN KEY (`issue_id`) REFERENCES `borrow_records` (`issue_id`) ON DELETE CASCADE,
  CONSTRAINT `fines_chk_1` CHECK ((`fine_amount` >= 0.00)),
  CONSTRAINT `fines_chk_2` CHECK ((`payment_status` in (_utf8mb4'Unpaid',_utf8mb4'Paid')))
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fines`
--

LOCK TABLES `fines` WRITE;
/*!40000 ALTER TABLE `fines` DISABLE KEYS */;
INSERT INTO `fines` VALUES (1,1,25.00,'Paid','2026-09-21'),(2,2,30.00,'Paid','2026-10-22'),(3,3,30.00,'Paid','2026-09-26'),(4,4,10.00,'Paid','2026-10-22'),(5,5,30.00,'Paid','2026-10-22'),(6,6,25.00,'Paid','2026-10-02'),(7,7,25.00,'Unpaid',NULL),(8,8,40.00,'Paid','2026-10-22'),(9,9,15.00,'Paid','2026-10-08'),(10,10,25.00,'Unpaid',NULL),(11,18,10.00,'Paid','2026-10-22');
/*!40000 ALTER TABLE `fines` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `members`
--

DROP TABLE IF EXISTS `members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `members` (
  `member_id` int NOT NULL AUTO_INCREMENT,
  `register_no` varchar(20) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `department` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(15) NOT NULL,
  PRIMARY KEY (`member_id`),
  UNIQUE KEY `register_no` (`register_no`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `members`
--

LOCK TABLES `members` WRITE;
/*!40000 ALTER TABLE `members` DISABLE KEYS */;
INSERT INTO `members` VALUES (1,'REG101','Aarav Sharma','CSE','aarav@college.edu','9876543210'),(2,'REG102','Diya Patel','ECE','diya@college.edu','9876543211'),(3,'REG103','Rohan Verma','MECH','rohan@college.edu','9876543212'),(4,'REG104','Sneha Reddy','CSE','sneha@college.edu','9876543213'),(5,'REG105','Vikram Nair','IT','vikram@college.edu','9876543214'),(6,'REG106','Ananya Iyer','EEE','ananya@college.edu','9876543215'),(7,'REG107','Karthik Raj','CSE','karthik@college.edu','9876543216'),(8,'REG108','Meera Joshi','CIVIL','meera@college.edu','9876543217'),(9,'REG109','Siddharth Rao','IT','siddharth@college.edu','9876543218'),(10,'REG110','Pooja Menon','ECE','pooja@college.edu','9876543219');
/*!40000 ALTER TABLE `members` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(20) DEFAULT 'Librarian',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  CONSTRAINT `users_chk_1` CHECK ((`role` in (_utf8mb4'Admin',_utf8mb4'Librarian')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'library_db'
--
/*!50003 DROP PROCEDURE IF EXISTS `IssueBook` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `IssueBook`(
    IN p_book_id INT,
    IN p_member_id INT,
    IN p_issue_date DATE,
    IN p_due_date DATE
)
BEGIN
    DECLARE v_avail INT;

    
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
        
        INSERT INTO Borrow_Records (book_id, member_id, issue_date, due_date, status)
        VALUES (p_book_id, p_member_id, p_issue_date, p_due_date, 'Issued');

        
        UPDATE Books
        SET available_copies = available_copies - 1
        WHERE book_id = p_book_id;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-10-22 22:34:03
