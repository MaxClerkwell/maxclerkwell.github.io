---
title: "ALINX AX7020, Stages 2 & 3: A Yocto Linux in QSPI Flash That Fetches Its Own Updates"
date: 2026-08-31
author: "Stephan Bökelmann"
description: "Stages 2 and 3 of the open bitstream pipeline: a self-built Yocto Linux for the ALINX AX7020, resident in QSPI flash, discoverable on the company network, key-only SSH: the walkthrough that works, followed by the nine detours it took to get there."
tags: [fpga, alinx, zynq, yocto, linux, u-boot, kexec, dropbear, fit-image, qspi, embedded, bring-up]
image: /assets/posts/alinx-ax7020-yocto-linux-qspi-august-2026/ssh-login-ax7020.png
hire_cta: "Zynq or embedded-Linux"
---

Stage 1 ended with mainline U-Boot booting from QSPI flash and answering over
the network, and I closed that article by saying the Linux build gets its own
post. This is that post, and true to form it contains a flash chip that
verified every checksum while storing everything one byte off, a bootloader
that goes mute the moment you plug it into a real switch, and a real-time
clock that turns out to be physically unreachable until the FPGA is
configured.

This covers Stages 2 and 3 of the
[bitstream pipeline plan](/posts/zynq-bitstream-deployment-concept-august-2026/)
for the AX7020 that [ALINX](https://www.alinx.com/) sent me: a **self-built
Yocto Linux that boots from QSPI flash on its own**, shows up on the company
network under its own hostname, accepts SSH logins only with a key, and
carries the tooling to fetch and `kexec` fresh development images from a
server: no PetaLinux, no vendor kernel tree, no SD card. Stage 2, the image
server, is in here too, though not in the shape the plan promised: a real
switch talked me out of netboot, and the server ended up as a plain HTTP
endpoint the running Linux pulls from; more on that below.

Same structure as last time: first the walkthrough that actually works,
reproducible from the Stage 1 end state. Then every detour, because the
detours are where the learning was, and at least three of them will bite
anyone doing this on any Zynq board.

```
OF: fdt: Machine model: Alinx AX7020 board
Memory: 1008588K/1048576K available
macb e000b000.ethernet eth0: Cadence GEM rev 0x00020118
fpga_manager fpga0: Xilinx Zynq FPGA Manager registered
of-fpga-region fpga-region: FPGA Region probed
```

That is the end state, booted straight out of flash. Here is the way there.

## The seven checkpoints

As in Stage 1, every step ends in something you can *test*, because the
expensive failures on this road are the ones that pass every check you did
think of. The walkthrough is built around seven checkpoints:

| # | After | What must be true |
|---|---|---|
| 1 | Yocto build | 3953 tasks succeed; the FIT exists, `dumpimage -l` lists kernel, DTB and initramfs with SHA256 hashes |
| 2 | RAM boot | `tftpboot` + `bootm` boots Linux; `/sys/class/fpga_manager/fpga0/` exists; **port 22 answers** (ping does not count) |
| 3 | board identity | DHCP log shows a lease for the fixed MAC `02:41:58:70:20:01` with hostname `ax7020`, surviving an environment wipe |
| 4 | flashing the FIT | read-back MD5 matches, **and** the first words at several different flash offsets differ from each other (see detour 7) |
| 5 | standalone boot | power cycle with J13 on QSPI: Linux up, SSH reachable, no JTAG, no TFTP |
| 6 | company network | the board appears in the DHCP inventory API by name; SSH works through the office switch |
| 7 | key-only SSH | login with the deployed key succeeds; wrong key, no key and password login are all rejected |

If a checkpoint fails, everything before it is known-good. All self-written
files (the Yocto layer, the U-Boot patches, the host tools) live in
[github.com/MaxClerkwell/ax7020-bringup](https://github.com/MaxClerkwell/ax7020-bringup).
Now the walkthrough.

## The starting point

The board is where Stage 1 left it: `boot.bin` (mainline SPL) and
`u-boot.img` in QSPI, operated entirely over U-Boot's netconsole on UDP port
6666, no serial cable. The lab tools are the same two Python scripts from the
repo: `tools/ncsh.py` for the netconsole and `tools/tftpd.py` as an
unprivileged TFTP server.

Goal of this session: **Linux.**

## Step 1: A Yocto build for a board Yocto has never heard of

### Picking the release

`scarthgap` (Yocto 5.0 LTS), and not out of preference:

```bash
git ls-remote --heads https://github.com/Xilinx/meta-xilinx | grep -E "scarthgap|styhead|walnascar"
# -> only scarthgap
```

meta-xilinx offers no newer release branch, and that pins the common
denominator for everything else: poky, meta-arm and meta-openembedded all get
checked out on `scarthgap`, as shallow clones, about 170 MB total.

One host-side wrinkle before the first `bitbake`: Debian 13 no longer ships
`liblz4-tool`, the binary lives in the `lz4` package, and Yocto wants it
under the old name `lz4c`, which lz4 ≥ 1.10 no longer installs. Instead of a
root-owned symlink in `/usr/local/bin`, the symlink lives in the repo
(`yocto/hostbin/lz4c → /usr/bin/lz4`) and `setup-build.sh` prepends
`hostbin` to `PATH`. No root, and the fix travels with the repository.

### The layer

`yocto/meta-ax7020/` holds everything board-specific. The machine
configuration builds on meta-xilinx's generic Zynq machine and narrows it
down:

```
require conf/machine/zynq-generic.conf

KERNEL_DEVICETREE = "xilinx/zynq-ax7020.dtb"

KERNEL_IMAGETYPE = "fitImage"
KERNEL_CLASSES   = "kernel-fitimage"
INITRAMFS_IMAGE  = "ax7020-initramfs"
INITRAMFS_IMAGE_BUNDLE = "0"

# U-Boot comes from mainline, not from Yocto
PREFERRED_PROVIDER_virtual/bootloader = ""
```

The kernel device tree is a sibling of the U-Boot one from Stage 1: every
value traced back to the ALINX `design_1.hwh` and the schematic, none of it
copied from a template. The load-bearing nodes:

```dts
&gem0 {
	status = "okay";
	phy-mode = "rgmii-id";
	phy-handle = <&ethernet_phy>;
	ethernet_phy: ethernet-phy@1 { reg = <1>; };   /* RTL8211E-VL */
};

&qspi {
	status = "okay";
	num-cs = <1>;
	flash@0 {
		compatible = "w25q256", "jedec,spi-nor";
		spi-rx-bus-width = <1>;
		spi-max-frequency = <25000000>;
	};
};
```

A kernel config fragment switches on what the project needs (the FPGA
manager framework, device-tree overlays, SPI-NOR, netconsole) and throws out
what the board does not have (DRM, sound, WLAN, IPv6). The pleasant surprise:
`zynq-7000.dtsi` already ships `devcfg@f8007000` and an `fpga-region` node
enabled, so the FPGA manager, the one feature this Linux absolutely must have
for the later stages, needed nothing board-specific at all.

The image recipe is `core-image-minimal` as a `cpio.gz` initramfs, plus
dropbear for SSH.

### Building

```bash
source yocto/setup-build.sh
bitbake virtual/kernel
```

One operational rule that cost an hour before it was a rule: start bitbake
*detached*. If the client terminal goes away, it takes the `bitbake-server`
with it ("Exiting as we could obtain the lock") and the build stalls:

```bash
setsid nohup bash -c 'source yocto/setup-build.sh >/dev/null 2>&1; \
    exec bitbake virtual/kernel' > build.log 2>&1 < /dev/null &
```

Restarts are cheap: `sstate-cache` and `tmp/work` let it resume where it
died. The build hit three genuine errors on the way through (detours 1–3
below); with those fixed, 3953 tasks completed overnight.

**Checkpoint 1: verify the artefacts on the host.**

| Component | Size |
|---|---|
| Kernel (linux-xlnx 6.6.40) | 3.79 MiB |
| Device tree | 11,651 B |
| initramfs `cpio.gz` | 4.27 MiB |
| **FIT total** | **8.06 MiB** |

`dumpimage -l fitImage` must list all three sub-images with their SHA256
hashes. Nothing downstream can work if this fails, and unlike everything
downstream, this failure comes with an error message.

## Step 2: First boot, from RAM only

Deliberately **without** touching the flash: a failure here costs nothing.

```
tftpboot 0x2000000 fitImage
setenv bootargs 'console=ttyPS0,115200 ip=dhcp'
bootm 0x2000000
```

U-Boot verified all three sub-images against their SHA256 hashes and handed
over. Linux came up, took a DHCP lease, and dropbear answered.

**Checkpoint 2: Linux is provably running.** Two parts. First,
`/sys/class/fpga_manager/fpga0/` must exist, with the attributes `name`,
`state`, `status` and `firmware`; the last one is the file-write interface
Stage 4 will use to load bitstreams. Second, **port 22 must answer**. Not
ping: U-Boot happily answers ICMP while sitting in its netconsole loop, so a
successful ping proves nothing about which of the two systems you are
talking to. The reliable liveness test for Linux is the SSH port.

(A `netconsole=` kernel parameter, the obvious way to keep the cable-free
console into Linux, stayed silent; that is detour 4.)

## Step 3: A fixed identity in U-Boot

Until now the board drew a random MAC on every boot
(`CONFIG_NET_RANDOM_ETHADDR`) and sent no hostname, which makes "find the
board on a network with 40 other devices" a daily annoyance. Two changes,
both baked into the U-Boot binary so they survive a wiped environment:

```
CONFIG_BOOTP_SEND_HOSTNAME=y
```

```c
#define CFG_EXTRA_ENV_SETTINGS	\
	"ethaddr=02:41:58:70:20:01\0"	\
	"hostname=ax7020\0"		\
	...
```

The MAC is locally administered (`02:`), `41:58` is "AX" in ASCII, `70:20`
the board number. Silly, memorable, and it can never collide with a vendor
OUI.

While rebuilding U-Boot anyway, a twelve-line patch went in for shared-lab
politeness: as long as `ncip` is the broadcast address, the first host that
types into the netconsole claims it; U-Boot sets `ncip` to that caller's
address, and everyone else's input is ignored. The claim lives only in the
RAM environment, so a reboot releases the board, and the owner can release
it early with `setenv ncip 255.255.255.255`. To be clear about what this is:
convenience, not security. The netconsole has no authentication; whoever
wins the race owns a bootloader prompt with `sf write` on it.

**Checkpoint 3: the identity sticks.** The DHCP server's log must show
the lease bound to the fixed MAC and carrying the name:

```
DHCPACK on 10.42.100.134 to 02:41:58:70:20:01 (ax7020) via eno4
```

## Step 4: The architecture decision the switch forced

The original plan for this stage was pure netboot: U-Boot fetches the FIT
over TFTP on every power-up, nothing but the bootloader in flash. On the lab
network, board and workstation joined by one USB Ethernet adapter, that
worked flawlessly. On the company switch it died in a way that took a packet
capture to understand (detour 6 has the full autopsy): U-Boot re-initialises
the Ethernet link on *every netconsole poll*, the switch port restarts its
spanning-tree timers on every link bounce, and the two livelock each other
forever. Two seconds of boot messages, then permanent silence.

The conclusion is worth stating as a design rule: **a bootloader is not a
network citizen.** U-Boot's network stack is a polling loop bolted to a
console; it was never meant to hold a link on managed infrastructure. Linux
brings the interface up once and handles link changes like an adult.

So the architecture flipped into what it should have been from the start: a
small, boring **maintenance system resident in flash**, and development
images that never get written to flash at all.

```
Flash (rarely changes)              Network (changes daily)
├─ SPL + U-Boot
└─ FIT: kernel + initramfs      ──►  Yocto image from HTTP/Nextcloud
   with curl, CA certificates,              │
   kexec, ntpd, dropbear                    │
        └── fetch, verify, kexec ───────────┘
```

The flash-resident image gained an updater package and `CONFIG_KEXEC=y` in
the kernel. The updater is a short shell script: fetch the image with curl,
check the first four bytes are the FIT magic `d00dfeed` (this catches error
pages and captive portals before they reach the kernel), then
`kexec -l` and `kexec -e` straight into the new system. No reboot, no flash
write, no jumper.

This is also where Stage 2 of the original plan quietly dissolved: the
"image server" is no longer special boot infrastructure the board depends
on, just any HTTP endpoint the updater can reach. Fetching over HTTPS
surfaced one genuinely obscure board fact about the RTC, which is detour 8.

### The new flash layout

The Stage 1 layout reserved 13 MiB for a 1 MiB U-Boot; that got tightened,
and the FIT gets the rest of the chip:

| Offset | Content | Slot |
|---|---|---|
| `0x000000` | `boot.bin` | 1 MiB |
| `0x100000` | `u-boot.img` | 2 MiB |
| `0x300000` | environment + redundant copy | 256 KiB |
| `0x340000` | **FIT** | **28.75 MiB** |

`bootcmd` went into the binary rather than the environment:

```
CONFIG_BOOTCOMMAND="sf probe 0 30000000 0; sf read 0x2000000 0x340000 0x1000000; bootm 0x2000000"
```

Two reasons, both learned the hard way: `saveenv` simply does not work in
JTAG boot mode (U-Boot reports `ENVL_NOWHERE` there), and long `setenv`
commands break over the netconsole, where a swallowed quote character leaves
the parser waiting for a continuation line and eating everything that
follows. The read covers 16 MiB rather than the exact image size so a
growing maintenance system fits later without a U-Boot rebuild.

## Step 5: Flash it, and read back more than one offset

The flashing itself is the Stage 1 recipe: TFTP the FIT into DDR, `sf
erase`, `sf write`, read back, compare MD5. It passed. And the board did not
boot, because of the single nastiest failure of this whole project, the BAR
address-mode bug of detour 7, whose defining property is that **write and
read-back were self-consistent and both wrong**. Every MD5 check passed
while every byte sat one position off in the physical array.

**Checkpoint 4** therefore has two parts, and the second exists purely
because of that detour: the read-back MD5 of the flashed region must match
the host, **and** reading the first words at `0`, `0x100000` and `0x340000`
must return *different* data at each offset. If several distant offsets read
identically, the flash addressing is broken, not the content, and no
checksum will ever tell you.

**Checkpoint 5: the board boots Linux entirely on its own.** JTAG cable
off, J13 on QSPI, power cycle. The chain is now BootROM → SPL → U-Boot →
FIT from flash → Linux, and the test is the same as checkpoint 2: a lease
for `ax7020` within seconds, and port 22 answering. On the company switch
this now works, because by the time spanning tree releases the port, the
one who retries is the Linux kernel, not a bootloader in a polling loop.

## Sidebar: finding the board again, and a DHCP inventory API

With the board destined for the company network, "which IP does it have
today" needed a real answer. That turned into a small service of its own: a
REST API that reports every device the DHCP server knows about as JSON,
reading the server's *state* (config reservations plus live leases) instead
of scanning the subnet, so it also finds devices that are currently off. It
is public and generic at
[github.com/MaxClerkwell/dhcp-inventory-api](https://github.com/MaxClerkwell/dhcp-inventory-api).

```bash
curl -s http://10.42.0.1:8000/get_all_network_clients | jq
```

Deploying it in a container on the actual router surfaced three details
that are anything but cosmetic, and each failed *silently*:

- **`--network host` is mandatory.** `/proc/net/arp` is per network
  namespace. A bind-mount of the file shows the container's three
  neighbours, not the router's 38, and the endpoint keeps answering
  cheerfully, just nearly empty.
- **Mount directories, not files.** ISC dhcpd rewrites its lease database
  via a temp file plus `rename`. A bind-mount of the file pins the old
  inode, and the container serves a snapshot frozen at container start.
  This was only noticed because the freshly connected AX7020 had a lease
  and did not appear in the list.
- **Pin the listener address.** With host networking the port would
  otherwise be open on every interface of the router, including the
  uplinks. `ss -lntp` must show exactly one bound address.

There was also a ghost device named `fantasia`: Debian's commented-out
example block in `dhcpd.conf`, faithfully parsed. The parser now strips
comments and only accepts a `fixed-address` that parses as an address.

**Checkpoint 6: the board is discoverable.** The API must list `ax7020`
with its fixed MAC and current address, and SSH must work through the
office switch.

## Step 6: Updating the flash without JTAG

Once Linux runs, the jumper dance is over for good. The MTD partitions from
the device tree are visible, and `/dev/mtdblockN` handles erasure itself:

```bash
# file onto the board: scp fails for lack of an sftp-server in the minimal image
ssh root@ax7020 'cat > /tmp/fitImage' < tftp/fitImage

# write and verify
ssh root@ax7020 '
  dd if=/tmp/fitImage of=/dev/mtdblock3 bs=64k conv=fsync
  sync
  dd if=/dev/mtdblock3 bs=1 count=<size> 2>/dev/null | md5sum'
```

About ten minutes at QSPI pace, then `reboot`. The maintenance system
updates itself over SSH; JTAG is now strictly a rescue tool.

## Step 7: SSH with keys only

A passwordless root login is fine on a point-to-point lab cable and
indefensible on a shared network. Two small recipes fix it: one installs
`authorized_keys` for root, one configures dropbear with `-s` (disable
password authentication).

One warning that will lock somebody out: poky's shipped `dropbear.default`
sets `-w`, which forbids root logins *entirely*, keys included; until now
only the `debug-tweaks` image feature was overriding that. Remove
`debug-tweaks` (as you must, it is what makes root passwordless) and leave
the rest as-is, and you have locked yourself out of the board. The correct
configuration is `-s` alone, with `*` in root's password field.

**Checkpoint 7, verified on the running board:**

| Test | Result |
|---|---|
| login with the deployed key | ✅ |
| login with a different key | ❌ rejected |
| login without a key | ❌ `Permission denied (publickey)` |
| login with a password | ❌ `Permission denied (publickey)` |

![Key-only SSH login on the AX7020](/assets/posts/alinx-ax7020-yocto-linux-qspi-august-2026/ssh-login-ax7020.png)

Stage 3 complete. BootROM, SPL, U-Boot, FIT, Linux: everything from flash,
on the company network, reachable only with the right key, with a tested
path to update itself over SSH and a built (though not yet fired) `kexec`
path for development images.

---

## The nine detours

Same rule as last time: the walkthrough above reads like a tidy evening, and
it was not. Chronologically, because several only make sense in sequence.

### 1. `${UNPACKDIR}` does not exist in scarthgap

```
| install: cannot stat '/zynq-ax7020.dts': No such file or directory
ERROR: linux-xlnx do_configure failed
```

The variable arrived with Yocto 5.1; in scarthgap, `SRC_URI` files land in
`${WORKDIR}`. Copy a `do_configure` snippet from current documentation into
an LTS build and the path expands to nothing, and the error message shows
the *result* of the empty expansion, not the variable that caused it.

**Fix, as it ended up:** the bbappend probes both locations:

```bash
src="${UNPACKDIR}/zynq-ax7020.dts"
[ -f "$src" ] || src="${WORKDIR}/zynq-ax7020.dts"
```

### 2. `bootgen-native` will not build with GCC 15

```
utils/src/cdo-load.c:140:14: error: assignment to 'char *' from incompatible
pointer type 'uint32_t *' [-Wincompatible-pointer-types]
```

Since GCC 14 this is an error, not a warning. The irony: this build does not
need bootgen at all, `boot.bin` comes from the mainline SPL, but meta-xilinx
pulls it into the dependency chain regardless.

**Fix, as it ended up:** a bbappend that defuses exactly this diagnostic
with `-Wno-incompatible-pointer-types`. Not pretty, but it patches a tool
whose output is thrown away.

### 3. An initramfs recipe needs an empty `IMAGE_NAME_SUFFIX`

```
ERROR: Could not find a valid initramfs type for ax7020-initramfs-ax7020,
the supported types are: cpio.lz4 cpio.lzo ... cpio.gz ...
```

scarthgap appends `.rootfs` to image names; `kernel-fitimage` looks for the
name without it. The supported types listed in the error are a red herring:
the type was fine, the *filename* was not.

**Fix, as it ended up:** `IMAGE_NAME_SUFFIX ?= ""` in the image recipe, the
same line poky's own initramfs recipes carry for exactly this reason.

### 4. `netconsole=` as a kernel parameter stays silent

The obvious way to keep the cable-free console into Linux,
`netconsole=6666@/eth0,6666@192.168.77.1/`, produced nothing. That early in
boot, the module cannot do ARP resolution; without the target MAC spelled
out in the parameter, it sends to nobody, and it does so without a single
complaint in `dmesg` that would point at the cause.

**Fix, as it ended up:** accepted rather than fought. Linux gets a real
console over SSH minutes later anyway; the netconsole matters for U-Boot,
where it stays. Filed under "the boot parameter needs the full MAC syntax
if it is ever needed."

### 5. Ping proves the wrong thing

During the first RAM boots, "the board answers ping" repeatedly stood in
for "Linux is up", and it repeatedly lied: U-Boot answers ICMP too, from
its netconsole loop, with the same IP the kernel would have. When a boot
hung, ping kept succeeding and the diagnosis ran in circles.

**Fix, as it ended up:** a procedural rule that made it into the
checkpoints: liveness for Linux is **port 22**, never ICMP. Checkpoints 2
and 5 both encode it.

### 6. The spanning-tree livelock: U-Boot goes mute on a real switch

The one that changed the architecture. On the company switch, the DHCP
handshake completed cleanly, two seconds of netconsole output arrived, then
nothing: no ARP, no ping, no console. Ever. The router had no `tcpdump`, so
a raw `AF_PACKET` capture in Python had to stand in, and it showed the
board sending its last packet at `15:14:01` and then falling silent.

The cause sits in plain sight in the source. Every netconsole poll calls
`net_loop()`, which re-initialises the Ethernet device; `zynq_gem_init()`
calls `phy_startup()`, which fails while the link is down. U-Boot even has
a provision to skip re-init when the last protocol was netconsole, but
after `dhcp` the last protocol is BOOTP, so the very first console poll
needs a full init. On a managed switch that init tears the link down while
the port is still in spanning-tree listening state, the switch restarts its
timers on the new link, and the two sides livelock: the port never
forwards, U-Boot never gets a link. On the lab's directly attached USB
adapter this can never happen, because autonegotiation there completes in
milliseconds with nobody holding the port back.

**Fix, as it ended up:** not a patch, a design change. A bootloader is not
a network citizen; the thing that lives on the network must be Linux. That
single realisation produced the flash-resident maintenance system of
Step 4, which is a better architecture anyway.

### 7. The BAR disaster: every checksum passes, every byte is wrong

After flashing the FIT, the BootROM parked at `0xffffff28` with the boot
mode correctly reading QSPI, exactly as if the flash were empty, although
all three regions had verified by MD5 immediately after writing. On the
next JTAG boot, offset 0 contained text data and `0x340000` zeros. A full
erase read back `0xFF` everywhere, so the chip was healthy.

The tell came from comparing several offsets:

```
sf read ... 0        -> fffffe00 fffffeea fffffeea
sf read ... 0x100000 -> fffffe00 fffffeea fffffeea      identical!
sf read ... 0x340000 -> fffffe00 fffffeea fffffeea      identical!
```

The same data at every address, shifted by one byte, and `eafffffe` is the
start of `boot.bin`. Cause: `CONFIG_SPI_FLASH_BAR`. The 32 MiB W25Q256 runs
in 4-byte address mode; with BAR enabled, U-Boot sends only three address
bytes, the chip consumes the dummy byte as the fourth address byte, the
address overflows and lands near zero, and all data arrives one byte
shifted. The vicious part: writes and reads went through the *same* broken
addressing, so they were mutually consistent. Every verification passed,
patiently confirming a wrong thing, while the BootROM, which correctly
speaks three-byte addressing on its own, found nothing where `boot.bin`
was supposed to be.

**Fix, as it ended up:** `./scripts/config --disable SPI_FLASH_BAR`,
rebuild; spi-nor then uses native 4-byte opcodes, and the same flash
procedure immediately produced a booting board. Plus the second half of
checkpoint 4: always read back *several distant offsets* and require them
to differ. That check costs seconds and is the only one in this list that
catches an addressing bug, because checksums by construction cannot.

### 8. The RTC is unreachable without a bitstream

The updater fetches images over HTTPS, and `curl` rejected every
certificate as "not yet valid": the clock stood at the epoch. Setting the
time with NTP would be routine, except for why there was no hardware clock
in the first place:

```bash
grep -o 'PCW_I2C[01]_I2C[01]_IO" VALUE="[^"]*"' design_1.hwh
# PCW_I2C0_I2C0_IO" VALUE="EMIO"
# PCW_I2C1_I2C1_IO" VALUE="EMIO"
```

Both I²C controllers are routed through EMIO, i.e. through the FPGA fabric.
Without a loaded bitstream there is physically no path from the processor
to the RTC. A dependency loop hides here: the pipeline exists to load
bitstreams over HTTPS, HTTPS needs the time, and the clock sits behind a
loaded bitstream.

**Fix, as it ended up:** the updater runs `ntpd -n -q` against a
configurable server before any HTTPS fetch, and dies with a clear message
if the clock cannot be set. Busybox ships the `ntpd` applet disabled; a
one-line config fragment enables it. The board simply has no usable RTC
until a bitstream provides the I²C route, and now the scripts know that.

### 9. Dropbear's `-w` locks out root completely

Hardening SSH nearly bricked the access instead: poky's default dropbear
arguments include `-w`, which rejects *all* root logins, key or not. The
only reason key logins had worked before was the `debug-tweaks` image
feature quietly overriding it. Removing `debug-tweaks`, which is mandatory
for anything leaving the lab since it is also what makes root passwordless,
would have left `-w` in force and the board unreachable, on a system whose
only console is SSH.

**Fix, as it ended up:** an own `dropbear.default` with `-s` alone
(password authentication off, key logins allowed), root's password field
set to `*`, and the four-row login test matrix of checkpoint 7 run before
the old image was overwritten. On a box with no serial console, test the
new lock before discarding the old key.

## Closing

The score this time: three build errors, one architecture change forced by
a switch, and one flash bug that defeated every checksum thrown at it. The
recurring shape is the same as in Stage 1, but sharpened: the worst
failures were not the loud ones, they were the ones where every
verification *passed*. The BAR bug confirmed a physically shifted flash
image with an unbroken chain of matching MD5s; the container served a
frozen lease file and an incomplete ARP table without a single error; ping
cheerfully vouched for a Linux that was not running. Verification can
patiently confirm a wrong thing, and the countermeasure is always the same:
test the property you actually need (different data at different offsets,
port 22, the inode inside the container) rather than a proxy for it.

Everything is in
[github.com/MaxClerkwell/ax7020-bringup](https://github.com/MaxClerkwell/ax7020-bringup):
the Yocto layer, the U-Boot identity and console-claim patches, the updater
recipes, the dropbear configuration, and this walkthrough in longer form.
The DHCP inventory API lives in its own repository,
[dhcp-inventory-api](https://github.com/MaxClerkwell/dhcp-inventory-api).

Next is Stage 4: a bitstream from the open toolchain, Yosys and
nextpnr-xilinx, written into `/sys/class/fpga_manager/fpga0/firmware` over
SSH. The FPGA manager is registered and waiting, the board is one `curl`
away, and somewhere behind an EMIO pin there is a real-time clock that
would very much like a bitstream to finally exist. That build gets its own
article.
