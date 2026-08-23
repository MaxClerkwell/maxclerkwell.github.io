---
title: "Physics Doesn't Explain Anything. And That's the Point."
date: 2026-06-04
tags: [physics, philosophy, education]
description: "My high school teacher told me physics explains the world. Years later I think that's completely wrong, and understanding why changes everything about how you approach the subject."
---

When I was in school, my physics teacher told me that physics *explains* the world.

I believed that for years. It sounded profound. It gave the subject a kind of grandeur, as if sitting through enough lectures about pendulums and ideal gases would eventually unlock some deep understanding of why reality is the way it is.

Today I think that framing is completely wrong. Not slightly off, not a useful simplification: wrong in a way that actively misleads people about what physics is and what it is for. And I think this misunderstanding is one of the main reasons students either develop an inflated reverence for the subject or walk away from it feeling like they missed something fundamental.

Physics does not explain the world. Physics *describes* it.

That is a small grammatical shift with enormous consequences.

---

## What Description Actually Means

To explain something is to give an account of *why* it is the way it is. To describe something is to document *how* it behaves reliably enough to be useful.

Physics is firmly in the second camp.

When Newton wrote down his law of universal gravitation, he was not explaining why mass attracts mass, or what the underlying mechanism of gravity is. He was documenting a relationship. "If you have two masses at this distance, the force between them will be this number." That relationship holds across an extraordinary range of circumstances. It let humans put spacecraft on precise trajectories to the outer planets. It is enormously useful. But it does not tell you *why* gravity exists. It tells you *how much* of it you will find, and *when* it matters.

Newton himself was quite honest about this. His famous phrase *hypotheses non fingo* ("I feign no hypotheses") was a direct statement that he was describing what he observed, not proposing a deeper cause.

The question "but *why* does gravity work like that?" is either a philosophical question, a question for a different and deeper layer of physics, or simply a question that nobody has answered yet. What physics gives you is the reliable relationship. The why, if it exists at all, keeps retreating one level deeper every time you think you have caught it.

---

## So Why Do We Do It?

If physics is not explaining the universe, what is the point?

The answer is practical and it is important to say it plainly: we build physics in order to build technology.

To make a machine do something useful, whether diverting water, holding a structure under load, moving heat from one place to another, or transmitting information, you need to trust that certain relationships will hold tomorrow the same way they held yesterday. You need rules you can rely on. *If A, then B.* Not approximately, not sometimes, but reliably enough that you can stake your design on it.

Physics is the process of finding, testing, and formalising those relationships. The output is a toolbox of formulas, models, and methods that engineers can use to simulate the effect of an action before committing to it in metal and money.

That is not a diminished vision of physics. It is an honest and rather extraordinary one. Every bridge, every microprocessor, every satellite, every chip fabrication plant: none of these were possible without honest observers using the most precise instruments they could build, documenting what they found, and abstracting it into mathematical language that someone else could use as a design tool.

That is what physicists do. They generate reliable descriptions of the world at a level of precision and generality that can be handed forward.

---

## States and Processes

Most of physics, once you strip away the particular domain (mechanics, thermodynamics, electrodynamics, quantum theory), reduces to two things: **states** and **processes that change states**.

A state is a snapshot. The position and momentum of a particle. The temperature and pressure of a gas. The charge distribution across a capacitor. The orientation of a spin.

A process is a rule that maps one state to another over time. A differential equation. A collision law. A decay probability.

Within physics, these two activities have actually split into distinct cultures. Experimentalists spend most of their working lives figuring out how to measure states as precisely as possible: designing instruments, controlling noise sources, and pushing the limits of what can be observed. Theorists spend most of their working lives on the other half: developing the mathematical framework that describes how to get from one state to another under given environmental circumstances. The two communities need each other. A theorist without experimental constraints produces untestable speculation. An experimentalist without theoretical guidance is collecting data with no idea what it means. The rest of the apparatus, the notation, the specialised vocabulary, the mathematical machinery, is infrastructure for making that collaboration work.

