--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.9
-- Dumped by pg_dump version 9.5.9

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
-- Name: statuses; Type: TYPE; Schema: public; Owner: vagrant
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


ALTER TYPE statuses OWNER TO vagrant;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: organizations; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE organizations (
    org_id integer NOT NULL,
    name character varying(100) NOT NULL,
    payee_email character varying(100) NOT NULL,
    logo_url character varying(200),
    mission_statement text,
    website_url character varying(200),
    has_chapters boolean
);


ALTER TABLE organizations OWNER TO vagrant;

--
-- Name: organizations_org_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE organizations_org_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE organizations_org_id_seq OWNER TO vagrant;

--
-- Name: organizations_org_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE organizations_org_id_seq OWNED BY organizations.org_id;


--
-- Name: referrals; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE referrals (
    ref_id integer NOT NULL,
    referrer_id integer NOT NULL,
    referred_id integer NOT NULL
);


ALTER TABLE referrals OWNER TO vagrant;

--
-- Name: referrals_ref_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE referrals_ref_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE referrals_ref_id_seq OWNER TO vagrant;

--
-- Name: referrals_ref_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE referrals_ref_id_seq OWNED BY referrals.ref_id;


--
-- Name: states; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE states (
    code character varying(4) NOT NULL,
    name character varying(40) NOT NULL
);


ALTER TABLE states OWNER TO vagrant;

--
-- Name: transactions; Type: TABLE; Schema: public; Owner: vagrant
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


ALTER TABLE transactions OWNER TO vagrant;

--
-- Name: transactions_transaction_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE transactions_transaction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE transactions_transaction_id_seq OWNER TO vagrant;

--
-- Name: transactions_transaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE transactions_transaction_id_seq OWNED BY transactions.transaction_id;


--
-- Name: user_orgs; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE user_orgs (
    user_org_id integer NOT NULL,
    user_id integer NOT NULL,
    org_id integer NOT NULL,
    rank integer
);


ALTER TABLE user_orgs OWNER TO vagrant;

--
-- Name: user_orgs_user_org_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE user_orgs_user_org_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE user_orgs_user_org_id_seq OWNER TO vagrant;

--
-- Name: user_orgs_user_org_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE user_orgs_user_org_id_seq OWNED BY user_orgs.user_org_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: vagrant
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
    last_login timestamp without time zone NOT NULL
);


ALTER TABLE users OWNER TO vagrant;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_user_id_seq OWNER TO vagrant;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE users_user_id_seq OWNED BY users.user_id;


--
-- Name: org_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY organizations ALTER COLUMN org_id SET DEFAULT nextval('organizations_org_id_seq'::regclass);


--
-- Name: ref_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY referrals ALTER COLUMN ref_id SET DEFAULT nextval('referrals_ref_id_seq'::regclass);


--
-- Name: transaction_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY transactions ALTER COLUMN transaction_id SET DEFAULT nextval('transactions_transaction_id_seq'::regclass);


--
-- Name: user_org_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY user_orgs ALTER COLUMN user_org_id SET DEFAULT nextval('user_orgs_user_org_id_seq'::regclass);


--
-- Name: user_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY users ALTER COLUMN user_id SET DEFAULT nextval('users_user_id_seq'::regclass);


--
-- Data for Name: organizations; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY organizations (org_id, name, payee_email, logo_url, mission_statement, website_url, has_chapters) FROM stdin;
8	Institute of Finishing Projects	beccarosenthal-facilitator@gmail.com	https://media.makeameme.org/created/how-about-getting.jpg	At the Institute of Finishing Projects, we finish proje	http://www.pawneeindiana.com/	f
9	Rent-A-Swag	beccarosenthal-facilitator-1@gmail.com	https://ih1.redbubble.net/image.294685880.6679/flat,800x800,075,f.jpg	At Rent-A-Swag, we bring you the dopest shirts, the swankiest jackets, the slickest cardigans, the flashiest fedoras, the hottest ties, the snazziest canes and more!	http://parksandrecreation.wikia.com/wiki/Rent-A-Swag	f
13	Alternative US National Parks Service	altnps@gmail.com	http://bit.ly/2ySo6D7	45 messed with the wrong set of vested park rangers.	https://twitter.com/altnatparkser?lang=en	f
15	The Derek Zoolander Center For Kids Who Can't Read Good And Wanna Learn To Do Other Stuff Good Too	readingcenter@gmail.com	http://bit.ly/2iq2LuI	We teach you that there's more to life than being really, really good looking	https://dzssite.wordpress.com/	f
16	Alt ACLU	altaclu@gmail.com	http://bit.ly/2hMlwex	An organization that strives to achieve all of the goals of the ACLU with none of the resources.	https://www.aclu.org/about-aclu	t
\.


