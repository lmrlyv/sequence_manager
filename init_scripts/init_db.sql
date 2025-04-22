CREATE DATABASE IF NOT EXISTS sequence_manager;

CREATE USER IF NOT EXISTS 'test_user'@'%' IDENTIFIED BY 'test_password';

GRANT ALL PRIVILEGES ON sequence_manager.* TO 'test_user'@'%';
GRANT ALL PRIVILEGES ON test_sequence_manager.* TO 'test_user'@'%';

ALTER USER 'root'@'%' IDENTIFIED BY 'test';

FLUSH PRIVILEGES;
