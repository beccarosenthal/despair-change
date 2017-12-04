--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.10
-- Dumped by pg_dump version 9.5.10

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- Name: statuses; Type: TYPE; Schema: public; Owner: user
--

CREATE TYPE statuses AS ENUM (
    'donation attempted',
    'payment object built',
    'paypal payment instantiated',
    'Invalid request',
    'payment failed',
    'payment succeeded',
    'pending delivery to org',
    'delivered to org'
);


ALTER TYPE statuses OWNER TO "user";

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: organizations; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE organizations (
    org_id integer NOT NULL,
    name character varying(100) NOT NULL,
    payee_email character varying(100) NOT NULL,
    logo_url character varying(200),
    mission_statement text,
    website_url character varying(200),
    has_chapters boolean,
    twitter_url character varying(200),
    short_name character varying(30)
);


ALTER TABLE organizations OWNER TO "user";

--
-- Name: organizations_org_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE organizations_org_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE organizations_org_id_seq OWNER TO "user";

--
-- Name: organizations_org_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE organizations_org_id_seq OWNED BY organizations.org_id;


--
-- Name: referrals; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE referrals (
    ref_id integer NOT NULL,
    referrer_id integer NOT NULL,
    referred_id integer NOT NULL
);


ALTER TABLE referrals OWNER TO "user";

--
-- Name: referrals_ref_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE referrals_ref_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE referrals_ref_id_seq OWNER TO "user";

--
-- Name: referrals_ref_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE referrals_ref_id_seq OWNED BY referrals.ref_id;


--
-- Name: states; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE states (
    code character varying(4) NOT NULL,
    name character varying(40) NOT NULL
);


ALTER TABLE states OWNER TO "user";

--
-- Name: transactions; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE transactions (
    transaction_id integer NOT NULL,
    org_id integer NOT NULL,
    user_id integer NOT NULL,
    payment_id character varying(40) NOT NULL,
    amount double precision NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    status statuses NOT NULL
);


ALTER TABLE transactions OWNER TO "user";

--
-- Name: transactions_transaction_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE transactions_transaction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE transactions_transaction_id_seq OWNER TO "user";

--
-- Name: transactions_transaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE transactions_transaction_id_seq OWNED BY transactions.transaction_id;


--
-- Name: user_orgs; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE user_orgs (
    user_org_id integer NOT NULL,
    user_id integer NOT NULL,
    org_id integer NOT NULL,
    rank integer
);


ALTER TABLE user_orgs OWNER TO "user";

--
-- Name: user_orgs_user_org_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE user_orgs_user_org_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE user_orgs_user_org_id_seq OWNER TO "user";

--
-- Name: user_orgs_user_org_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE user_orgs_user_org_id_seq OWNED BY user_orgs.user_org_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE users (
    user_id integer NOT NULL,
    user_email character varying(64) NOT NULL,
    password character varying(150) NOT NULL,
    fname character varying(15) NOT NULL,
    lname character varying(30) NOT NULL,
    age integer,
    zipcode character varying(5),
    state_code character varying(4),
    default_amount double precision NOT NULL,
    phone character varying(15),
    created_at timestamp without time zone NOT NULL,
    last_login timestamp without time zone NOT NULL,
    set_password boolean DEFAULT true
);


ALTER TABLE users OWNER TO "user";

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_user_id_seq OWNER TO "user";

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE users_user_id_seq OWNED BY users.user_id;


--
-- Name: org_id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY organizations ALTER COLUMN org_id SET DEFAULT nextval('organizations_org_id_seq'::regclass);


--
-- Name: ref_id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY referrals ALTER COLUMN ref_id SET DEFAULT nextval('referrals_ref_id_seq'::regclass);


--
-- Name: transaction_id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY transactions ALTER COLUMN transaction_id SET DEFAULT nextval('transactions_transaction_id_seq'::regclass);


--
-- Name: user_org_id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY user_orgs ALTER COLUMN user_org_id SET DEFAULT nextval('user_orgs_user_org_id_seq'::regclass);


--
-- Name: user_id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY users ALTER COLUMN user_id SET DEFAULT nextval('users_user_id_seq'::regclass);


--
-- Data for Name: organizations; Type: TABLE DATA; Schema: public; Owner: user
--

