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