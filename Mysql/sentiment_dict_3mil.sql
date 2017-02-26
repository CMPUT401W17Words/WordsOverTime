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
# pscp -l ubuntu -i "C:\Users\Owner\Desktop\401\putty words over time key.ppk" "C:\Users\Owner\Desktop\401\sentiment_dict_3mil.tgz" 199.116.235.53:/mnt/D/sentiment_dict_3mil.tgz
# pscp -l ubuntu -i "C:\Users\Owner\Desktop\401\putty words over time key.ppk" "C:\Users\Owner\Desktop\401\articles-can.tgz" 199.116.235.53:/mnt/D/articles-can.tgz

#Move mysql onto the volume  http://stackoverflow.com/questions/1795176/how-to-change-mysql-data-directory
sudo /etc/init.d/mysql stop
sudo cp -R -p /var/lib/mysql /mnt/D
sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf #Look for the entry for datadir, and change the path (which should be /var/lib/mysql) to the new data directory.
sudo vim /etc/apparmor.d/tunables/alias  # Add "alias /var/lib/mysql/ -> /newpath/,"
sudo /etc/init.d/apparmor reload
sudo /etc/init.d/mysql restart

#Unpack the tgz with
# tar zxvf sentiment_dict_3mil.tgz
# tar zxvf articles-can.tgz

#start mysql with
#mysql -u root -p



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

load data local infile "/mnt/D/sentiment_dict_3mil.csv" into table Client_Generated_Data.sentiment_dict_3mil FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES (Word, Valence, Arousal, Dominance, Concreteness, AoA);

drop table if exists articles_can;

create table articles_can
(
 articleID int unsigned NOT NULL,
 language varchar(255) NOT NULL,
 province char(2) NOT NULL,
 city varchar(255) NOT NULL,
 country char(3) NOT NULL,
 publication_date date NOT NULL,
 wordcount int unsigned NOT NULL,
 parsed_article text NOT NULL,

 PRIMARY KEY (articleID)
);

load data local infile "/mnt/D/articles-can.csv" into table Client_Generated_Data.articles_can FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES (articleID, language, province, city, country, publication_date, wordcount, parsed_article);


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
 word_one varchar(255) NOT NULL,
 word_two varchar(255) NOT NULL,
 word_three varchar(255) NOT NULL,
 word_four varchar(255) NOT NULL,
 word_five varchar(255) NOT NULL,
 average_arousal_doc decimal(13,12) NOT NULL,
 average_valence_doc decimal(13,12) NOT NULL,
 average_arousal_words decimal(13,12) NOT NULL,
 average_valence_words decimal(13,12) NOT NULL,

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
 term_frequency decimal(14,12) NOT NULL,

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