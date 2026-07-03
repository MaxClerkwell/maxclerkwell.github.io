---
title: "From Aristotle to the Bit"
date: 2026-07-03
tags: [information-theory, shannon, philosophy, history, education]
description: "The bit did not fall from the sky in 1948. It is the last step in a chain that starts with a Greek philosopher arguing about sea battles and ends with Claude Shannon measuring surprise."
---

I want to tell you about a chain of ideas that took roughly 2300 years to complete.

It starts with Aristotle sitting in Athens arguing about whether a statement like "there will be a sea battle tomorrow" is true or false *right now*. It ends with Claude Shannon (Fig. 1), in a small office at Bell Labs in 1948, writing down a formula that tells you exactly how much information is contained in a message. The distance between those two moments is the distance between informal common sense and a mathematically precise engineering tool. Understanding that distance, how each step in the chain was necessary and what each step actually contributed, is one of the most clarifying things you can do if you are trying to understand how digital technology actually works at its root.

So let me walk through it. Not as a history lecture, but as a chain of dependencies. Each person in the chain solved a problem the previous person left open. The chain runs like this:

**Aristotle** (4th century BC) established that every proposition is either true or false, with no third option. **Ramon Llull** (13th century) showed that a sequence of such yes/no decisions can be used to systematically navigate any space of possibilities. **Leibniz** (1703) gave us binary arithmetic and showed that base 2 is the minimally sufficient number system. **Boole** (1854) turned logical reasoning into algebra you can compute mechanically. **Gauss and Weber** (1833) built the first device that physically encoded and transmitted binary signals over a wire. And **Shannon** (1937, 1948) built the final two bridges: from Boolean algebra to electrical circuits, and from physical signals to a precise mathematical measure of information.

That is the chain. Now let me explain what each step actually contributed, and why the previous step was not enough.

---

## Step One: Aristotle and the Two-Valued World

Aristotle gave us two principles that most people today accept so automatically that they forget they are principles at all.

The first is the *law of non-contradiction*: a statement cannot be both true and false at the same time. The second is the *law of excluded middle*: every statement is either true or false, with no third option, no middle ground, no "sort of true".

These sound obvious. But Aristotle knew they were not. In *De Interpretatione*, chapter 9, he worried specifically about statements concerning future events. Is "there will be a sea battle tomorrow" true or false *today*? If it is already determined one way or the other, does that mean the future is fixed? He did not fully resolve this tension, and philosophers still argue about it. But the working assumption he left behind, that meaningful propositions have exactly one of two truth values, became the bedrock of all formal logic.

Notice what this does not give you. It gives you a framework for evaluating single statements. It does not give you a way to *chain* statements systematically, to *compute* with them, or to *encode the world* as a sequence of yes/no decisions. Aristotle drew the line between two truth values. Someone else had to figure out what to do with it.

---

## Step One-and-a-Half: Llull and the Art of Asking

Ramon Llull was a Catalan philosopher and theologian working in the 13th century, roughly 1232 to 1316. His *Ars Magna*, the "Great Art", was an attempt to create a universal method for finding truth by combining a fixed set of basic concepts through systematic questioning. You start with a small vocabulary of fundamental attributes. You ask yes/no questions about each combination. You work through the tree of possibilities exhaustively. Complex questions reduce to chains of binary decisions.

Llull was not doing mathematics in the modern sense, and his specific framework was embedded in medieval Christian theology in ways that do not travel well to the present. But the structural idea, that you can specify and distinguish any complex thing through a sufficient sequence of yes/no questions, is exactly right, and it predates both Leibniz and Boole by several centuries. Leibniz knew Llull's work and was directly influenced by it when developing his own vision of a *calculus ratiocinator*, a machine for resolving arguments by computation.

Aristotle told you each statement is true or false. Llull told you that a *chain* of such statements can be used to navigate a space of possibilities and zero in on a target. That is a different and important idea. It is, in embryonic form, the idea of a binary search tree, a decision tree, a classification algorithm. Every time you play "20 questions" and converge on the right answer, you are using Llull's insight.

---

## An Interlude: Leibniz and the Lines in the I Ching

Gottfried Wilhelm Leibniz, in 1703, published a paper called *Explication de l'Arithmétique Binaire* in which he systematically laid out binary arithmetic: the idea that you can represent any number using only the digits 0 and 1, by assigning place values that are powers of two instead of powers of ten.

