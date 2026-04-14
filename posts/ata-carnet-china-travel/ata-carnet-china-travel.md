---
layout: post
title: "Travelling to China with a Peli Case Full of Electronics"
date: 2026-04-07
tags: [china, travel, hardware, EMC, logistics]
description: "A practical guide for engineers taking commercial electronics to China for testing — ATA Carnet, Peli cases, Frankfurt T2, Guangzhou customs, and everything the internet doesn't tell you."
permalink: /posts/ata-carnet-china-travel/
---

When I went to Dongguan for [EMC testing in March](/posts/dongguan-emc-march-2026/), I brought a Peli case full of custom electronics as checked luggage. This post is the logistics companion to that trip — everything I learned about ATA Carnets, airport customs, and travelling with hardware that looks suspicious to anyone who doesn't build it.

![Peli case at the airport, ready for check-in](assets/peli-airport.jpg)

## Why Not Just Ship It?

Shipping electronics to China for testing and back is a customs nightmare. Import duties, VAT, potential seizure, weeks of waiting. The cleaner solution for temporary export of commercial goods is an **ATA Carnet** — essentially a passport for your equipment. You declare that you are taking specific items out of your home country, into a foreign country, and bringing them back. No duties, no VAT, as long as everything returns.

## Preparing the ATA Carnet

In Germany, ATA Carnets are issued by the **IHK** (Chamber of Commerce). My assistant Vanessa handled most of the paperwork, which I would strongly recommend if you have the option — the form requires a complete list of every item you're carrying, including descriptions, values, and serial numbers.

**The serial number point is important.** Every significant component needs one. We went through our modules and labelled anything that didn't already have a serial number. This paid off at every customs checkpoint: when an officer picks up a device and asks what it is, you point to the serial number, point to the list, and that's the end of the conversation. Without serial numbers, you're explaining what an Edge Compute Module is to a customs officer at 6am.

**Timeline in Germany:**
- IHK: approximately 4 business days from application to ready document
- Zollamt Bochum: about one hour in-person, no appointment needed

Go to the Zollamt in person. They check everything on the list against what you've actually packed, then stamp and sign the document. After that, you're cleared for departure.

## Packing

I used a Peli case with foam cut to fit. The system was packed snugly enough that nothing moved during the flight. I used two TSA-compliant locks.

One of them didn't survive the journey. On arrival in Frankfurt I found one lock broken — the TSA key had clearly been used at some point. The second lock was fine. If you're packing anything sensitive, assume the case will be opened in transit and pack accordingly. Nothing was missing or damaged inside.

## Frankfurt Airport: Terminal 2 and the Customs Process

If you're flying to China from Frankfurt, note that most China routes depart from **Terminal 2**. Allow an extra 15 minutes to get there, and plan at least 3 hours before departure if you're carrying ATA goods.

The process at check-in is slightly unusual. You check in at the desk to get your baggage tag — but then you ask for the bag back. Yes, they will be confused. Insist politely. You need to carry the tagged bag yourself to the customs office.

At the customs office, an officer goes through the entire list with you, item by item. Everything comes out of the case. Everything gets counted. Then it goes back in, gets stamped, and you carry the case to the bag drop that the officer directs you to. **Budget 60 minutes for this process** on your first time, possibly more. My assistant Vanessa's preparation made it significantly faster — the serial numbers meant I never had to explain what anything was, just confirm it matched the list.

## Arrival in China

At the Chinese customs on arrival, the process mirrors the German departure. Find a customs officer immediately — don't walk through the green channel. Show the ATA Carnet, let them inspect, they take one of the pages, sign the document, and you're done. It takes longer than in Germany. If someone is waiting for you, warn them in advance.

## Apps to Install Before You Leave

Install these before departure, not on arrival:

- **WeChat** — essential. Nearly everyone reachable for business in China responds faster on WeChat than email. You also need to wait a few days after installation before you can set a username, so install it early. You can add me: **MaxClerkwell**. Add your credit card too — WeChat Pay is the default payment method almost everywhere.
- **DiDi** — Chinese Uber. Works reliably, some premium drivers speak English. Every driver will have a bottle of water for you.
- **Trip.com** — hotels and train tickets.
- **Amap** — local maps. Google Maps works with a VPN but has gaps in business listings.
- **Google Translate** — download the English–Chinese language pack offline.

For connectivity: buy a **Holafly eSIM** before departure (~30 USD/week). Install it correctly before you get to the airport. European SIM data roaming costs are not worth it. Watch out for cheaper plans that prohibit hotspot sharing.

For everything else: set up a **WireGuard VPN** before you go. A self-hosted instance is better than a commercial VPN service. WhatsApp and Google work in China with this setup.

## The Guangzhou Departure

Leaving China on the return trip is the same process in reverse — except it takes longer. Guangzhou Baiyun Airport has an unusual arrangement where customs and the security check are sequenced in a way that requires you to pass through security with your full luggage including tools. I had a screwdriver set in the Peli case, which triggered additional checks since screwdrivers are not permitted through security onto the aircraft.

The resolution was diplomatic: I explained the situation, showed the ATA Carnet, and the officers were helpful in directing me to the right channel to drop the tools as checked luggage and continue to the gate. Chinese customs officers were, throughout the trip, genuinely curious rather than obstructive — several wanted to understand what the modules actually did. Being able to explain it simply (a measurement system for industrial ovens) was worth more than any amount of paperwork.

Allow **90 minutes** for the Guangzhou departure process if you're carrying ATA goods.

## On Arrival Back in Germany

Take the red channel, get the documents signed again on return. Then bring the completed ATA Carnet back to the IHK. This is a formal requirement — failing to return it means you may be liable for import duties on the declared value of everything you took.

## Summary Checklist

**Weeks before departure:**
- [ ] Install WeChat, set username, add payment card
- [ ] Apply for ATA Carnet at IHK (allow 4+ working days)
- [ ] Label all items with serial numbers
- [ ] Buy Holafly eSIM, install and test before airport
- [ ] Set up WireGuard VPN
- [ ] Buy TSA-compliant locks (assume they will be used)

**At Frankfurt airport:**
- [ ] Depart from Terminal 2 (most China routes)
- [ ] Allow 3 hours before departure
- [ ] Check in, get baggage tag, take bag back
- [ ] Go to customs office with ATA Carnet — plan 60 min
- [ ] Drop bag where customs officer directs you

**On arrival in China:**
- [ ] Go directly to customs, do not use green channel
- [ ] Present ATA Carnet without hesitation

**Returning from China (Guangzhou):**
- [ ] Allow 90 minutes for customs + security
- [ ] Pack tools in checked luggage or be prepared to check them separately

**Back home:**
- [ ] Return completed ATA Carnet to IHK

---

*Questions about factory visits in China or EMC testing? Hit me up on [WeChat or X](/).*
