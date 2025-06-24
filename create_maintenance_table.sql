-- 创建维保申请表
CREATE TABLE IF NOT EXISTS `maintenance_requests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(100) NOT NULL,
  `contact_phone` varchar(50) NOT NULL,
  `contact_email` varchar(100) DEFAULT NULL,
  `elevator_location` varchar(500) NOT NULL,
  `elevator_type` varchar(100) DEFAULT NULL,
  `maintenance_type` varchar(50) NOT NULL,
  `urgency_level` varchar(50) NOT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `preferred_time` varchar(50) DEFAULT NULL,
  `status` varchar(50) NOT NULL DEFAULT 'Pending',
  `technician_notes` text,
  `scheduled_time` datetime DEFAULT NULL,
  `completed_time` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci; 