COPY organizations (org_id, name, payee_email, logo_url, mission_statement, website_url, has_chapters, twitter_url, short_name) FROM stdin;
8	Institute of Finishing Projects	beccarosenthal-facilitator@gmail.com	https://media.makeameme.org/created/how-about-getting.jpg	At the Institute of Finishing Projects, we finish proje	http://www.pawneeindiana.com/	f	\N	\N
9	Rent-A-Swag	beccarosenthal-facilitator-1@gmail.com	https://ih1.redbubble.net/image.294685880.6679/flat,800x800,075,f.jpg	At Rent-A-Swag, we bring you the dopest shirts, the swankiest jackets, the slickest cardigans, the flashiest fedoras, the hottest ties, the snazziest canes and more!	http://parksandrecreation.wikia.com/wiki/Rent-A-Swag	f	\N	\N
13	Alternative US National Parks Service	altnps@gmail.com	http://bit.ly/2ySo6D7	45 messed with the wrong set of vested park rangers.	https://twitter.com/altnatparkser?lang=en	f	\N	\N
15	The Derek Zoolander Center For Kids Who Can't Read Good And Wanna Learn To Do Other Stuff Good Too	readingcenter@gmail.com	http://bit.ly/2iq2LuI	We teach you that there's more to life than being really, really good looking	https://dzssite.wordpress.com/	f	\N	\N
16	Alt ACLU	altaclu@gmail.com	http://bit.ly/2hMlwex	An organization that strives to achieve all of the goals of the ACLU with none of the resources.	http://ortho.ucla.edu/sports-medicine	t	\N	\N
\.


--
-- Name: organizations_org_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('organizations_org_id_seq', 16, true);


--
-- Data for Name: referrals; Type: TABLE DATA; Schema: public; Owner: user
--

COPY referrals (ref_id, referrer_id, referred_id) FROM stdin;
1	16	17
2	16	22
3	22	15
4	15	23
9	23	30
10	20	31
11	23	32
12	16	33
\.


--
-- Name: referrals_ref_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('referrals_ref_id_seq', 12, true);


--
-- Data for Name: states; Type: TABLE DATA; Schema: public; Owner: user
--

COPY states (code, name) FROM stdin;
AK	Alaska\n
AZ	Arizona\n
AR	Arkansas\n
CA	California\n
CO	Colorado\n
CT	Connecticut\n
DE	Delaware\n
DC	District of Columbia\n
FL	Florida\n
GA	Georgia\n
HI	Hawaii\n
ID	Idaho\n
IL	Illinois\n
IN	Indiana\n
IA	Iowa\n
KS	Kansas\n
KY	Kentucky\n
LA	Louisiana\n
ME	Maine\n
MD	Maryland\n
MA	Massachusetts\n
MI	Michigan\n
MN	Minnesota\n
MS	Mississippi\n
MO	Missouri\n
MT	Montana\n
NE	Nebraska\n
NV	Nevada\n
NH	New Hampshire\n
NJ	New Jersey\n
NM	New Mexico\n
NY	New York\n
NC	North Carolina\n
ND	North Dakota\n
OH	Ohio\n
OK	Oklahoma\n
OR	Oregon\n
PA	Pennsylvania\n
PR	Puerto Rico\n
RI	Rhode Island\n
SC	South Carolina\n
SD	South Dakota\n
TN	Tennessee\n
TX	Texas\n
UT	Utah\n
VT	Vermont\n
VA	Virginia\n
WA	Washington\n
WV	West Virginia\n
WI	Wisconsin\n
WY	Wyoming\n
\.


--
-- Data for Name: transactions; Type: TABLE DATA; Schema: public; Owner: user
--

