---
title: "Annotations and Type Checking in Python"
date: 2021-10-20
description: "Annotations and Type Checking in Python"
summary: "In this article, we will be looking at how to add annotations and type checking to our Python code."
draft: false
---

Python is a dynamically typed programming language. This means that type checking is done at run-time. [PEP 484](https://www.python.org/dev/peps/pep-0484/) introduced type hints, which makes it possible to add type hints to variables and function signatures.

In this article, we will be looking at how to add annotations and type checking to our Python code.

## Adding annotations to a Python function

Let us begin by considering the change required to annotate a basic Python function.

Imagine a function `say_hello` that takes and returns a string. Without hints, this function would look like this:

```py
def say_hello(name):
    return "Hello " + name
```

It can be annotated as follows:

```py
def say_hello(name: str) -> str:
    return "Hello " + name
```

### Type aliases

In this section, I will show you how to use the `typings` module to create type aliases.

A type alias is a name that refers to a previously defined type.

To define a function `itemize_names` that takes a list of names of length `n` and returns a new list with names numbered from 1 to `n`. An implementation of the function can be found below:

```py
def itemize_names(names):
    return [f"{pos + 1}. {name}" for pos, name in enumerate(names)]
```

To annotate the function, an alias can be created for names:

```py
from typing import List

NameList = List[str]

def itemize_names(names: NameList) -> NameList:
    return [f"{pos + 1}. {name}" for pos, name in enumerate(names)]
```

The typing module provides support for so much more, such as:

- Creating a new type
- Annotating a function that takes a callback
- Generics

You can find the [documentation here](https://docs.python.org/3/library/typing.html) to learn how to add type hints to your Python code.

## Type checking

While you can add type annotations to your code, the Python runtime does not enforce type annotations. In this section of the article, I will outline how to enforce type checking on your annotated Python code.

To demonstrate, the `say_hello` function defined earlier can be re-written, incorrectly, like this without producing any change in functionality.

```py
def say_hello(name: str) -> int:
    return "Hello " + name
```
You will also not get a warning from Python.

To enforce type checks, there are a number of static type checkers available. I would be using [mypy](http://mypy-lang.org/).

Let's install `mypy` to get those type checks we need. You can install `mypy` with this command:

```sh
$ python3 -m pip install mypy
```

To type check our `say_hello` function, let's say it is contained in a `say_hello.py` file:

```sh
$ mypy say_hello.py 

say_hello.py:2: error: Incompatible return value type (got "str", expected "int")
Found 1 error in 1 file (checked 1 source file)
```

Let's fix the error by changing the expected return type back to `str` and type check our file again:

```sh
$ mypy say_hello.py

Success: no issues found in 1 source file
```

The [mypy documentation](https://mypy.readthedocs.io/en/stable/introduction.html) provides all the information required on how to use `mypy` in your projects.

## Conclusion

Python is a dynamically typed programming language and does not enforce type checking out of the box. In this article, I have written about how to annotate Python code and enforce type checking at runtime.