One of the things Leibniz understood clearly, and that often gets glossed over, is that base 2 is not *special* in any deep mathematical sense. You can build a positional number system in any base: base 10 (what we use daily), base 60 (Babylonian astronomers), base 16 (hexadecimal in every programmer's life), or base 2. They are all equivalent in expressive power. Any number representable in one base is representable in every other. Leibniz knew this, and he was clear that the choice of base 2 was about *minimality*: it is the smallest base that works at all. You need at least two distinct symbols to build a positional system, because with only one symbol you cannot distinguish place values meaningfully. Two symbols is the minimum.

That argument is purely mathematical. What it means physically, why the minimum-symbol property turns out to be important for building machines, is a story that comes later in the chain.

What I find remarkable about Leibniz is that while working on this, he received a letter from a Jesuit missionary named Joachim Bouvet, who was stationed in China and had been studying the *I Ching*. Bouvet sent Leibniz a diagram of the 64 hexagrams: ancient Chinese symbols made of six stacked lines, each line either broken (yin, 陰) or unbroken (yang, 陽). Leibniz immediately recognised his own binary system in them. Six binary positions give you 2⁶ = 64 combinations. The hexagrams are, structurally, six-digit binary numbers. They were developed roughly 2000 years before Leibniz was born.

I am not saying the ancient Chinese invented binary computing. They did not have that goal. But this moment is worth sitting with: a combinatorial structure powerful enough to encode 64 distinct states was independently arrived at in two civilisations separated by millennia and thousands of miles, because it is a natural consequence of stacking binary choices. The structure was waiting to be discovered. I first had this connection pointed out to me by [Meihui Huang](https://github.com/kathematician), who drew the line from the Bagua directly to Leibniz in a way that has stuck with me since.

<figure>
  <img src="/assets/posts/from-aristotle-to-the-bit-july-2026/bagua.svg" alt="The eight trigrams (Bagua) of the I Ching arranged in the Fuxi Early Heaven sequence, each labelled with its binary value" style="max-width:340px; display:block; margin: 0 auto 0.5rem;">
  <figcaption><strong>Fig. 2:</strong> The eight trigrams (Bagua, 八卦) in the Fuxi "Early Heaven" arrangement. Each trigram is a stack of three lines: solid (yang, 陽, 1) or broken (yin, 陰, 0), giving 2³ = 8 distinct three-bit patterns. The 64 hexagrams of the I Ching extend this to six lines: 2⁶ = 64 combinations, structurally identical to a six-digit binary number. Illustration by the author.</figcaption>
</figure>

What Leibniz still did not have was a way to use binary notation for *logic* rather than just *numbers*. That step came next.

---

## Step Two: Boole and the Algebra of Thought

George Boole, in 1854, published *An Investigation of the Laws of Thought*, and the title is not modest but it is accurate.

Boole's idea was to treat logical operations, AND, OR, NOT, as algebraic operations on symbols that could take only the values 0 and 1. Under his system, "A and B" becomes multiplication (A x B), "A or B" becomes addition (with a correction for overlap), and "not A" becomes 1 - A. You can write down logical arguments as equations and solve them the same way you would solve any algebra problem.

This was a genuine conceptual leap. Before Boole, logic was something you did in natural language, following Aristotle's rules informally. After Boole, logic was a branch of mathematics. It had a notation. It had rules you could apply mechanically. You did not need to understand the *meaning* of what you were computing: you could manipulate the symbols and trust the algebra.

One of the most important results that falls out of this system is functional completeness. The four operations AND, OR, NOT, and the identity operation (a variable that simply passes its value through unchanged) are sufficient to express every possible logical function. Any truth table you can write down, any condition, any combination of inputs and outputs, can be built from those four primitives and nothing else. This is not obvious when you first encounter it, but it has a profound consequence: if you can build physical devices that implement AND, OR, and NOT, you can build any logical computation whatsoever. The entire complexity of modern computing rests on that fact.

Boole was not alone in developing these ideas. Augustus De Morgan, working in the same period, established what are now called De Morgan's laws: the rule that negating an AND gives an OR of the negations, and vice versa. These laws are the reason you can freely interchange AND-based and OR-based formulations of the same logic, and they are used constantly in circuit design. Hugh MacColl, writing in the 1870s and 1880s, pushed propositional logic further toward a formal calculus and was among the first to treat it as a purely symbolic system independent of its philosophical content. Together, Boole, De Morgan, and MacColl transformed logic from a branch of philosophy into a branch of mathematics ready to be handed to engineers.

The 0 and 1 in Boolean algebra are not yet bits in the modern sense. They are truth values. But the connection is coming.

---

## Step Two-and-a-Half: Gauss, Weber, and the First Binary Wire

Between Boole's algebra and Shannon's circuits, there is a physical milestone that rarely gets the attention it deserves.

In 1833, the mathematician Carl Friedrich Gauss and the physicist Wilhelm Weber strung a wire roughly a kilometre across the rooftops of Göttingen, connecting the physics institute to the astronomical observatory. Over that wire they sent signals by reversing the direction of an electrical current. One direction meant one thing, the other direction meant something else: two distinguishable states, transmitted electrically. They used this to spell out words in a code of their own design, sending the first intentional electromagnetic telegraph messages in history.

What makes this relevant to our chain is not just the historical curiosity. It is the physical realisation of something Leibniz had only described mathematically: two symbols, and nothing more, are sufficient to carry any message you want. Gauss and Weber did not need ten voltage levels or twenty. They needed two. The minimal system Leibniz had argued for on mathematical grounds turned out to be exactly what a wire through the air could carry reliably.

The telegraph that Gauss and Weber built was not yet a commercial system, and the code they used was not Morse code. But the idea that a long-distance communication channel could be built around the binary opposition of two physical states was demonstrated right there, on the rooftops of a German university town, fifteen years before Boole published his algebra and 115 years before Shannon measured what was flowing through such a channel.

---

## Step Three: Shannon and the Two Transitions

<figure>
  <img src="/assets/posts/from-aristotle-to-the-bit-july-2026/claude-shannon.jpg" alt="Portrait photograph of Claude Shannon" style="max-width:260px; display:block; margin: 0 auto 0.5rem;">
  <figcaption><strong>Fig. 1:</strong> Claude Elwood Shannon (1916–2001). Photograph by Konrad Jacobs, 1960s. Source: <a href="https://commons.wikimedia.org/wiki/File:ClaudeShannon_MFO3807.jpg" target="_blank" rel="noopener">Wikimedia Commons / Mathematisches Forschungsinstitut Oberwolfach</a>, <a href="https://creativecommons.org/licenses/by-sa/2.0/de/" target="_blank" rel="noopener">CC BY-SA 2.0 DE</a>.</figcaption>
</figure>

Claude Shannon made two contributions so different in nature that they tend to blur together in popular accounts. I want to keep them separate.

**The first contribution came in 1937**, when Shannon was a 21-year-old master's student at MIT. His thesis, which many historians consider the most important master's thesis of the 20th century, showed that Boolean algebra maps directly onto electrical switching circuits. A switch is either open or closed: 0 or 1. An AND gate is two switches in series. An OR gate is two switches in parallel. Every logical function Boole had described algebraically could be physically implemented as an arrangement of relays.

This was the moment when logic left the realm of pure mathematics and entered the world of engineering. From this point forward, you could design a circuit the same way you designed a logical argument, and you could design a logical argument the same way you designed a circuit. Aristotle's two-valued logic and Leibniz's binary arithmetic had been waiting, for two thousand years, for a physical substrate. Gauss and Weber had shown that a wire could carry two states. Shannon showed that those two states could implement any logical function you could describe.

The immediate practical consequence was telephone routing. At the time, connecting one telephone to another across a large network required banks of electromechanical relays, and designing those relay networks was done by hand, by intuition, with no systematic method. Shannon's thesis gave engineers a mathematical language for that design problem. You could now specify a switching network as a Boolean expression, simplify it algebraically, and derive the minimal relay circuit that implemented it. Automatic telephone exchanges, where a dialled number triggers a sequence of relay operations that routes your call without a human operator, had existed in rudimentary form since the 1890s. But building them efficiently at scale, across networks with millions of possible connections, only became tractable once you could reason about relay logic mathematically. Shannon's thesis is the reason automatic dialling as we know it actually worked.

**The second contribution came in 1948**, with a paper called *A Mathematical Theory of Communication*. This one is harder to summarise briefly, because it opened an entirely new field. But let me try to isolate the single idea I think is most important for what we are building towards.

Shannon asked a question that nobody had posed precisely before: *how do you measure the amount of information in a message?*

His answer was the concept of entropy. The entropy of a message is a number, measured in bits, that captures how surprising the message is, or equivalently, how much uncertainty it resolves. A message you were almost certain was coming contains very little information. A message that was one of many equally likely possibilities contains a lot. Shannon gave a precise mathematical formula for computing this number, and he proved, with a theorem, that this number sets a hard lower limit on how efficiently you can encode the message. You cannot compress a message below its entropy without losing something.

The word "bit", short for binary digit, was used by Shannon's colleague John Tukey in the same period, and Shannon popularised it in this paper. A bit is the amount of information in the answer to a single yes/no question where both answers are equally likely. Everything else is built from that.

A note on the word "entropy", because it carries baggage. Shannon borrowed the term from thermodynamics, where it measures the disorder of a physical system: how many microscopic arrangements of particles are consistent with what you can observe at the macroscopic level. The more arrangements, the higher the entropy, and the less you can infer about the details. Shannon's entropy measures something structurally identical: how many possible messages are consistent with what you know before receiving one. More possible messages, higher entropy, more information in each one when it arrives. The formula is the same in both cases, and Shannon reportedly chose the name on the advice of John von Neumann, who pointed out that nobody really understood thermodynamic entropy either, which would give Shannon an advantage in debates.

The commonality is real: both entropies measure uncertainty over a set of possibilities. But the domains differ sharply. Thermodynamic entropy describes physical systems and points in a direction, time's arrow, because macroscopic disorder tends to increase in isolated systems. Shannon entropy describes probability distributions over messages and has no preferred direction. You can encode a high-entropy source and decode it perfectly. You cannot un-mix a cup of coffee. In an earlier article I explored a third framing, borrowed from Wolfram, in which entropy looks like the signature of computational irreducibility: the universe refusing to yield its future to any calculation shorter than running itself forward. That framing connects all three, but it is worth knowing they are distinct ideas that happen to share a name and a formula. If you want to follow that thread, the earlier piece on [Conway's Game of Life and computational irreducibility](/posts/game-of-life-may-2026/) picks it up from a different angle.

---

## What Each Step Actually Contributed

Let me put the chain together in a way I find useful to teach.

Aristotle contributed **the two-valued constraint**. A statement is true or false. No third option. This is the conceptual foundation without which none of the rest makes sense.

Llull contributed **the chain**. A sequence of yes/no questions can navigate any space of possibilities, however complex. Binary choice is not just a property of single statements: it is a method for systematically reaching conclusions.

Leibniz contributed **the representation system**. Any number, and it turns out any discrete state, can be represented as a sequence of 0s and 1s. Not because base 2 is mathematically special, but because it is the minimal base: the fewest possible symbols to build a positional system at all.

Boole, De Morgan, and MacColl contributed **the algebra**. Logical operations between truth values can be written as mathematical equations and manipulated mechanically. Four primitives, AND, OR, NOT, and identity, are sufficient to express every possible logical function. Logic becomes computable.

Gauss and Weber contributed **the physical demonstration**. Two electrical states on a wire are sufficient to carry any message. The minimal system Leibniz had identified mathematically turned out to be exactly what a physical channel could implement reliably.

Shannon contributed **two bridges**. The first was the bridge between Boolean algebra and physical circuits: he showed that logic could be *built* from switches. The second was the bridge between messages and mathematics: he showed that information is *measurable*, with a precise unit, and that there are hard limits on how efficiently it can be stored and transmitted.

The bit, as Shannon defined it, is not just a 0 or a 1 in the sense of a binary digit. It is a unit of *information content*, a measure of how much uncertainty was resolved by a message. This is the concept that makes digital communication an engineering discipline rather than an art. You can calculate how many bits a message contains. You can calculate how many bits per second a channel can carry. You can calculate the minimum number of bits needed to represent a source. Everything else in data compression, error correction, and channel coding flows from that.

---

## Why This Chain Matters

When I explain this to students, I find that the historical sequence helps with something that often confuses people: the difference between a 0 or 1 as a *symbol* and a bit as a *unit of information*.

Every bit you store on your hard drive is a 0 or a 1. But not every 0 or 1 carries one bit of information in Shannon's sense. If a file is entirely made up of the same byte repeated a million times, the redundancy means it can be compressed. The actual information content is much less than the number of binary digits used to store it. This is why compressed files are smaller. It is not magic. It is Shannon's entropy bound being used practically by a compression algorithm.

Understanding that distinction, symbol versus information content, takes the bit from being a vaguely understood unit ("how much storage I have on my phone") to being a precisely defined and deeply useful concept. And the reason the concept has that precision is the 2300-year chain we just walked through.

Aristotle cleared the ground. Llull showed you could chain binary questions into a method. Leibniz built the representation and identified base 2 as the minimal case. Boole, De Morgan, and MacColl built the algebra and proved four primitives are enough for everything. Gauss and Weber put two states on a wire. Shannon showed how to build logic from those states, and then measured how much information they could carry.

---

#### Image sources

- **Fig. 1:** Claude Shannon. Photograph by Konrad Jacobs. [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:ClaudeShannon_MFO3807.jpg), Mathematisches Forschungsinstitut Oberwolfach. [CC BY-SA 2.0 DE](https://creativecommons.org/licenses/by-sa/2.0/de/).
- **Fig. 2:** Bagua diagram. Illustration by the author. Public domain.

---

*In the next article, I pick up the thread where Shannon left off: from the Universal Approximation Theorem to the architecture of modern language models. If the first article asked "what is a bit and where did it come from", the second asks "what does a neural network actually do, and why does training it count as a form of intelligence?"*

If you want to talk through any of this, whether you are studying physics, electrical engineering, or just find these ideas interesting, come find us on Discord.

<div><a href="https://discord.gg/2BXuUY6hrX" class="link-card-discord" target="_blank" rel="noopener noreferrer"><i class="fab fa-discord"></i><div class="discord-text"><span class="discord-name">Discord — Full Stack Engineering</span><span class="discord-note">Direct access to me and my colleagues. Webinars, live Q&A, and community discussions for engineers across the full stack.</span><span class="discord-join">Join the server →</span></div></a></div>
