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

insert into sentiment_dict_3mil ( Word, Valence, Arousal, Dominance, Concreteness, AoA) Values ( "Allanah_Munsun", 0.56058281834, 0.425037156176, 0.52818428423, 0.589157272835, 9.69062278082 ), ("WINDS_WILL",0.333449219993,0.350146763467,0.409175708194,0.435814704683,17.4777314468);

select * from sentiment_dict_3mil;

"C:\Users\Owner\Desktop\401\sentiment_dict_3mil.csv"