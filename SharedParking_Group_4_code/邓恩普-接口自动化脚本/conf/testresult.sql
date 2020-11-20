/*
Navicat MySQL Data Transfer

Source Server         : con69
Source Server Version : 50649
Source Host           : 172.16.13.69:3306
Source Database       : testresult

Target Server Type    : MYSQL
Target Server Version : 50649
File Encoding         : 65001

Date: 2020-11-04 17:24:18
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for test_result
-- ----------------------------
DROP TABLE IF EXISTS `test_result`;
CREATE TABLE `test_result` (
  `result_id` int(11) NOT NULL AUTO_INCREMENT,
  `version` varchar(10) NOT NULL,
  `module` varchar(20) NOT NULL,
  `type` varchar(20) NOT NULL,
  `case_id` varchar(50) NOT NULL,
  `case_desc` varchar(200) NOT NULL,
  `test_result` varchar(10) NOT NULL,
  `execute_time` datetime DEFAULT NULL,
  `error_msg` varchar(20) NOT NULL,
  `error_screenshot` varchar(50) NOT NULL,
  PRIMARY KEY (`result_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of test_result
-- ----------------------------
