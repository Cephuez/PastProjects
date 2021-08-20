INSERT INTO Member(EmailAddress, Name, SelfIntroduction, Location, Birthday, IsAdopter, IsSender, AdoptingExperience)
VALUES ('catlover42@gmail.com', 'Richard', 'My name is Richard Johnson', 'Tucson, Arizona', TO_DATE('071187', 'MMDDYY'), 'y', 'n', NULL);

INSERT INTO Member(EmailAddress, Name, SelfIntroduction, Location, Birthday, IsAdopter, IsSender, AdoptingExperience)
VALUES ('sadiek@gmail.com', 'Sadie', 'My name is Sadie Keesler', 'Tucson, Arizona', TO_DATE('101497', 'MMDDYY'), 'y', 'n', NULL );

INSERT INTO Member(EmailAddress, Name, SelfIntroduction, Location, Birthday, IsAdopter, IsSender, AdoptingExperience)
VALUES('reneeB@gmail.com', 'Renee',  'My name is Renee Bollinger', 'Phoenix, Arizona', TO_DATE('091267', 'MMDDYY'), 'y', 'n', NULL);

INSERT INTO Member(EmailAddress, Name, SelfIntroduction, Location, Birthday, IsAdopter, IsSender, AdoptingExperience)
VALUES ('ddavis@gmail.com', 'Derek', 'My name is Derek', 'Tucson, Arizona', TO_DATE('010395', 'MMDDYY'), 'n', 'y', NULL);

INSERT INTO Member(EmailAddress, Name, SelfIntroduction, Location, Birthday, IsAdopter, IsSender, AdoptingExperience)
VALUES ('ashWhite@gmail.com', 'Ash White', 'My name is Ash', 'Wilcox, Arizona', TO_DATE('040696', 'MMDDYY'), 'n', 'y', NULL);

INSERT INTO Pet(EmailAddress, Name, Birthday, IsSterilized, Breed, DaysWalk, BiteWire)
VALUES ('ddavis@gmail.com', 'Spot', TO_DATE('101415', 'MMDDYY'), 'y', 'Dog', 2, NULL);

INSERT INTO Pet(EmailAddress, Name, Birthday, IsSterilized, Breed, DaysWalk, BiteWire)
VALUES ('ddavis@gmail.com', 'Kittles', TO_DATE('101413', 'MMDDYY'), 'y', 'Cat', NULL, NULL);

INSERT INTO Pet(EmailAddress, Name, Birthday, IsSterilized, Breed, DaysWalk, BiteWire)
VALUES ('ashWhite@gmail.com', 'Garf', TO_DATE('101415', 'MMDDYY'), 'y', 'Cat', NULL, NULL);

INSERT INTO Favorite(EmailAddressMember, EmailAddressPet, PetName, Birthday)
VALUES ('ddavis@gmail.com', 'ddavis@gmail.com', 'Spot', TO_DATE('101415', 'MMDDYY'));

INSERT INTO Favorite(EmailAddressMember, EmailAddressPet, PetName, Birthday)
VALUES ('catlover42@gmail.com', 'ddavis@gmail.com', 'Kittles', TO_DATE('101413', 'MMDDYY'));

INSERT INTO Favorite(EmailAddressMember, EmailAddressPet, PetName, Birthday)
VALUES ('catlover42@gmail.com', 'ashWhite@gmail.com', 'Garf', TO_DATE('101415', 'MMDDYY'));

INSERT INTO Favorite(EmailAddressMember, EmailAddressPet, PetName, Birthday)
VALUES ('sadiek@gmail.com', 'ashWhite@gmail.com', 'Garf', TO_DATE('101415', 'MMDDYY'));

INSERT INTO Favorite(EmailAddressMember, EmailAddressPet, PetName, Birthday)
VALUES ('sadiek@gmail.com', 'ddavis@gmail.com', 'Kittles', TO_DATE('101413', 'MMDDYY'));

INSERT INTO Favorite(EmailAddressMember, EmailAddressPet, PetName, Birthday)
VALUES ('reneeB@gmail.com', 'ddavis@gmail.com', 'Kittles', TO_DATE('101413', 'MMDDYY'));