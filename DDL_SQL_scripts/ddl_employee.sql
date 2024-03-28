-- Creating the Employee Table
CREATE TABLE Employee (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone1 VARCHAR(15),
    phone2 VARCHAR(15),
    email VARCHAR(255),
    company_id INT,
    department_id INT,
    FOREIGN KEY (company_id) REFERENCES Company(company_id),
    FOREIGN KEY (department_id) REFERENCES Department(department_id)
);