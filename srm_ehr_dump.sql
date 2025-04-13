-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: srm_ehr
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `appointments`
--

DROP TABLE IF EXISTS `appointments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `patient_id` varchar(10) DEFAULT NULL,
  `doctor_id` varchar(10) DEFAULT NULL,
  `appointment_time` datetime DEFAULT NULL,
  `notes` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `patient_id` (`patient_id`),
  KEY `doctor_id` (`doctor_id`),
  CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `users` (`id`),
  CONSTRAINT `appointments_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointments`
--

LOCK TABLES `appointments` WRITE;
/*!40000 ALTER TABLE `appointments` DISABLE KEYS */;
INSERT INTO `appointments` VALUES (1,'p_1','d_1','2025-04-14 10:00:00','Follow-up for migraine','2025-04-12 19:07:28'),(2,'p_2','d_2','2025-04-15 11:00:00','Initial consultation for flu','2025-04-12 19:07:28');
/*!40000 ALTER TABLE `appointments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `approved_admins`
--

DROP TABLE IF EXISTS `approved_admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `approved_admins` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `dob` date NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `approved_admins`
--

LOCK TABLES `approved_admins` WRITE;
/*!40000 ALTER TABLE `approved_admins` DISABLE KEYS */;
INSERT INTO `approved_admins` VALUES (1,'Admin Alice','1975-06-15','admin@ehr.com');
/*!40000 ALTER TABLE `approved_admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `approved_doctors`
--

DROP TABLE IF EXISTS `approved_doctors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `approved_doctors` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `dob` date NOT NULL,
  `department` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `approved_doctors`
--

LOCK TABLES `approved_doctors` WRITE;
/*!40000 ALTER TABLE `approved_doctors` DISABLE KEYS */;
INSERT INTO `approved_doctors` VALUES (1,'Dr. John Smith','1980-01-20','Cardiology','john@ehr.com'),(2,'Dr. Clara Oswald','1985-03-10','Neurology','clara@ehr.com'),(3,'Dr. Rithika ','2006-10-11','dermatolog','rithikarithup0897@gmail.com'),(4,'Dr. Nandha','1997-10-06','dermatology','knandha08@gmail.com');
/*!40000 ALTER TABLE `approved_doctors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `approved_patients`
--

DROP TABLE IF EXISTS `approved_patients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `approved_patients` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `dob` date NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `approved_patients`
--

LOCK TABLES `approved_patients` WRITE;
/*!40000 ALTER TABLE `approved_patients` DISABLE KEYS */;
INSERT INTO `approved_patients` VALUES (1,'Patient One','1995-02-14','p1@ehr.com'),(2,'Patient Two','1990-10-05','p2@ehr.com'),(3,'sharmila','1983-06-05','sharmilarithu1983@gmail.com');
/*!40000 ALTER TABLE `approved_patients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patients`
--

DROP TABLE IF EXISTS `patients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients` (
  `id` varchar(10) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `age` int DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `symptoms` text,
  `diagnosis` text,
  `created_by` varchar(10) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `patients_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients`
--

LOCK TABLES `patients` WRITE;
/*!40000 ALTER TABLE `patients` DISABLE KEYS */;
INSERT INTO `patients` VALUES ('p_1','Patient One','1995-02-14',29,'Female','Headache, fever','Migraine','a_1','2025-04-12 19:07:11'),('p_2','Patient Two','1990-10-05',34,'Male','Cough, sore throat','Flu','a_1','2025-04-12 19:07:11');
/*!40000 ALTER TABLE `patients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reports`
--

DROP TABLE IF EXISTS `reports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reports` (
  `id` int NOT NULL AUTO_INCREMENT,
  `patient_id` varchar(10) DEFAULT NULL,
  `file_path` varchar(255) DEFAULT NULL,
  `uploaded_by` varchar(10) DEFAULT NULL,
  `uploaded_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `patient_id` (`patient_id`),
  KEY `uploaded_by` (`uploaded_by`),
  CONSTRAINT `reports_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `users` (`id`),
  CONSTRAINT `reports_ibfk_2` FOREIGN KEY (`uploaded_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reports`
--

LOCK TABLES `reports` WRITE;
/*!40000 ALTER TABLE `reports` DISABLE KEYS */;
INSERT INTO `reports` VALUES (1,'p_1','reports/migraine_report_p1.pdf','a_1','2025-04-12 19:07:28'),(2,'p_2','reports/flu_test_p2.pdf','a_1','2025-04-12 19:07:28'),(3,'p_1','reports/data_science_ass_468.pdf','a_1','2025-04-12 19:22:00'),(4,'p_1','reports/z2.pdf','a_1','2025-04-12 19:25:19'),(5,'p_1','reports/z2.pdf','a_1','2025-04-12 19:25:19'),(6,'p_1','reports/z2.pdf','a_1','2025-04-12 19:26:16');
/*!40000 ALTER TABLE `reports` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` varchar(10) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) DEFAULT NULL,
  `role` enum('admin','doctor','patient') NOT NULL,
  `dob` date DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('a_1','Admin Alice','admin@ehr.com','admin123','admin','1975-06-15','2025-04-13 00:36:23'),('d_1','Dr. John Smith','john@ehr.com','docpass','doctor','1980-01-20','2025-04-13 00:36:23'),('d_2','Dr. Clara Oswald','clara@ehr.com','456123','doctor','1985-03-10','2025-04-13 00:36:23'),('d_3','Dr. Nandha','knandha08@gmail.com','741258','doctor','1997-10-06','2025-04-13 03:38:47'),('p_1','Patient One','p1@ehr.com',NULL,'patient','1995-02-14','2025-04-13 00:36:23'),('p_2','Patient Two','p2@ehr.com','p2pass','patient','1990-10-05','2025-04-13 00:36:23'),('p_3','kiruthika','kiruthika2586@gmail.com',NULL,'patient','2005-02-08','2025-04-13 00:46:27'),('p_4','sharmila','sharmilarithu1983@gmail.com','789654','patient','1983-06-05','2025-04-13 02:08:35');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-13 19:06:33
