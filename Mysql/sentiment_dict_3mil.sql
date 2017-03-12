#attach volume with cybera https://docs.google.com/document/d/12_iH7oFfP2MTBi7wCR92PiIalhsB8i2bcz2G89wUsmk/edit#
#Format the volume:
#	$ sudo mkfs.ext4 /dev/sdc
#Note: attached volumes will typically be assigned device names in sequential order (i.e. /dev/sdc, /dev/sdd, /dev/sde, etc.) List all disks from within the instance with 
#$ sudo fdisk -l. /dev/sda and /dev/sdb are the system volumes that make up the instance.
#Create a mount point for the volume:
#	$ sudo mkdir /mnt/<mount_point_name>
#Mount the volume device to the mount point:
#$ sudo mount /dev/sdc /mnt/<mount_point_name>
#Permissions may need to be changed on the new volume, as they are initially set to root:
#	$ sudo chown ubuntu:ubuntu /mnt/<mount_point_name>

#install mysql:
#sudo apt-get update
#sudo apt-get install mysql-server
#sudo mysql_secure_installation

#Download the csv files at: 
# http://www.ualberta.ca/~hollis/files/sentiment_dict_3mil.tgz
# http://www.ualberta.ca/~hollis/files/articles-can.tgz
#wget is linux's command to download, but it wouldn't work for me

#on your local computer, use this command to send the file. This is done on a windows computer with Putty installed
#ex: pscp -l username -i "C:\Path\to\key.ppk" "c:\file.foo" 199.116.235.53:file.foo
# pscp -l ubuntu -i "C:\Users\Owner\Desktop\401\demo-server-key.ppk" "C:\Users\Owner\Desktop\401\sentiment_dict_3mil.tgz" 199.116.235.204:/mnt/vol/sentiment_dict_3mil.tgz
# pscp -l ubuntu -i "C:\Users\Owner\Desktop\401\demo-server-key.ppk" "C:\Users\Owner\Desktop\401\articles-can.tgz" 199.116.235.204:/mnt/vol/articles-can.tgz

#Move mysql onto the volume  http://stackoverflow.com/questions/1795176/how-to-change-mysql-data-directory
#sudo /etc/init.d/mysql stop
#sudo cp -R -p /var/lib/mysql /mnt/vol
#sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf #Look for the entry for datadir, and change the path (which should be /var/lib/mysql) to the new data directory.
#sudo vim /etc/apparmor.d/tunables/alias  # Add "alias /var/lib/mysql/ -> /newpath/," Note the comma
#sudo /etc/init.d/apparmor reload
#sudo /etc/init.d/mysql restart

#Unpack the tgz with
# tar zxvf sentiment_dict_3mil.tgz
# tar zxvf articles-can.tgz

#start mysql with
#mysql -u root -p

# run this with 'SOURCE /path/to/precalculated.sql'

Create database Client_Generated_Data;

Create database Precalculated_Data;

USE Client_Generated_Data;

DROP TABLE IF EXISTS sentiment_dict_3mil;

CREATE TABLE sentiment_dict_3mil
(
 Word varchar(255) NOT NULL,
 Valence decimal(15,13) NOT NULL,
 Arousal decimal(15,13) NOT NULL,
 Dominance decimal(15,13) NOT NULL,
 Concreteness decimal(15,13) NOT NULL,
 AoA decimal(15,13) NOT NULL,

 PRIMARY KEY (Word)
);

load data local infile "/mnt/vol/sentiment_dict_3mil.csv" into table Client_Generated_Data.sentiment_dict_3mil FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES (Word, Valence, Arousal, Dominance, Concreteness, AoA);

drop table if exists articles_can;

create table articles_can
(
 id int unsigned NOT NULL auto_increment,
 articleID int unsigned NOT NULL,
 language varchar(255) NOT NULL,
 province char(2) NOT NULL,
 city varchar(255) NOT NULL,
 country char(3) NOT NULL,
 publication_date date NOT NULL,
 wordcount int unsigned NOT NULL,
 parsed_article text NOT NULL,

 PRIMARY KEY (id)
);

load data local infile "/mnt/vol/articles-can.csv" into table Client_Generated_Data.articles_can FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES (articleID, language, province, city, country, publication_date, wordcount, parsed_article);


