---
layout: post
title: "Viewing Plots from My Homelab Over SSH X11 Forwarding"
date: 2026-05-13
tags: [linux, networking]
description: "How to forward X11 through a bastion server to display images and plots from a home machine on a university workstation, without copying files."
keywords: "X11 forwarding SSH, bastion server X11, SSH jump host display, homelab remote plotting, WireGuard SSH X11, Linux remote GUI"
permalink: /posts/x11-forwarding-bastion-may-2026/
---

Sometimes I am in a terminal on my home machine, a Python or C++ script runs through, it produces a plot, and I want to look at it. The problem: I am sitting at my university workstation. Switching to another terminal, running `scp`, opening the file locally, then switching back — that is enough friction to be genuinely annoying when you are in the middle of iterating on something.

SSH X11 forwarding solves this. The image renders on the remote machine and the window appears locally, as if the application were running here. Getting it to work through a bastion server took a few steps worth writing down.

## The Setup

My homelab sits behind a router with no public IP. Between it and the outside world is Heimdall — a rented server with a public IP address. Heimdall is a **bastion server**: a hardened, publicly reachable machine whose sole job is to be the single entry point into a private network. Nothing in the homelab is exposed directly; all access goes through Heimdall first.

Heimdall and my home machine Qingdao share a WireGuard VPN, which I set up together with [@philippthecron](https://x.com/philippthecron). I will write about that separately at some point. The relevant part here is that Heimdall can reach Qingdao over that tunnel, and nobody else can.

## Network Topology

```
┌─────────────────────────────────────────────────────────────┐
│  University network                                         │
│                                                             │
│   ┌───────┐                                                 │
│   │ pc54  │                                                 │
│   └───┬───┘                                                 │
└───────┼─────────────────────────────────────────────────────┘
        │ SSH (public internet)
        ▼
   ┌──────────┐
   │ heimdall │  ← bastion server, public IP
   └─────┬────┘
         │ SSH over WireGuard tunnel
         ▼
┌────────────────────────────────────────────────────────────┐
│  Homelab                                                   │
│                                                            │
│   ┌─────────┐                                              │
│   │ qingdao │                                              │
│   └─────────┘                                              │
└────────────────────────────────────────────────────────────┘
```

X11 display data travels the same path in reverse: Qingdao renders the window, Heimdall passes it through, pc54 displays it.

## Configuring the SSH Client on pc54

SSH has a built-in mechanism for chained connections: `ProxyJump`. It connects to the jump host first, then tunnels the onward connection through it. From Qingdao's perspective, the connection arrives from Heimdall. From pc54's perspective, `ssh qingdao` just works.

In `~/.ssh/config` on pc54:

```
Host heimdall
    HostName <heimdall-public-ip>
    User maxclerkwell

Host qingdao
    HostName <qingdao-wireguard-ip>
    User maxclerkwell
    ProxyJump heimdall
    ForwardX11 yes
```

The IP under `HostName` for Qingdao is its WireGuard address — visible to Heimdall, not to pc54 directly. pc54 does not need to be able to route there itself; Heimdall handles that leg.

`ForwardX11 yes` is the equivalent of passing `-X` on the command line. It tells SSH to carry the X11 display traffic back through the tunnel to pc54's local X server.

## Does Heimdall Need Any Configuration?

No changes to Heimdall's `sshd_config` are needed for this to work. Heimdall is just a relay — SSH's ProxyJump establishes a direct tunnel between pc54 and Qingdao through it. The X11 forwarding negotiation happens end-to-end between pc54 and Qingdao, not via Heimdall.

## Enabling X11 Forwarding on Qingdao

On Qingdao, X11 forwarding needs to be permitted at the SSH daemon level:

```bash
grep X11 /etc/ssh/sshd_config
```

The relevant line should read:

```
X11Forwarding yes
```

If it is commented out or set to `no`, change it and restart: `sudo systemctl restart ssh`.

The other requirement is `xauth`, a small utility that manages X authentication tokens. Without it, the forwarding handshake fails silently:

```bash
sudo apt install xauth
```

## Adding the SSH Key (Optional)

Password login works. But typing a password through two SSH hops every time gets old. Copying the public key from pc54 to Qingdao makes the connection passwordless:

```bash
ssh-copy-id -i ~/.ssh/id_rsa.pub qingdao
```

With the ProxyJump already configured, `ssh-copy-id` routes through Heimdall automatically. One less thing to type.

## Testing

```bash
ssh qingdao
xeyes
```

A pair of eyes should appear on pc54's screen. For something more practical:

```bash
ssh qingdao
eog plot.jpg        # GNOME image viewer
display plot.jpg    # ImageMagick
feh plot.jpg        # lightweight viewer
```

No file transfer. The image renders on Qingdao, the window appears on pc54.

## How Well Does X11 Forwarding Over SSH Actually Perform?

For static images — plots, diagrams, anything that just needs to be displayed — the latency is irrelevant. The window opens, you look at it, you close it. Two SSH hops add no meaningful delay to that.

For interactive GUI applications it is a different story. I have used this occasionally to run Vivado on Qingdao from pc54, because the license is tied to that machine. It works. But you notice the lag on every click and every redraw. KiCad I tried once — Qingdao has more RAM and I wanted to offload a heavy board — but the interaction was too sluggish to be useful. For tools where you are clicking around and waiting for the interface to respond, X11 forwarding over two hops is not the right answer.

For looking at a plot: perfectly fine.

## A Note on ForwardX11Trusted

SSH has two modes for X11 forwarding. `ForwardX11 yes` (or `-X`) applies security restrictions on what the remote application can do with the local display. `ForwardX11Trusted yes` (or `-Y`) removes those restrictions and is sometimes faster, but gives the remote machine full control over the local X session.

`ForwardX11Trusted yes` did not work reliably in my setup. `ForwardX11 yes` did. The more cautious default turned out to also be the one that works.

## Why Use X11 Forwarding Instead of Copying Files?

Most of my work on Qingdao stays in the terminal. But every now and then a matplotlib figure or a C++ rendering comes out and I want to glance at it without breaking stride. This setup costs nothing to run, requires no extra ports or services, and is already there once SSH is configured. For the occasional Vivado session it has also saved me from needing a second license. Not a tool I reach for every day — but exactly right for what it does.
