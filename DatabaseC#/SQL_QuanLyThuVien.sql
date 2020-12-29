create database ManageLibrary
go 
use ManageLibrary
create table BookShelf(
bookShelfID varchar(5) not null,
bookShelfName varchar(50) not null,
)

alter table BookShelf add constraint PK_bookShelfID primary key (bookShelfID)

create table Book(
bookID varchar(5) not null,
bookName varchar(50) not null,
kind varchar(50) not null,
publisherID varchar(10),
bookShelfID varchar(5) not null,
timeInput datetime,
fettle varchar(50)
)
alter table Book add constraint PK_bookID primary key (bookID)
alter table Book add constraint FK_bookShelfID Foreign key(bookShelfID) references BookShelf(bookShelfID)

insert into BookShelf(bookShelfID,bookShelfName)
values ('A','Science Fiction'),
('B','Foreign Language'),
('C','Psychology'),
('D','Comics'),
('E','Action & Adventure'),
('F','Romance'),
('G','Horror'),
('H','Poetry'),
('I','History')

insert into Book(bookID,bookName,kind,publisherID,bookShelfID,timeInput,fettle)
values('C12','Physiology for Dummies','Psychology','USA','C','2019/01/01',null),
('A10','The Time Machine','Science Fiction','NYT','A','2018/09/01',null),
('F15','The Fault in Our Stars','Romance','NYT','F','2018/09/01',null),
('I15','WAR II','History','EUP','I','2019/05/01','Book is lent'),
('B15','How to learn English ?','Foreign Language','NXB','B','2019/02/22',null),
('G15','Insidious','Horror','NXB','G','2019/03/22','Book is lent')

insert into Book(bookID,bookName,kind,publisherID,bookShelfID,timeInput,fettle)
values('C13','Physiology for BRAIN','Psychology','USA','C','2019/01/01',null),
('A11','The Time Machine II','Science Fiction','NYT','A','2018/09/01',null),
('F16','The Fault in Our Stars II','Romance','NYT','F','2018/09/01',null),
('I14','WAR I','History','EUP','I','2019/05/01','Book is lent'),
('B16','How to learn Vietnamese ?','Foreign Language','NXB','B','2019/02/22',null),
('G16','Insidious I','Horror','NXB','G','2019/03/22','Book is lent')
