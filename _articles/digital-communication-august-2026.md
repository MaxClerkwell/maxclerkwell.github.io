---
title: "Digital Communication: Getting a Thought Out of One Head and Into Another"
date: 2026-08-21
tags: [communication, electronics, embedded, signal-integrity, information-theory, education]
description: "Communication has one job: move the internal state of one system into another. This is a walk from a thought in your head to a wave on a wire, through the four sides of a message, a water canal, a push-pull driver, Shannon's channel, and the eye diagram that measures it all."
keywords: "digital communication explained, serialization, Shannon channel model, Schulz von Thun four sides, bus protocol, signal integrity, crosstalk, eye diagram, BCD code, communication theory"
math: true
---

*Communication has exactly one job. Everything else about it, the words, the wires, the protocols, the noise, is machinery in service of that one job.*

---

## The Mandate

You have a model in your head. It has no clean shape. It is made of pictures, feelings, memories, half-formed intentions, a smell from last summer, a plan for tomorrow. It is entirely yours, and as long as it stays inside you it is useless to anyone else.

The moment you want to cooperate, that changes. Cooperation means two systems acting on a shared understanding, and a shared understanding requires that the model in your head somehow also come to exist in someone else's. If we rule out telepathy for the moment, the only thing you can do is take that internal, shapeless state and push it out through whatever channels you have available so that another person can pick it up and rebuild a copy of it inside themselves.

This is the mandate, and it never changes: **move the internal state of one system into another.** Hold on to that sentence. Every layer we add from here, human or electronic, is just a different way of carrying it out.

As humans we have a rich set of tools for the job: words, gestures, facial expressions, hand signals, sounds, drawings, music. What all of them have in common is that they are ways of *serializing* a model. Your inner state is high-dimensional and parallel; a channel is narrow and mostly sequential. So you flatten the model, stream it out symbol by symbol over the channels you have, and trust that the receiver on the other end can take that stream and reconstruct the state inside their own head.

## The Same Problem, in Silicon

Now look at a microcontroller, and you will find the identical problem wearing different clothes.

Inside my program I have a data structure. Maybe it holds a measured state: a temperature, a set of flags, a timestamp. It lives in memory as a particular arrangement of bits, meaningful only inside this one processor. If a second processor is to act on that measurement, the arrangement has to be reproduced over there.

So a driver takes the structure, serializes it into a stream of symbols, and imprints that stream onto a bus. On the far side, another processor with the matching bus receivers picks the stream back up and reconstructs the structure in its own memory. Sender, serialization, channel, reception, reconstruction. It is the same five steps, and it is the same mandate. A person talking and a chip driving a bus are solving one problem at two scales.

## A Message Has More Than One Side

Human communication theory noticed long ago that a single message is never just its literal content. Paul Watzlawick and, in more structured form, Friedemann Schulz von Thun described a message as having four sides at once. The interesting thing is that all four reappear, almost one to one, in a digital bus frame.

- **Self-revelation** (*Selbstoffenbarung*): what the sender discloses about its own state. On a bus this is the status information a node reports about itself: its mode, its health, its measured values.
- **Appeal** (*Appell*): what the sender wants the receiver to do. These are the commands, the writes, the "set output high", the "start conversion".
- **Relationship** (*Beziehung*): what the message says about how sender and receiver stand to each other, how much they trust and are aligned. On a bus this is the control apparatus wrapped around the payload: the addressing, the acknowledgements, the checksums and CRCs. It is the layer that says "you and I agree on the terms of this exchange, and here is the proof that I am speaking to you correctly".

The fourth side is the one that is most obvious in hindsight, because it is the part we usually think *is* the whole message: the **factual content** (*Sachinhalt*). It is the raw payload, the number, the data field itself. Strip away who is sending it, what they want done with it, and the machinery that proves the frame's integrity, and there is still a bare fact being conveyed. In a bus frame it is simply the data bytes sitting between the header and the checksum.

Four sides in a human sentence, four fields in a frame. The overhead you see wrapped around every payload on every serious bus is not bureaucracy; it is the electronic version of tone, stance, and intent riding along with the words.

## You Still Need Something Physical to Push On

None of this moves without a physical channel: something the sender can modulate and the receiver can sense.

Take air pressure. With my breath, my vocal cords, and the shape of my mouth and throat, I set the air vibrating in specific patterns. Those pressure waves travel outward, and the receiver's eardrum vibrates in sympathy. First the ear filters the signal physically, by mechanical resonance, and only then do circuits in the brain get to work, unpacking the pattern step by step and in parallel until a meaning falls out.

## When the Ends Are Far Apart

Now push the sender and receiver so far apart that they can no longer see or hear each other directly. The channel of open air gives out. What can we do?

One option is to *guide* the physical excitation instead of letting it spread. Speak into a long pipe, and the pressure wave, instead of dissipating in every direction, propagates along the tube and arrives with far more of its energy intact. The speaking tube on old ships is exactly this idea.

Here is a stranger alternative that makes the underlying principle unmistakable. Run a long water canal from sender to receiver. Before we start, both parties agree on a protocol, a contract that says what the signal will mean. Now the sender pours a bucket of water into their end. A wave travels down the canal, and after a while the level at the receiver's end rises. Or the sender scoops water out, and after a while the far level drops.

