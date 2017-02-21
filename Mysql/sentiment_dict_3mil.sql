# use http://stackoverflow.com/questions/2783313/how-can-i-get-around-mysql-errcode-13-with-select-into-outfile to configure app armor

#mysql -u root -p


Create database Client_Generated_Data;

USE Client_Generated_Data;

DROP TABLE IF EXISTS sentiment_dict_3mil;

CREATE TABLE sentiment_dict_3mil
(
 Word varchar(255) NOT NULL,
 Valence decimal(12,11) NOT NULL,
 Arousal decimal(12,11) NOT NULL,
 Dominance decimal(12,11) NOT NULL,
 Concreteness decimal(12,11) NOT NULL,
 AoA decimal(13,11) NOT NULL,

 PRIMARY KEY (Word)
);

load data local infile "C:\\sentiment_dict_3mil.csv" into table Client_Generated_Data.sentiment_dict_3mil FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' (Word, Valence, Arousal, Dominance, Concreteness, AoA);


drop table if exists articles-can;

create table articles-can
(
 articleID int unsigned NOT NULL,
 language varchar(255) NOT NULL,
 province char(2) NOT NULL,
 city varchar(255) NOT NULL,
 country char(3) NOT NULL,
 publicationdate date NOT NULL,
 wordcount int unsigned NOT NULL,
 parsedarticle text NOT NULL,

 PRIMARY KEY (articleID)
)

load data local infile "C:\\articles-can.csv" into table Client_Generated_Data.articles-can FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' (articleID, language, province, city, country, publicationdate, wordcount, parsedarticle);