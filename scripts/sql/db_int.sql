-- Création de l'utilisateur    
CREATE USER "events_tracker_appuser" WITH PASSWORD 'xxx';

-- Création de la base de données
CREATE DATABASE "events_tracker_testsdb"
WITH ENCODING 'UTF8'
LC_COLLATE = 'C.UTF-8'
LC_CTYPE = 'C.UTF-8'
TEMPLATE template0;

-- Attribution de l'utilisateur à la base de données
ALTER DATABASE "events_tracker_testsdb" OWNER TO "events_tracker_appuser";

-- Attribution des permissions à l'utilisateur
GRANT ALL PRIVILEGES ON DATABASE "events_tracker_testsdb" TO "events_tracker_appuser";
