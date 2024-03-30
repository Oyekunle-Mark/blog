---
title: "SQL Insert Into Select Statement - An Overview"
date: 2021-09-26
description: "SQL Insert Into Select Statement - An Overview"
summary: "In this article, I will introduce you to the `INSERT INTO SELECT` statement that is supported by every major SQL engine. This statement allows you to copy a large amount of data from one or more tables into another table efficiently."
draft: false
---

Copying a large number of records from one table, or by joining more than one table, into another table is a frequently performed action in database systems. This straightforward operation can be performed in a number of ways. Many of the popular ORMs also have ways to chunk these records when the size becomes large.

In this article, I will introduce you to the `INSERT INTO SELECT` statement that is supported by every major SQL engine. This statement allows you to copy a large amount of data from one or more tables into another table efficiently.

After this tutorial, you will be able to use the statement to write large records from one table, either using simple statements or using complex join statements, to another.

## Prerequisite

To make the most of this article, you're expected to have a basic understanding of SQL. The code samples in this article will be written in the MySQL flavor of SQL. Doing the same in other database engines should require very few modifications.

## Why copy data between tables?

The need to copy data from one table to another can arise for a number of reasons. The most important reason I've had to use this statement was to populate a table that was meant to hold the result of joining multiple tables. This new table can be used for simple reporting purposes.

Reading data from this new table is a lot faster than performing the multi-table join every time the report records are needed.

Another scenario where this statement would come in handy is when you need to build a table off of another one with some columns modified along the way. This statement shines when the table you're copying from has a lot of historic data and has hundreds of thousands of rows.

## Insert into select in action

In this section, I will show you how to use the `INSERT INTO SELECT` statement. We will be creating some tables, writing into them, and using our shiny new SQL statement to copy data from some tables into another.

The examples presented in this section are contrived so emphasis can be on learning the concept itself rather than picking through complex SQL queries.

Let us begin by creating three tables. The `students`, `courses`, and `student_courses` tables. The SQL queries to do this is presented below:

```sql
CREATE TABLE students (
    student_id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    date_of_birth DATE NOT NULL,
    PRIMARY KEY (student_id)
);

CREATE TABLE courses (
    course_id INT NOT NULL AUTO_INCREMENT,
    course_name VARCHAR(120) NOT NULL,
    course_code VARCHAR(30) NOT NULL,
    PRIMARY KEY (course_id)
);

CREATE TABLE student_courses (
    student_course_id INT NOT NULL AUTO_INCREMENT,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    PRIMARY KEY (student_course_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);
```

Let us perform some insertions into these tables:

```sql
INSERT INTO students(first_name, last_name, gender, date_of_birth)
VALUES 
("Wale", "Uche", "Male", "2010-10-21"),
("Ngozi", "Jumoke", "Female", "1990-02-01"),
("Sango", "Oya", "Male", "2002-05-30");

INSERT INTO courses(course_name, course_code)
VALUES 
("Introduction to Programming", "ICT101"),
("C Programming for Noobs", "CPN210"),
("Numerical Analysis", "MTH354"),
("Database Design for Dummies", "DDD322");

INSERT INTO student_courses(student_id, course_id)
VALUES 
("1", "2"),
("1", "3"),
("2", "1"),
("2", "4"),
("3", "1"),
("3", "2"),
("3", "3"),
("3", "4");
```

To demonstrate how to use the `INSERT INTO SELECT`, we will create a `female_students` table so we can write the result of selecting female students from the `students` table into this new table.

```sql
CREATE TABLE female_students (
    female_students_id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    date_of_birth DATE NULL,
    PRIMARY KEY (female_students_id)
);

INSERT INTO female_students
SELECT * from students
WHERE gender = "Female";
```

Performing a select query on the `female_students` table produces this result:

![](https://i.imgur.com/l7i8QfD.png)


To select specific columns. We will truncate the table and use this query:

```sql
TRUNCATE female_students;

INSERT INTO female_students(first_name, last_name, gender)
SELECT first_name, last_name, gender from students
WHERE gender = "Female";
```

This produces this result

![](https://i.imgur.com/2R3ZHoK.png)


## Writing the result of multi-table joins into another table with insert into select

In this section, we will build on what we have learned in the previous section and use `INSERT INTO SELECT` with join statements.

Often, you will have the need to write the result of multi-table joins into another table. The query might need to be run by a cron job at specific intervals (say, end-of-day) to batch the result of the expensive multi-table joins into another table for easier reads.

The query to do this is similar to the ones presented earlier. Let us create a new `detailed_student_courses` table.

```sql
CREATE TABLE detailed_student_courses (
    student_id INT NOT NULL,
    student_first_name VARCHAR(30) NOT NULL,
    student_last_name VARCHAR(30) NOT NULL,
    course_id  INT NOT NULL,
    course_name VARCHAR(120) NOT NULL,
    course_code VARCHAR(30) NOT NULL
);
```

We will write into this table via a 3-table join statement as follows:

```sql
INSERT INTO detailed_student_courses
SELECT s.student_id, s.first_name as student_first_name, s.last_name as student_last_name, c.course_id, c.course_name, c.course_code
FROM students AS s
INNER JOIN student_courses AS sc
ON s.student_id = sc.student_id
INNER JOIN courses AS c
ON c.course_id = sc.course_id;
```

A select query on `detailed_student_courses` will present us with this result:

![](https://i.imgur.com/TYpIg8f.png)


## Conclusion

Copying data between tables will continue to be a frequent operation performed by Developers. The `INSERT INTO SELECT` statement allows you to copy data from one table to another. This article has covered how to do use this statement in simple and not so simple queries.
