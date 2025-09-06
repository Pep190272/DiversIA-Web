--
-- PostgreSQL database dump
--

-- Dumped from database version 16.9 (84ade85)
-- Dumped by pg_dump version 17.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- Name: admin_users; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.admin_users (
    id integer NOT NULL,
    username character varying(80) NOT NULL,
    email character varying(120) NOT NULL,
    password_hash character varying(128) NOT NULL,
    is_active boolean,
    created_at timestamp without time zone,
    last_login timestamp without time zone
);


ALTER TABLE public.admin_users OWNER TO neondb_owner;

--
-- Name: admin_users_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.admin_users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.admin_users_id_seq OWNER TO neondb_owner;

--
-- Name: admin_users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.admin_users_id_seq OWNED BY public.admin_users.id;


--
-- Name: admins; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.admins (
    id integer NOT NULL,
    username character varying(80) NOT NULL,
    email character varying(120) NOT NULL,
    password_hash character varying(256) NOT NULL,
    full_name character varying(150),
    active boolean DEFAULT true NOT NULL,
    created_at timestamp(6) with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_login timestamp(6) with time zone
);


ALTER TABLE public.admins OWNER TO neondb_owner;

--
-- Name: admins_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.admins_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.admins_id_seq OWNER TO neondb_owner;

--
-- Name: admins_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.admins_id_seq OWNED BY public.admins.id;


--
-- Name: asociaciones; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.asociaciones (
    id integer NOT NULL,
    nombre_asociacion character varying(200) NOT NULL,
    acronimo character varying(20),
    pais character varying(10) NOT NULL,
    otro_pais character varying(100),
    tipo_documento character varying(100) NOT NULL,
    numero_documento character varying(50) NOT NULL,
    descripcion_otro_documento text,
    neurodivergencias_atendidas text,
    servicios text,
    certificaciones text,
    ciudad character varying(100) NOT NULL,
    direccion text,
    telefono character varying(20),
    email character varying(120) NOT NULL,
    sitio_web character varying(200),
    descripcion text,
    "años_funcionamiento" integer,
    numero_socios character varying(50),
    contacto_nombre character varying(150),
    contacto_cargo character varying(100),
    ip_solicitud character varying(45),
    user_agent character varying(500),
    estado character varying(20) DEFAULT 'pendiente'::character varying NOT NULL,
    created_at timestamp(6) with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp(6) with time zone NOT NULL
);


ALTER TABLE public.asociaciones OWNER TO neondb_owner;

--
-- Name: asociaciones_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.asociaciones_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.asociaciones_id_seq OWNER TO neondb_owner;

--
-- Name: asociaciones_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.asociaciones_id_seq OWNED BY public.asociaciones.id;


--
-- Name: companies; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.companies (
    id integer NOT NULL,
    nombre_empresa character varying(200) NOT NULL,
    email_contacto character varying(120) NOT NULL,
    telefono character varying(20),
    sector character varying(100) NOT NULL,
    tamano_empresa character varying(50) NOT NULL,
    ciudad character varying(100) NOT NULL,
    sitio_web character varying(200),
    descripcion_empresa text,
    experiencia_neurodivergentes boolean DEFAULT false NOT NULL,
    politicas_inclusion text,
    adaptaciones_disponibles text,
    created_at timestamp(6) with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp(6) with time zone NOT NULL
);


ALTER TABLE public.companies OWNER TO neondb_owner;

--
-- Name: companies_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.companies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.companies_id_seq OWNER TO neondb_owner;

--
-- Name: companies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.companies_id_seq OWNED BY public.companies.id;


--
-- Name: crm_contacts; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.crm_contacts (
    id integer NOT NULL,
    name character varying(150) NOT NULL,
    email character varying(120) NOT NULL,
    phone character varying(20),
    company character varying(200),
    neurodivergence character varying(50),
    contact_reason character varying(100),
    city character varying(100),
    status character varying(20) DEFAULT 'new'::character varying NOT NULL,
    notes text,
    created_at timestamp(6) with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp(6) with time zone NOT NULL
);


ALTER TABLE public.crm_contacts OWNER TO neondb_owner;

--
-- Name: crm_contacts_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.crm_contacts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.crm_contacts_id_seq OWNER TO neondb_owner;

--
-- Name: crm_contacts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.crm_contacts_id_seq OWNED BY public.crm_contacts.id;


--
-- Name: email_marketing; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.email_marketing (
    id integer NOT NULL,
    comunidad_autonoma character varying(100) NOT NULL,
    asociacion character varying(200) NOT NULL,
    email character varying(120) NOT NULL,
    telefono character varying(20),
    direccion character varying(300),
    servicios text,
    fecha_enviado character varying(20),
    respuesta text,
    notas_especiales text,
    notas_personalizadas text,
    estado_email character varying(50) DEFAULT 'enviado'::character varying NOT NULL,
    fecha_respuesta timestamp(6) with time zone,
    tipo_respuesta character varying(100),
    seguimiento_programado timestamp(6) with time zone,
    created_at timestamp(6) with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp(6) with time zone NOT NULL
);


ALTER TABLE public.email_marketing OWNER TO neondb_owner;

--
-- Name: email_marketing_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.email_marketing_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.email_marketing_id_seq OWNER TO neondb_owner;

--
-- Name: email_marketing_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.email_marketing_id_seq OWNED BY public.email_marketing.id;


--
-- Name: empleados; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.empleados (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    rol character varying(100) NOT NULL,
    active boolean DEFAULT true
);


ALTER TABLE public.empleados OWNER TO neondb_owner;

--
-- Name: empleados_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.empleados_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.empleados_id_seq OWNER TO neondb_owner;

--
-- Name: empleados_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.empleados_id_seq OWNED BY public.empleados.id;


--
-- Name: employees; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.employees (
    id integer NOT NULL,
    name character varying(150) NOT NULL,
    email character varying(120) NOT NULL,
    rol character varying(100) NOT NULL,
    department character varying(100),
    telefono character varying(20),
    fecha_ingreso character varying(20),
    especialidades text,
    notas text,
    active boolean DEFAULT true NOT NULL,
    created_at timestamp(6) with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp(6) with time zone NOT NULL
);


ALTER TABLE public.employees OWNER TO neondb_owner;

--
-- Name: employees_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.employees_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.employees_id_seq OWNER TO neondb_owner;

--
-- Name: employees_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.employees_id_seq OWNED BY public.employees.id;


--
-- Name: form_submissions; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.form_submissions (
    id integer NOT NULL,
    form_type character varying(50) NOT NULL,
    data text NOT NULL,
    ip_address character varying(45),
    user_agent character varying(200),
    processed boolean DEFAULT false NOT NULL,
    crm_id integer,
    created_at timestamp(6) with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    processed_at timestamp(6) with time zone
);


ALTER TABLE public.form_submissions OWNER TO neondb_owner;

--
-- Name: form_submissions_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.form_submissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.form_submissions_id_seq OWNER TO neondb_owner;

--
-- Name: form_submissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.form_submissions_id_seq OWNED BY public.form_submissions.id;


--
-- Name: general_leads; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.general_leads (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    apellidos character varying(100) NOT NULL,
    email character varying(120) NOT NULL,
    telefono character varying(20),
    ciudad character varying(100) NOT NULL,
    fecha_nacimiento date,
    tipo_neurodivergencia character varying(50),
    diagnostico_formal boolean DEFAULT false NOT NULL,
    habilidades text,
    experiencia_laboral text,
    formacion_academica text,
    intereses_laborales text,
    adaptaciones_necesarias text,
    motivaciones text,
    convertido_a_perfil boolean DEFAULT false NOT NULL,
    created_at timestamp(6) with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp(6) with time zone NOT NULL
);


ALTER TABLE public.general_leads OWNER TO neondb_owner;

--
-- Name: general_leads_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.general_leads_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.general_leads_id_seq OWNER TO neondb_owner;

--
-- Name: general_leads_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.general_leads_id_seq OWNED BY public.general_leads.id;


--
-- Name: job_offers; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.job_offers (
    id integer NOT NULL,
    company_id integer NOT NULL,
    titulo_puesto character varying(200) NOT NULL,
    descripcion text NOT NULL,
    tipo_contrato character varying(50) NOT NULL,
    modalidad_trabajo character varying(50) NOT NULL,
    salario_min integer,
    salario_max integer,
    requisitos text,
    adaptaciones_disponibles text,
    neurodivergencias_target character varying(200),
    activa boolean DEFAULT true NOT NULL,
    created_at timestamp(6) with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp(6) with time zone NOT NULL
);


ALTER TABLE public.job_offers OWNER TO neondb_owner;

--
-- Name: job_offers_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.job_offers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.job_offers_id_seq OWNER TO neondb_owner;

