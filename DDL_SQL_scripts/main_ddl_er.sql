-- public.employee definition

-- Drop table

-- DROP TABLE public.employee;

CREATE TABLE public.employee (
	employee_id serial4 NOT NULL,
	first_name varchar(100) NOT NULL,
	last_name varchar(100) NOT NULL,
	phone1 varchar(15) NULL,
	phone2 varchar(15) NULL,
	email varchar(255) NULL,
	company_id int4 NULL,
	department_id int4 NULL,
	CONSTRAINT employee_pkey PRIMARY KEY (employee_id)
);


-- public.employee foreign keys

ALTER TABLE public.employee ADD CONSTRAINT employee_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.company(company_id);
ALTER TABLE public.employee ADD CONSTRAINT employee_department_id_fkey FOREIGN KEY (department_id) REFERENCES public.department(department_id);


-- public.department definition

-- Drop table

-- DROP TABLE public.department;

CREATE TABLE public.department (
	department_id serial4 NOT NULL,
	department_name varchar(255) NOT NULL,
	CONSTRAINT department_pkey PRIMARY KEY (department_id)
);


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