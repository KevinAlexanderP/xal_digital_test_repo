ALTER TABLE public.employee
ADD CONSTRAINT employee_manager_id_fkey
FOREIGN KEY (manager_id) REFERENCES public.employee(employee_id);