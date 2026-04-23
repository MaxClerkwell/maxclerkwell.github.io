---
layout: post
title: "DBMS 01: Why a Filesystem Is Not a Database"
date: 2026-04-23
tags: [databases, teaching, THGA, SQL]
description: "A practicum that makes the case for relational databases by forcing students to feel the pain of querying flat files first."
permalink: /posts/dbms-01-why-files-are-not-enough/
---

Yes, I'm aware: nobody in production actually stores sensor data as 120 CSV files in a flat directory. At least I hope not. But that's precisely why this works as a teaching exercise — it's artificial enough to be harmless, and realistic enough to sting.

The first practicum I built for the DBMS course at THGA Bochum ([DBMS_01](https://github.com/MaxClerkwell/DBMS_01)) doesn't teach students how SQL works. It teaches them why SQL exists.

## The Setup

Students generate synthetic sensor data: temperature readings from four sensors, three times a day, over thirty days. That's 120 CSV files and 360 rows total. Nothing exotic. Exactly the kind of mess that accumulates when a small team decides "we'll figure out the storage later."

Then they solve three tasks:

1. Filter and sort readings from one specific sensor.
2. Find all measurements above a threshold within a date range.
3. Compute min, max, and average per sensor across the full dataset.

Twice. Once with shell tools. Once with SQL against a SQLite database.

## Where It Breaks Down

Task 1 is fine. `grep`, `sort`, done. Everyone feels good about themselves.

Task 2 is where the cracks appear. Date range filtering across files *named by date* means matching filenames against a range, looping, and then filtering contents. It works. It's just longer than it has any right to be for such a simple question.

Task 3 breaks the illusion completely. Aggregating across 120 files while tracking per-sensor state requires either a temporary file, an associative array, or a nested loop. At this point the shell script isn't solving a data problem anymore — it's solving a parsing problem that shouldn't exist.

The SQL versions stay flat. Three lines for Task 1. Five for Task 2. One `GROUP BY` for Task 3.

## The Thing That Lands

The shell pipeline tells the computer *how* to find the answer. SQL tells the database *what* the answer looks like.

That distinction — imperative vs. declarative — is easy to define on a slide and very hard to actually feel. Students who write the shell version first and then write the SQL version have the comparison running in their heads. No slide needed.

## Why SQLite

No server. No installation. No credentials. `sqlite3 sensors.db` and you're in.

Every removed obstacle is a removed excuse for the concept not to land. The goal is for students to spend their cognitive budget on the query language, not on connection strings.

## What This Doesn't Cover

Transactions, normalization, indexing, query planning — all of that comes later. This practicum makes exactly one claim: *for structured data you need to query, a database gives you a better language than a filesystem does.*

Once you've felt that, rather than been told it, everything else builds on solid ground.

The repository is open: [github.com/MaxClerkwell/DBMS_01](https://github.com/MaxClerkwell/DBMS_01).