COPY transactions (transaction_id, org_id, user_id, payment_id, amount, "timestamp", status) FROM stdin;
144	13	31	PAY-7WG94077XF457050DLIKI44A	1	2017-11-21 20:37:03.665919	pending delivery to org
35	8	16	insert valid payment_id here	1	2017-11-09 23:15:18.607708	pending delivery to org
146	16	32	PAY-4HB18612AA740002VLIKK2IA	1	2017-11-21 22:47:54.381357	pending delivery to org
36	8	17	PAY-0TH27171V8654210FLICOFZA	1	2017-11-09 23:21:07.21415	pending delivery to org
71	8	17	PAY-4G344979HS960754CLIDDT5Q	1	2017-11-10 23:44:53.167617	pending delivery to org
97	9	17	PAY-5LK376456J651290FLIFCWMA	1	2017-11-13 23:30:54.011873	pending delivery to org
54	9	17	PAY-13099643BN378464CLICR2SI	1	2017-11-10 03:30:13.774835	pending delivery to org
81	8	15	PAY-9SG885538C8035604LIDZMGQ	1	2017-11-12 00:30:13.99119	pending delivery to org
148	9	33	PAY-63995858C2519452BLIKPL4I	1	2017-11-22 03:58:38.600089	pending delivery to org
56	8	16	PAY-8YH737846R155454LLIC65QY	1	2017-11-10 18:24:02.144469	pending delivery to org
58	9	17	PAY-5RV82910RS263183YLIDBMII	1	2017-11-10 21:12:00.744933	pending delivery to org
88	9	17	PAY-7MS40158AJ1805400LIE7A3Y	1	2017-11-13 19:20:13.805819	pending delivery to org
82	9	15	PAY-65G14888R3148142ELIDZMXY	1	2017-11-12 00:31:26.592939	pending delivery to org
67	8	17	PAY-3B525776ES8696119LIDCA4I	1	2017-11-10 21:55:57.950865	pending delivery to org
93	9	17	PAY-58T14199JT3838204LIFCFXA	1	2017-11-13 22:55:22.655029	pending delivery to org
77	8	17	PAY-3EY037353X121194DLIDXYNI	1	2017-11-11 22:39:46.953158	pending delivery to org
89	9	17	PAY-97R27153000882052LIE7G3A	1	2017-11-13 19:32:47.599025	pending delivery to org
84	9	16	PAY-4FT17276386324948LID2OSA	1	2017-11-12 01:43:35.790855	pending delivery to org
78	8	17	PAY-6K155929ME0327738LIDX4XQ	1	2017-11-11 22:49:00.341086	pending delivery to org
79	8	17	PAY-59123976KX186845DLIDYQUY	1	2017-11-11 23:31:25.588547	pending delivery to org
85	9	16	PAY-8PJ7075621748753KLIE5MAY	1	2017-11-13 17:27:28.398072	pending delivery to org
90	8	16	PAY-0PP10291UJ016353FLIE7IQA	1	2017-11-13 19:36:29.251849	pending delivery to org
86	9	17	PAY-45D5819946353872ULIE5M7I	1	2017-11-13 17:29:31.091005	pending delivery to org
100	15	17	PAY-1CR30319DP127223ALIFDRPI	1	2017-11-14 00:28:43.717789	pending delivery to org
91	8	17	PAY-1FJ398898N180720TLIFCDFY	1	2017-11-13 22:49:57.507758	pending delivery to org
96	8	17	PAY-30U65395VF4922504LIFCVYY	1	2017-11-13 23:29:37.851206	pending delivery to org
99	13	17	PAY-7CK41217EB0946344LIFDHGQ	1	2017-11-14 00:06:49.380952	pending delivery to org
103	15	16	PAY-6A356375P4748663CLIFD4XI	1	2017-11-14 00:52:44.433343	pending delivery to org
101	13	16	PAY-16U61370A2215290CLIFDSDY	1	2017-11-14 00:30:06.818075	pending delivery to org
70	9	17	PAY-28P90279MM774333NLIDDRYY	1	2017-11-10 23:40:18.189063	pending delivery to org
102	13	16	PAY-9YP069191X4450701LIFD4FQ	1	2017-11-14 00:51:30.965819	pending delivery to org
104	16	16	PAY-1GF228788X209021KLIFEJVQ	1	2017-11-14 01:20:20.765129	pending delivery to org
106	16	16	PAY-3FU93943YR874761ALIFUGZA	1	2017-11-14 19:26:26.174883	pending delivery to org
107	8	16	PAY-6PY202840X335321SLIFUIRQ	1	2017-11-14 19:29:58.757966	pending delivery to org
108	9	16	PAY-1R885537CY238715GLIFWH4Q	1	2017-11-14 21:45:20.148098	pending delivery to org
109	9	22	PAY-1N0652796R3888336LIF3JCI	1	2017-11-15 03:29:11.36234	pending delivery to org
110	15	22	PAY-75Y15807V3444513SLIF3KBQ	1	2017-11-15 03:31:16.889663	pending delivery to org
111	16	16	PAY-62D5161183904624YLIF5U6A	1	2017-11-15 06:10:39.919817	pending delivery to org
112	9	15	PAY-4AT21635XF1611823LIGLMVY	1	2017-11-15 21:49:03.767609	pending delivery to org
113	16	15	PAY-8X647050L1944882JLIGLM7A	1	2017-11-15 21:49:46.598321	pending delivery to org
114	16	23	PAY-9PP57812E4754033YLIHBALI	1	2017-11-16 22:24:43.977206	pending delivery to org
115	16	23	PAY-30R8406069881852ULIHG5EQ	1	2017-11-17 05:07:03.392449	pending delivery to org
116	13	23	PAY-0KF848189S7725242LIHG5RA	1	2017-11-17 05:08:16.81669	pending delivery to org
118	9	20	PAY-63C3422285366423CLIHHAGI	1	2017-11-17 05:14:00.697669	pending delivery to org
119	16	16	PAY-6HR25324VS620715DLIHUVCQ	1	2017-11-17 20:46:00.253287	pending delivery to org
120	16	23	PAY-6TV32220AT4643157LIHVSXI	5	2017-11-17 21:49:11.682272	pending delivery to org
121	16	23	PAY-2HH93817NK717992VLIHW43Q	10	2017-11-17 23:19:09.389972	pending delivery to org
122	13	23	PAY-4VD18096PK197800XLIHW7RY	10	2017-11-17 23:24:54.777449	pending delivery to org
142	16	30	PAY-32Y9143033211063FLIJYN6I	1	2017-11-21 01:52:46.70705	pending delivery to org
123	8	20	PAY-1KK69503R63637446LIIRYNY	1	2017-11-19 05:52:43.751863	pending delivery to org
124	15	20	PAY-1PE99442JH818873ULIITC7A	1	2017-11-19 07:23:37.676274	pending delivery to org
147	13	17	PAY-7HB38767JL352490TLIKMQZI	1	2017-11-22 00:44:14.889525	pending delivery to org
126	16	20	PAY-4MH94135M15215534LIJB4QA	1	2017-11-20 00:13:49.062516	pending delivery to org
128	9	16	PAY-1V138884RH1420400LIJTSXI	2	2017-11-20 20:21:45.626432	pending delivery to org
129	15	16	PAY-1LK19632L2928664PLIJUGDI	2	2017-11-20 21:03:05.524336	pending delivery to org
\.