--
-- Name: job_offers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.job_offers_id_seq OWNED BY public.job_offers.id;


--
-- Name: neurodivergent_profiles_new; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.neurodivergent_profiles_new (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    apellidos character varying(100) NOT NULL,
    email character varying(120) NOT NULL,
    telefono character varying(20),
    ciudad character varying(100) NOT NULL,
    fecha_nacimiento date NOT NULL,
    tipo_neurodivergencia character varying(50) NOT NULL,
    diagnostico_formal boolean DEFAULT false NOT NULL,
    habilidades text,
    experiencia_laboral text,
    formacion_academica text,
    intereses_laborales text,
    adaptaciones_necesarias text,
    motivaciones text,
    campos_especificos text,
    tipo_tdah character varying(50),
    nivel_atencion character varying(50),
    impulsividad character varying(50),
    hiperactividad character varying(50),
    medicacion character varying(50),
    created_at timestamp(6) with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp(6) with time zone NOT NULL
);


ALTER TABLE public.neurodivergent_profiles_new OWNER TO neondb_owner;

--
-- Name: neurodivergent_profiles_new_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.neurodivergent_profiles_new_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.neurodivergent_profiles_new_id_seq OWNER TO neondb_owner;

--
-- Name: neurodivergent_profiles_new_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.neurodivergent_profiles_new_id_seq OWNED BY public.neurodivergent_profiles_new.id;


--
-- Name: notifications_backup; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.notifications_backup (
    id integer NOT NULL,
    tipo character varying(50) NOT NULL,
    destinatario character varying(120) NOT NULL,
    asunto character varying(200) NOT NULL,
    contenido text NOT NULL,
    email_html text,
    estado character varying(20) DEFAULT 'pendiente'::character varying NOT NULL,
    prioridad character varying(10) DEFAULT 'media'::character varying NOT NULL,
    created_at timestamp(6) with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    sent_at timestamp(6) with time zone,
    read_at timestamp(6) with time zone
);


ALTER TABLE public.notifications_backup OWNER TO neondb_owner;

--
-- Name: notifications_backup_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.notifications_backup_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.notifications_backup_id_seq OWNER TO neondb_owner;

--
-- Name: notifications_backup_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.notifications_backup_id_seq OWNED BY public.notifications_backup.id;


