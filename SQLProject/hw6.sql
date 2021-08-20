CREATE TABLE	Member(MemberID int, EmailAddress varchar(255), Name varchar(255), Location varchar(255), 
			SelfIntroduction varchar(255) NOT NULL, Birthday varchar(255) , Age int NOT NULL, PRIMARY KEY(MemberID, EmailAddress));

CREATE TABLE	Adopter(MemberType varchar(7) CHECK (MemberType in ('Adopter')), 
			MemberID int, AdoptingExperience varchar(255) NOT NULL, FOREIGN KEY(MemberID) REFERENCES Member(MemberID));

CREATE TABLE	Sender(MemberType varchar(7) CHECK (MemberType in ('Sender')), 
			MemberID int, FOREIGN KEY(MemberID) REFERENCES Member(MemberID));

CREATE TABLE	Pet(PetID int, Name varchar(255), Birthday varchar(255) NOT NULL, Age int NOT NULL, Breed varchar(1) CHECK(Breed in ('C', 'D', 'R')), 
			IsSterilized varchar(1) CHECK (IsSterilized in('Y', 'N')));

CREATE TABLE	Cat(PetID int, Name varchar(255), FOREIGN KEY(PetID) REFERENCES PetID(PetID), FOREIGN KEY(Name) REFERENCES PetID(Name));

CREATE TABLE	Dog(PetID int, Name varchar(255), DaysForWalk int CHECK(DaysForWalk between 0 and 7) NOT NULL,
			FOREIGN KEY(PetID) REFERENCES PetID(PetID), FOREIGN KEY(Name) REFERENCES PetID(Name));

CREATE TABLE	Rabbit(PetID int, Name varchar(255), BiteWire varchar(1) CHECK(BiteWire in ('Y', 'N')),
			FOREIGN KEY(PetID) REFERENCES PetID(PetID), FOREIGN KEY(Name) REFERENCES PetID(Name));

CREATE TABLE	Message(ID int PRIMARY KEY, PostingTime varchar(255) NOT NULL);

CREATE TABLE	Op(UserType varchar(2) CHECK (UserType in('Op')) PRIMARY KEY, ID int, MemberID int, Content varchar(1000) NOT NULL, 
			FOREIGN KEY(ID) REFERENCES Message(ID), FOREIGN KEY(MemberID) REFERENCES Member);

CREATE TABLE	Reply(UserType varchar(5) CHECK (UserType in ('Reply')) PRIMARY KEY, ID int, MemberID int, Repliy varchar(1000) NOT NULL,
			FOREIGN KEY(ID) REFERENCES Message(ID), FOREIGN KEY(MemberID) REFERENCES Member);

CREATE TABLE	Link(ID, FOREIGN KEY(ID) REFERENCES Message(ID));

CREATE TABLE 	Favorite(MemberID int, Favorite int,
			FOREIGN KEY(MemberID) REFERENCES Member(MemberID), FOREIGN KEY(Favorite) REFERENCES Pet(PetID));

CREATE TABLE	Chat(MemberID int, ID int, FOREIGN KEY(MemberID) REFERENCES Member, FOREIGN KEY(ID) REFERENCES Message);

CREATE TABLE	Has(MemberID int, PetID, FOREIGN KEY(MemberID) REFERENCES Member, FOREIGN KEY(PetID) REFERENCES Pet(PetID)); 

INSERT INTO	Member(MemberID, EmailAddress, Name, SelfIntroduction, Age) VALUES (1, 'cephy@email.arizona.edu', 'Saul', 'I like Cats.', 22);
INSERT INTO	Member(MemberID, EmailAddress, Name, SelfIntroduction, Age) VALUES (2, 'jacky@email.arizona.edu', 'Jacky', 'I like dogs.', 30);
INSERT INTO	Member(MemberID, EmailAddress, Name, SelfIntroduction, Age) VALUES (3, 'nate@email.arizona.edu', 'Nate', 'I like this site.', 20);
INSERT INTO	Member(MemberID, EmailAddress, Name, SelfIntroduction, Age) VALUES (4, 'dave@email.arizona.edu', 'Dave', 'I like all pets.', 25);
INSERT INTO	Member(MemberID, EmailAddress, Name, SelfIntroduction, Age) VALUES (5, 'steve@email.arizona.edu', 'Steve', 'I like adopting pets!.', 19);
INSERT INTO	Member(MemberID, EmailAddress, Name, SelfIntroduction, Age) VALUES (6, 'andrew.arizona.edu', 'Andrew', 'Greetings.', 35);
INSERT INTO	Member(MemberID, EmailAddress, Name, SelfIntroduction, Age) VALUES (7, 'rick.arizona.edu', 'Rick', 'What is popping?.', 28);
INSERT INTO	Member(MemberID, EmailAddress, Name, SelfIntroduction, Age) VALUES (8, 'peter@email.arizona.edu', 'Peter', 'Hello to everyone!', 36);
INSERT INTO	Member(MemberID, EmailAddress, Name, SelfIntroduction, Age) VALUES (9, 'zack@email.arizona.edu', 'Zack', 'I love dogs.', 38);
INSERT INTO	Member(MemberID, EmailAddress, Name, SelfIntroduction, Age) VALUES (10, 'robert@email.arizona.edu', 'Robert', 'Hi.', 40);

