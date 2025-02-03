---
title: "The Crusher Programming Language"
date: 2022-09-17
description: "Crusher is a lightweight, interpreted procedural programming language."
summary: "Crusher is a lightweight, interpreted procedural programming language."
tags: ["projects"]
---

## What is Crusher?

Crusher is a lightweight, interpreted procedural programming language.

## What does Crusher look like?

Below is what Crusher code looks like.

This snippet doesn't achieve anything in particular.
It's purpose is to show you some of Crusher's feature and how writing procedures in Crusher (like the `fibonacci` function below) is quite similar to most C-like programming language.

```rust
let age = 12;

print age;

fn sum(a, b, c) {
    let age = 10;
    print age;

    return a + b + c;
}

let result = sum(2, 3, 5);
print result;

result = 0;
print result;

let start = 10;
let inc = 0;

fn increment_sum() {
    inc = inc + 1;
}

while (start > 0) {
    increment_sum();
    start = start - 1;
}

print start;
print inc;

fn fibonacci(n) {
    if (n <= 1) {
        return n;
    }

    return fibonacci(n - 1) + fibonacci(n - 2);
}

let thirteenth_fib = fibonacci(13);

if (thirteenth_fib == 233) {
    print "Crusher is crushing it";
} else {
    print "Oooh oooo. Damn bugs!!!!";
}

print true and false;
print false or true;

print null == null;
print 1 != 2;
```

## Where can I find it?
[GitHub Repository](https://github.com/Oyekunle-Mark/crusher_lang)

The *README* file acts as the project documentation and shows how to use Crusher