--
-- Name: tareas_empresa; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.tareas_empresa (
    id integer NOT NULL,
    nombre character varying(255) NOT NULL,
    colaborador character varying(100),
    fecha_inicio character varying(20),
    fecha_final character varying(20),
    estado character varying(50) DEFAULT 'Pendiente'::character varying,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.tareas_empresa OWNER TO neondb_owner;

--
-- Name: tareas_empresa_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.tareas_empresa_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tareas_empresa_id_seq OWNER TO neondb_owner;

--
-- Name: tareas_empresa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.tareas_empresa_id_seq OWNED BY public.tareas_empresa.id;


--
-- Name: tasks; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.tasks (
    id integer NOT NULL,
    tarea character varying(300) NOT NULL,
    colaborador character varying(100),
    fecha_inicio character varying(50),
    fecha_final character varying(50),
    estado character varying(50) DEFAULT 'Pendiente'::character varying NOT NULL,
    notas text,
    created_at timestamp(6) with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp(6) with time zone NOT NULL
);


ALTER TABLE public.tasks OWNER TO neondb_owner;

--
-- Name: tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.tasks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tasks_id_seq OWNER TO neondb_owner;

--
-- Name: tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.tasks_id_seq OWNED BY public.tasks.id;


--
-- Name: test_results; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.test_results (
    id integer NOT NULL,
    user_id integer NOT NULL,
    tipo_test character varying(50) NOT NULL,
    puntuacion_total integer NOT NULL,
    resultados_detalle text,
    recomendaciones text,
    created_at timestamp(6) with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.test_results OWNER TO neondb_owner;

--
-- Name: test_results_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.test_results_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.test_results_id_seq OWNER TO neondb_owner;

--
-- Name: test_results_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.test_results_id_seq OWNED BY public.test_results.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.users (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    apellidos character varying(100) NOT NULL,
    email character varying(120) NOT NULL,
    telefono character varying(20),
    ciudad character varying(100) NOT NULL,
    fecha_nacimiento date NOT NULL,
    tipo_neurodivergencia character varying(50) NOT NULL,
    diagnostico_formal boolean DEFAULT false NOT NULL,
    habilidades text,
    experiencia_laboral text,
    formacion_academica text,
    intereses_laborales text,
    adaptaciones_necesarias text,
    motivaciones text,
    tipo_tdah character varying(20),
    nivel_atencion character varying(10),
    impulsividad character varying(10),
    hiperactividad character varying(10),
    medicacion boolean DEFAULT false NOT NULL,
    nivel_comunicacion character varying(10),
    sensibilidades text,
    rutinas_importantes text,
    areas_dificultad character varying(100),
    herramientas_apoyo text,
    created_at timestamp(6) with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp(6) with time zone NOT NULL
);


ALTER TABLE public.users OWNER TO neondb_owner;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO neondb_owner;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: admin_users id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.admin_users ALTER COLUMN id SET DEFAULT nextval('public.admin_users_id_seq'::regclass);


--
-- Name: admins id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.admins ALTER COLUMN id SET DEFAULT nextval('public.admins_id_seq'::regclass);


--
-- Name: asociaciones id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.asociaciones ALTER COLUMN id SET DEFAULT nextval('public.asociaciones_id_seq'::regclass);


--
-- Name: companies id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.companies ALTER COLUMN id SET DEFAULT nextval('public.companies_id_seq'::regclass);


--
-- Name: crm_contacts id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.crm_contacts ALTER COLUMN id SET DEFAULT nextval('public.crm_contacts_id_seq'::regclass);


--
-- Name: email_marketing id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.email_marketing ALTER COLUMN id SET DEFAULT nextval('public.email_marketing_id_seq'::regclass);


--
-- Name: empleados id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.empleados ALTER COLUMN id SET DEFAULT nextval('public.empleados_id_seq'::regclass);


--
-- Name: employees id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.employees ALTER COLUMN id SET DEFAULT nextval('public.employees_id_seq'::regclass);


--
-- Name: form_submissions id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.form_submissions ALTER COLUMN id SET DEFAULT nextval('public.form_submissions_id_seq'::regclass);


--
-- Name: general_leads id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.general_leads ALTER COLUMN id SET DEFAULT nextval('public.general_leads_id_seq'::regclass);


--
-- Name: job_offers id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.job_offers ALTER COLUMN id SET DEFAULT nextval('public.job_offers_id_seq'::regclass);


--
-- Name: neurodivergent_profiles_new id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.neurodivergent_profiles_new ALTER COLUMN id SET DEFAULT nextval('public.neurodivergent_profiles_new_id_seq'::regclass);


--
-- Name: notifications_backup id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.notifications_backup ALTER COLUMN id SET DEFAULT nextval('public.notifications_backup_id_seq'::regclass);


--
-- Name: tareas_empresa id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tareas_empresa ALTER COLUMN id SET DEFAULT nextval('public.tareas_empresa_id_seq'::regclass);


--
-- Name: tasks id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tasks ALTER COLUMN id SET DEFAULT nextval('public.tasks_id_seq'::regclass);


--
-- Name: test_results id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.test_results ALTER COLUMN id SET DEFAULT nextval('public.test_results_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: admin_users; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.admin_users (id, username, email, password_hash, is_active, created_at, last_login) FROM stdin;
1	DiversiaEternals	diversiaeternals@gmail.com	1bbcf47bc99169acbeff9ecff57f4bdf393b4f94c279da742bd72c12924a9907	t	2025-08-30 22:12:00.811573	\N
\.


--
-- Data for Name: admins; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.admins (id, username, email, password_hash, full_name, active, created_at, last_login) FROM stdin;
\.


--
-- Data for Name: asociaciones; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.asociaciones (id, nombre_asociacion, acronimo, pais, otro_pais, tipo_documento, numero_documento, descripcion_otro_documento, neurodivergencias_atendidas, servicios, certificaciones, ciudad, direccion, telefono, email, sitio_web, descripcion, "años_funcionamiento", numero_socios, contacto_nombre, contacto_cargo, ip_solicitud, user_agent, estado, created_at, updated_at) FROM stdin;
1	Ladronesdebesos	LDB	ES	\N	nif_es	46057860S	\N	ansiedad	apoyo_familias,terapia,grupos_apoyo	ninguna	la torre de claramunt	Avinguda d'Espoía, 762	687408629	Ladronesdebesos@gmail.com	Https://www.ladronesdebesos.com	Sensibilidad con animales y personas a través de la interacción entre ellos. Resolvemos problemas de ansiedad y sindrome del abandono tanto en personas como en mascotas.	2	menos_50	Pep	CEO	10.83.5.180	\N	pendiente	2025-09-02 12:19:56.045662+00	2025-09-02 12:19:56.045665+00
\.


--
-- Data for Name: companies; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.companies (id, nombre_empresa, email_contacto, telefono, sector, tamano_empresa, ciudad, sitio_web, descripcion_empresa, experiencia_neurodivergentes, politicas_inclusion, adaptaciones_disponibles, created_at, updated_at) FROM stdin;
1	TechInclusiva SL	test.diversia.empresa@gmail.com	555-0125	tecnologia	mediana	Valencia	\N	\N	f	\N	\N	2025-09-01 08:22:44.143577+00	2025-09-01 08:22:44.14358+00
2	TestEmpresa2	test.diversia.empresa2@gmail.com	555-0126	salud	grande	Sevilla	\N	\N	f	\N	\N	2025-09-01 08:23:08.237853+00	2025-09-01 08:23:08.237857+00
3	TechInclusiva	test.diversia.empresa@gmail.com	555-0137	Tecnología	mediana	Madrid	\N	\N	f	\N	\N	2025-09-01 09:00:14.700893+00	2025-09-01 09:00:14.700896+00
4	Acelerai 	automatizatunegocio@acelerai.eu	687408629	tecnologia	startup	la torre de claramunt	\N	\N	f	\N	\N	2025-09-02 12:13:31.450489+00	2025-09-02 12:39:59.185479+00
\.


--
-- Data for Name: crm_contacts; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.crm_contacts (id, name, email, phone, company, neurodivergence, contact_reason, city, status, notes, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: email_marketing; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.email_marketing (id, comunidad_autonoma, asociacion, email, telefono, direccion, servicios, fecha_enviado, respuesta, notas_especiales, notas_personalizadas, estado_email, fecha_respuesta, tipo_respuesta, seguimiento_programado, created_at, updated_at) FROM stdin;
6	La Rioja	ACAC La Rioja	info@acaclarioja.org	+34941222334	Logroño	Asociación de altas capacidades La Rioja	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:42.464906+00	2025-09-02 08:42:05.059319+00
41	Castilla-La Mancha	APANDAH Albacete	apandah@gmail.com	+34687728786	C/ Doctor Fleming 12, Albacete	Apoyo local en TDAH	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:47.431584+00	2025-09-02 08:42:10.02106+00
78	Ceuta	ATELCE	info@atelce.es	+34650404721	Ceuta	Intervención TEL-TDL, apoyo escolar	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:52.663061+00	2025-09-02 08:42:15.252961+00
1	Extremadura	A.N.D.A.H. Cáceres	contacto@andah.es	+34615974879	C/ Arsenio Gallego Hernández 6, Cáceres	Apoyo infantil/adulto, asesoramiento familiar	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:41.739976+00	2025-09-02 08:42:04.350482+00
2	Madrid	AAACM Madrid	info@aaacm.org	+34910222334	Madrid	Asociación Altas Capacidades Madrid, formación y apoyo familiar	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:41.896456+00	2025-09-02 08:42:04.49417+00
3	Aragón	AATEDA	aatedaz@gmail.com	+34976522293	C/ Poeta Blas de Otero 2, Zaragoza	Diagnóstico, talleres, grupos de apoyo	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:42.038042+00	2025-09-02 08:42:04.635391+00
4	Castilla y León	ABUDAH Burgos	asociacionabudah@gmail.com	+34650767693	Paseo Comendadores s/n, Burgos	Talleres y apoyo familiar	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:42.180404+00	2025-09-02 08:42:04.776669+00
5	Castilla y León	ABUPHI Ávila	abuphi@hotmail.com	+34692554477	Av. Juan Carlos I 45, Ávila	Apoyo familiar y escolar	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:42.323575+00	2025-09-02 08:42:04.917931+00
7	Cantabria	ACAL Cantabria	contacto@acalcantabria.org	+34942222334	Santander	Asociación de altas capacidades Cantabria, talleres educativos	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:42.605891+00	2025-09-02 08:42:05.200278+00
8	Cantabria	ACANDIS Cantabria	dislexiacantabria@hotmail.com	+34695354511	Santander	Apoyo DEA: Dislexia y Discalculia	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:42.747452+00	2025-09-02 08:42:05.341451+00
9	Cantabria	ACANPADAH	acanpadah@hotmail.com	+34647874045	Avda. Los Castros 141, Santander	Grupos de familias, apoyo escolar	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:42.889067+00	2025-09-02 08:42:05.483124+00
10	Islas Baleares	ACCAB Baleares	contacto@accab.org	+34971222334	Palma de Mallorca	Asociación de altas capacidades Baleares, actividades extracurriculares	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:43.030318+00	2025-09-02 08:42:05.624607+00
11	Cataluña	ACD Catalunya	contacta@acd.cat	+34932030346	Barcelona	Atención a Discalculia, formación a docentes	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:43.171364+00	2025-09-02 08:42:05.76631+00
12	Andalucía	ACODAH Córdoba	acodah@gmail.com	+34625263515	Av. La Alameda 1, Puente Genil, Córdoba	Apoyo a familias, talleres	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:43.312327+00	2025-09-02 08:42:05.907581+00
13	Islas Canarias	ACTE Canarias	info@actecanarias.org	+34928333222	Las Palmas	Apoyo a superdotación y altas capacidades, orientación escolar	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:43.45391+00	2025-09-02 08:42:06.048888+00
14	Castilla-La Mancha	ACUAPRENDE Cuenca	acuaprende15@gmail.com	+34655443322	Cuenca	Apoyo escolar y recursos educativos	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:43.595184+00	2025-09-02 08:42:06.190004+00
15	Murcia	ADAAC Murcia	contacto@adaacmurcia.org	+34968222334	Murcia	Apoyo a altas capacidades, orientación escolar	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:43.736396+00	2025-09-02 08:42:06.332036+00
16	País Vasco	ADAHIgi Guipúzcoa	adahigi@adahigi.org	+34943459594	Katalina Eleizegi 40, Donostia	Intervención psicológica, talleres, bolsa de empleo	30/07/2025	ESTAN DE VACACIONES  HASTA 24 AGOSTO		\N	enviado	\N	\N	\N	2025-09-02 08:41:43.877817+00	2025-09-02 08:42:06.473226+00
17	Galicia	ADAHPO Pontevedra	adahpo@hotmail.es	886204436	C/ Rosalía de Castro 36, Pontevedra	Apoyo global, formación, defensa de derechos	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:44.021684+00	2025-09-02 08:42:06.614938+00
18	Asturias	ADANSI	info@adansi.es	+34984564827	C/ Senda del Convento 4, Oviedo	Asociación de familias y personas con autismo, terapias, orientación	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:44.163555+00	2025-09-02 08:42:06.756263+00
19	Navarra	ADHI Navarra	info@adhinavarra.org	+34948252963	C/ Erletokieta 1, Pamplona	Apoyo infantil/adolescente, grupos, escuela de familias	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:44.304888+00	2025-09-02 08:42:06.89776+00
20	Extremadura	ADISLEX Extremadura	adislex.extremadura@gmail.com	+34661223344	Badajoz	Apoyo educativo, sensibilización	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:44.44594+00	2025-09-02 08:42:07.039286+00
21	Murcia	ADIXMUR Murcia	adixmur@adixmur.org	+34670526187	Molina de Segura	Asociación DEA: Discalculia y recursos educativos	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:44.587166+00	2025-09-02 08:42:07.180975+00
22	Extremadura	AESTEX Extremadura	contacto@aestex.org	+34924222334	Mérida	Apoyo a superdotación, asesoramiento escolar y familiar	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:44.728456+00	2025-09-02 08:42:07.32261+00
23	Madrid	AFANTDAH 940	info@afantdah.org	+34685537770	C/ Mónaco 3, Fuenlabrada, Madrid	Terapias grupales, escuela de padres	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:44.870052+00	2025-09-02 08:42:07.464972+00
24	Andalucía	AFHIP Cádiz	afhip@hotmail.com	+34679704875	C/ Tío Juanes, Jerez de la Frontera	Asociación provincial, apoyo escolar y familiar	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:45.02113+00	2025-09-02 08:42:07.606619+00
25	Galicia	AGADIX Galicia	agadix@hotmail.es	+34608570211	Narón (A Coruña)	Asociación DEA: apoyo a Discalculia y Dislexia	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:45.162574+00	2025-09-02 08:42:07.748553+00
26	País Vasco	AHIDA Bizkaia	ahida05@gmail.com	+34944315783	Parque J.M. Txabarri, Getxo, Bizkaia	Apoyo familiar, formación, defensa de derechos	30/07/2025	VACACIONES HASTA EL 1 SEPTIEMBRE		\N	enviado	\N	\N	\N	2025-09-02 08:41:45.303915+00	2025-09-02 08:42:07.89004+00
27	Castilla y León	ALENHI León	info@alenhi.org	+34987248177	Av. Campos Góticos s/n, León	Intervención y apoyo psicopedagógico	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:45.445619+00	2025-09-02 08:42:08.031897+00
28	Ceuta	Altas Capacidades Ceuta	contacto@aacceuta.org	+34650222334	Ceuta	Programas de apoyo a altas capacidades	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:45.587275+00	2025-09-02 08:42:08.176686+00
29	Melilla	Altas Capacidades Melilla	info@aacmelilla.org	+34952222334	Melilla	Asociación de niños con altas capacidades y superdotación	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:45.72865+00	2025-09-02 08:42:08.318297+00
30	Castilla-La Mancha	AMHIDA Ciudad Real	amhida@castillalamancha.es	+34655956611	C/ Toledo 32, Ciudad Real	Diagnóstico, talleres, apoyo familiar	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:45.870353+00	2025-09-02 08:42:08.459814+00
31	Madrid	AMPASTTA Madrid	info@ampastta.org	+34910345678	Madrid	Asociación nacional Tourette, apoyo integral	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:46.011938+00	2025-09-02 08:42:08.601786+00
32	Murcia	AMUTELHA	contacto@amutelha.es	+34968222333	Murcia	Programa educativo TEL-TDL, convenio público	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:46.15348+00	2025-09-02 08:42:08.743562+00
33	Navarra	ANAC Navarra	info@anacnavarra.org	+34948222334	Pamplona	Asociación de niños y jóvenes con altas capacidades	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:46.295502+00	2025-09-02 08:42:08.887616+00
34	Castilla y León	ANACyL Castilla y León	contacto@anacyl.org	+34984222334	Valladolid	Asociación de niños con altas capacidades, formación	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:46.436748+00	2025-09-02 08:42:09.029486+00
35	Galicia	ANHIDA Vigo	anhidavigo@anhida.org	+34654735266	C/ Anton Beiras 8, Vigo	Terapia educativa, orientación familiar	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:46.57813+00	2025-09-02 08:42:09.171067+00
36	Asturias	ANHIPA	anhipa@gmail.com	+34667425279	Av. Galicia 42, Oviedo / Hnos. Felgueroso 78, Gijón	Grupos, talleres, asesoramiento, divulgación	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:46.720895+00	2025-09-02 08:42:09.313303+00
37	Madrid	ANSHDA Madrid	info@anshda.org	+34913560207	C/ Molina de Segura 33, Madrid	Apoyo a familias, grupos de ayuda	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:46.861966+00	2025-09-02 08:42:09.454971+00
38	Asturias	APADAC Asturias	info@apadacasturias.org	+34985333222	Oviedo	Atención a altas capacidades, formación a docentes	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:47.004266+00	2025-09-02 08:42:09.596443+00
39	Comunidad Valenciana	APADAHCAS Castellón	apadahcas@gmail.com	+34634504644	C/ Dean Martí 46, Castellón	Apoyo familiar, charlas, talleres	30/07/2025	HAY UN CORREO NUEVO LO ENVIO DE NUEVO		\N	enviado	\N	\N	\N	2025-09-02 08:41:47.145581+00	2025-09-02 08:42:09.738202+00
40	Islas Canarias	APANATE	apanate@apanate.org	+34922398998	C/ San Francisco Javier 9, Santa Cruz de Tenerife	Atención a personas con TEA, terapias, apoyo a familias	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:47.29018+00	2025-09-02 08:42:09.879806+00
42	Comunidad Valenciana	APNADAH Valencia	asociacion@apnadah.org	+34963382096	C/ Assagador de les Monges 1D, Valencia	Escuela de familias, campamentos, ocio juvenil	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:47.572828+00	2025-09-02 08:42:10.162352+00
43	Cantabria	APTACAN	aptacan@aptacan.org	+34942223645	C/ Francisco Tomás y Valiente 13, Santander	Apoyo a familias TEA, orientación y servicios terapéuticos	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:47.71438+00	2025-09-02 08:42:10.30316+00
44	Cataluña	APYDA Tarragona	apyda@apyda.com	+34620863402	Av. Ramón y Cajal 39, Tarragona	Psicoterapia, talleres, apoyo familiar	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:47.856932+00	2025-09-02 08:42:10.445868+00
45	La Rioja	ARPA Autismo Rioja	info@autismorioja.org	+34941234567	Logroño, La Rioja	Apoyo a familias TEA, terapias y formación	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:47.998488+00	2025-09-02 08:42:10.586919+00
46	La Rioja	ARPANIH	info@tdahrioja.es	+34608692614	Av. de La Rioja 12, Logroño	Talleres, técnicas de estudio, apoyo familiar	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:48.139891+00	2025-09-02 08:42:10.728334+00
47	Andalucía	ASA Altas Capacidades Andalucía	info@altascapacidadesandalucia.org	+34951011223	Sevilla	Apoyo a niños con altas capacidades, orientación familiar y escolar	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:48.281223+00	2025-09-02 08:42:10.869792+00
48	Galicia	ASAC Galicia	info@asacgalicia.org	+34982222334	Santiago de Compostela	Apoyo a niños con altas capacidades, talleres	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:48.422354+00	2025-09-02 08:42:11.011335+00
49	Andalucía	ASANDIS Andalucía	fedis@fedis.org	+34691018018	Málaga	Apoyo a Discalculia y otras DEA, formación y sensibilización	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:48.56364+00	2025-09-02 08:42:11.152801+00
50	Extremadura	ASHDANEX Plasencia	ashdanex@gmail.com	+34622889954	C/ Fernando Calvo 2, Plasencia	Apoyo familiar local	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:48.704962+00	2025-09-02 08:42:11.29385+00
51	Islas Baleares	Asociación Asperger Baleares	info@aspergerbaleares.org	+34670345678	C/ Aragón 32, Palma de Mallorca	Atención a TEA nivel 1 (Asperger), orientación y terapias	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:48.846535+00	2025-09-02 08:42:11.435814+00
52	Islas Canarias	Asociación BESAY (La Palma)	tdahbesay@hotmail.com	+34922486562	Av. Venezuela 1, El Paso, La Palma	Apoyo local a familias y jóvenes con TDAH	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:48.987453+00	2025-09-02 08:42:11.57789+00
54	Aragón	Asociación Dislexia y Discalculia Aragón	dislexia.aragon@gmail.com	+34660871300	Huesca	Atención a Discalculia, talleres y orientación escolar	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:49.270112+00	2025-09-02 08:42:11.860233+00
55	Navarra	Asociación Navarra de Autismo (ANA)	info@autismonavarra.org	+34948252963	Pamplona/Tudela	Diagnóstico TEA, terapias, formación y escuela de verano	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:49.411345+00	2025-09-02 08:42:12.001087+00
56	Islas Baleares	Asociación STILL (Mallorca)	stilltdah@yahoo.es	+34971460230	C/ Josep Anselm i Clavé 8, Palma de Mallorca	Apoyo a personas con TDAH y familias	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:49.55243+00	2025-09-02 08:42:12.14244+00
57	Andalucía	Asociación TDAH Almería	web@tdah-andalucia.es	+34674862158	C/ Fuente de los Molinos 122, Almería	Apoyo a familias, talleres, charlas	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:49.693497+00	2025-09-02 08:42:12.283674+00
58	Ceuta	Asociación TDAH Ceuta	asociaciontdahceuta@gmail.com	+34650404721	C/ Dean Navarro 6, Ceuta	Apoyo psicopedagógico, escuela de padres, talleres	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:49.834423+00	2025-09-02 08:42:12.424981+00
59	Aragón	Asociación Tourette Aragón	contacto@tourettearagon.org	+34976234567	Zaragoza	Orientación familiar y terapias Tourette	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:49.976091+00	2025-09-02 08:42:12.566331+00
60	Islas Baleares	Asociación Tourette Baleares	contacto@tourettebaleares.org	+34971345678	Palma de Mallorca	Apoyo a afectados por Tourette	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:50.117162+00	2025-09-02 08:42:12.707405+00
61	Cantabria	Asociación Tourette Cantabria	contacto@tourettecantabria.org	+34942345678	Santander	Apoyo a familias y afectados por Tourette	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:50.258056+00	2025-09-02 08:42:12.848976+00
62	Aragón	Asociación TPS Aragón	info@tpsaragon.org	+34976000000	Zaragoza	Atención a niños con TPS, talleres de integración sensorial	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:50.399361+00	2025-09-02 08:42:12.991496+00
63	Islas Baleares	Asociación TPS Baleares	contacto@tpsbaleares.org	+34971000000	Palma de Mallorca	Apoyo a TPS, integración sensorial	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:50.541023+00	2025-09-02 08:42:13.132866+00
64	Cantabria	Asociación TPS Cantabria	info@tpscantabria.org	+34942000000	Santander	Tratamientos de integración sensorial	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:50.683049+00	2025-09-02 08:42:13.27408+00
65	Cataluña	Asociación TPS Cataluña	info@tpscatalunya.org	+34932000000	Barcelona	TPS, terapia ocupacional, estimulación sensorial	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:50.824344+00	2025-09-02 08:42:13.4154+00
66	Madrid	Asociación TPS Madrid	info@tpsmadrid.org	+34910000000	Madrid	Tratamientos de TPS, integración sensorial	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:50.965398+00	2025-09-02 08:42:13.557351+00
67	Madrid	ASTEA Henares	info@asteahenares.org	+34686215032	C/ Santiago 5, Alcalá de Henares	Apoyo a familias TEA, talleres y terapias	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:51.106637+00	2025-09-02 08:42:13.699357+00
68	Murcia	ASTRADE	astrade@astrade.es	+34968206862	Carretera del Chorrico s/n, Molina de Segura	Atención integral TEA, intervención y apoyo familiar	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:51.248251+00	2025-09-02 08:42:13.840287+00
69	Andalucía	ASTTA Andalucía	info@astta.org	+34951012345	Sevilla	Apoyo a personas con Síndrome de Tourette y familias	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:51.389483+00	2025-09-02 08:42:13.981382+00
70	Andalucía	ATELAN (Andalucía)	info@atelan.es	+34958400222	Sevilla	Atención TEL-TDL, orientación y formación	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:51.530849+00	2025-09-02 08:42:14.122811+00
71	Aragón	ATELAR (Aragón)	atelar@atelar.es	+34976223344	Zaragoza	Apoyo familiar, terapias TEL-TDL	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:51.6722+00	2025-09-02 08:42:14.264173+00
72	Asturias	ATELAS Asturias	info@telasturias.es	+34984567890	Cangas del Narcea / Oviedo	Acompañamiento psicoeducativo, apoyo familiar	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:51.813487+00	2025-09-02 08:42:14.40503+00
73	Islas Baleares	ATELBA	contacto@atelba.org	+34971222333	Palma de Mallorca	Intervención y apoyo TEL-TDL	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:51.954719+00	2025-09-02 08:42:14.546171+00
74	Cantabria	ATELCA	info@atelca.es	+34942222333	Santander	Apoyo a niños con TEL y familias	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:52.09676+00	2025-09-02 08:42:14.68819+00
75	Castilla-La Mancha	ATELCAM	info@atelcam.es	+34922222333	Toledo	Intervención temprana TEL-TDL	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:52.238019+00	2025-09-02 08:42:14.829351+00
76	Islas Canarias	ATELCAN	info@atelcan.org	+34928222333	Las Palmas	Apoyo terapéutico TEL-TDL, sensibilización	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:52.379674+00	2025-09-02 08:42:14.970627+00
77	Cataluña	ATELCAT	info@atelcat.cat	+34932222333	Barcelona	Atención específica TEL y formación a docentes	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:52.5209+00	2025-09-02 08:42:15.111881+00
79	Castilla y León	ATELCYL	info@atelcyl.org	+34984222333	Valladolid	Terapias, asesoramiento y orientación TEL-TDL	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:52.804473+00	2025-09-02 08:42:15.393949+00
80	País Vasco	ATELEUS	info@ateleus.org	+34943222333	Bilbao	Apoyo TEL-TDL, inclusión escolar	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:52.945357+00	2025-09-02 08:42:15.535141+00
81	Extremadura	ATELEx	info@atelex.org	+34912222333	Mérida	Atención a TEL-TDL, programas educativos	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:53.086564+00	2025-09-02 08:42:15.676421+00
82	Galicia	ATELGA	info@atelga.org	+34982222333	Santiago de Compostela	Apoyo TEL-TDL, talleres familiares	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:53.22849+00	2025-09-02 08:42:15.817418+00
83	Madrid	ATELMA	asociacion@atelma.es	+34664594749	C/ Marcelina 32 local 3, Madrid	Terapia TEL, orientación, formación y ocio adaptado	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:53.369379+00	2025-09-02 08:42:15.958571+00
84	Melilla	ATELME	info@atelme.org	+34952222333	Melilla	Atención a niños con TEL-TDL y familias	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:53.510407+00	2025-09-02 08:42:16.099851+00
85	Navarra	ATELNA	info@atelna.org	+34948222333	Pamplona	Atención a niños TEL-TDL, orientación familiar	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:53.651633+00	2025-09-02 08:42:16.243288+00
86	La Rioja	ATELRIO	info@atelrioja.org	+34941222333	Logroño	Terapias TEL-TDL, apoyo familiar	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:53.792928+00	2025-09-02 08:42:16.384501+00
87	Comunidad Valenciana	ATELVA	info@atelva.org	+34962222333	Valencia	Terapias TEL-TDL, orientación escolar	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:53.934002+00	2025-09-02 08:42:16.526291+00
88	Aragón	Atenciona Zaragoza	asociacionatenciona@gmail.com	876164948	C/ Concepción Saiz de Otero 16, Zaragoza	Evaluación, talleres psicoeducativos	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:54.0749+00	2025-09-02 08:42:16.667737+00
89	Islas Canarias	ATIMANA-DAH (Tenerife)	secretariaatimana@gmail.com	647 94 23 08	Santa Cruz de Tenerife	Información y asesoramiento para familias	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:54.216428+00	2025-09-02 08:42:16.809004+00
90	País Vasco	AUPA País Vasco	contacto@aupaeuskadi.org	+34946222334	Bilbao	Apoyo a superdotación y altas capacidades	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:54.357516+00	2025-09-02 08:42:16.950579+00
91	Aragón	Autismo Aragón	autismoaragon@gmail.com	+34976514004	C/ María Montessori 9, Zaragoza	Sensibilización, apoyo a familias	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:54.498713+00	2025-09-02 08:42:17.091857+00
92	Islas Baleares	Autismo Baleares	info@autismobaleares.com	+34971307222	C/ Manacor 44, Palma de Mallorca	Intervención TEA, apoyo familiar y escolar	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:54.639761+00	2025-09-02 08:42:17.234401+00
93	Andalucía	Autismo Cádiz	info@autismocadiz.org	+34956472839	C/ Rosadas 11510, Puerto Real (Cádiz)	Apoyo familiar, talleres, sensibilización	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:54.781448+00	2025-09-02 08:42:17.375786+00
94	Ceuta	Autismo Ceuta	autismoceuta@gmail.com	+34650404721	C/ Dean Navarro 6, Ceuta	Apoyo psicopedagógico TEA, talleres y escuela de padres	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:54.92315+00	2025-09-02 08:42:17.517071+00
95	Melilla	Autismo Melilla	info@autismomelilla.org	951768402	Melilla	Entidad de referencia TEA pendiente de contacto oficial	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:55.06456+00	2025-09-02 08:42:17.658462+00
96	Comunidad Valenciana	AVADIS Valencia	m.noguera@dixle.com	+34656428505	Valencia	Apoyo a Discalculia y DEA, recursos matemáticos	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:55.205383+00	2025-09-02 08:42:17.799961+00
97	Castilla-La Mancha	AVANZA TDAH Almansa	almansa@avanzatdah.com	+34634294026	C/ La Estrella 15, Almansa	Asociación local de apoyo familiar	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:55.347117+00	2025-09-02 08:42:17.941724+00
98	Comunidad Valenciana	AVAST Comunidad Valenciana	info@avast.org	+34962222334	Valencia	Asociación valenciana de superdotación y altas capacidades	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:55.488919+00	2025-09-02 08:42:18.08322+00
99	Asturias	Centro Neurodesarrollo Asturias	info@neuroasturias.org	+34985000000	Oviedo	Tratamiento TPS, terapias ocupacionales	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:55.630037+00	2025-09-02 08:42:18.225167+00
100	Islas Baleares	DISFAM Baleares	contacto@disfam.org	+34902886565	Palma de Mallorca	Apoyo a Dislexia y Discalculia, recursos educativos	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:55.77138+00	2025-09-02 08:42:18.366754+00
101	País Vasco	DISLEBI Euskadi	info@dislexiaeuskadi.com	+34946569211	Bilbao	Apoyo DEA: Discalculia, formación y sensibilización	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:55.912843+00	2025-09-02 08:42:18.507899+00
102	Islas Canarias	DISLECAN Canarias	dislecan@gmail.com	+34922820854	Tenerife	Apoyo a Discalculia, talleres educativos	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:56.054723+00	2025-09-02 08:42:18.649454+00
103	Castilla y León	DISLEON León	dislexialeon@gmail.com	+34625570546	León	Asociación DEA: Discalculia, orientación y talleres	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:56.195741+00	2025-09-02 08:42:18.791+00
53	Asturias	Dislexia Asturias (Discalculia incluida)	dislexiasturias@gmail.com	+34622240356	Gijón	Apoyo a Discalculia como parte de DEA	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:49.128886+00	2025-09-02 08:42:18.933598+00
104	Navarra	DISNAVARRA Navarra	disnavarra@gmail.com	+34677889900	Pamplona	Apoyo a Discalculia, orientación escolar	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:56.482461+00	2025-09-02 08:42:19.076444+00
105	Castilla-La Mancha	FACAM TDAH	presidentafacam.tdah@gmail.com	+34949339785	C/ Infantes 3, Ciudad Real	Coordinación regional, apoyo a asociaciones	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:56.623778+00	2025-09-02 08:42:19.217883+00
106	Castilla y León	FACYL-TDAH	facyl.comunicacion@gmail.com	+34609938721	C/ Mariano García Abril 2, Valladolid	Federación autonómica de TDAH	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:56.764926+00	2025-09-02 08:42:19.359291+00
107	Andalucía	FAHYDA	afa@afandaluzas.org	+34954091988	C/ Laraña 4, Sevilla	Federación andaluza de asociaciones de TDAH	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:56.906352+00	2025-09-02 08:42:19.50102+00
108	Castilla-La Mancha	FANJAC Castilla-La Mancha	info@fanjacclm.org	+34922222334	Toledo	Federación de asociaciones de altas capacidades	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:57.047661+00	2025-09-02 08:42:19.642256+00
109	Cataluña	FANJAC Cataluña	info@fanjac.org	+34932222334	Barcelona	Federación de asociaciones de altas capacidades Cataluña	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:57.188725+00	2025-09-02 08:42:19.783448+00
110	Cataluña	FCAFA-TDAH	info@federaciocatalanatdah.org	No disponible	C/ Convent 36, Sabadell	Federación catalana de asociaciones de TDAH	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:57.329946+00	2025-09-02 08:42:19.924392+00
111	Comunidad Valenciana	FECOVADAH	fecovadah@gmail.com	+34626215746	Valencia	Federación regional de TDAH	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:57.471539+00	2025-09-02 08:42:20.065716+00
112	Cataluña	Federació Catalana d'Autisme (FECA)	info@fedcatalanautisme.org	683158309	Sabadell (Barcelona)	Federación de asociaciones TEA catalanas	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:57.612951+00	2025-09-02 08:42:20.206756+00
113	Castilla y León	Federación Autismo Castilla y León	federacion@autismocastillayleon.com	+34947268993	Pº Comendadores s/n, Burgos	Federación de asociaciones TEA regionales	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:57.7547+00	2025-09-02 08:42:20.348321+00
114	Galicia	Federación Autismo Galicia	info@autismogalicia.org	+34981575744	Av. de Madrid 44, Santiago de Compostela	Federación de entidades TEA gallegas	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:57.896275+00	2025-09-02 08:42:20.489989+00
115	Cantabria	Fundación CADAH	info@fundacioncadah.org	+34942213766	C/ Francisco Tomás y Valiente 13B, Santander	Asesoramiento, formación, intervención educativa	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:58.038157+00	2025-09-02 08:42:20.631855+00
116	Madrid	Fundación Conectea	info@fundacionconectea.es	+34916587378	C/ José Hierro 10, SS Reyes	Atención integral a TEA, inclusión social	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:58.17994+00	2025-09-02 08:42:20.773011+00
117	Madrid	Fundación Educación Activa	info@educacionactiva.com	+34913572633	C/ Jimena Menéndez Pidal 8-A, Madrid	Psicopedagogía, formación docente/familiar	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:58.321417+00	2025-09-02 08:42:20.914469+00
118	Galicia	Fundación INGADA	info@fundacioningada.net	+34722521381	C/ Federico García 2, A Coruña	Diagnóstico, terapia, formación	31/07/2025	respuesta el 31/07/2025 piden reunion de 15 minutos para el dia 6		\N	enviado	\N	\N	\N	2025-09-02 08:41:58.463531+00	2025-09-02 08:42:21.055863+00
119	País Vasco	Gautena	info@gautena.org	+34943231323	San Sebastián, Guipúzcoa	Atención a personas con TEA, inclusión, servicios integrales	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:58.605217+00	2025-09-02 08:42:21.197181+00
120	Andalucía	Integración Sensorial Andalucía	contacto@integracionsensorialandalucia.org	+34951000000	Sevilla	Apoyo a TPS, terapias ocupacionales y estimulación sensorial	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:58.746824+00	2025-09-02 08:42:21.338019+00
121	Islas Canarias	Integración Sensorial Canarias	info@tpscanarias.org	+34928000000	Santa Cruz de Tenerife	TPS, terapia ocupacional, orientación familiar	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:58.888018+00	2025-09-02 08:42:21.479575+00
122	País Vasco	Integración Sensorial Euskadi	info@tpseuskadi.org	+34946000000	Bilbao	Apoyo a TPS, intervención temprana	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:59.029647+00	2025-09-02 08:42:21.620965+00
123	Galicia	Integración Sensorial Galicia	info@tpsgalicia.org	+34982000000	Santiago de Compostela	Apoyo a TPS, terapia ocupacional	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:59.171255+00	2025-09-02 08:42:21.762262+00
124	Madrid	Madrid con la Dislexia	info@madridconladislexia.org	+34608570211	Madrid	Sensibilización y recursos educativos	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:59.312304+00	2025-09-02 08:42:21.903393+00
125	Madrid	NorTEA	asociacion.nortea@gmail.com	619 36 13 05	Avda. Aragón 1 bis, 2ºD, SS Reyes	Apoyo familiar, talleres, orientación TEA	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:59.453613+00	2025-09-02 08:42:22.044746+00
126	Comunidad Valenciana	Proyecto Autista	socios@proyectoautista.org	+34687764329	Pasaje 25 de Abril 6, Alaquàs, Valencia	Apoyo familiar, terapias, sensibilización	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:59.594987+00	2025-09-02 08:42:22.186168+00
127	La Rioja	Rioja Dislexia	riojadislexia@gmail.com	+34941223344	Logroño	Apoyo familiar y educación	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:59.736248+00	2025-09-02 08:42:22.327284+00
128	Aragón	SIN LIMITES Aragón	contacto@sinlimitesaragon.org	+34976222111	Zaragoza	Asociación de altas capacidades, talleres y programas educativos	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:41:59.877654+00	2025-09-02 08:42:22.468683+00
129	Madrid	SURESTEA	sio@surestea.org	+34633135700	La Poveda, Arganda del Rey, Madrid	Apoyo a familias, intervención temprana TEA	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:42:00.018819+00	2025-09-02 08:42:22.610372+00
130	Islas Canarias	TDAH Gran Canaria	asociacion@tdahgc.org.es	+34695179439	C/ Presidente Alvear 18, Las Palmas	Apoyo a familiares, sensibilización, jornadas	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:42:00.160352+00	2025-09-02 08:42:22.752126+00
131	Islas Baleares	TDAH Menorca	tdahmenorca@hotmail.com	+34608597590	Centre Polivalent Carlos Mir, Maó	Apoyo local y colaboración con escuelas	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:42:00.301611+00	2025-09-02 08:42:22.893498+00
132	Extremadura	TDAH Tierra de Barros	info@tdahtierradebarros.es	+34699567607	C/ Salvador 223, Almendralejo, Badajoz	Apoyo local a familias y afectados	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:42:00.443057+00	2025-09-02 08:42:23.034942+00
133	Castilla-La Mancha	TDAH Toledo	tdahtoledo@gmail.com	+34671764460	C/ Río Bullaque 24, Toledo	Terapia, logopedia, charlas y talleres	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:42:00.58713+00	2025-09-02 08:42:23.176279+00
134	Cataluña	TDAH Vallès (Sabadell)	administracion@tdahvalles.org	937274605	Sabadell, Barcelona	Diagnóstico, psicología, servicios jurídicos	30/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:42:00.728289+00	2025-09-02 08:42:23.317256+00
135	Asturias	Tourette Asturias	info@touretteasturias.org	+34985345678	Oviedo	Apoyo a Tourette, sensibilización y talleres	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:42:00.879854+00	2025-09-02 08:42:23.458348+00
136	Islas Canarias	Tourette Canarias	info@tourettecanarias.org	+34928345678	Las Palmas	Terapias, orientación y talleres Tourette	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:42:01.021175+00	2025-09-02 08:42:23.600588+00
137	Castilla y León	Tourette Castilla y León	contacto@tourettecyl.org	+34984345678	Valladolid	Apoyo a personas con Tourette y orientación familiar	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:42:01.162354+00	2025-09-02 08:42:23.741816+00
138	Castilla-La Mancha	Tourette Castilla-La Mancha	info@touretteclm.org	+34922345678	Toledo	Sensibilización y talleres Tourette	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:42:01.303278+00	2025-09-02 08:42:23.883066+00
139	Cataluña	Tourette Catalunya	info@tourettecatalunya.org	+34932345678	Barcelona	Asociación de apoyo Tourette, terapias y recursos	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:42:01.444855+00	2025-09-02 08:42:24.024462+00
140	Ceuta	Tourette Ceuta	contacto@touretteceuta.org	+34650345678	Ceuta	Sensibilización y apoyo Tourette	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:42:01.585934+00	2025-09-02 08:42:24.165396+00
141	Comunidad Valenciana	Tourette Comunidad Valenciana	contacto@tourettecv.org	+34962345678	Valencia	Apoyo y orientación Tourette	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:42:01.72739+00	2025-09-02 08:42:24.306714+00
142	País Vasco	Tourette Euskadi	contacto@touretteeuskadi.org	+34946345678	Bilbao	Orientación y sensibilización sobre Tourette	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:42:01.868705+00	2025-09-02 08:42:24.447942+00
143	Extremadura	Tourette Extremadura	info@touretteextremadura.org	+34924345678	Mérida	Talleres, apoyo familiar y terapias	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:42:02.009947+00	2025-09-02 08:42:24.589557+00
144	Galicia	Tourette Galicia	contacto@tourettegalicia.org	+34982345678	Santiago de Compostela	Apoyo y sensibilización Tourette	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:42:02.151254+00	2025-09-02 08:42:24.730849+00
145	La Rioja	Tourette La Rioja	info@tourettelarioja.org	+34941345678	Logroño	Apoyo familiar y terapias Tourette	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:42:02.292653+00	2025-09-02 08:42:24.872045+00
146	Melilla	Tourette Melilla	info@tourettemelilla.org	+34952345678	Melilla	Asociación de apoyo a Tourette	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:42:02.434278+00	2025-09-02 08:42:25.014036+00
147	Murcia	Tourette Murcia	contacto@tourettesmurcia.org	+34968345678	Murcia	Terapias y apoyo familiar	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:42:02.575584+00	2025-09-02 08:42:25.155661+00
148	Navarra	Tourette Navarra	info@tourettenavarra.org	+34948345678	Pamplona	Asociación de apoyo a Tourette	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:42:02.716937+00	2025-09-02 08:42:25.296831+00
149	Castilla y León	TPS Castilla y León	info@tpscyl.org	+34984000000	Valladolid	Integración sensorial, orientación familiar	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:42:02.85813+00	2025-09-02 08:42:25.437892+00
150	Castilla-La Mancha	TPS Castilla-La Mancha	contacto@tpsclm.org	+34922000000	Toledo	Apoyo a TPS, talleres y terapias ocupacionales	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:42:02.999827+00	2025-09-02 08:42:25.579094+00
151	Ceuta	TPS Ceuta	info@tpsceuta.org	+34650000000	Ceuta	Tratamientos de integración sensorial	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:42:03.140945+00	2025-09-02 08:42:25.721021+00
152	Comunidad Valenciana	TPS Comunidad Valenciana	contacto@tpscv.org	+34962000000	Valencia	Tratamientos de integración sensorial, apoyo familiar	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:42:03.282425+00	2025-09-02 08:42:25.862122+00
153	Extremadura	TPS Extremadura	info@tpsextremadura.org	+34924000000	Mérida	TPS, talleres de estimulación sensorial	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:42:03.423746+00	2025-09-02 08:42:26.003343+00
154	La Rioja	TPS La Rioja	contacto@tpslarioja.org	+34941000000	Logroño	TPS, terapia ocupacional y apoyo familiar	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:42:03.565186+00	2025-09-02 08:42:26.144708+00
155	Melilla	TPS Melilla	info@tpsmelilla.org	+34952000000	Melilla	TPS, terapias ocupacionales y estimulación sensorial	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:42:03.706333+00	2025-09-02 08:42:26.286208+00
156	Murcia	TPS Murcia	contacto@tpsmurcia.org	+34968000000	Murcia	Apoyo a TPS, terapia ocupacional y orientación familiar	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:42:03.854833+00	2025-09-02 08:42:26.430033+00
157	Navarra	TPS Navarra	info@tpsnavarra.org	+34948000000	Pamplona	TPS, talleres de integración sensorial	31/07/2025			\N	enviado	\N	\N	\N	2025-09-02 08:42:03.996028+00	2025-09-02 08:42:26.571009+00
\.


--
-- Data for Name: empleados; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.empleados (id, name, rol, active) FROM stdin;
1	Pep	Desarrollador	t
2	Olga	Marketing	t
3	Ana	Diseñadora	t
\.


--
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.employees (id, name, email, rol, department, telefono, fecha_ingreso, especialidades, notas, active, created_at, updated_at) FROM stdin;
2	Pep	pep@neuriak.com	Developer	IT	\N	\N	\N	\N	t	2025-09-05 16:12:32.161844+00	2025-09-05 16:13:28.776237+00
3	Olga	olga@neuriak.com	Marketing Manager	Marketing	\N	\N	\N	\N	t	2025-09-05 16:12:32.161844+00	2025-09-05 16:13:42.806835+00
4	Ana	ana@diversia.com	UX Designer	Design	\N	\N	\N	\N	f	2025-09-05 16:12:32.161844+00	2025-09-05 16:13:58.820552+00
\.


--
-- Data for Name: form_submissions; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.form_submissions (id, form_type, data, ip_address, user_agent, processed, crm_id, created_at, processed_at) FROM stdin;
\.


--
-- Data for Name: general_leads; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.general_leads (id, nombre, apellidos, email, telefono, ciudad, fecha_nacimiento, tipo_neurodivergencia, diagnostico_formal, habilidades, experiencia_laboral, formacion_academica, intereses_laborales, adaptaciones_necesarias, motivaciones, convertido_a_perfil, created_at, updated_at) FROM stdin;
9	Lisberia	Uzcategui	lisberiauzcategui@gmail.com	+528118846300	Apodaca	\N	\N	f	\N	\N	\N	capacitación	\N	redes_sociales	f	2025-09-04 19:45:40.146673+00	2025-09-04 19:45:40.146676+00
\.


--
-- Data for Name: job_offers; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.job_offers (id, company_id, titulo_puesto, descripcion, tipo_contrato, modalidad_trabajo, salario_min, salario_max, requisitos, adaptaciones_disponibles, neurodivergencias_target, activa, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: neurodivergent_profiles_new; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.neurodivergent_profiles_new (id, nombre, apellidos, email, telefono, ciudad, fecha_nacimiento, tipo_neurodivergencia, diagnostico_formal, habilidades, experiencia_laboral, formacion_academica, intereses_laborales, adaptaciones_necesarias, motivaciones, campos_especificos, tipo_tdah, nivel_atencion, impulsividad, hiperactividad, medicacion, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: notifications_backup; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.notifications_backup (id, tipo, destinatario, asunto, contenido, email_html, estado, prioridad, created_at, sent_at, read_at) FROM stdin;
\.


--
-- Data for Name: tareas_empresa; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.tareas_empresa (id, nombre, colaborador, fecha_inicio, fecha_final, estado, created_at) FROM stdin;
2	LinkedIn	Pep	29/07/2025	29/07/2025	Terminada	2025-09-05 17:49:16.547895
3	Discord con bot	Olga	30/07/2025	30/07/2025	Terminada	2025-09-05 17:49:16.547895
4	Instagram	Pep	03/08/2025	03/08/2025	Terminada	2025-09-05 17:49:16.547895
5	Telegram	Pep	04/08/2025	04/08/2025	Terminada	2025-09-05 17:49:16.547895
6	Web con formularios y agente de IA	Pep	29/07/2025	\N	En curso	2025-09-05 17:49:16.547895
7	Aplicación (App)	\N	06/09/2025	\N	Pendiente	2025-09-05 17:49:16.547895
8	Campañas publicitarias en redes sociales	Olga	25/08/2025	\N	En curso	2025-09-05 17:49:16.547895
1	Marketing por correo electrónico	Olga	29/07/2025	29/07/2025	Terminada	2025-09-05 17:49:16.547895
\.


--
-- Data for Name: tasks; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.tasks (id, tarea, colaborador, fecha_inicio, fecha_final, estado, notas, created_at, updated_at) FROM stdin;
37	Marketing por correo electrónico	Olga	29/07/2025	29/07/2025	Terminada	\N	2025-09-05 17:36:05.062811+00	2025-09-05 17:36:05.062815+00
38	LinkedIn	Pep	29/07/2025	29/07/2025	Terminada	\N	2025-09-05 17:36:05.062816+00	2025-09-05 17:36:05.062816+00
39	Discord con bot	Olga	30/07/2025	30/07/2025	Terminada	\N	2025-09-05 17:36:05.062817+00	2025-09-05 17:36:05.062819+00
40	Instagram	Pep	03/08/2025	03/08/2025	Terminada	\N	2025-09-05 17:36:05.06282+00	2025-09-05 17:36:05.06282+00
41	Telegram	Pep	04/08/2025	04/08/2025	Terminada	\N	2025-09-05 17:36:05.062821+00	2025-09-05 17:36:05.062821+00
42	Web con formularios y agente de IA	Pep	29/07/2025	\N	En curso	\N	2025-09-05 17:36:05.062822+00	2025-09-05 17:36:05.062822+00
43	Aplicación (App)	\N	06/09/2025	\N	Pendiente	\N	2025-09-05 17:36:05.062822+00	2025-09-05 17:36:05.062823+00
44	Campañas publicitarias en redes sociales	Olga	25/08/2025	\N	En curso	\N	2025-09-05 17:36:05.062823+00	2025-09-05 17:36:05.062823+00
\.


--
-- Data for Name: test_results; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.test_results (id, user_id, tipo_test, puntuacion_total, resultados_detalle, recomendaciones, created_at) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.users (id, nombre, apellidos, email, telefono, ciudad, fecha_nacimiento, tipo_neurodivergencia, diagnostico_formal, habilidades, experiencia_laboral, formacion_academica, intereses_laborales, adaptaciones_necesarias, motivaciones, tipo_tdah, nivel_atencion, impulsividad, hiperactividad, medicacion, nivel_comunicacion, sensibilidades, rutinas_importantes, areas_dificultad, herramientas_apoyo, created_at, updated_at) FROM stdin;
\.


--
-- Name: admin_users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.admin_users_id_seq', 1, true);


--
-- Name: admins_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.admins_id_seq', 1, false);


--
-- Name: asociaciones_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.asociaciones_id_seq', 1, true);


--
-- Name: companies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.companies_id_seq', 4, true);


--
-- Name: crm_contacts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.crm_contacts_id_seq', 1, false);


--
-- Name: email_marketing_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.email_marketing_id_seq', 157, true);


--
-- Name: empleados_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.empleados_id_seq', 3, true);


--
-- Name: employees_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.employees_id_seq', 4, true);


--
-- Name: form_submissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.form_submissions_id_seq', 1, false);


--
-- Name: general_leads_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.general_leads_id_seq', 13, true);


--
-- Name: job_offers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.job_offers_id_seq', 1, false);


--
-- Name: neurodivergent_profiles_new_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.neurodivergent_profiles_new_id_seq', 41, true);


--
-- Name: notifications_backup_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.notifications_backup_id_seq', 1, false);


--
-- Name: tareas_empresa_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.tareas_empresa_id_seq', 8, true);


--
-- Name: tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.tasks_id_seq', 44, true);


--
-- Name: test_results_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.test_results_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.users_id_seq', 1, false);


--
-- Name: admin_users admin_users_email_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.admin_users
    ADD CONSTRAINT admin_users_email_key UNIQUE (email);


--
-- Name: admin_users admin_users_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.admin_users
    ADD CONSTRAINT admin_users_pkey PRIMARY KEY (id);


--
-- Name: admin_users admin_users_username_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.admin_users
    ADD CONSTRAINT admin_users_username_key UNIQUE (username);


--
-- Name: admins admins_email_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_email_key UNIQUE (email);


--
-- Name: admins admins_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_pkey PRIMARY KEY (id);


--
-- Name: admins admins_username_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_username_key UNIQUE (username);


--
-- Name: asociaciones asociaciones_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.asociaciones
    ADD CONSTRAINT asociaciones_pkey PRIMARY KEY (id);


--
-- Name: companies companies_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.companies
    ADD CONSTRAINT companies_pkey PRIMARY KEY (id);


--
-- Name: crm_contacts crm_contacts_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.crm_contacts
    ADD CONSTRAINT crm_contacts_pkey PRIMARY KEY (id);


--
-- Name: email_marketing email_marketing_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.email_marketing
    ADD CONSTRAINT email_marketing_pkey PRIMARY KEY (id);


--
-- Name: empleados empleados_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.empleados
    ADD CONSTRAINT empleados_pkey PRIMARY KEY (id);


--
-- Name: employees employees_email_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_email_key UNIQUE (email);


--
-- Name: employees employees_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (id);


--
-- Name: form_submissions form_submissions_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.form_submissions
    ADD CONSTRAINT form_submissions_pkey PRIMARY KEY (id);


--
-- Name: general_leads general_leads_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.general_leads
    ADD CONSTRAINT general_leads_pkey PRIMARY KEY (id);


--
-- Name: job_offers job_offers_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.job_offers
    ADD CONSTRAINT job_offers_pkey PRIMARY KEY (id);


--
-- Name: neurodivergent_profiles_new neurodivergent_profiles_new_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.neurodivergent_profiles_new
    ADD CONSTRAINT neurodivergent_profiles_new_pkey PRIMARY KEY (id);


--
-- Name: notifications_backup notifications_backup_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.notifications_backup
    ADD CONSTRAINT notifications_backup_pkey PRIMARY KEY (id);


--
-- Name: tareas_empresa tareas_empresa_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tareas_empresa
    ADD CONSTRAINT tareas_empresa_pkey PRIMARY KEY (id);


--
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- Name: test_results test_results_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.test_results
    ADD CONSTRAINT test_results_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: asociaciones_created_at_idx; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX asociaciones_created_at_idx ON public.asociaciones USING btree (created_at);


--
-- Name: companies_created_at_idx; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX companies_created_at_idx ON public.companies USING btree (created_at);


--
-- Name: companies_email_contacto_idx; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX companies_email_contacto_idx ON public.companies USING btree (email_contacto);


--
-- Name: crm_contacts_created_at_idx; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX crm_contacts_created_at_idx ON public.crm_contacts USING btree (created_at);


--
-- Name: crm_contacts_email_idx; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX crm_contacts_email_idx ON public.crm_contacts USING btree (email);


--
-- Name: crm_contacts_name_idx; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX crm_contacts_name_idx ON public.crm_contacts USING btree (name);


--
-- Name: form_submissions_created_at_idx; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX form_submissions_created_at_idx ON public.form_submissions USING btree (created_at);


--
-- Name: form_submissions_form_type_idx; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX form_submissions_form_type_idx ON public.form_submissions USING btree (form_type);


--
-- Name: general_leads_created_at_idx; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX general_leads_created_at_idx ON public.general_leads USING btree (created_at);


--
-- Name: general_leads_email_idx; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX general_leads_email_idx ON public.general_leads USING btree (email);


--
-- Name: general_leads_email_key; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE UNIQUE INDEX general_leads_email_key ON public.general_leads USING btree (email);


--
-- Name: job_offers_created_at_idx; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX job_offers_created_at_idx ON public.job_offers USING btree (created_at);


--
-- Name: neurodivergent_profiles_new_created_at_idx; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX neurodivergent_profiles_new_created_at_idx ON public.neurodivergent_profiles_new USING btree (created_at);


--
-- Name: neurodivergent_profiles_new_email_idx; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX neurodivergent_profiles_new_email_idx ON public.neurodivergent_profiles_new USING btree (email);


--
-- Name: notifications_backup_created_at_idx; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX notifications_backup_created_at_idx ON public.notifications_backup USING btree (created_at);


--
-- Name: test_results_created_at_idx; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX test_results_created_at_idx ON public.test_results USING btree (created_at);


--
-- Name: users_created_at_idx; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX users_created_at_idx ON public.users USING btree (created_at);


--
-- Name: users_email_idx; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX users_email_idx ON public.users USING btree (email);


--
-- Name: users_email_key; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE UNIQUE INDEX users_email_key ON public.users USING btree (email);


--
-- Name: job_offers job_offers_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.job_offers
    ADD CONSTRAINT job_offers_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: test_results test_results_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.test_results
    ADD CONSTRAINT test_results_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: public; Owner: cloud_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE cloud_admin IN SCHEMA public GRANT ALL ON SEQUENCES TO neon_superuser WITH GRANT OPTION;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: cloud_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE cloud_admin IN SCHEMA public GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLES TO neon_superuser WITH GRANT OPTION;


--
-- PostgreSQL database dump complete
--

