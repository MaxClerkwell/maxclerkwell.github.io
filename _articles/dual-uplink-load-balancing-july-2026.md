---
title: "Dual Uplink, Part Two: From Failover to Load Balancing (and the Two Bugs That Broke It)"
date: 2026-07-12
tags: [networking, linux]
description: "The follow-up to our dual-uplink failover setup: weighted multipath load balancing, source-based policy routing, pinning a host to one link, and the two persistence bugs that silently killed it on every reboot."
keywords: "weighted multipath, ECMP Linux, policy routing, ip rule, dual uplink load balancing, Starlink DSL, systemd network-online, sysctl.d, iptables-nft masquerade"
---

Back in February, [Philipp](https://x.com/philippthecron) and I put a second uplink into the office and built [dual-uplink failover on AI-heimdall](/posts/dual-uplink-feb-2026/): two default routes in the main table, separated by metric, DSL preferred and Starlink as a hot standby. That article ended on a promise. Two named routing tables, `starlink` (200) and `dsl` (201), were already registered in `/etc/iproute2/rt_tables`, sitting there unused, "as preparation for proper policy routing." This is the article where they get used.

The move from failover to load balancing sounds like a small config change. It is not. Failover is one route winning; load balancing is every layer of the stack agreeing on which uplink a given packet leaves through. And getting it to survive a reboot turned out to hinge on two bugs that had nothing to do with routing at all.

## Failover Was Never the Goal, Just the Safe First Step

Metric-based failover has a property that is great for a first deployment and useless for a busy office: only one link ever carries traffic. The lower-metric route wins completely, and the other one is a cold spare the kernel only touches when the primary disappears. We had resilience, but on a normal day all fifteen people were still crammed onto DSL while a perfectly good Starlink link sat idle.

Load balancing is a different construct entirely. Instead of two default routes ranked by metric, you write **one** default route with multiple weighted next-hops:

```sh
ip route replace default \
  nexthop via 192.168.1.1  dev eno2 weight 2 \
  nexthop via 192.168.99.1 dev eno1 weight 1
```

That is `eno2` (Starlink) and `eno1` (DSL) both carrying traffic at the same time, split roughly 2:1. One route, two next-hops, weights proportional to how much I want each link to shoulder.

## Per-Flow, Not Per-Packet: The Expectation to Kill First

The first thing to get straight, before anyone gets excited about "combined bandwidth," is what multipath actually balances. Modern kernels hash the route by flow, using the layer-3 and layer-4 headers, not per packet. A single TCP connection is pinned to one uplink for its whole life; conntrack keeps established flows on the path they started on. Balancing happens *across* connections, not *within* one.

So `weight 2:1` means about two thirds of new connections go to Starlink, not two thirds of any single download's packets. You cannot bond one connection's bandwidth across two links this way. A single large `git push` rides one uplink at that uplink's speed. What you gain is that fifteen people's fifteen-plus connections spread out instead of stacking. For an office, that is exactly the win you want; for a single giant transfer, it does nothing, and it is better to say so up front than to field the "why isn't my download twice as fast" question later.

## The Four Pieces That Have to Agree

A working multi-uplink router is four separate things, and leaving any one out produces a failure that looks like something else:

1. **Forwarding.** `net.ipv4.ip_forward=1`. Obvious, and the source of bug number one below.
2. **NAT per uplink.** Every interface that packets egress from needs its own masquerade rule:
   ```sh
   iptables -t nat -A POSTROUTING -o eno1 -j MASQUERADE
   iptables -t nat -A POSTROUTING -o eno2 -j MASQUERADE
   ```
   This is the sneaky one. With failover there was only ever one active egress, so one masquerade rule was enough. The moment the multipath route starts sending some flows out the second uplink, those flows leave with un-rewritten internal source IPs, the upstream discards them, and you get the classic "half my connections just don't work" symptom with nothing obviously wrong in the routes.
3. **The weighted multipath default route.** The single default with weighted next-hops above. This governs new outbound connections from forwarded clients.
4. **Source-based policy routing.** This is what the two named tables were reserved for:
   ```sh
   ip route replace default via 192.168.99.1 dev eno1 table dsl
   ip route replace default via 192.168.1.1  dev eno2 table starlink
   ip rule add from 192.168.99.2  table dsl
   ip rule add from 192.168.1.248 table starlink
   ```

That fourth piece is not optional polish, and it is the part people skip when they think "I only want load balancing." Multipath handles traffic *forwarded through* the router. But the router itself, and any connection arriving at one of its uplink IPs, must reply *out the same uplink the request came in on*. Without a source rule, the router's own reply follows the multipath default and can leave via the other uplink. That is asymmetric routing, and stateful firewalls plus `rp_filter` drop it on sight. The per-uplink tables and source rules are what make both links usable in both directions.

## Pinning One Host to One Uplink

We have a concrete reason for this, not a hypothetical one. One machine talks to a license server that verifies against our public IP, and for that verification to work we had to arrange a static IP with the provider. That static IP lives on the DSL line. So the machine that connects to the license server must always egress via DSL; if load balancing ever sent its verification traffic out Starlink, it would arrive from the wrong public address and the check would fail. Failover never had this problem because everything used DSL anyway. The moment traffic started spreading across both links, that one host had to be nailed down.

An `ip rule` with a **lower priority number** than the general source rules gets evaluated first:

```sh
ip rule add from 10.42.100.50 table dsl priority 100
```

The mental model is a walk down the rule list in priority order, low number first. A host-pin rule at priority 100 catches that machine's forwarded traffic and hands it straight to the `dsl` table's default route, before the weighted multipath default is ever consulted. Everything else falls through to `main` and gets split by flow-hash. Rule, then route, then NAT: every layer has to name the same uplink, or the flow breaks somewhere in the middle.

## The Two Bugs That Broke It on Every Reboot

Here is the honest order of events, because it is why I touched a working configuration at all. The trigger was not ambition, it was the power going out. We had planned maintenance work that cut the electricity, so AI-heimdall went down and came back up on its own. And when it came back, it did not come online the way I wanted: the office was not routing as expected. Only then, with the router misbehaving after an unplanned reboot, did I sit down and dig into what was actually persisting across boots and what was not. That is when the two hidden problems surfaced.

Runtime `ip`, `iptables`, and `sysctl` state is ephemeral, which I knew; what I did not expect was that my careful persistence setup was being defeated by two unrelated traps.

### Bug 1: `/etc/sysctl.conf` was being ignored

`ip_forward` was set in `/etc/sysctl.conf`, and after every boot it was back to `0`, so no traffic was forwarded at all and the whole thing looked dead. The cause has nothing to do with routing. `systemd-sysctl` reads `/etc/sysctl.d/*.conf`, `/run/`, and `/usr/lib/`, but it only picks up `/etc/sysctl.conf` through the conventional symlink `/etc/sysctl.d/99-sysctl.conf -> ../sysctl.conf`. On this box that symlink was missing, so the file was silently skipped at boot and I had been setting forwarding by hand without realising it. The fix is to stop relying on the symlink and drop a real file into the directory:

```sh
printf 'net.ipv4.ip_forward=1\n' > /etc/sysctl.d/99-heimdall.conf
```

### Bug 2: the DHCP uplink was not ready when the route script ran

The second one is nastier because it is a race. The routing script runs as a systemd oneshot ordered `After=network-online.target`. But the Starlink interface is DHCP and marked `allow-hotplug` rather than `auto`, and with ifupdown a hotplug interface is **not** waited on by `network-online.target`. So the oneshot fired before the DHCP lease arrived, `ip route ... nexthop via <dhcp-gw>` failed with "Nexthop has invalid gateway," and because the script runs under `set -e`, the whole setup aborted. A oneshot does not retry, so load balancing stayed dead until the next manual run.

The fix is belt and suspenders:

- Make the script **wait** for the DHCP uplink's subnet route to appear before touching the multipath route (poll `ip route show dev eno2 | grep <subnet>` with a timeout around 60 seconds), so the oneshot no longer races the lease.
- Also invoke the same script from `/etc/network/if-up.d/`, so it re-runs whenever the Starlink link comes up or renews its lease. This second hook matters for more than boot: a DHCP renewal happily reinstalls a plain default route that clobbers the multipath one, and the `if-up.d` hook is what puts it back.

## Two More Traps Worth Naming

While hardening the setup, two smaller things bit and are worth writing down.

**Do not mix `nft` and `iptables` for NAT.** If `nft list table ip nat` warns that the table is "managed by iptables-nft, do not touch," add masquerade rules with `iptables -t nat`, not `nft add rule`. Against an iptables-nft-managed chain, `nft add rule ... masquerade` fails with a baffling "No such file or directory." Persist the result with `netfilter-persistent save`, which writes `/etc/iptables/rules.v4`.

**`ip rule add` never deduplicates.** It inserts a new entry every time, even if an identical rule already exists, so re-running the setup script quietly accumulates duplicate rules. Delete-then-add makes it idempotent:

```sh
while ip rule del from 192.168.1.248 table starlink 2>/dev/null; do :; done
ip rule add from 192.168.1.248 table starlink
```

## Verifying Each Link Independently

The one command that made all of this debuggable is `curl --interface`, which forces egress from a given source address, which hits that address's source rule, which selects that uplink:

```sh
curl --interface 192.168.1.248 https://ifconfig.co   # Starlink's public IP
curl --interface 192.168.99.2  https://ifconfig.co   # DSL's public IP
```

Two distinct WAN addresses come back, proving each path reaches the internet on its own. Combined with the Python dashboard from the [first article](/posts/dual-uplink-feb-2026/), it is easy to confirm at a glance that traffic is actually spreading across both links instead of quietly collapsing onto one.

---

*Failover was the safe version: one link at a time, automatic backup, nothing clever. Load balancing is the version that actually uses the capacity we pay for, and it demands that forwarding, per-uplink NAT, the weighted multipath route, and source-based rules all agree on the same uplink for every packet. The routing was the easy part. Making it survive a reboot came down to a missing sysctl symlink and a DHCP interface that was not ready when the script assumed it was. The durable setup is a real file in `/etc/sysctl.d/`, NAT via `netfilter-persistent`, and a routing script driven by both a self-contained systemd oneshot that waits for the DHCP uplink and an `if-up.d` hook that re-applies on every renewal. Belt and suspenders, because DHCP will erase your multipath the moment you stop putting it back.*