--
-- Name: organizations_org_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('organizations_org_id_seq', 16, true);


--
-- Data for Name: referrals; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY referrals (ref_id, referrer_id, referred_id) FROM stdin;
1	16	17
2	16	22
3	22	15
4	15	23
\.


--
-- Name: referrals_ref_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('referrals_ref_id_seq', 4, true);


--
-- Data for Name: states; Type: TABLE DATA; Schema: public; Owner: vagrant
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
-- Data for Name: transactions; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY transactions (transaction_id, org_id, user_id, payment_id, amount, "timestamp", status) FROM stdin;
47	9	16	PAY-3XX08742D5767004ELICRFFQ	1	2017-11-10 02:44:37.5878	payment object built
48	8	15	PAY-8CK055977G9357839LICRLSY	1	2017-11-10 02:58:17.988899	paypal payment instantiated
46	8	16	PAY-9VH65583UV426360RLICRE3I	1	2017-11-10 02:43:54.608611	payment object built
39	9	16	PAY-32L02051S8470815CLICOVXA	1	2017-11-09 23:55:07.722074	payment object built
49	9	15	PAY-2BP653364L9537029LICRMGA	1	2017-11-10 02:59:34.305476	paypal payment instantiated
40	8	16	PAY-2L098467XF251620BLICPF3Y	1	2017-11-10 00:29:27.792961	paypal payment instantiated
45	8	16	PAY-6H218914V93485054LICRAGI	1	2017-11-10 02:33:59.442798	payment object built
38	9	16	PAY-4FT65753RE751393NLICOPKQ	1	2017-11-09 23:41:28.57906	payment object built
50	8	17	PAY-6VN28402RA787842SLICRMYQ	1	2017-11-10 03:00:45.387545	paypal payment instantiated
41	9	16	PAY-34207390ML2550212LICPNFQ	1	2017-11-10 00:45:09.315783	paypal payment instantiated
51	8	17	Unrequested	1	2017-11-10 03:16:11.058388	donation attempted
37	9	17	PAY-7KM63695VS472702ALICOKQY	1	2017-11-09 23:31:12.394828	payment object built
44	8	17	PAY-9Y031395GF524280KLICPZBQ	1	2017-11-10 01:10:29.493029	payment object built
52	8	17	PAY-9L71868875198102WLICRU3I	1	2017-11-10 03:18:04.29079	paypal payment instantiated
35	8	16	insert valid payment_id here	1	2017-11-09 23:15:18.607708	pending delivery to org
43	8	17	PAY-71459851XF9850706LICPYGI	1	2017-11-10 01:08:39.606975	payment object built
42	8	16	PAY-61362488Y5154094KLICPOMY	1	2017-11-10 00:47:46.937453	paypal payment instantiated
53	8	15	PAY-46D46287TU0017610LICRXQA	1	2017-11-10 03:23:41.453241	paypal payment instantiated
36	8	17	PAY-0TH27171V8654210FLICOFZA	1	2017-11-09 23:21:07.21415	pending delivery to org
71	8	17	PAY-4G344979HS960754CLIDDT5Q	1	2017-11-10 23:44:53.167617	pending delivery to org
69	8	17	PAY-2FB52121S4887763KLIDDKLQ	1	2017-11-10 23:24:29.117911	payment object built
97	9	17	PAY-5LK376456J651290FLIFCWMA	1	2017-11-13 23:30:54.011873	pending delivery to org
54	9	17	PAY-13099643BN378464CLICR2SI	1	2017-11-10 03:30:13.774835	pending delivery to org
55	9	16	PAY-17L31818AR262204MLIC64TA	1	2017-11-10 18:22:00.116694	paypal payment instantiated
68	9	17	PAY-98V37397GR306634FLIDCCLQ	1	2017-11-10 21:59:09.221128	payment object built
81	8	15	PAY-9SG885538C8035604LIDZMGQ	1	2017-11-12 00:30:13.99119	pending delivery to org
72	8	17	PAY-4BV166828D962935VLIDDV2I	1	2017-11-10 23:48:55.986661	payment succeeded
56	8	16	PAY-8YH737846R155454LLIC65QY	1	2017-11-10 18:24:02.144469	pending delivery to org
57	8	20	PAY-8GH65326WG459343FLIDBMFA	1	2017-11-10 21:11:41.818901	paypal payment instantiated
73	8	17	PAY-399911396S190590ELIDD6EA	1	2017-11-11 00:06:39.093624	payment succeeded
58	9	17	PAY-5RV82910RS263183YLIDBMII	1	2017-11-10 21:12:00.744933	pending delivery to org
88	9	17	PAY-7MS40158AJ1805400LIE7A3Y	1	2017-11-13 19:20:13.805819	pending delivery to org
74	9	17	PAY-2LB84096FD1387901LIDHTMY	1	2017-11-11 04:16:49.121264	paypal payment instantiated
59	9	17	PAY-6D1378137B890974KLIDBV4Y	1	2017-11-10 21:32:34.469443	paypal payment instantiated
60	8	17	Unrequested	1	2017-11-10 21:38:00.629975	payment object built
61	9	17	Unrequested	1	2017-11-10 21:38:35.090476	payment object built
62	9	17	Unrequested	1	2017-11-10 21:39:21.629271	payment object built
63	9	17	PAY-3HE41696DS508321NLIDBZSY	1	2017-11-10 21:40:25.983601	paypal payment instantiated
75	8	17	Unrequested	1	2017-11-11 04:41:05.384957	payment object built
64	9	17	PAY-89X78111D3800394TLIDB2JI	1	2017-11-10 21:41:56.539135	paypal payment instantiated
65	8	17	Unrequested	1	2017-11-10 21:52:15.615788	payment object built
66	8	17	Unrequested	1	2017-11-10 21:53:40.134495	payment object built
105	16	16	Unrequested	1	2017-11-14 19:25:58.035432	donation attempted
82	9	15	PAY-65G14888R3148142ELIDZMXY	1	2017-11-12 00:31:26.592939	pending delivery to org
76	9	17	PAY-4GV63277W2182742KLIDU5OQ	1	2017-11-11 19:25:44.977562	payment succeeded
67	8	17	PAY-3B525776ES8696119LIDCA4I	1	2017-11-10 21:55:57.950865	pending delivery to org
83	9	16	PAY-8LM299991G663391MLID2OOY	1	2017-11-12 01:43:22.213414	paypal payment instantiated
93	9	17	PAY-58T14199JT3838204LIFCFXA	1	2017-11-13 22:55:22.655029	pending delivery to org
94	8	17	Unrequested	1	2017-11-13 23:28:32.702606	donation attempted
77	8	17	PAY-3EY037353X121194DLIDXYNI	1	2017-11-11 22:39:46.953158	pending delivery to org
89	9	17	PAY-97R27153000882052LIE7G3A	1	2017-11-13 19:32:47.599025	pending delivery to org
84	9	16	PAY-4FT17276386324948LID2OSA	1	2017-11-12 01:43:35.790855	pending delivery to org
78	8	17	PAY-6K155929ME0327738LIDX4XQ	1	2017-11-11 22:49:00.341086	pending delivery to org
98	13	17	PAY-5ST62748PM292402HLIFDHGA	1	2017-11-14 00:06:46.288302	paypal payment instantiated
79	8	17	PAY-59123976KX186845DLIDYQUY	1	2017-11-11 23:31:25.588547	pending delivery to org
85	9	16	PAY-8PJ7075621748753KLIE5MAY	1	2017-11-13 17:27:28.398072	pending delivery to org
80	9	17	PAY-86G550723S0882504LIDYRAA	1	2017-11-11 23:32:15.949436	paypal payment instantiated
95	8	17	PAY-7XF32472XF278213YLIFCVTQ	1	2017-11-13 23:28:56.726727	paypal payment instantiated
90	8	16	PAY-0PP10291UJ016353FLIE7IQA	1	2017-11-13 19:36:29.251849	pending delivery to org
86	9	17	PAY-45D5819946353872ULIE5M7I	1	2017-11-13 17:29:31.091005	pending delivery to org
87	9	17	PAY-9KV55495W06166643LIE5NHQ	1	2017-11-13 17:30:00.435917	paypal payment instantiated
100	15	17	PAY-1CR30319DP127223ALIFDRPI	1	2017-11-14 00:28:43.717789	pending delivery to org
91	8	17	PAY-1FJ398898N180720TLIFCDFY	1	2017-11-13 22:49:57.507758	pending delivery to org
96	8	17	PAY-30U65395VF4922504LIFCVYY	1	2017-11-13 23:29:37.851206	pending delivery to org
92	8	17	PAY-5E776717KA330332JLIFCFRA	1	2017-11-13 22:54:50.620723	paypal payment instantiated
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
117	13	20	PAY-6SL46698A0662293JLIHG7TI	1	2017-11-17 05:12:44.845	paypal payment instantiated
118	9	20	PAY-63C3422285366423CLIHHAGI	1	2017-11-17 05:14:00.697669	pending delivery to org
119	16	16	PAY-6HR25324VS620715DLIHUVCQ	1	2017-11-17 20:46:00.253287	pending delivery to org
120	16	23	PAY-6TV32220AT4643157LIHVSXI	5	2017-11-17 21:49:11.682272	pending delivery to org
121	16	23	PAY-2HH93817NK717992VLIHW43Q	10	2017-11-17 23:19:09.389972	pending delivery to org
122	13	23	PAY-4VD18096PK197800XLIHW7RY	10	2017-11-17 23:24:54.777449	pending delivery to org
\.


