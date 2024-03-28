-- public.company definition

-- Drop table

-- DROP TABLE public.company;

CREATE TABLE public.company (
	company_id serial4 NOT NULL,
	company_name varchar(255) NOT NULL,
	address varchar(255) NOT NULL,
	city varchar(100) NOT NULL,
	state bpchar(2) NOT NULL,
	zip bpchar(5) NOT NULL,
	CONSTRAINT company_pkey PRIMARY KEY (company_id)
);