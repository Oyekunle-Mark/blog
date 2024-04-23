---
title: "Building a Simple Auto-Complete Program in Javascript"
date: 2021-11-15
description: "Building a Simple Auto-Complete Program in Javascript"
summary: "In this article, we will be learning enough to understand what autocomplete programs are and how they work. We will also cobble together a rudimentary autocomplete program that can efficiently suggest valid words that match our entries. We will also be learning about the trie data structure and the role it plays in building autocomplete programs."
draft: false
tags: ["javascript", "data-structures"]
---

Autocompletes, or Word completions, are ubiquitous. They help us complete our entries in so many places, that we've now taken them for granted. 

In this article, we will be learning enough to understand what autocomplete programs are and how they work. We will also cobble together a rudimentary autocomplete program that can efficiently suggest valid words that match our entries. We will also be learning about the trie data structure and the role it plays in building autocomplete programs.

## Prerequisites

We will be building the autocomplete program in JavaScript. So some familiarity with that programming language would indeed be helpful. If you're coming from another programming language, you should be able to follow along.

Also, familiarity with the trie data structure would be helpful. Although this is not a requirement as an implementation is provided in this tutorial.

## What is an autocomplete?

I will defer the exercise of appropriately defining what an autocomplete is to Wikipedia. The [wikipedia page for autocomplete](https://en.wikipedia.org/wiki/Autocomplete) has this to say:

> Autocomplete, or word completion, is a feature in which an application predicts the rest of a word a user is typing. In Android and iOS smartphones, this is called predictive text. In graphical user interfaces, users can typically press the tab key to accept a suggestion or the down arrow key to accept one of several.

Autocompletes find usage in a lot of software programs such as web browsers, email clients, search engines, code editors, command-line interpreters, and word processors.

## Implementation of an autocomplete program

In this section, and its sub-sections, we will move into the implementation of a usable autocomplete program. Starting out with an inefficient first attempt, we will improve and optimize it to deliver something that at its heart, represents what most practical autocompletes are built on.

The code presented in this article can be found [here](https://github.com/Oyekunle-Mark/find_match) on GitHub

### A naive implementation

Let us begin with a naive implementation. Since the main purpose of the autocomplete is to suggest words that would be ending in the prefix provided by the users as they type their inputs. One way to achieve this is to loop through a list of valid words, find the ones starting with the user's input, and return those as the suggestions.

With an array of ten valid words:

```javascript
const validWords = ["flatware", "clash", "twin", "escape", "describe", "golf", "communication", "coffee", "split", "language"];
```

We can create a function, that loops through all the valid words to find words that have prefixes matching user input. This is demonstrated below:

```javascript
function findMatches(validWords, userInput) {
    return validWords.filter(word => word.startsWith(userInput));
}
```

Straightforward enough. Is it not?
We can test this by logging the result of passing the function some user input:

```javascript=
console.log(findMatches(validWords, "flat"));
console.log(findMatches(validWords, "c"));
console.log(findMatches(validWords, "esp"));
console.log(findMatches(validWords, "communi"));
```

This produces:

![](https://i.imgur.com/sT9Y52q.png)

So far so good, you will say. But taking a critical look at this basic algorithm reveals its fundamental flaw. What happens when the valid words are in hundreds of thousands? The function will perform a string comparison with all the valid words. Which will greatly degrade performance.

If you don't find this unacceptable enough, consider that most autocomplete systems will have a growing list of words. That means performance will continue to degrade as words are added until the entire system is brought to its knees.

Surely, we can do better.

### A not so naive implementation

The main bottleneck with the implementation in the previous section was the comparison with every single valid word. To improve performance, we have to look for a way of getting suggestions without running through all the valid words in our record.

It should become obvious at this point that performing the search on an array would not cut it. We need a data structure better suited to our purpose. One such data structure is the `trie`.

A trie is a tree data structure that is based on the prefix of a string and is particularly efficient for retrieving data. If you are unfamiliar with tries, I suggest you read about them in the links provided at the end of this article.

We will be implementing our own trie and using that to perform word search and get suggestions for user input in this section.


#### The Trie

We will begin our implementation with the `TrieNode`. This class will represent each node in the Trie. The code for this class is presented below:

```javascript
class TrieNode {
    constructor() {
        this.marksEndOfWord = false;
        this.children = {};
        this.word = null;
    }

    hasChild(character) {
        return this.children[character] ? true : false;
    }

    getChildTrieNode(character) {
        if (this.hasChild(character))
            return this.children[character];

        return null;
    }

    insertChild(character, trieNode) {
        this.children[character] = trieNode;
    }

    markEndOfWord(word) {
        this.marksEndOfWord = true;
        this.word = word;
    }

    isEndOfWord() {
        return this.marksEndOfWord;
    }

    getWordForTrieNode() {
        return this.word;
    }
}
```

The `marksEndOfWord` property will be used to indicate if the current TrieNode marks the end of a valid word. In a trie, not only leaf nodes can mark the end of a valid word. Using an example, imagine that the word `cat` has been inserted into the trie and the nodes link as follows:

```txt
C->A->T
```

Inserting `catalogue` into the try will update the trie nodes to this:

```txt
C->A->T->A->L->O->G->U->E
```

Without a way of marking a trie node as the terminating node for a valid word, it will be very hard for us to decipher valid words that are prefixes of other words in the trie.

The `children` property is a javascript object that maps the character represented by the trie node to the trie node itself.

`word` property is updated if the TrieNode is a terminating node for a valid word. It's more for convenience so we can easily retrieve the valid word from the node. It is only provided for TrieNodes with its `marksEndOfWord` property set to true to reduce memory usage.

The rest of the methods on the `TrieNode` class are straightforward and do not require further explanation.

With the `TrieNode` class in place, we will provide the `Trie` class which will hold the root node and perform insertion and retrieval on the trie nodes.

The class is presented in-full below:

```javascript
class Trie {
    constructor() {
        this.root = new TrieNode();
    }

    insertWord(word) {
        if (!word) return;

        let currentNode = this.root;

        for (let i = 0; i < word.length; i++) {
            if (currentNode.hasChild(word[i])) {
                currentNode = currentNode.getChildTrieNode(word[i]);
            } else {
                const newTrieNode = new TrieNode();
                currentNode.insertChild(word[i], newTrieNode);
                currentNode = newTrieNode;
            }
        }

        currentNode.markEndOfWord(word);
    }

    findMatches(word) {
        const matches = [];

        if (!word) {
            return matches;
        }

        this.buildMatches(this.findTailTrieNodeForWord(word), matches);

        return matches;
    }

    findTailTrieNodeForWord(word) {
        let currentNode = this.root;

        for (let i = 0; i < word.length; i++) {
            if (!currentNode.hasChild(word[i])) return null;

            currentNode = currentNode.getChildTrieNode(word[i]);
        }

        return currentNode;
    }

    buildMatches(root, matches = []) {
        if (root === null) return;

        if (root.isEndOfWord()) {
            matches.push(root.getWordForTrieNode())
        }

        for (const nodeProperty in root.children) {
            const childNode = root.children[nodeProperty];
            this.buildMatches(childNode, matches);
        }
    }
}
```

The `Trie` class has one property, `root`, which acts as a sentinel node.

The `insertWord` method takes the word to be inserted into the trie, and starting from the root node, inserts trie nodes for the word, character by character. If the word already has a prefix, it simply just iterates onto the next node. The last `TrieNode` is marked as a valid word at the end of this method.

The operation of `findMatches` is a little more involved. Most of the operation is deffered to the `buildMatches` method. Before passing execution into the `buildMatches` method, the `findTailTrieNodeForWord` method is used to find the 
TrieNode that represents the last character in the word. The `buildMatches` method uses this node, retrieved by `findTailTrieNodeForWord`, as its starting point and fans out to find all valid words that could be found with `word` as its prefix.

## Getting autocomplete suggestions using the Trie class

With the `Trie` class implemented in the previous section, we will use that class for our autocomplete program. Working with the same test valid words, we will get suggestions for the same user inputs we validated with our naive implementation.

```javascript
const trie = new Trie();

validWords.map(word => {
    trie.insertWord(word);
});

console.log(trie.findMatches("flat"));
console.log(trie.findMatches("c"));
console.log(trie.findMatches("esp"));
console.log(trie.findMatches("communi"));
```

This produces the same result as before:

![](https://i.imgur.com/3bvuEm6.png)

## Improvement achieved by using a trie

By using a trie, as a base data structure for finding and retrieving the autocomplete suggestions, we are no longer limited by the bottleneck of the size of the keywords. The trie navigates to only nodes that match the characters in the user input and cuts out visiting other nodes.

This will greatly improve the speed of searching and retrieval.

## Further improvements that can be made to the trie

In this section, I will highlight the problems with the autocomplete algorithm we've implemented so far. I leave the improvements to the reader.

Even though the trie does not have the bottleneck of iterating through every valid word to find suggestions, building the trie would still require that all valid words be inserted into the trie. Our simple program holds the trie and all its nodes in memory. This would not be very practical for a huge word size as memory is limited on a single machine.

One other improvement that can be made is to limit the number of suggestions returned by the `findMatches` method. The method keeps recursing downwards to find matches. The size of the suggestion might be too big. The computer might run out of call stack too. Perhaps refactor to an iterative implementation and limit suggestions returned to a reasonable size
An adventurous engineer might even come up with an algorithm for prioritizing which, among all the suggestions, should be returned and ranked by order.

## Conclusion

In this tutorial, we have implemented a very crude autocomplete program. We started out with a naive implementation, identified its bottleneck, and provided another implementation of the autocomplete program using a trie.

A detailed implementation of the trie data structure was also provided and explained with the hope that this would serve to improve your knowledge on the importance and usage of the trie data structure.

Thank you for sticking with me all the way to the end.