INSERT INTO	Adopter(MemberType, MemberID, AdoptingExperience) VALUES ('Adopter', 1, 'It was good');
INSERT INTO	Adopter(MemberType, MemberID, AdoptingExperience) VALUES ('Adopter', 2, 'It was fast and easy!');
INSERT INTO	Adopter(MemberType, MemberID, AdoptingExperience) VALUES ('Adopter', 3, 'Nothing too bad. Everything worked find during the process');
INSERT INTO	Adopter(MemberType, MemberID, AdoptingExperience) VALUES ('Adopter', 4, 'It was fun!');
INSERT INTO	Adopter(MemberType, MemberID, AdoptingExperience) VALUES ('Adopter', 5, 'Easy!');

INSERT INTO	Sender(MemberType, MemberID) VALUES ('Sender', 6);
INSERT INTO	Sender(MemberType, MemberID) VALUES ('Sender', 7);
INSERT INTO	Sender(MemberType, MemberID) VALUES ('Sender', 8);
INSERT INTO	Sender(MemberType, MemberID) VALUES ('Sender', 9);
INSERT INTO	Sender(MemberType, MemberID) VALUES ('Sender', 10);

INSERT INTO	Pet(PetID, Name, Birthday, Age, Breed, IsSterilized) VALUES (100, 'Derpy', '10/11/21', 2, 'C', 'Y');
INSERT INTO	Pet(PetID, Name, Birthday, Age, Breed, IsSterilized) VALUES (101, 'Cat', '10/11/21', 3, 'C', 'N');
INSERT INTO	Pet(PetID, Name, Birthday, Age, Breed, IsSterilized) VALUES (102, 'Jade', '10/11/21', 5, 'C', 'Y');
INSERT INTO	Pet(PetID, Name, Birthday, Age, Breed, IsSterilized) VALUES (103, 'Mew', '08/30/20', 1, 'C', 'N');
INSERT INTO	Pet(PetID, Name, Birthday, Age, Breed, IsSterilized) VALUES (104, 'Shay', '09/07/20', 1, 'C', 'N');

INSERT INTO	Pet(PetID, Birthday, Name, Age, Breed, IsSterilized) VALUES (105, '10/11/21','Rocko', 3, 'D', 'N');
INSERT INTO	Pet(PetID, Birthday, Name, Age, Breed, IsSterilized) VALUES (106, '05/22/20','Choco', 1, 'D', 'Y');

INSERT INTO	Pet(PetID, Birthday, Name, Age, Breed, IsSterilized) VALUES (107, '10/11/21','Rabby', 5, 'R', 'N');
INSERT INTO	Pet(PetID, Birthday, Name, Age, Breed, IsSterilized) VALUES (108, '05/22/20','Jumper', 1, 'R', 'N');


INSERT INTO	Cat(PetID, Name) VALUES (100, 'Derpy');
INSERT INTO	Cat(PetID, Name) VALUES (101, 'Cat');
INSERT INTO	Cat(PetID, Name) VALUES (102, 'Jade');
INSERT INTO	Cat(PetID, Name) VALUES (103, 'Mew');
INSERT INTO	Cat(PetID, Name) VALUES (104, 'Shay');

INSERT INTO	Dog(PetID, Name, DaysForWalk) VALUES (105, 'Rocko', 7);
INSERT INTO	Dog(PetID, Name, DaysForWalk) VALUES (106, 'Choco', 5);

INSERT INTO	Rabbit(PetID, Name, BiteWire) VALUES (107, 'Rabby', 'Y');
INSERT INTO	Rabbit(PetID, Name, BiteWire) VALUES (108, 'Jumper', 'Y');

INSERT INTO	Favorite(MemberID, Favorite) VALUES (1, 100);
INSERT INTO	Favorite(MemberID, Favorite) VALUES (2, 100);
INSERT INTO	Favorite(MemberID, Favorite) VALUES (3, 100);
INSERT INTO	Favorite(MemberID, Favorite) VALUES (4, 100);
INSERT INTO	Favorite(MemberID, Favorite) VALUES (1, 100);

SELECT		Member.name, Member.MemberID, Favorite.Favorite
FROM		Member, Adopter, Sender, Favorite
WHERE		Favorite.MemberID = Member.MemberID AND Favorite.Favorite = 100
GROUP BY	Member.MemberID
ORDER BY	Member.MemberID DESC;

SELECT		Pet.PetID, Pet.Age, Pet.Name, Pet.Breed
FROM		Pet, Cat
WHERE		Pet.PetID > 0 AND Pet.IsSterilized = 'Y' AND Pet.breed = 'C'
GROUP BY	Pet.PetID
HAVING COUNT 	(Cat.petid) < 10;

DROP TABLE	Member;
DROP TABLE	Adopter;
DROP TABLE	Sender;
DROP TABLE	Pet;
DROP TABLE	Cat;
DROP TABLE	Dog;
DROP TABLE	Rabbit;
DROP TABLE	Message;
DROP TABLE	Op;
DROP TABLE	Reply;
DROP TABLE	Link;
DROP TABLE	Favorite;
DROP TABLE	Chat;
DROP TABLE	Has;






