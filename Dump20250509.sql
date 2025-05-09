-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: industock
-- ------------------------------------------------------
-- Server version	8.0.35

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `manager`
--

DROP TABLE IF EXISTS `manager`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `manager` (
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `surname` varchar(50) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone` char(10) DEFAULT NULL,
  `role` enum('STORE MANAGER','STORAGE MANAGER') DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `manager`
--

LOCK TABLES `manager` WRITE;
/*!40000 ALTER TABLE `manager` DISABLE KEYS */;
INSERT INTO `manager` VALUES ('dmavr25467','mtg54614556','Dionisis','Mavrotsoukalos','dmavrotsoukalos@mail.com','6945869275','STORE MANAGER'),('mazo3568','gmaz4336','Giorgos','Mazonakis','gmazonakis@mail.com','6925489696','STORAGE MANAGER'),('pret4548','74548rp!','Panagiotis','Retsos','pretsos@mail.com','6937548659','STORE MANAGER');
/*!40000 ALTER TABLE `manager` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `manufacturer` varchar(50) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `price` double DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (1,'Βίδα Μ8 40εκ Φλάντζα','Fournier Metalworks','BOLT',2.15),(2,'Βίδα Μ8 20εκ Φλάντζα','Fournier Metalworks','BOLT',1.6),(3,'Βίδα Μ4 20εκ Φλάντζα','Fournier Metalworks','BOLT',1.6),(4,'Παξιμάδι Μ8 με Πατούρα','Fournier Metalworks','NUT',1.79),(5,'Παξιμάδι Μ4 με Πατούρα','Fournier Metalworks','NUT',1.79),(6,'Σωλήνας Φ50 Καουτσούκ 1μ','Pipelayers','PIPE',3.4),(7,'Σωλήνας Φ50 Καουτσούκ 0.5μ','Pipelayers','PIPE',1.9),(8,'Κόφτης Καλωδίων','MKPSES Tools','TOOLS',4.8),(9,'Κατσαβίδι με καστάνια','MKPSES Tools','TOOLS',7.9),(10,'Κάβουρας','MKPSES Tools','TOOLS',5.8);
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_storage_stock`
--

DROP TABLE IF EXISTS `product_storage_stock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_storage_stock` (
  `product` int DEFAULT NULL,
  `storage` int DEFAULT NULL,
  `stock` int DEFAULT NULL,
  KEY `product` (`product`),
  KEY `storage` (`storage`),
  CONSTRAINT `product_storage_stock_ibfk_1` FOREIGN KEY (`product`) REFERENCES `product` (`id`),
  CONSTRAINT `product_storage_stock_ibfk_2` FOREIGN KEY (`storage`) REFERENCES `storage` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_storage_stock`
--

LOCK TABLES `product_storage_stock` WRITE;
/*!40000 ALTER TABLE `product_storage_stock` DISABLE KEYS */;
/*!40000 ALTER TABLE `product_storage_stock` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_store_stock`
--

DROP TABLE IF EXISTS `product_store_stock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_store_stock` (
  `product` int DEFAULT NULL,
  `store` int DEFAULT NULL,
  `stock` int DEFAULT NULL,
  KEY `product` (`product`),
  KEY `store` (`store`),
  CONSTRAINT `product_store_stock_ibfk_1` FOREIGN KEY (`product`) REFERENCES `product` (`id`),
  CONSTRAINT `product_store_stock_ibfk_2` FOREIGN KEY (`store`) REFERENCES `store` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_store_stock`
--

LOCK TABLES `product_store_stock` WRITE;
/*!40000 ALTER TABLE `product_store_stock` DISABLE KEYS */;
/*!40000 ALTER TABLE `product_store_stock` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `storage`
--

DROP TABLE IF EXISTS `storage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `storage` (
  `id` int NOT NULL AUTO_INCREMENT,
  `address` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone` char(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `storage`
--

LOCK TABLES `storage` WRITE;
/*!40000 ALTER TABLE `storage` DISABLE KEYS */;
INSERT INTO `storage` VALUES (1,'Agiou Andreou 30','storageagand@store.com','2610224499');
/*!40000 ALTER TABLE `storage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `storage_manager`
--

DROP TABLE IF EXISTS `storage_manager`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `storage_manager` (
  `username` varchar(50) NOT NULL,
  `storage` int DEFAULT NULL,
  PRIMARY KEY (`username`),
  KEY `storage` (`storage`),
  CONSTRAINT `storage_manager_ibfk_1` FOREIGN KEY (`username`) REFERENCES `manager` (`username`),
  CONSTRAINT `storage_manager_ibfk_2` FOREIGN KEY (`storage`) REFERENCES `storage` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `storage_manager`
--

LOCK TABLES `storage_manager` WRITE;
/*!40000 ALTER TABLE `storage_manager` DISABLE KEYS */;
INSERT INTO `storage_manager` VALUES ('mazo3568',1);
/*!40000 ALTER TABLE `storage_manager` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `storage_order`
--

DROP TABLE IF EXISTS `storage_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `storage_order` (
  `id` int NOT NULL AUTO_INCREMENT,
  `storage` int DEFAULT NULL,
  `status` enum('PENDING','COMPLETED','CANCELED') DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `storage` (`storage`),
  CONSTRAINT `storage_order_ibfk_1` FOREIGN KEY (`storage`) REFERENCES `storage` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `storage_order`
--

LOCK TABLES `storage_order` WRITE;
/*!40000 ALTER TABLE `storage_order` DISABLE KEYS */;
/*!40000 ALTER TABLE `storage_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `storage_order_product`
--

DROP TABLE IF EXISTS `storage_order_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `storage_order_product` (
  `order_num` int DEFAULT NULL,
  `product` int DEFAULT NULL,
  `amount` int DEFAULT NULL,
  KEY `product` (`product`),
  KEY `order_num` (`order_num`),
  CONSTRAINT `storage_order_product_ibfk_1` FOREIGN KEY (`product`) REFERENCES `product` (`id`),
  CONSTRAINT `storage_order_product_ibfk_2` FOREIGN KEY (`order_num`) REFERENCES `storage_order` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `storage_order_product`
--

LOCK TABLES `storage_order_product` WRITE;
/*!40000 ALTER TABLE `storage_order_product` DISABLE KEYS */;
/*!40000 ALTER TABLE `storage_order_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `storage_worker`
--

DROP TABLE IF EXISTS `storage_worker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `storage_worker` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `surname` varchar(50) DEFAULT NULL,
  `storage` int DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone` char(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `storage` (`storage`),
  CONSTRAINT `storage_worker_ibfk_1` FOREIGN KEY (`storage`) REFERENCES `storage` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `storage_worker`
--

LOCK TABLES `storage_worker` WRITE;
/*!40000 ALTER TABLE `storage_worker` DISABLE KEYS */;
INSERT INTO `storage_worker` VALUES (1,'Pantelis','Pantelidis',1,'ppantelidis@mail.com','6922576895'),(2,'Nikos','Oikonomopoulos',1,'noikonomopoulos@mail.com','6923568492');
/*!40000 ALTER TABLE `storage_worker` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `storage_worker_shift`
--

DROP TABLE IF EXISTS `storage_worker_shift`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `storage_worker_shift` (
  `worker` int NOT NULL,
  `shift_date` date NOT NULL,
  `start_time` char(5) DEFAULT NULL,
  `end_time` char(5) DEFAULT NULL,
  PRIMARY KEY (`worker`,`shift_date`),
  CONSTRAINT `storage_worker_shift_ibfk_1` FOREIGN KEY (`worker`) REFERENCES `storage_worker` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `storage_worker_shift`
--

LOCK TABLES `storage_worker_shift` WRITE;
/*!40000 ALTER TABLE `storage_worker_shift` DISABLE KEYS */;
/*!40000 ALTER TABLE `storage_worker_shift` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store`
--

DROP TABLE IF EXISTS `store`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store` (
  `id` int NOT NULL AUTO_INCREMENT,
  `address` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone` char(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store`
--

LOCK TABLES `store` WRITE;
/*!40000 ALTER TABLE `store` DISABLE KEYS */;
INSERT INTO `store` VALUES (1,'Korintou 65','korinthou@store.gr','2610244411'),(2,'Agias Sophias 3','agsophias@store.com','2610133322');
/*!40000 ALTER TABLE `store` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_manager`
--

DROP TABLE IF EXISTS `store_manager`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_manager` (
  `username` varchar(50) NOT NULL,
  `store` int DEFAULT NULL,
  PRIMARY KEY (`username`),
  KEY `store` (`store`),
  CONSTRAINT `store_manager_ibfk_1` FOREIGN KEY (`username`) REFERENCES `manager` (`username`),
  CONSTRAINT `store_manager_ibfk_2` FOREIGN KEY (`store`) REFERENCES `store` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_manager`
--

LOCK TABLES `store_manager` WRITE;
/*!40000 ALTER TABLE `store_manager` DISABLE KEYS */;
INSERT INTO `store_manager` VALUES ('dmavr25467',1),('pret4548',2);
/*!40000 ALTER TABLE `store_manager` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_order`
--

DROP TABLE IF EXISTS `store_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_order` (
  `id` int NOT NULL AUTO_INCREMENT,
  `store` int DEFAULT NULL,
  `storage` int DEFAULT NULL,
  `priority` enum('NORMAL','HIGH') DEFAULT NULL,
  `status` enum('PENDING','COMPLETED','CANCELED') DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `store` (`store`),
  KEY `storage` (`storage`),
  CONSTRAINT `store_order_ibfk_1` FOREIGN KEY (`store`) REFERENCES `store` (`id`),
  CONSTRAINT `store_order_ibfk_2` FOREIGN KEY (`storage`) REFERENCES `storage` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_order`
--

LOCK TABLES `store_order` WRITE;
/*!40000 ALTER TABLE `store_order` DISABLE KEYS */;
/*!40000 ALTER TABLE `store_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_order_product`
--

DROP TABLE IF EXISTS `store_order_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_order_product` (
  `order_num` int DEFAULT NULL,
  `product` int DEFAULT NULL,
  `amount` int DEFAULT NULL,
  KEY `product` (`product`),
  KEY `order_num` (`order_num`),
  CONSTRAINT `store_order_product_ibfk_1` FOREIGN KEY (`product`) REFERENCES `product` (`id`),
  CONSTRAINT `store_order_product_ibfk_2` FOREIGN KEY (`order_num`) REFERENCES `store_order` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_order_product`
--

LOCK TABLES `store_order_product` WRITE;
/*!40000 ALTER TABLE `store_order_product` DISABLE KEYS */;
/*!40000 ALTER TABLE `store_order_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_sale`
--

DROP TABLE IF EXISTS `store_sale`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_sale` (
  `id` int NOT NULL AUTO_INCREMENT,
  `store` int DEFAULT NULL,
  `sale_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `store` (`store`),
  CONSTRAINT `store_sale_ibfk_1` FOREIGN KEY (`store`) REFERENCES `store` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_sale`
--

LOCK TABLES `store_sale` WRITE;
/*!40000 ALTER TABLE `store_sale` DISABLE KEYS */;
/*!40000 ALTER TABLE `store_sale` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_sale_product`
--

DROP TABLE IF EXISTS `store_sale_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_sale_product` (
  `sale_num` int DEFAULT NULL,
  `product` int DEFAULT NULL,
  `amount` int DEFAULT NULL,
  KEY `product` (`product`),
  KEY `sale_num` (`sale_num`),
  CONSTRAINT `store_sale_product_ibfk_1` FOREIGN KEY (`product`) REFERENCES `product` (`id`),
  CONSTRAINT `store_sale_product_ibfk_2` FOREIGN KEY (`sale_num`) REFERENCES `store_sale` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_sale_product`
--

LOCK TABLES `store_sale_product` WRITE;
/*!40000 ALTER TABLE `store_sale_product` DISABLE KEYS */;
/*!40000 ALTER TABLE `store_sale_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_worker`
--

DROP TABLE IF EXISTS `store_worker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_worker` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `surname` varchar(50) DEFAULT NULL,
  `store` int DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone` char(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `store` (`store`),
  CONSTRAINT `store_worker_ibfk_1` FOREIGN KEY (`store`) REFERENCES `store` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_worker`
--

LOCK TABLES `store_worker` WRITE;
/*!40000 ALTER TABLE `store_worker` DISABLE KEYS */;
INSERT INTO `store_worker` VALUES (1,'Fotis','Tsidemoglou',1,'ftsidemoglou@mail.com','6947112311'),(2,'Markos','Mavrotsoukalos',1,'mmavrotsoukalos@mail.com','6948568932'),(3,'Makis','Kotsampasis',1,'mkotsampasis@mail.com','6945821549'),(4,'Charalampos','Kostoulas',2,'ckostoulas@mail.com','6937254884'),(5,'Christos','Mouzakitis',2,'cmouzakitis@mail.com','6937856996');
/*!40000 ALTER TABLE `store_worker` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_worker_shift`
--

DROP TABLE IF EXISTS `store_worker_shift`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_worker_shift` (
  `worker` int NOT NULL,
  `shift_date` date NOT NULL,
  `start_time` char(5) DEFAULT NULL,
  `end_time` char(5) DEFAULT NULL,
  PRIMARY KEY (`worker`,`shift_date`),
  CONSTRAINT `store_worker_shift_ibfk_1` FOREIGN KEY (`worker`) REFERENCES `store_worker` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_worker_shift`
--

LOCK TABLES `store_worker_shift` WRITE;
/*!40000 ALTER TABLE `store_worker_shift` DISABLE KEYS */;
/*!40000 ALTER TABLE `store_worker_shift` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-09 18:44:54