--
-- Name: transactions_transaction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('transactions_transaction_id_seq', 148, true);


--
-- Data for Name: user_orgs; Type: TABLE DATA; Schema: public; Owner: user
--

COPY user_orgs (user_org_id, user_id, org_id, rank) FROM stdin;
5	16	9	1
18	15	15	1
6	15	16	2
19	15	13	3
20	22	15	1
21	22	9	2
22	22	8	3
24	16	16	2
25	16	13	3
23	23	16	1
28	23	9	2
29	23	13	3
30	20	13	1
31	20	8	2
32	17	15	1
33	17	13	2
34	17	16	3
\.


--
-- Name: user_orgs_user_org_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('user_orgs_user_org_id_seq', 34, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: user
--

COPY users (user_id, user_email, password, fname, lname, age, zipcode, state_code, default_amount, phone, created_at, last_login, set_password) FROM stdin;
27	EMAIL_SUBJECT_TO_CHANGE	12345678	Anonymous	User	\N	\N	\N	1	\N	2017-11-17 23:39:13.883366	2017-11-17 23:39:13.883373	t
15	fuckingperfect@iampink.com	$2b$10$Gn3KoZJFpVLv/DdKiHCBfuzo8vifZJ3d9oGcZTyWUNUK68BQMjFam	Alicia	Moore	38	90210	CA	1	3108008135	2017-11-09 23:15:18.593836	2017-11-09 23:15:18.593844	t
17	beccarosenthal-buyer-1@gmail.com	$2b$10$CvvqL8McViaYqBlADuZQ8OSjxbtwqzvCe.8geRLrjiE0YNGMhKXOO	Chinandler	Bong	40	10012	NY	1	4087379192	2017-11-09 23:15:18.597031	2017-11-09 23:15:18.597036	t
22	hello@itsme.com	$2b$10$zTIk8Lpy7pLk64mOGdJqZ.2kPzgby81Wm0bMxcPhP3fESqV0VJdYy	Adele	Atkins	28	94644	CA	1	8184898484	2017-11-15 00:24:42.617496	2017-11-15 00:24:42.617512	t
23	beccarosenthal-buyer-2@gmail.com	$2b$10$deWlU8Lx2lkrqNuDsRRwDOble9V/f8NHCuv.XRlaAz8QkO.ZdzdKi	Rebecca	Bunch	29	91723	CA	10	9175225614	2017-11-16 21:53:43.716692	2017-11-16 21:53:43.716705	t
16	beccarosenthal-buyer@gmail.com	$2b$10$oymYTQqFKfP2OYZaxgPrDOll96E80zQ85miBEKztTrPb44o9etqfm	Glen	Coco	17	94611	CA	2	4087379192	2017-11-09 23:15:18.596606	2017-11-09 23:15:18.596611	t
30	superclimactic@bigOtires.com	$2b$10$3g5vcV1noucYzGYlHKgbyOw9FwrOWgHIQhjBzCIQND4NDv9VjePxO	Treaddy	Rubber	\N	\N	\N	1	\N	2017-11-21 01:55:55.74527	2017-11-21 01:55:55.745286	t
20	vomitfreesince93@mosbiusdesign.com	$2b$10$hHTf1ddsD2HxGPyr0r.28OP1tC2V2XW1HvaWZg5ZZw4JGExTkUfau	Ted	Mosby	52	02251	DE	2	6546546541	2017-11-10 03:47:24.575641	2017-11-10 03:47:24.575647	t
31	clocks@vivalavida.com	$2b$10$qWTp3eTKYVk1awBumDdJju64wUPSNuDAWbsZd1bYFMaE/hOrYL6rK	Chris	Martin	\N	\N	\N	1	\N	2017-11-21 20:38:36.233909	2017-11-21 20:38:36.233918	t
32	beccarosenthal-buyer-5@gmail.com	$2b$10$ZKD5d0XYJzcY4VQi9yLLru4xnj85Ti6BZMQsAjYxglIZH/OfhgaFW	Liz	Lemon	\N	\N	\N	1	\N	2017-11-21 22:49:54.010084	2017-11-21 22:49:54.010092	t
33	beccarosenthal-buyer-3@gmail.com	$2b$10$wyW1ZI5JutELEKK0K5p5r.dUFlykozxHGHFC1pqH3nI.05VTXBAdm	Austin	Powers	\N	\N	\N	1	\N	2017-11-22 04:01:43.166039	2017-11-22 04:01:43.166049	t
34	misscongeniality@FBI.gov	$2b$10$7Y2bn9fgt9fekWqeFxOI.uM27B6tmS2beK2RpxljVRLTzyKI0T57u	Gracie Lou	Freebush	48	07001	NJ	1	9737923000	2017-11-22 07:24:33.770787	2017-11-22 07:24:33.770804	t
\.


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('users_user_id_seq', 66, true);


--
-- Name: organizations_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY organizations
    ADD CONSTRAINT organizations_pkey PRIMARY KEY (org_id);


--
-- Name: referrals_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY referrals
    ADD CONSTRAINT referrals_pkey PRIMARY KEY (ref_id);


--
-- Name: states_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY states
    ADD CONSTRAINT states_pkey PRIMARY KEY (code);


--
-- Name: transactions_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY transactions
    ADD CONSTRAINT transactions_pkey PRIMARY KEY (transaction_id);


--
-- Name: user_orgs_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY user_orgs
    ADD CONSTRAINT user_orgs_pkey PRIMARY KEY (user_org_id);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: referrals_referred_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY referrals
    ADD CONSTRAINT referrals_referred_id_fkey FOREIGN KEY (referred_id) REFERENCES users(user_id);


--
-- Name: referrals_referrer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY referrals
    ADD CONSTRAINT referrals_referrer_id_fkey FOREIGN KEY (referrer_id) REFERENCES users(user_id);


--
-- Name: transactions_org_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY transactions
    ADD CONSTRAINT transactions_org_id_fkey FOREIGN KEY (org_id) REFERENCES organizations(org_id);


--
-- Name: transactions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY transactions
    ADD CONSTRAINT transactions_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: user_orgs_org_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY user_orgs
    ADD CONSTRAINT user_orgs_org_id_fkey FOREIGN KEY (org_id) REFERENCES organizations(org_id);


--
-- Name: user_orgs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY user_orgs
    ADD CONSTRAINT user_orgs_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: users_state_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_state_code_fkey FOREIGN KEY (state_code) REFERENCES states(code);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

