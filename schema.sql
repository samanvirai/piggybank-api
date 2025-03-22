--
-- PostgreSQL database dump
--

-- Dumped from database version 15.10 (Homebrew)
-- Dumped by pg_dump version 15.11 (Homebrew)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: username
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO username;

--
-- Name: assets; Type: TABLE; Schema: public; Owner: username
--

CREATE TABLE public.assets (
    id integer NOT NULL,
    uuid uuid NOT NULL,
    name character varying,
    ticker character varying,
    logo_url character varying,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.assets OWNER TO username;

--
-- Name: assets_id_seq; Type: SEQUENCE; Schema: public; Owner: username
--

CREATE SEQUENCE public.assets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.assets_id_seq OWNER TO username;

--
-- Name: assets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: username
--

ALTER SEQUENCE public.assets_id_seq OWNED BY public.assets.id;


--
-- Name: gifts; Type: TABLE; Schema: public; Owner: username
--

CREATE TABLE public.gifts (
    id integer NOT NULL,
    uuid uuid NOT NULL,
    sent_from integer,
    sent_to integer,
    amount integer,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    asset_id integer
);


ALTER TABLE public.gifts OWNER TO username;

--
-- Name: gifts_id_seq; Type: SEQUENCE; Schema: public; Owner: username
--

CREATE SEQUENCE public.gifts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gifts_id_seq OWNER TO username;

--
-- Name: gifts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: username
--

ALTER SEQUENCE public.gifts_id_seq OWNED BY public.gifts.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: username
--

CREATE TABLE public.users (
    id integer NOT NULL,
    uuid uuid NOT NULL,
    legal_first_name character varying(50),
    legal_last_name character varying(50),
    phone_number character varying(15),
    email character varying(100),
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    password_hash character varying(256) NOT NULL,
    is_active boolean NOT NULL,
    email_verified boolean NOT NULL,
    phone_verified boolean NOT NULL,
    profile_picture character varying
);


ALTER TABLE public.users OWNER TO username;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: username
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO username;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: username
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: assets id; Type: DEFAULT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.assets ALTER COLUMN id SET DEFAULT nextval('public.assets_id_seq'::regclass);


--
-- Name: gifts id; Type: DEFAULT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.gifts ALTER COLUMN id SET DEFAULT nextval('public.gifts_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: username
--

COPY public.alembic_version (version_num) FROM stdin;
\.


--
-- Data for Name: assets; Type: TABLE DATA; Schema: public; Owner: username
--

COPY public.assets (id, uuid, name, ticker, logo_url, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: gifts; Type: TABLE DATA; Schema: public; Owner: username
--

COPY public.gifts (id, uuid, sent_from, sent_to, amount, created_at, updated_at, asset_id) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: username
--

COPY public.users (id, uuid, legal_first_name, legal_last_name, phone_number, email, created_at, updated_at, password_hash, is_active, email_verified, phone_verified, profile_picture) FROM stdin;
\.


--
-- Name: assets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: username
--

SELECT pg_catalog.setval('public.assets_id_seq', 1, false);


--
-- Name: gifts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: username
--

SELECT pg_catalog.setval('public.gifts_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: username
--

SELECT pg_catalog.setval('public.users_id_seq', 1, false);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: assets assets_pkey; Type: CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.assets
    ADD CONSTRAINT assets_pkey PRIMARY KEY (id);


--
-- Name: assets assets_uuid_key; Type: CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.assets
    ADD CONSTRAINT assets_uuid_key UNIQUE (uuid);


--
-- Name: gifts gifts_pkey; Type: CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.gifts
    ADD CONSTRAINT gifts_pkey PRIMARY KEY (id);


--
-- Name: gifts gifts_uuid_key; Type: CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.gifts
    ADD CONSTRAINT gifts_uuid_key UNIQUE (uuid);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_uuid_key; Type: CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_uuid_key UNIQUE (uuid);


--
-- Name: gifts fk_gifts_sent_from; Type: FK CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.gifts
    ADD CONSTRAINT fk_gifts_sent_from FOREIGN KEY (sent_from) REFERENCES public.users(id);


--
-- Name: gifts fk_gifts_sent_to; Type: FK CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.gifts
    ADD CONSTRAINT fk_gifts_sent_to FOREIGN KEY (sent_to) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