When you understand this, a lot of the apparent mysticism around physics dissolves. You are not trying to access some hidden truth about reality. You are building a model that predicts the next state from the current one, and checking how well it performs against measurement. When the model performs well enough, engineers can use it. When it breaks down, physicists go back and refine it.

---

## The Human Animal and Its Workaround

Most animals adapt to their environment. Evolution tunes them over generations to fit the niche they occupy. A beetle optimises for a particular humidity range, a particular diet, a particular set of predators.

Humans do something different. We adjust the environment to fit ourselves.

Joe Rogan, in a [recent podcast with astrophysicist Michelle Thaller](https://youtu.be/GZCmYrgOZU0?si=Q5U7YATSzNcmDrT6), made an observation that stuck with me. He described humans as something like "the electronic caterpillar": a species that just keeps building, keeps improving, never quite deciding that the current version of the hive is good enough. His point was that bees, at some stage, arrived at a design that was sufficient and stopped there. Humans never did that. Innovation seems to be our evolutionary program.

Physics is one of the most powerful tools we developed in service of that program.

We do not adapt fast enough biologically to deal with cold climates, deep water, the vacuum of space, or infectious disease at scale. So instead we build a layer between ourselves and the universe that compensates. Insulation, submarines, spacesuits, antibiotics. None of these require the universe to change, and none of them require us to change genetically. We build a hardware abstraction layer between our bodies and raw physical reality, and that layer gets thicker and more capable every generation.

This framing comes naturally to me from working with microcontrollers. A microcontroller is, in one sense, a device that makes a specific chunk of physics behave predictably at a level of abstraction a programmer can use without worrying about electron transport in silicon. Physics is the bedrock. Engineering stacks abstraction layers on top until the underlying complexity is hidden. The programmer does not need to understand quantum tunnelling to blink an LED. But someone, at some point, had to understand it well enough to design the transistor.

That someone was a physicist.

---

## The Limits of Description

At this point you might object: if physics is about building reliable predictive models, can we not, in principle, make those models arbitrarily precise? Given enough instruments and enough computation, could we not simulate anything?

This is where two concepts come in that most people do not fully reckon with.

### Heisenberg's Uncertainty Principle

The first limit is one you may have heard of: Heisenberg's uncertainty principle. In its most common form, it states that the more precisely you know the position of a particle, the less precisely you can know its momentum, and vice versa. This is not a limitation of instruments. It is not merely a matter of disturbing the particle when you measure it, though that intuition is not entirely wrong. It is a fundamental feature of how quantum systems work: the state you are trying to measure does not have a determinate value for both quantities at once.

This has been tested, contested, and tested again for nearly a century. Every experiment designed to disprove it has failed. At this point we treat it as a hard constraint on what physics can ever tell us about initial conditions, which means it is a hard constraint on how well we can predict future states.

### Wolfram's Computational Irreducibility

The second limit is less well known, and I find it even more unsettling.

I wrote about Wolfram and computational irreducibility in an earlier post on [Conway's Game of Life](/posts/game-of-life-may-2026/), where I approached it as a question about entropy and the direction of time. Here I want to take a different angle: what does it mean for physics as an engineering tool?

The basic idea, briefly: for certain systems, there is no shortcut. The only way to know what state the system will be in after a million steps is to run all million steps. No formula collapses the computation. The future is not analytically reachable from the present; the system must be lived through, not solved.

In the earlier post I used this to ask whether entropy might be the signature of irreducibility, a measure not just of disorder but of how far ahead the universe refuses to be calculated. That framing was about understanding nature. Here I want to use the same concept to ask a more operational question: what does this tell us about the *reach* of the models we hand to engineers?

Imagine a sealed box at zero degrees Celsius. You place one ball inside and take all the time you need to measure its position and momentum as precisely as the laws of physics allow. You close the box.

After an instant, the ball is essentially where you left it. Easy.

After one second, using Newtonian mechanics and elastic collision laws, you can estimate its state quite well. Some accumulated error from measurement uncertainty, some from the Heisenberg floor, but the prediction is good.

After a thousand seconds, the errors compound. Every collision introduces a small deviation between your model and reality. Heisenberg's floor means the initial conditions were never perfectly known. And here is where computational irreducibility bites: even if they *were* perfectly known, the future state of a sufficiently complex system is not analytically reachable. You must simulate every intermediate step.

But the universe is not computing a shortcut on your behalf while you run your simulation. The universe *is* the simulation. The collisions are happening, the uncertainty is propagating, and the future state is being produced by the actual execution of physical processes, not by any equation that represents them. The equations are our map. The territory does not care about the map.

What this means, practically, is that there is no oracle anywhere in the universe that can tell you the exact future state of any sufficiently complex system without running that system forward in real time. No superintelligence, no Laplacian demon, nothing. The computation required to determine the future is embedded in the fabric of the universe itself and cannot be shortcut.

Physics does not give us a window into the future. It gives us progressively better approximations, valid over progressively longer ranges, with progressively smaller errors. But perfect prediction at infinite time? Not on the menu. Not because we have not worked hard enough. Because it is structurally impossible.

---

## Does This Make Physics a Fool's Errand?

Not at all. Quite the opposite.

The fact that perfect prediction is impossible does not mean imperfect prediction is worthless. The gap between *no reliable model* and *a good enough model* is the difference between medieval engineering and modern civilisation.

You do not need to know exactly where an electron will be in ten years to design a transistor that works reliably for twenty. You need to know the probability distributions well enough to choose the right doping concentrations and oxide thicknesses. Physics gives you that. It does not give you certainty. It gives you a compressed, testable, transmissible description of how the world tends to behave, and that description is extraordinary.

The recognition that physics describes rather than explains, that all models are approximations, and that fundamental limits exist on prediction: these do not undermine the project. They clarify it. They tell you what you are actually doing when you do physics, and they tell you why the project is worth doing even though it will never be finished.

There is something honest and even liberating about this. You are not hunting for final answers. You are building better tools. The universe is not going to yield its secrets, but it will, under patient and quantitative attention, reveal how it tends to behave. That turns out to be enough. More than enough, actually. We built everything we have on the back of that much.

---

## A Note for People Considering Their Education

If you are thinking about studying engineering, or if you already have an engineering degree and are wondering whether going back for physics would be worth your time, I want to say something directly.

It would.

Engineering education, in my experience, tends to hand you formulas and teach you when to apply them. Physics education hands you the process by which those formulas were derived and teaches you how to derive new ones when the existing ones stop working. Those are genuinely different skills. The engineer who understands where their formulas come from is better at knowing when to trust them and when to go looking for something better.

A physicist learns how to observe, how to measure, how to identify the relevant state variables for a given system, and how to build mathematical models that are honest about their own assumptions. That is a very different cognitive toolkit from the one you build by solving textbook problems in applied statics.

I am not saying one is better than the other. I am saying they are complementary in a way that the education system does not always make clear, and the combination is remarkable. If you can afford the time, pursue both. If you are early in your trajectory and can only pick one to start, physics first will give you a foundation that engineering can build on. The converse is harder.

The universe is not going to hand us a complete theory of everything on a silver platter. But it will, under the right kind of patient, honest, quantitative attention, keep showing us how it behaves. Understanding that this is the real goal, description and not explanation, tools and not truth, is the thing my high school teacher forgot to tell me. If you are standing at the beginning of your education and trying to decide which door to walk through first, I wrote a longer piece on exactly that question: [Physics, Math, or Engineering: How Do You Decide?](/posts/physics-math-or-engineering-how-do-you-decide/)

I hope it is less of a surprise to you.

---

*If you want to read more about computational irreducibility and the deeper question of whether the universe itself might be a computational process, the earlier post on [Conway's Game of Life and the limits of prediction](/posts/game-of-life-may-2026/) picks up that thread from a different angle.*

If you want to talk about any of this, come find us on Discord.

<div><a href="https://discord.gg/2BXuUY6hrX" class="link-card-discord" target="_blank" rel="noopener noreferrer"><i class="fab fa-discord"></i><div class="discord-text"><span class="discord-name">Discord — Full Stack Engineering</span><span class="discord-note">Direct access to me and my colleagues. Webinars, live Q&amp;A, and community discussions for engineers across the full stack.</span><span class="discord-join">Join the server →</span></div></a></div>
