---
layout: post
title: "A Database Is Not an API"
date: 2026-04-24
tags: [databases, architecture, FastAPI, Keycloak, nerd_force1]
description: "Why we never expose a database directly — and what we put in front of it instead."
permalink: /posts/databases-behind-an-api/
---

When we set up databases for clients at [nerd_force1](https://nerd-force1.com), one rule holds without exception: the database is never the outermost layer. This post explains why, and what we put in front of it instead.

## The Temptation of Direct Access

Every relational database ships with access control. MySQL has users and privileges. PostgreSQL has roles and schemas. You can, technically, hand a client a connection string and call it done.

The problem is that a database's built-in access model is designed for database administrators, not for application users. It answers questions like "can this user read this table?" — but not "can this user read *their own* rows in this table, filtered by their organization, with rate limiting, and with that action logged?" For anything beyond the simplest internal tooling, the native access control is the wrong abstraction.

Views and stored procedures are the traditional workaround: define the allowed queries inside the database, expose those, hide the rest. This works, but it has costs. Logic leaks into the database layer where it is hard to version, hard to test, and hard to hand off to a client who does not employ a DBA. The database becomes responsible for things it was not designed to own.

## What We Do Instead

We model the database in UML and express the allowed operations as predefined queries in relational algebra — not SQL code, but the logical structure: what data is needed, how it is joined, what filters apply. SQL is an implementation detail of that intent, not the documentation of it.

In front of the database we run a thin API layer — typically FastAPI. Each allowed operation becomes an endpoint. The URL is the contract; the SQL behind it is an internal concern.

```
Client
  │
  ▼
Keycloak (Authentication & Authorization)
  │
  ▼
FastAPI (Predefined endpoints, input validation, logging)
  │
  ▼
Database (PostgreSQL / MySQL — never directly reachable from outside)
```

Keycloak handles authentication and issues tokens. FastAPI validates those tokens, enforces authorization rules, and routes requests to the appropriate query. The database receives only parameterized queries from a trusted service account. No client ever touches a connection string.

## Why This Holds Up

**The database stays clean.** Schema design, normalization, and indexing are not polluted by access-control workarounds. The data model reflects the domain, not the security requirements.

**Behavior is testable and versionable.** An API endpoint is a function. You can write unit tests for it, version it, document it with OpenAPI, and replace the underlying query without touching the contract.

**Authorization is explicit.** What a user can do is defined in one place — the API layer — not scattered across database roles, view definitions, and stored procedure grants.

**The client gets a stable interface.** If the schema changes, the API absorbs the change. The client's code does not break.

## The Short Version

A database is for storing and querying data with integrity guarantees. An API is for defining what the outside world is allowed to ask, and how. These are two different jobs. Giving them to the same system means both are done worse than if they were separated.

When clients come to us with a database problem, we almost always end up drawing the same diagram: a database behind a FastAPI service, with Keycloak in front of that. It is not a clever trick. It is just a clean separation of concerns — and it holds up over time.

If you are designing a system where a database needs to be accessible to more than one service or one team, start there.
