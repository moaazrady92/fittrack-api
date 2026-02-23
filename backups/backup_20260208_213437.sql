--
-- PostgreSQL database cluster dump
--

\restrict AhM5ZqVVFvr4nNaZw2g5sYYsfJkm3w8TZJywvqHymf2u4sGNwaMUozkOwBfMY6h

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Roles
--

CREATE ROLE workoutuser;
ALTER ROLE workoutuser WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS PASSWORD 'SCRAM-SHA-256$4096:NfYlYaY4VYS/LF3i60Hngg==$a+Nnh5O3Y3p/W/fp+ziay+4qzU30Wvpy/N1TmaJYZes=:P6LEjNqxaaj6enE4okUgWA1uch6kIUVe4tQ0IBFEQUk=';

--
-- User Configurations
--








\unrestrict AhM5ZqVVFvr4nNaZw2g5sYYsfJkm3w8TZJywvqHymf2u4sGNwaMUozkOwBfMY6h

--
-- Databases
--

--
-- Database "template1" dump
--

\connect template1

--
-- PostgreSQL database dump
--

\restrict 1pJgzZcs2CDqRcIY8XzIn1Ma7xZQdCrFepXxTdfW8Ua7RViQztEtj6yfoYcVCNi

-- Dumped from database version 15.15
-- Dumped by pg_dump version 15.15

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- PostgreSQL database dump complete
--

\unrestrict 1pJgzZcs2CDqRcIY8XzIn1Ma7xZQdCrFepXxTdfW8Ua7RViQztEtj6yfoYcVCNi

--
-- Database "postgres" dump
--

\connect postgres

--
-- PostgreSQL database dump
--

\restrict j1f7EXD04pndYjS3S52wes4RtN3lQtGWAM0EjRSmmf3Ik99duxIM8fR6QsLIJzj

-- Dumped from database version 15.15
-- Dumped by pg_dump version 15.15

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- PostgreSQL database dump complete
--

\unrestrict j1f7EXD04pndYjS3S52wes4RtN3lQtGWAM0EjRSmmf3Ik99duxIM8fR6QsLIJzj

--
-- Database "workoutdb" dump
--

--
-- PostgreSQL database dump
--

\restrict 6oLvoCzxM60tesPSC8dsalREKe8g1sniuvDLjpyYAN5l58blGGeCYUbhGD3EkbC

-- Dumped from database version 15.15
-- Dumped by pg_dump version 15.15

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: workoutdb; Type: DATABASE; Schema: -; Owner: workoutuser
--

CREATE DATABASE workoutdb WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE workoutdb OWNER TO workoutuser;

\unrestrict 6oLvoCzxM60tesPSC8dsalREKe8g1sniuvDLjpyYAN5l58blGGeCYUbhGD3EkbC
\connect workoutdb
\restrict 6oLvoCzxM60tesPSC8dsalREKe8g1sniuvDLjpyYAN5l58blGGeCYUbhGD3EkbC

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: workoutdb; Type: DATABASE PROPERTIES; Schema: -; Owner: workoutuser
--

ALTER DATABASE workoutdb SET "TimeZone" TO 'UTC';
ALTER DATABASE workoutdb SET "DateStyle" TO 'ISO, DMY';


\unrestrict 6oLvoCzxM60tesPSC8dsalREKe8g1sniuvDLjpyYAN5l58blGGeCYUbhGD3EkbC
\connect workoutdb
\restrict 6oLvoCzxM60tesPSC8dsalREKe8g1sniuvDLjpyYAN5l58blGGeCYUbhGD3EkbC

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: btree_gin; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS btree_gin WITH SCHEMA public;


--
-- Name: EXTENSION btree_gin; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION btree_gin IS 'support for indexing common datatypes in GIN';


--
-- Name: pg_trgm; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pg_trgm WITH SCHEMA public;


--
-- Name: EXTENSION pg_trgm; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pg_trgm IS 'text similarity measurement and index searching based on trigrams';


--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


--
-- PostgreSQL database dump complete
--

\unrestrict 6oLvoCzxM60tesPSC8dsalREKe8g1sniuvDLjpyYAN5l58blGGeCYUbhGD3EkbC

--
-- PostgreSQL database cluster dump complete
--

