-- Initialize the vulnerable demo database
-- Passwords are stored in PLAINTEXT intentionally for demo purposes

CREATE DATABASE IF NOT EXISTS vulnapp;
USE vulnapp;

CREATE TABLE users (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50)  NOT NULL,
    password VARCHAR(50)  NOT NULL,
    role     VARCHAR(20)  DEFAULT 'user',
    email    VARCHAR(100)
);

INSERT INTO users (username, password, role, email) VALUES
    ('admin',  'Adm!nS3cur3#2024',  'admin', 'admin@cybercorp.internal'),
    ('alice',  'alice1234',          'user',  'alice@cybercorp.internal'),
    ('bob',    'bob5678',            'user',  'bob@cybercorp.internal'),
    ('carol',  'letmein',            'user',  'carol@cybercorp.internal');
