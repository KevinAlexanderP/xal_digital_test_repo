-- Creating the Company Table
CREATE TABLE Company (
    company_id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state CHAR(2) NOT NULL,
    zip CHAR(5) NOT NULL
);

-- Creating the Department Table
CREATE TABLE Department (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(255) NOT NULL
);

-- Creating the Employee Table
CREATE TABLE Employee (
    employee_id SERIAL PRIMARY KEY,
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
