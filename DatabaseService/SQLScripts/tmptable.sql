create table trend (id SERIAL, InvoiceNo varchar(20), StockCode varchar(20), Description varchar(50), Quantity varchar(20), InvoiceDate varchar(20), UnitPrice varchar(20), CustomerID varchar(20), Country varchar(20),userid varchar(20));

	grant all privileges on database sales to docker;

	ALTER ROLE "docker" WITH LOGIN;

	GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO docker;

	GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO docker;

	INSERT INTO trend (userid,InvoiceNo,StockCode,Description,Quantity,InvoiceDate,UnitPrice,CustomerID,Country) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)