USE Precalculated_Data;

DROP TABLE IF EXISTS Document_Data;

create table Document_Data
(
 articleID int unsigned NOT NULL,
 language varchar(255) NOT NULL,
 province char(2) NOT NULL,
 city varchar(255) NOT NULL,
 country char(3) NOT NULL,
 publication_date date NOT NULL,
 word_count int unsigned NOT NULL,
 word_one varchar(255) default '',
 word_two varchar(255) default '',
 word_three varchar(255) default '',
 word_four varchar(255) default '',
 word_five varchar(255) default '',
 average_arousal_doc decimal(13,12) NOT NULL,
 average_valence_doc decimal(13,12) NOT NULL,
 average_arousal_words decimal(13,12),
 average_valence_words decimal(13,12),

 PRIMARY KEY (articleID)
);

DROP TABLE IF EXISTS Word_Data;

CREATE TABLE Word_Data
(
 word varchar(255) NOT NULL,
 articleID int unsigned NOT NULL,
 language varchar(255) NOT NULL,
 Province char(2) NOT NULL,
 city varchar(255) NOT NULL,
 country char(3) NOT NULL,
 publication_Date date NOT NULL,
 word_count int unsigned NOT NULL,
 term_frequency decimal(14,12), # log(word count / document word count)

 PRIMARY KEY (Word, articleID)
);


DROP TABLE IF EXISTS Corpus_Data;

CREATE TABLE Corpus_Data
(
 corpusID int unsigned NOT NULL,
 inverse_document_Frequency decimal(14,12) NOT NULL,
 start_date date NOT NULL,
 end_date date NOT NULL,

 PRIMARY KEY (CorpusID)
);


#below is the extremely slow function to calculate document and word data from the client data. Takes about a minute a document...

DROP PROCEDURE IF EXISTS wordperword;
DELIMITER ;;

CREATE PROCEDURE wordperword(articleIDpassed int) #pulls words from a text
BEGIN
DECLARE n INT DEFAULT 0;
DECLARE i INT DEFAULT 0;
SELECT wordcount FROM Client_Generated_Data.articles_can where articleID = articleIDpassed INTO n;
SET i=0;
SET n=N*2;
WHILE i<n DO 
  insert into Temp_word_data (word, articleID) #pulls 'i'th word from specificed record  http://stackoverflow.com/questions/4538259/how-can-i-split-up-a-string-field-sentence-into-words-and-insert-them-into-a-new
  select replace(substring(substring_index(Client_Generated_Data.articles_can.parsed_article, ' ', i+1), 
   length(substring_index(Client_Generated_Data.articles_can.parsed_article, ' ', i)) + 1), ' ', ''), Client_Generated_Data.articles_can.articleID as item1
   from Client_Generated_Data.articles_can
   where ID = articleIDpassed
   having item1 <> '';
  SET i = i + 1;
END WHILE;
DELETE FROM Temp_word_data WHERE word ='';
End;
;;

DELIMITER ;


DROP PROCEDURE IF EXISTS worddatafirst; #http://stackoverflow.com/questions/5817395/how-can-i-loop-through-all-rows-of-a-table-mysql
DELIMITER ;;

CREATE PROCEDURE worddatafirst()
BEGIN
DECLARE n INT DEFAULT 0;
DECLARE i INT DEFAULT 0;
SELECT COUNT(*) FROM Temp_word_data INTO n;
SET i=0;
WHILE i<n DO 
INSERT INTO Word_Data (word, articleID, language, province, city, country, publication_date, word_count)
 select 
   Temp_word_data.word, 
   Temp_word_data.articleID,  
   Client_Generated_Data.articles_can.language, 
   Client_Generated_Data.articles_can.province, 
   Client_Generated_Data.articles_can.city, 
   Client_Generated_Data.articles_can.country, 
   Client_Generated_Data.articles_can.publication_date,
   1
 from Temp_word_data, Client_Generated_Data.articles_can
 where Temp_word_data.id = i and Client_Generated_Data.articles_can.articleID = Temp_word_data.articleID
 on duplicate key update word_count = word_count + 1;
  SET i = i + 1;
