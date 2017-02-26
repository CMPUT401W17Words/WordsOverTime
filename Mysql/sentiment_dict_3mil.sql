#install mysql:
#sudo apt-get update
#sudo apt-get install mysql-server
#sudo mysql_secure_installation

#Download the csv files at: 
# http://www.ualberta.ca/~hollis/files/sentiment_dict_3mil.tgz
# http://www.ualberta.ca/~hollis/files/articles-can.tgz

#on your local computer, use this command to send the file. This is done on a windows computer with Putty installed
#ex: pscp -l username -i "C:\Path\to\key.ppk" "c:\file.foo" 199.116.235.53:file.foo
# pscp -l ubuntu -i "C:\Users\Owner\Desktop\401\putty words over time key.ppk" "C:\Users\Owner\Desktop\401\sentiment_dict_3mil.tgz" 199.116.235.53:/home/ubuntu/files/sentiment_dict_3mil.tgz
# pscp -l ubuntu -i "C:\Users\Owner\Desktop\401\putty words over time key.ppk" "C:\Users\Owner\Desktop\401\articles-can.tgz" 199.116.235.53:/home/ubuntu/files/articles-can.tgz

#following stuff is executed on the linuz machine

#Unpack the tgz with
# tar zxvf sentiment_dict_3mil.tgz
# tar zxvf articles-can.tgz

#start mysql
#mysql -u root -p




Create database Client_Generated_Data;

Create database Precalculated_Data;

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

#This command should load the file off of the system you're sshing from, but it doesn't for some reason. interent says permission issues?
#load data local infile "C:\\sentiment_dict_3mil.csv" into table Client_Generated_Data.sentiment_dict_3mil FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES (Word, Valence, Arousal, Dominance, Concreteness, AoA);

load data infile "/home/ubuntu/files/sentiment_dict_3mil.csv" into table Client_Generated_Data.sentiment_dict_3mil FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES (Word, Valence, Arousal, Dominance, Concreteness, AoA);

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

#load data local infile "C:\\articles-can.csv" into table Client_Generated_Data.articles-can FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES (articleID, language, province, city, country, publicationdate, wordcount, parsedarticle);

load data infile "/home/ubuntu/files/articles-can.csv" into table Client_Generated_Data.sentiment_dict_3mil FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES (Word, Valence, Arousal, Dominance, Concreteness, AoA);


USE Precalculated_Data;

DROP TABLE IF EXISTS Document_Data;

create table Document_Data
(
 article_ID int unsigned NOT NULL,
 language varchar(255) NOT NULL,
 province char(2) NOT NULL,
 city varchar(255) NOT NULL,
 country char(3) NOT NULL,
 publication_date date NOT NULL,
 word_count int unsigned NOT NULL,
 Length int unsigned NOT NULL,
 Word_One varchar(255) NOT NULL,
 Word_Two varchar(255) NOT NULL,
 Word_Three varchar(255) NOT NULL,
 Word_Four varchar(255) NOT NULL,
 Word_Five varchar(255) NOT NULL,
 Average_Arousal_Doc decimal(12,11) NOT NULL,
 Average_Valence_Doc decimal(12,11) NOT NULL,
 Average_Arousal_Words decimal(12,11) NOT NULL,
 Average_Valence_Words decimal(12,11) NOT NULL,

 PRIMARY KEY (article_ID)
)

DROP TABLE IF EXISTS Word_Data;

CREATE TABLE Word_Data
(
 Word varchar(255) NOT NULL,
 Article_ID int unsigned NOT NULL,
 Language varchar(255) NOT NULL,
 Province char(2) NOT NULL,
 City varchar(255) NOT NULL,
 Country char(3) NOT NULL,
 Publication_Date date NOT NULL,
 Word_Count int unsigned NOT NULL,
 Term_Frequency decimal(13,11) NOT NULL,

 PRIMARY KEY (Word, Article_ID)
);

DROP TABLE IF EXISTS Corpus_Data;

CREATE TABLE Corpus_Data
(
 corpus_ID int unsigned NOT NULL,
 Inverse_document_Frequency decimal(13,11) NOT NULL,
 Start_Date date NOT NULL,
 End_Date date NOT NULL,

 PRIMARY KEY (Word, Corpus_ID)
);