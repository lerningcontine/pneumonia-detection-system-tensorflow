﻿create database Category;

use Category;

CREATE TABLE IF NOT EXISTS user_informations (
    user_sco VARCHAR(100) PRIMARY KEY NOT NULL,
    password VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(100),
    sex VARCHAR(100),
    number VARCHAR(100),
    insert_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO user_informations (user_sco, password, name, address, sex, number) VALUES ('123','123','顾言','重庆','男','1502333877');
INSERT INTO user_informations (user_sco, password, name, address, sex, number) VALUES ('admin','admin','忘却','广东','女','1502345177');
INSERT INTO user_informations (user_sco, password, name, address, sex, number) VALUES ('adm','adm','忘却','广东','女','1502345177');
INSERT INTO user_informations (user_sco, password, name, address, sex, number) VALUES ('ad','ad','忘却','广东','女','1502345177');


CREATE TABLE IF NOT EXISTS Cate(
    user_sco VARCHAR(100) NOT NULL,
    class VARCHAR(100),
		img_path VARCHAR(100),
    insert_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		FOREIGN KEY (user_sco) REFERENCES user_informations(user_sco)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO Cate(user_sco, class) VALUES ('2199','gg');