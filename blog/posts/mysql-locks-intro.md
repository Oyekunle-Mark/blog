---
title: "An Introduction to MySQL Locks"
date: 2022-01-03
description: "An Introduction to MySQL Locks"
summary: "Concurrent access to database records from different client sessions can impact data integrity and lead to the expected behavior of computer programs that perform specific actions depending on the value of the data retrieved from the database. In this article, I will give you an introduction to how MySQL locks can be used for concurrency control and guarantee data integrity while allowing multiple users or sessions to safely interact with data. I will also write about the popular types of MySQL locks."
draft: false
tags: ["sql"]
---

Concurrent access to database records from different client sessions can impact data integrity and lead to the expected behavior of computer programs that perform specific actions depending on the value of the data retrieved from the database. In this article, I will give you an introduction to how MySQL locks can be used for concurrency control and guarantee data integrity while allowing multiple users or sessions to safely interact with data. I will also write about the popular types of MySQL locks.

## Prerequisite

This article assumes that you have an intermediate understanding of SQL. Examples are presented, and concepts are explained using MySQL.

## What is a lock?

The [wikipedia](https://en.wikipedia.org/wiki/Lock_(computer_science)) page on locks has this to say about what a lock is:

> In computer science, a lock or mutex (from mutual exclusion) is a synchronization primitive: a mechanism that enforces limits on access to a resource when there are many threads of execution. A lock is designed to enforce a mutual exclusion concurrency control policy, and with a variety of possible methods, there exist multiple unique implementations for different applications.

From a database standpoint, a lock is used to restrict some database data so that only one session or user can make changes to that data.

## Why you should use database locks

The biggest benefit of using database locks is that when employed correctly, it guarantees data integrity while allowing concurrent access to data. Database locks exist to prevent two or more users or sessions from updating the same exact piece of data at the same exact time.

You should use locks to prevent potential loss of data due to concurrent updates.

## How to use MySQL locks

In this section, we will learn about how to use locks in MySQL. The two popular types of MySQL locks will also be explained.

Let us begin by creating the table we will be demonstrating with. Use the statement below to create the `members` table.

```sql
CREATE TABLE members (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
);
```

We will also be connecting to the database from two sessions so we can demonstrate the behavior of each lock type. We can check the connection id of the current session as follows:

```sql
SELECT CONNECTION_ID();
```

The syntax for acquiring a table lock is presented below:

```sql
-- lock a single table
LOCK TABLES table_name [READ | WRITE]

-- lock many tables
LOCK TABLES table_name1 [READ | WRITE], table_name2 [READ | WRITE], ... ;
```

A client session that acquires a lock is solely responsible for releasing the lock. A session cannot release a lock for another session.

Locks are released using the `UNLOCK` statement.
```sql
UNLOCK TABLES;
```

## Types of MySQL locks

We will look at the popular types of MySQL locks and how to use them in this section of the article.

The two types of MySQL locks we will learn in this article are:

1. Read (Shared) locks
2. Write (Exclusive) locks

### 1. Read (Shared) locks

Read or shared locks are locks that prevent a write lock from being acquired but not other read locks. It allows multiple sessions to obtain a lock on a table for the sole purpose of reading it.

Read locks have the following attributes:

1. A read lock for a table can be acquired by multiple sessions at the same time. Other sessions can also read data from the table without acquiring the lock.
2. The client session that holds a read lock can only read data from the table, but cannot write. Other sessions cannot write data to the table until the lock is released. A write operation from another session will be put into the waiting states until the read lock is released.

To demonstrate, we will make some writes into the `members` table we created in the previous section, acquire a read lock on the table and perform a read.

First, we will check the connection id of the session we will be performing these actions from:

```sql
SELECT CONNECTION_ID();
```
![](https://i.imgur.com/UTGGGh8.png)

Now we will proceed with the rest of the operations.

```sql
INSERT INTO members(name)
VALUES('Moremi Lewis');

LOCK TABLE members READ;

SELECT * FROM members;
```

The result of these statements is predictable. The select statement returns the expected output:

![](https://i.imgur.com/VAcHBrP.png)

Let us take it a step further by attempting to perform a write into the table.

```sql
INSERT INTO members(name)
VALUES('Sango Uche');
```

This statement produces an error because a client session that holds a read lock can only read data from the table, but cannot write.

![](https://i.imgur.com/NeqglKs.png)

Next, we will check the behavior of a read lock from another session.

Using another session, we will attempt to perform read and write operations.

We can confirm that it is indeed another session by using the `CONNECTION_ID()` MySQL function to check the current connection id. 

```sql
SELECT CONNECTION_ID();
```
![](https://i.imgur.com/j9wfFtB.png)

Now let us read from the `members` table.

```sql
SELECT * FROM members;
```
The read request from another session is processed.

![](https://i.imgur.com/WV4mcAL.png)

A write into a table with a read lock from another session will be put in the `waiting` state until the lock is released. Let us verify this behavior by performing the following actions:

Insert into the `members` table:

```sql
INSERT INTO members(name)
VALUES('Mallam Uba');
```
The server waits while the lock is held.

![](https://i.imgur.com/YrZL9DE.png)

We can view the state of the write using the `SHOW PROCESSLIST` statement.

![](https://i.imgur.com/Pf9ho1V.png)

The state is `Waiting for table metadata lock`.

From the first session, release the lock.

```sql
UNLOCK TABLES;
```

Query for all members from the second session.

```sql
SELECT * FROM members;
```
![](https://i.imgur.com/wmsmbuS.png)

We can see that the write is processed after the session holding the lock releases it.

### 1. Write (Exclusive) locks

Write or exclusive locks are locks that prevent any other lock of any kind from being obtained from another session on the same table.

Write locks have the following attributes:

1. The session that holds a write lock on a table can read and write data from the table.
2. Other sessions cannot read or write data to the table until the write lock is released.

We will validate these attributes by obtaining a write lock from the first session and attempt to perform a write from the second session.

From the first session, lock the `members` table.

```sql
LOCK TABLE members WRITE;
```

The session with the write lock can perform a read and write as demonstrated below:

```sql
INSERT INTO members(name)
VALUES('Another Member');

SELECT * FROM members;
```
![](https://i.imgur.com/GpUxmUo.png)

Now from the second session, let us attempt to write into the table.

```sql
INSERT INTO members(name)
VALUES('second session Member');
```

The operation goes into the `waiting state`. We can check this using `SHOW PROCESSLIST`

```sql
SHOW PROCESSLIST
```
![](https://i.imgur.com/YktKW6W.png)

From the first session, release the lock and query the table, the write is done.

```sql
SELECT * FROM members
```
![](https://i.imgur.com/2mxq1AK.png)

## Conclusion

Guaranteeing data integrity and providing concurrency control so that multiple processes of our application can use database data safely is a standard requirement in every well-built computer program. MySQL locks are used to ensure that our database records are not left in an inconsistent or invalid state due to the interaction of multiple sessions with it.

This article demonstrated how MySQL read and write locks can be used to eliminate inaccuracies due to race conditions when multiple instances of our programs attempt to access database records at the same time.
