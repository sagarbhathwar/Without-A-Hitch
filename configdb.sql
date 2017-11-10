DROP DATABASE withoutahitch;
CREATE DATABASE withoutahitch;

CREATE USER team7 WITH PASSWORD 'password';

ALTER ROLE team7 SET client_encoding TO 'utf8';
ALTER ROLE team7 SET default_transaction_isolation TO 'read committed';
ALTER ROLE team7 SET timezone TO 'Asia/Kolkata';

GRANT ALL PRIVILEGES ON DATABASE withoutahitch TO team7;