END WHILE;
End;
;;

DELIMITER ;

#http://stackoverflow.com/questions/5817395/how-can-i-loop-through-all-rows-of-a-table-mysql
#above link provided structural code

DROP PROCEDURE IF EXISTS ROWPERROW; 
DELIMITER ;;

CREATE PROCEDURE ROWPERROW()
BEGIN
DECLARE m INT DEFAULT 100;
DECLARE j INT DEFAULT 0;
SELECT COUNT(*) FROM Client_Generated_Data.articles_can INTO m;
#SET m=100;
SET j=0;
WHILE j<m DO 
  
DROP TABLE IF EXISTS Temp_word_data;

CREATE TABLE Temp_word_data
(
 id int unsigned NOT NULL auto_increment,
 articleID int unsigned NOT NULL,
 word varchar(255) NOT NULL,
 valence decimal(15,13),
 arousal decimal(15,13),
 dominance decimal(15,13),
 concreteness decimal(15,13),
 aoa decimal(15,13),

 PRIMARY KEY (id)
);

CALL wordperword(j);

UPDATE Temp_word_data
   INNER JOIN  Client_Generated_Data.sentiment_dict_3mil ON Temp_word_data.word = Client_Generated_Data.sentiment_dict_3mil.word
   SET Temp_word_data.valence = Client_Generated_Data.sentiment_dict_3mil.valence, 
     Temp_word_data.arousal  = Client_Generated_Data.sentiment_dict_3mil.arousal, 
     Temp_word_data.dominance = Client_Generated_Data.sentiment_dict_3mil.dominance, 
     Temp_word_data.concreteness = Client_Generated_Data.sentiment_dict_3mil.concreteness, 
     Temp_word_data.aoa = Client_Generated_Data.sentiment_dict_3mil.aoa;

call worddatafirst();

update Word_Data W, 
  (SELECT COUNT(*) as count FROM Temp_word_data) as C  
  set W.term_frequency = log10(W.word_count/C.count);

INSERT INTO Document_Data (articleID, language, province, city, country, publication_date, word_count, average_arousal_doc, average_valence_doc)
  SELECT
   Client_Generated_Data.articles_can.articleID,
   Client_Generated_Data.articles_can.language, 
   Client_Generated_Data.articles_can.province, 
   Client_Generated_Data.articles_can.city, 
   Client_Generated_Data.articles_can.country, 
   Client_Generated_Data.articles_can.publication_date,
   (select COUNT(*) FROM Temp_word_data) as count,
   (select sum(Temp_word_data.arousal) from Temp_word_data) / (select count),
   (select sum(Temp_word_data.valence) from Temp_word_data) / (select count)
  from Client_Generated_Data.articles_can, Temp_word_data
  where Temp_word_data.id = 1 and Client_Generated_Data.articles_can.articleID = Temp_word_data.articleID;


  SET j = j + 1;
END WHILE;
End;
;;

DELIMITER ;

call rowperrow();


#for each document if word in allwords in document then add to count
#select count(*) from Word_Data where word = X and articleID = Y;
# total documents / num docs containing word

DROP PROCEDURE IF EXISTS IDFCALC; 
DELIMITER ;;

CREATE PROCEDURE IDFCALC()
BEGIN
  DECLARE cursor_ID INT;
  DECLARE cursor_VAL VARCHAR;
  DECLARE done INT DEFAULT FALSE;
  DECLARE cursor_i CURSOR FOR SELECT ID,VAL FROM table_A;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
  OPEN cursor_i;
  read_loop: LOOP
    FETCH cursor_i INTO cursor_ID, cursor_VAL;
    IF done THEN
      LEAVE read_loop;
    END IF;
    INSERT INTO table_B(ID, VAL) VALUES(cursor_ID, cursor_VAL);
  END LOOP;
  CLOSE cursor_i;
END;
;;


CREATE USER darcyprojectuser@localhost IDENTIFIED BY '12345';
GRANT ALL PRIVILEGES ON Client_Generated_Data.* TO darcyprojectuser@localhost;
GRANT ALL PRIVILEGES ON Precalculated_Data.* TO darcyprojectuser@localhost;
FLUSH PRIVILEGES;
