---
title: "Admit it, your memory is just as bad as everyone's"
date: 2024-04-26
description: "Admit it, your memory is just as bad as everyone's"
summary: "I think that admitting that your memory isn't something out of the ordinary and that you will in a matter of a few days lose remembrance of the things you recently worked on can be a liberating first step in embracing the commonly evangelised engineering practices."
tags: ["best-practices"]
draft: true
---

My recent observation(relative to this article's publication date) is that Software Engineers naturally expect their memory to serve them well into the future when dealing with a codebase, infrastructure, component, or sub-system. We seem to think we are documenting this for other team members who do lack the context we have about this specific topic, so we really should come around to it because, after all, it is a good practice. I perceive it is lost upon us the very transient nature of our own memory. You are nothing special when it comes to remembrance. Like everyone else, you will forget. And a lot sooner than you believe too!

Acceptance is often the first step to making changes. And accepting that we, like everyone else, will struggle to remember most things after a few weeks if we do not repeatedly engage with the topic can impress upon us the importance of documenting our work, and writing code with consideration of everyone(including yourself) who will later have to read and update that code.

There are a few invariants of memory that shouldn't be lost upon us:
1. We will forget most things we are working on right now in a few weeks unless we engage actively with them.
2. Given enough passage of time where we do not have to work on something, we will need to be reminded of that thing in the same way as the other people who did not work on it.
3. We are not an exception to invariants 1 and 2.
4. Invarants 1 and 2 are true in all situations, irrespective of the current engagement level with our work. That is, no matter how knee-deep you consider yourself in that subject, you will forget soon enough.

If you agree to those, or to most of them, then you will naturally work in a manner that does not result in those human natures being a hindrance to our delivery as an engineer. How do we do this? We:
1. **Document**. With the belief that this serves everyone in coming to a level of understanding acceptable enough to acquire the understanding and context of the topic. We document the data flow, the architecture, assumption and logic. We also store the document with the purpose of it being found - as easily as possible - by everyone else.
2. **Write code for everyone**. Because we will be everyone soon enough. Our current privileged position of knowledge will not last long. Time is the ultimate equaliser.

I believe that it is this assumption about our memory that will set us free, and allow us to embrace the practice that we know will serve us well but have hitherto, considered an inconvenience.

I will end this article by quoting this riddle that Gollum asked Bilbo in The Hobbit[^1].

> This thing all things devours;\
> Birds, beasts, trees, flowers;\
> Gnaws iron, bites steel;\
> Grinds hard stones to meal;\
> Slays king, ruins town,\
> And beats mountain down

[^1]: [The Hobbit](https://en.wikipedia.org/wiki/The_Hobbit)
