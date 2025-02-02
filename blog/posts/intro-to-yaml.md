---
title: "Introduction to YAML - Syntax and Applications"
date: 2021-08-21
description: "Introduction to YAML - Syntax and Applications"
summary: "In this tutorial, you will learn about YAML, its syntax, and its applications. After reading this tutorial, you will know enough to read, understand, and write YAML files"
draft: false
tags: ["config"]
---

YAML is a text-based human-readable language used mostly used for storing configuration information and data exchange. It is a [data serialization](https://devopedia.org/data-serialization) language similar to XML and JSON.

YAML originally stood for *Yet Another Markup Language* but it was later changed to the recursive acronym *YAML Ain't Markup Language*  to highlight that its usage is for data storage and transmission and not as a markup language.

According to the [YAML specification](https://yaml.org/spec/history/2002-04-07.html), YAML is designed for human readability and interaction with scripting languages such as Perl and Python.

In this tutorial, you will learn about YAML, its syntax, and its applications. After reading this tutorial, you will know enough to read, understand, and write YAML files.


## YAML Syntax

The following are the basic rules of the YAML syntax:

1. Spaces and indentations are used to define document structure.
2. Tabs are not allowed.
3. YAML files use either `.yml` or `.yaml` file extensions.
4. YAML is case-sensitive.

### Data Types in YAML

In this section, we’ll look at the YAML data types and their uses.

#### Strings

YAML strings can be written with a pair of single(`'`) or double(`"`) quotes or without quotes.

```yaml
text: unquoted
another: 'a single-quoted string'
alternative: "another way to write strings in YAML"
```

Multiline strings start with `|`
```yaml
description: |
  A man of word
  and not of deed
```

#### Numbers

```yaml
# integer
age: 16

# float
salary: 200.84

# scientific notation
balance: 2.89e+6
```

#### Boolean


```yaml
deleted: true
posted: false
```

#### Null

```yaml
blank:
tilde: ~
pointer: null
price: Null
profit: NULL
```

#### Date and Time

YAML supports ISO 8601 formatted date and time.

```yaml
canonical: 2001-12-15T02:59:43.1Z
iso8601: 2001-12-14t21:59:43.10-05:00
time: 2020-12-07T01:02:59:34.02Z
timestamp: 2020-12-07T01:02:59:34.02 +05:30
date: 2013-11-08
```

#### Sequences

Sequences allow us to declare series of items in YAML

```yaml
# list of some African countries
countries:
  - Nigeria
  - Ghana
  - Kenya
```

### Comments

Comments in YAML start with `#`

```yaml
Nigeria: # this is a comment
  population-in-million: 201
  land-mass-per-squar-kilometre: 923,768 # anothe rcomment
```

### Nesting Values

Detailed structures can be created in YAML by nesting.

```yaml
# using nesting with sequences to create a list of objects
bands:
  - Led-Zeppelin:
      genre: Rock
      albums:
        - Presence
        - Led Zeppelin
        - Led Zeppelin I
  - Pink-Floyd:
      genre: Rock
      albums:
        - The Wall
        - The Division
        - The Dark Side of the Moon
```

The equivalent of this in JSON would be

```json
{
    "bands": [
        {
            "Led-Zeppelin": {
                "genre": "Rock",
                "albums": [
                    "Presence",
                    "Led Zeppelin",
                    "Led Zeppelin I"
                ]
            }
        },
        {
            "Pink-Floyd": {
                "genre": "Rock",
                "albums": [
                    "The Wall",
                    "The Division",
                    "The Dark Side of the Moon"
                ]
            }
        }
    ]
}
```

Using YAML to represent a stream of employee documents

```yaml
---
# An employee record
name: Lukas Adebowale
job: Software Engineer
languages:
  - Perl
  - Python
  - C#
address:
  city: Lagos
  zip: 100001
bio: Hacked his way from boredom to stardom.
--- # separate different documents with three dashes
name: Phillip Uche
job: DevOps Engineer
languages:
  - Go
  - Bash
  - Groovy
address:
  city: Lagos
  zip: 100001
bio: Nothing but IT for devs
... # mark end of the document without starting a new one
```

The equivalent representation in JSON is given below

```json
[
    {
        "name": "Lukas Adebowale",
        "job": "Software Engineer",
        "languages": [
            "Perl",
            "Python",
            "C#"
        ],
        "address": {
            "city": "Lagos",
            "zip": "100001"
        },
        "bio": "Hacked his way from boredom to stardom."
    },
    {
        "name": "Phillip Uche",
        "job": "DevOps Engineer",
        "languages": [
            "Go",
            "Bash",
            "Groovy"
        ],
        "address": {
            "city": "Lagos",
            "zip": "100001"
        },
        "bio": "Nothing but IT for devs"
    }
]
```

## Applications

YAML's human-readability and user-friendliness have led to its widespread adoption for creating configuration files. Below are some of the popular tools that use YAML:

1. Docker
2. Kubernetes
3. Swagger
4. Travis CI
5. CircleCI
6. Ansible
7. Jenkins X
8. Spring Book


## Conclusion

YAML makes it easier to create human-readable configuration files and interact with scripting languages such as Perl and Python compared to JSON or XML. The syntax YAML provides allows for the creation of simple to complex data structures while still remaining human readable. Its adoption by popular DevOps tools has made learning YAML a productive skill.
