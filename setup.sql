CREATE DATABASE tandora;
CREATE USER tandorauser WITH PASSWORD 'somepassword';
ALTER ROLE tandorauser SET client_encoding TO 'utf8';
ALTER ROLE tandorauser SET default_transaction_isolation TO 'read committed';
ALTER ROLE tandorauser SET timezone TO 'UTC';
ALTER USER tandorauser CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE tandora TO tandorauser;
