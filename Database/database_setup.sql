-- Active: 1774110803206@@localhost@3306@style_recommendation
-- 1. Database Creation
CREATE DATABASE IF NOT EXISTS style_recommendation;
USE style_recommendation;

-- 2. Login User Table
CREATE TABLE IF NOT EXISTS user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Supportive Tables
CREATE TABLE IF NOT EXISTS face_shape (
    fsid INT PRIMARY KEY, 
    fs_name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS skin_tone (
    stid INT PRIMARY KEY, 
    st_name VARCHAR(50), 
    undertone VARCHAR(50)
);

-- 4. Recommendations Tables
CREATE TABLE IF NOT EXISTS hairstyle (
    hsid INT PRIMARY KEY,
    hs_name VARCHAR(100),
    fsid INT,
    hs_image VARCHAR(255),
    FOREIGN KEY (fsid) REFERENCES face_shape(fsid)
);

CREATE TABLE IF NOT EXISTS hair_colour (
    hcid INT PRIMARY KEY,
    hc_name VARCHAR(100),
    stid INT,
    hc_image VARCHAR(255),
    FOREIGN KEY (stid) REFERENCES skin_tone(stid)
);

CREATE TABLE IF NOT EXISTS cloth_colour (
    ccid INT PRIMARY KEY,
    cc_name VARCHAR(100),
    stid INT,
    cc_image VARCHAR(255),
    FOREIGN KEY (stid) REFERENCES skin_tone(stid)
);

-- 5. INSERT MASTER DATA (IDs 1-5)
INSERT IGNORE INTO face_shape VALUES (1,'Oval'), (2,'Round'), (3,'Square'), (4,'Heart'), (5,'Diamond');
INSERT IGNORE INTO skin_tone VALUES (1,'Fair','Cool'), (2,'Medium','Warm'), (3,'Olive','Neutral'), (4,'Dusky','Warm'), (5,'Dark','Neutral');

-- 6. INSERT HAIRSTYLE DATA (.png paths)
INSERT IGNORE INTO hairstyle VALUES 
(1,'Layered Cut', 1, 'images/layered.png'),
(2,'Bob Cut', 2, 'images/blunt_bob.png'),
(3,'Pixie Cut', 3, 'images/pixie.png'),
(4,'Long Waves', 4, 'images/long_waves.png'),
(5,'Side Part', 5, 'images/side_bob.png'),
(6,'Shoulder Length', 1, 'images/shoulder_layer.png'),
(7,'Curtain Bangs', 1, 'images/long_straight.png'),
(8,'Curly Lob', 2, 'images/curly_lob.png'),
(9,'Short Layered', 3, 'images/short_layered.png'),
(10,'Textured Lob', 5, 'images/textured_lob.png');

-- 7. INSERT HAIR COLOUR DATA (.png paths)
INSERT IGNORE INTO hair_colour VALUES 
(1,'Ash Blonde', 1, 'images/ash_blonde.png'),
(2,'Caramel Brown', 2, 'images/caramel.png'),
(3,'Chocolate Brown', 3, 'images/chocolate.png'),
(4,'Jet Black', 5, 'images/jet_black.png'),
(5,'Burgundy', 5, 'images/burgundy.png'),
(6,'Golden Blonde', 2, 'images/golden_blonde.png'),
(7,'Chestnut', 3, 'images/chestnut.png');

-- 8. INSERT CLOTH COLOUR DATA (.png paths)
INSERT IGNORE INTO cloth_colour VALUES 
(1,'Lavender', 1, 'images/lavender.png'),
(2,'Navy Blue', 3, 'images/royal_blue.png'),
(3,'Emerald Green', 4, 'images/emerald.png'),
(4,'Maroon', 5, 'images/maroon.png'),
(5,'Mustard Yellow', 3, 'images/mustard.png'),
(6,'Olive Green', 4, 'images/olive.png'),
(7,'Teal', 2, 'images/teal.png');