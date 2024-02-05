/*
Navicat MySQL Data Transfer

Source Server         : local-mysql
Source Server Version : 80030
Source Host           : 127.0.0.1:3306
Source Database       : wordpress

Target Server Type    : MYSQL
Target Server Version : 80030
File Encoding         : 65001

Date: 2024-02-05 14:37:29
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for wp_embedding_records
-- ----------------------------
DROP TABLE IF EXISTS `wp_embedding_records`;
CREATE TABLE `wp_embedding_records` (
  `emb_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `file_name` varchar(191) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT '' COMMENT 'file name',
  `file_size` decimal(10,1) NOT NULL COMMENT 'file size in thousands byte',
  `owner` varchar(191) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT '' COMMENT 'file uploader',
  `file_status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT 'uploaded' COMMENT 'uploaded, inprogress,failed',
  `vector_ids` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci COMMENT 'vector ids in vector db after file embedded',
  `vector_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT 'vector path in vector db after file embedded',
  `file_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`emb_id`)
) ENGINE=InnoDB AUTO_INCREMENT=134 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='file embedding records';