Two states, level-up and level-down, look like almost nothing. But if the protocol is good enough, two states are plenty. The trick is to stop trying to send whole complex symbols at once, and instead serialize each symbol into a *chain* of these tiny information units. We invent new, coded symbols: agreed sequences of highs and lows that stand for the larger pieces of meaning. BCD is one such scheme, four level-changes standing in for one decimal digit. Give me a reliable two-state channel and a code, and I can send you anything.

## From Water to Wire

Swap the water canal for an electrical conductor and the picture snaps into focus as a real digital bus.

Now the sender is a push-pull stage. To send "high" it floods the line with electrons; to send "low" it pulls them back off. On the receiving end a comparator with a fixed threshold decides, at each moment, whether the level is above or below the line, and reconstructs the stream of highs and lows. Push-pull and comparator are just the bucket and the water-level gauge, moving far faster.

And the same subtleties survive the translation. The signal still takes *time* to arrive: a wave has to propagate down the wire, exactly as it did down the canal. More surprising, and worth sitting with: the information does not really travel *inside* the wire. The conductor only guides it. The signal is a field arrangement around and along the line, and the wire is a rail that keeps that arrangement aimed at the receiver.

You can tell this is true precisely because it can be disturbed from outside. On a high-speed bus, a neighboring line's switching field couples into yours, and you get crosstalk. A "loud" switching voltage regulator sitting nearby can inject enough of its own field to make a clean signal hard to read. Back in the world of our speaking pipe, the equivalent is a diesel generator the pipe happens to run past: it radiates its own noise straight into the channel, and now the receiver has to separate your words from the engine. The channel was never sealed. It was only ever guided, and anything that can reach the guide can add to the signal.

## Shannon Drew the Same Picture

In 1948, Claude Shannon gave this whole story its canonical diagram, and everything above is a retelling of it. His model is a straight line of five boxes with one arrow coming in from the side:

**information source → transmitter → channel → receiver → destination**, with a **noise source** injecting into the channel.

Map it onto what we already built and it lines up exactly. The information source is the model in your head, or the struct in memory. The transmitter is your vocal tract, or the push-pull driver, doing the serialization and modulation. The channel is the air, the pipe, the canal, the wire. The receiver is the ear, or the comparator. The destination is the reconstructed model in the other head, or the reconstructed struct in the other processor. And the noise source, entering at the channel and nowhere else, is the diesel generator, the crosstalk, the loud regulator.

Shannon's real contribution was to make this quantitative. He showed that a channel with bandwidth $B$ and a signal-to-noise ratio $S/N$ has a hard ceiling on how many bits per second you can push through it error-free:

$$
C = B \log_2\!\left(1 + \frac{S}{N}\right).
$$

Read that formula against everything so far and it says something almost obvious in hindsight. Your throughput is bounded by how fast you can wiggle the channel ($B$) and by how far your signal stands above the noise ($S/N$). The diesel generator does not just annoy you; it lowers $S/N$ and, with it, the number of bits the channel can ever carry. Noise is not a nuisance layered on top of communication. It is one of the two terms that decide what communication is even possible.

## Where We Are

Step back and the arc is simple. Communicating a message is how the internal representation of one processor, silicon or biological, is transferred into another. But the channel alone is not enough. A wire, a canal, or a column of vibrating air only carries meaning if both ends run the same protocol: the same conventions, the same agreement about which pattern stands for what. Without that shared contract the signal arrives perfectly intact and means nothing. The physics delivers the envelope; the protocol is what lets the receiver open it. And the channel is never private either: disturbances can always couple in, and they set a ceiling on what can get through.

## Measuring the Channel Without Reading the Message

There is a beautiful last move here. Because all of this is content-independent, we can judge the *quality* of a link without caring what it is saying.

Put an oscilloscope on the line and overlay every received symbol period on top of each other, aligned to the clock. The individual bits blur together into a shape called an **eye diagram**: a bright open region in the middle, framed by the tangle of rising and falling edges. That open "eye" is the margin the receiver has to work with. A wide, tall eye means the comparator can pick high from low with room to spare. A collapsing eye, edges smeared by crosstalk, levels pulled together by a noisy regulator, jitter blurring the timing, means the receiver is being asked to decide in a shrinking window, and errors are coming.

The elegance is that none of this depends on the payload. You are not reading the data; you are measuring the shape it leaves behind. Content-independent quality metrics, jitter, noise margin, eye height and width, let you say how good a channel is before you have decoded a single meaningful bit through it. It is the same physical mandate we started with, now turned into something you can put a number on and watch on a screen.

This is exactly what I showed in a couple of short Instagram videos, if you want to see a real eye diagram open and close on a scope instead of just reading about it:

<div style="display: flex; flex-wrap: wrap; gap: 1em; justify-content: center; margin: 1.5em 0;">
  <iframe
    src="https://www.instagram.com/reel/DbBlZC-taQJ/embed/"
    width="326"
    height="560"
    title="What are eye diagrams?"
    frameborder="0"
    scrolling="no"
    allowtransparency="true"
    allowfullscreen
    style="border-radius:6px; max-width:100%;"
  ></iframe>
  <iframe
    src="https://www.instagram.com/reel/DbGlh0xsOt-/embed/"
    width="326"
    height="560"
    title="More about eye diagrams"
    frameborder="0"
    scrolling="no"
    allowtransparency="true"
    allowfullscreen
    style="border-radius:6px; max-width:100%;"
  ></iframe>
</div>

*Communication had exactly one job. From a thought in your head to a wave on a wire, it never stopped being the same job.*
