DROP TABLE IF EXISTS `Persons`;

CREATE TABLE Persons (
    PersonID int,
    LastName varchar(255),
    FirstName varchar(255),
    Address varchar(255),
    City varchar(255)
);


CREATE TABLE user_value (
    id varchar(200),
    first_name varchar(255),
    last_name varchar(255),
    email_address varchar(255),
    password varchar(255),
    account_created varchar(255),
    account_updated varchar(255),
    salt varchar(255)
);



CREATE TABLE bill (
    id varchar(200),
    created_ts varchar(255),
    updated_ts varchar(255),
    owner_id varchar(255),
    vendor varchar(255),
    bill_date varchar(255),
    due_date varchar(255),
    amount_due varchar(255),
    categories varchar(255),
    paymentStatus varchar(255)
);



INSERT INTO Persons
VALUES (
	1,
	"Foo",
	"Baz",
	"123 Bar Street",
	"FooBazBar City"
);
