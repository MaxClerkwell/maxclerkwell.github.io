---
title: "From the UAT to the Modern Neural Network"
date: 2026-07-03
tags: [ai, information-theory, history, education]
description: "We have the bit. Now the question is what we can compute with it, and whether a machine can learn to compute things nobody explicitly programmed. The answer runs from Hilbert through Turing to a theorem most engineers have never heard of."
---

The previous article ended with a precise unit: the bit, as Shannon defined it, measures how much uncertainty a message resolves. We have a way to represent information. We have a way to build logical operations from switches. We know, from Gauss and Weber, that a wire can carry two distinguishable states. The question this article asks is the next one in the chain: *what can we actually compute with all of this, and is there a limit?*

That question turns out to be older than the computer. It starts with a mathematician who wanted to mechanise all of mathematics, runs through a logician who showed that was impossible, and ends with a computer scientist who redefined what "mechanical" even means.

---

## Hilbert's Question: Can a Machine Decide Everything?

In 1928, David Hilbert posed what he called the *Entscheidungsproblem*, the decision problem. The question was this: is there a mechanical procedure that, given any mathematical statement, can decide in a finite number of steps whether the statement is true or false?

Hilbert's hope was that mathematics was complete (every true statement is provable), consistent (no contradictions exist), and decidable (there is an algorithm for each question). This was not naive optimism. It was a serious research programme, and Hilbert believed it could succeed.

Three years later, in 1931, Kurt Gödel demolished the first two hopes. His incompleteness theorems showed that any sufficiently powerful formal system contains true statements that cannot be proved within that system, and that no such system can prove its own consistency. Mathematics is not complete. There are truths that lie beyond the reach of any fixed set of axioms.

This did not yet answer Hilbert's third question. Even if some truths are unprovable, there might still be a mechanical procedure that always terminates with a correct yes or no. That question required a different kind of answer: not a proof about what mathematics contains, but a precise definition of what "mechanical procedure" means in the first place.

---

## Turing's Answer: The Machine as a Definition

In 1936, Alan Turing published "On Computable Numbers, with an Application to the Entscheidungsproblem". What he did was unusual. Instead of taking "mechanical procedure" as an informal concept and arguing about it, he defined it: a mechanical procedure is precisely what can be carried out by what we now call a Turing machine, an abstract device with a tape, a read/write head, and a finite set of rules for transitioning between states.

This definition was not a restriction. Turing argued, convincingly, that anything a human could compute by following explicit rules could be computed by such a machine. The definition captured the concept.

With the definition in hand, Turing could answer Hilbert's question exactly. He proved that no Turing machine can solve the *halting problem*: given an arbitrary program and an input, determine whether the program will eventually stop or run forever. Because deciding all mathematical statements would require solving the halting problem, the Entscheidungsproblem has no solution. There is no universal decision algorithm.

The negative result is not what I want to emphasise here, though. What matters for our chain is the positive content of Turing's definition: a complete, precise account of what computation is. Any computation is a process that reads a finite input, follows deterministic rules, and produces a finite output. It takes in data, transforms it, and produces data. That pattern, data in and data out, is the foundation everything else in this article rests on.

---

## Every Program Is a Function

Shannon had already shown that logical operations can be built from switches. Turing showed that any computation can be expressed as a sequence of such operations. Put those two results together and you get something important: *every program that terminates is a function*.

It takes an input, which is a finite sequence of bits, and it produces an output, which is another finite sequence of bits. The same input always produces the same output (for a deterministic program). That is the definition of a mathematical function. A sorting algorithm is a function from unsorted lists to sorted lists. An image classifier is a function from pixel arrays to label strings. A language model, at inference time, is a function from a token sequence to a probability distribution over the next token.

I want to make this concrete with a schema, because I think it cuts through a lot of confusion: DATA + DATA gives you TRANSFORMATION gives you DATA. The first DATA is your input. The second DATA is the program itself (its weights, its rules, its parameters), which is also just a sequence of bits stored somewhere. The TRANSFORMATION is the act of running the program. The final DATA is the output. Nothing in this picture requires consciousness, understanding, or anything mysterious. A running program is a function being evaluated.

This reframing matters because it connects computation directly to mathematics, and specifically to the question of which functions are computable and how well they can be approximated.

---

## The Approximation Tradition: Gauss, Runge, and Kutta

Before we get to neural networks, I want to make an argument that is rarely made explicitly: the idea that you can *learn* a function from data did not appear from nowhere in the 1980s. It has roots in numerical mathematics that go back to the 19th century, and without those roots, the Universal Approximation Theorem would have been much harder to conceive.

Carl Friedrich Gauss, in 1809, formulated the method of least squares: given a set of noisy observations, find the function (within a specified family, say, polynomials of a given degree) that minimises the sum of squared differences between the function's predictions and the observations. This is, in structure, exactly what a neural network trainer does. You have data. You have a family of functions parameterised by numbers. You minimise an error measure. The conceptual template was there two centuries before backpropagation.

Gauss-Jordan elimination, the method for solving the linear system that arises from the normal equations of least squares, made that minimisation computationally tractable. It gave engineers a systematic, mechanical procedure for finding the parameters that best fit a dataset, within the class of linear models.

