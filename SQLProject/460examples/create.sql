CREATE TABLE CatUser(
	UserID NUMBER(9),
	PhoneNum NUMBER(10),
	Password NUMBER(10),
	Email VARCHAR(20),
	primary key(UserID)
);

CREATE TABLE INDIVIDUAL(
	FirstName VARCHAR(20),
	LastName VARCHAR(20),
	DoB DATE,
	UserID NUMBER(9),
	primary key(FirstName , LastName , DoB),
	foreign key(UserID) references CatUser(UserID)
);

CREATE TABLE MERCHANDISE(
	UserID NUMBER(9),
	MID NUMBER(10),
	Section CHAR(1),
	AskingPrice NUMBER(6),
	HowOldMonth NUMBER (6),
	Description VARCHAR(100),
	primary key(UserID , MID),
	foreign key(UserID) references CatUser(UserID)
);

CREATE TABLE ADVERTISES(
	UserID NUMBER(9),
	StartingDate DATE,
	MID NUMBER(10),
	primary key(UserID , MID , StartingDate),
	foreign key(UserID) references CatUser(UserID),
	foreign key(UserID, MID) references MERCHANDISE(UserID , MID)
);

CREATE TABLE BOOK(
	UserID NUMBER(9),
	MID NUMBER(10),
	BookTitle VARCHAR(70),
	BookAuthor VARCHAR(50),
	primary key(UserID , MID),
	foreign key(UserID , MID) references MERCHANDISE(UserID , MID)
);	

insert into CatUser values(1,5204448879,354645,'bla@bla.net');
insert into CatUser values(2,4145646654,1234,'jimmy@margarita.net');
insert into CatUser values(3,5204448879,354645,'bla@bla.net');
insert into CatUser values(4,6028910043,9,'fifty@g.net');
insert into CatUser values(5,5890754,123456,'richard@cox.net');
insert into CatUser values(6,5202459593,1,'a@a.com');

insert into INDIVIDUAL values('Chris','Franklin','12-Oct-1957',4);
insert into INDIVIDUAL values('Henry','Winkler','14-Feb-1956',5);
insert into INDIVIDUAL values('Jimmy','Buffet','27-Feb-1979',2);
insert into INDIVIDUAL values('Steven','Tyler','06-Jun-1920',3);
insert into INDIVIDUAL values('Mike','Timsonite','27-Nov-1982',1);
insert into INDIVIDUAL values('a','a','01-Jan-1999',6);

insert into MERCHANDISE values(1,40,'F',15,2,'Table and Legs');
insert into MERCHANDISE values(1,44,'F',10,2,'Table');
insert into MERCHANDISE values(1,45,'F',10,2,'Table Legs');
insert into MERCHANDISE values(2,1,'B',60,80,'book set');
insert into MERCHANDISE values(2,2,'A',5000,36,'');
insert into MERCHANDISE values(2,3,'B',25,80,'book 1');
insert into MERCHANDISE values(2,4,'B',26,80,'book 2');
insert into MERCHANDISE values(2,5,'B',25,80,'book 3');
insert into MERCHANDISE values(2,6,'A',2000,80,'');
insert into MERCHANDISE values(5,20,'B',30,4,'Instruction Book');
insert into MERCHANDISE values(5,111111111,'A',20000,4,'');
 
insert into ADVERTISES values(5,'1-Oct-2005',20);
insert into ADVERTISES values(2,'30-Oct-2005',1);
insert into ADVERTISES values(2,'1-Oct-2005',2);
insert into ADVERTISES values(2,'1-Oct-2005',3);
insert into ADVERTISES values(2,'1-Oct-2005',4);
insert into ADVERTISES values(2,'1-Oct-2005',5);
insert into ADVERTISES values(2,'1-Oct-2005',6);
insert into ADVERTISES values(5,'1-Oct-2005',111111111);

insert into BOOK values(2,3,'Fundamentals of Database System','Ramez Elmasri');
insert into BOOK values(2,4,'Java 2','Pei Wei Jr.');
insert into BOOK values(2,5,'Java 4','Pei Wei');
insert into BOOK values(5,20,'How To Ride A Bike','SuperDave'); 