--
-- Name: transactions_transaction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('transactions_transaction_id_seq', 122, true);


--
-- Data for Name: user_orgs; Type: TABLE DATA; Schema: public; Owner: vagrant
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
\.


--
-- Name: user_orgs_user_org_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('user_orgs_user_org_id_seq', 29, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY users (user_id, user_email, password, fname, lname, age, zipcode, state_code, default_amount, phone, created_at, last_login) FROM stdin;
16	beccarosenthal-buyer@gmail.com	$2b$10$oymYTQqFKfP2OYZaxgPrDOll96E80zQ85miBEKztTrPb44o9etqfm	Glen	Coco	17	94611	CA	1	4087379192	2017-11-09 23:15:18.596606	2017-11-09 23:15:18.596611
15	fuckingperfect@iampink.com	$2b$10$Gn3KoZJFpVLv/DdKiHCBfuzo8vifZJ3d9oGcZTyWUNUK68BQMjFam	Alicia	Moore	38	90210	CA	1	3108008135	2017-11-09 23:15:18.593836	2017-11-09 23:15:18.593844
17	beccarosenthal-buyer-1@gmail.com	$2b$10$CvvqL8McViaYqBlADuZQ8OSjxbtwqzvCe.8geRLrjiE0YNGMhKXOO	Chinandler	Bong	40	10012	NY	1	4087379192	2017-11-09 23:15:18.597031	2017-11-09 23:15:18.597036
20	vomitfreesince93@mosbiusdesign.com	$2b$10$hHTf1ddsD2HxGPyr0r.28OP1tC2V2XW1HvaWZg5ZZw4JGExTkUfau	Ted	Mosby	52	02251	DE	1	6546546541	2017-11-10 03:47:24.575641	2017-11-10 03:47:24.575647
22	hello@itsme.com	$2b$10$zTIk8Lpy7pLk64mOGdJqZ.2kPzgby81Wm0bMxcPhP3fESqV0VJdYy	Adele	Atkins	28	94644	CA	1	8184898484	2017-11-15 00:24:42.617496	2017-11-15 00:24:42.617512
23	beccarosenthal-buyer-2@gmail.com	$2b$10$deWlU8Lx2lkrqNuDsRRwDOble9V/f8NHCuv.XRlaAz8QkO.ZdzdKi	Rebecca	Bunch	29	91723	CA	10	9175225614	2017-11-16 21:53:43.716692	2017-11-16 21:53:43.716705
27	EMAIL_SUBJECT_TO_CHANGE	12345678	Anonymous	User	\N	\N	\N	1	\N	2017-11-17 23:39:13.883366	2017-11-17 23:39:13.883373
\.


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('users_user_id_seq', 27, true);


--
-- Name: organizations_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY organizations
    ADD CONSTRAINT organizations_pkey PRIMARY KEY (org_id);


--
-- Name: referrals_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY referrals
    ADD CONSTRAINT referrals_pkey PRIMARY KEY (ref_id);


--
-- Name: states_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY states
    ADD CONSTRAINT states_pkey PRIMARY KEY (code);


--
-- Name: transactions_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY transactions
    ADD CONSTRAINT transactions_pkey PRIMARY KEY (transaction_id);


--
-- Name: user_orgs_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY user_orgs
    ADD CONSTRAINT user_orgs_pkey PRIMARY KEY (user_org_id);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: referrals_referred_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY referrals
    ADD CONSTRAINT referrals_referred_id_fkey FOREIGN KEY (referred_id) REFERENCES users(user_id);


--
-- Name: referrals_referrer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY referrals
    ADD CONSTRAINT referrals_referrer_id_fkey FOREIGN KEY (referrer_id) REFERENCES users(user_id);


--
-- Name: transactions_org_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY transactions
    ADD CONSTRAINT transactions_org_id_fkey FOREIGN KEY (org_id) REFERENCES organizations(org_id);


--
-- Name: transactions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY transactions
    ADD CONSTRAINT transactions_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: user_orgs_org_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY user_orgs
    ADD CONSTRAINT user_orgs_org_id_fkey FOREIGN KEY (org_id) REFERENCES organizations(org_id);


--
-- Name: user_orgs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY user_orgs
    ADD CONSTRAINT user_orgs_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: users_state_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
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