Carl Runge and Martin Wilhelm Kutta, working in the 1890s, contributed a different but equally important idea: iterative numerical integration of differential equations. If you cannot find a closed-form solution to an equation describing how a system evolves, you can instead take many small steps, updating your estimate of the solution at each step. The error accumulates, but with small enough steps and a good enough scheme, the approximation converges to the true solution.

That structure, iterating small updates toward a solution you cannot reach in closed form, is the computational backbone of gradient descent. Training a neural network is Runge-Kutta applied to a loss landscape instead of a differential equation. Without a century of experience showing that iterative numerical methods converge reliably, the proposal to train a network by repeatedly nudging its parameters in the direction of decreasing error would have looked much more speculative than it did.

---

## The Banach Fixed Point Theorem: Why Iteration Converges

The mathematical guarantee behind all of this is the Banach fixed point theorem, proved by Stefan Banach in 1922. It says: if you have a mapping that is a contraction (each application brings two points strictly closer together), and the space you are working in is complete, then iterating the mapping from any starting point will converge to a unique fixed point.

Gradient descent, under appropriate conditions on the loss function and the step size, is a contraction. Each update step moves the parameters closer to a minimum. The theorem guarantees not only that the process converges, but that it converges to the same place regardless of where you start, provided the contraction conditions hold. In practice, the loss landscapes of deep networks are far too complex for Banach's conditions to hold globally. But the theorem explains why the procedure works at all, and it tells you what to look for when it does not: a step size that is too large breaks the contraction, and a loss landscape with many local minima means Banach's uniqueness guarantee no longer applies.

---

## The Universal Approximation Theorem

With all of that in place, we can state the central result.

In the mid-1950s, at the Dartmouth conference that inaugurated the field of artificial intelligence, researchers were already circulating informal versions of a powerful conjecture: that a network of simple threshold units, given enough of them, could approximate any function. The intuition was compelling. Turing had shown any computation is a function. Boolean algebra had shown any logical function can be built from a handful of primitives. The leap was to ask whether something similar held for the much broader class of continuous functions.

The formal proof had to wait. In 1989, George Cybenko proved a precise version for networks with sigmoid activation functions: a single hidden layer with sufficiently many neurons can approximate any continuous function on a compact subset of real-valued inputs to any desired accuracy. In 1991, Kurt Hornik extended this to arbitrary nonlinear activation functions and removed several technical restrictions.

The theorem makes a striking claim. You do not need to design a function by hand. You do not need to know in advance what the function looks like. Given enough neurons, the right architecture, and a training procedure, a network can approximate any continuous input-output relationship from data alone.

This is where the connection to Gauss closes: least squares found the best linear approximation within a fixed function family. The UAT says that with a neural network, the function family is rich enough to contain an approximation to *anything*. The training procedure (gradient descent, Banach's iteration) finds it.

Two caveats matter here and are often missed. First, the theorem guarantees existence: there is a network that approximates the function. It says nothing about how to find it, how much data you need, or how many neurons are required. Second, approximation is not the same as representation. A network that approximates a function to within 0.01 on a test set may behave completely differently outside that set. The theorem is a licence to try, not a guarantee of success.

---

## From UAT to Modern Architectures

Once the UAT established that the approximation game was worth playing, the history of deep learning is largely the history of building better function families and better trainers.

Frank Rosenblatt's perceptron (1957) was the first learned classifier: a single-layer network trained by a simple update rule. Minsky and Papert showed in 1969 that a single layer cannot separate all patterns (the XOR problem), which required the multi-layer networks the UAT had theoretically justified. Backpropagation, developed through the 1970s and popularised by Rumelhart, Hinton, and Williams in 1986, gave us the trainer: a systematic way to compute how much each weight contributed to the error and adjust it accordingly.

The architectures that followed are each a different answer to the question "what structure should the function family have?". Convolutional networks (LeCun, 1998) built in the knowledge that spatial patterns are translation-invariant. LSTMs (Hochreiter and Schmidhuber, 1997) built in sequential memory. Transformers (Vaswani et al., 2017) built in the ability to attend to arbitrary positions in a sequence, with no assumption about locality. AlphaFold, GPT, diffusion models: all of them sit on the UAT's foundation. They are different choices of structure for the approximating function and different strategies for training it.

The "intelligence" in all of these systems does not live in the trained model. At inference time, a network is a fixed deterministic function: x in, y out. The same input always produces the same output. What makes it remarkable is its origin: it was not written by hand. A trainer searched a vast space of possible functions and found one that fits the data. That search, and the choice of what space to search in and what to optimise for, is where all the interesting decisions are made.

---

*These two articles have traced a single line from Aristotle's two truth values to the architectures that underpin modern language models. The bit is the atom. The Turing machine is the definition of computation. The UAT is the licence to approximate. Training is Gauss's least squares generalised by Banach's convergence guarantee. Every transformer, every diffusion model, every large language model is an instance of that chain, searched rather than written.*

If you want to talk through any of this, come find us on Discord.

<div><a href="https://discord.gg/2BXuUY6hrX" class="link-card-discord" target="_blank" rel="noopener noreferrer"><i class="fab fa-discord"></i><div class="discord-text"><span class="discord-name">Discord — Full Stack Engineering</span><span class="discord-note">Direct access to me and my colleagues. Webinars, live Q&A, and community discussions for engineers across the full stack.</span><span class="discord-join">Join the server →</span></div></a></div>
