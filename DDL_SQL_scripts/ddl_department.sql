-- public.department definition

-- Drop table

-- DROP TABLE public.department;

CREATE TABLE public.department (
	department_id serial4 NOT NULL,
	department_name varchar(255) NOT NULL,
	CONSTRAINT department_pkey PRIMARY KEY (department_id)
);