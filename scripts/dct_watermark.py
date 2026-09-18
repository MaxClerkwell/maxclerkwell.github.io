#!/usr/bin/env python3
"""Keyed spread-spectrum watermark in the 8x8 block-DCT domain (luminance).

  embed : dct_watermark.py embed IN OUT [--key K] [--text T] [--alpha A]
  detect: dct_watermark.py detect FILE [--key K] [--len N]

Blind detection: the original image is not needed, only the key.
"""
import argparse
import hashlib
import os

import numpy as np
from PIL import Image
from scipy.fft import dctn, idctn

DEFAULT_KEY = os.environ.get("WM_KEY", "maxclerkwell")
DEFAULT_TEXT = "maxclerkwell.tech"
# mid-band coefficients: survive JPEG quantisation, stay invisible
COEFFS = [(u, v) for u in range(8) for v in range(8) if 3 <= u + v <= 6]


def _blocks(y):
    h, w = (y.shape[0] // 8) * 8, (y.shape[1] // 8) * 8
    b = y[:h, :w].reshape(h // 8, 8, w // 8, 8).transpose(0, 2, 1, 3)
    return b, h, w


def _layout(key, nblocks, nbits):
    seed = int.from_bytes(hashlib.sha256(key.encode()).digest()[:8], "big")
    rng = np.random.default_rng(seed)
    n = nblocks * len(COEFFS)
    bit_of_chip = rng.permutation(n) % nbits
    pn = rng.integers(0, 2, n) * 2 - 1
    return bit_of_chip, pn


def _chips(d):
    us, vs = zip(*COEFFS)
    return d[:, :, us, vs].reshape(-1)


def embed(src, dst, key=DEFAULT_KEY, text=DEFAULT_TEXT, alpha=3.0, quality=92, subsampling=0):
    im = Image.open(src)
    a = im.convert("RGBA").getchannel("A") if im.mode in ("RGBA", "LA", "P") else None
    img = im.convert("RGB").convert("YCbCr")
    arr = np.asarray(img, dtype=np.float64).copy()
    b, h, w = _blocks(arr[:, :, 0])
    d = dctn(b, axes=(2, 3), norm="ortho")
    bits = np.unpackbits(np.frombuffer(text.encode(), dtype=np.uint8))
    bit_of_chip, pn = _layout(key, d.shape[0] * d.shape[1], len(bits))
    delta = alpha * pn * (bits[bit_of_chip] * 2.0 - 1.0)
    us, vs = zip(*COEFFS)
    d[:, :, us, vs] += delta.reshape(d.shape[0], d.shape[1], len(COEFFS))
    b2 = idctn(d, axes=(2, 3), norm="ortho")
    arr[:h, :w, 0] = b2.transpose(0, 2, 1, 3).reshape(h, w)
    out = Image.fromarray(np.clip(arr.round(), 0, 255).astype(np.uint8), "YCbCr")
    out = out.convert("RGB")
    if str(dst).lower().endswith(".png"):
        if a is not None:
            out.putalpha(a)
        out.save(dst, optimize=True)
    else:
        out.save(dst, quality=quality, subsampling=subsampling, optimize=True)


def detect(src, key=DEFAULT_KEY, nbytes=len(DEFAULT_TEXT.encode())):
    y = np.asarray(Image.open(src).convert("RGB").convert("YCbCr"), dtype=np.float64)[:, :, 0]
    b, _, _ = _blocks(y)
    d = dctn(b, axes=(2, 3), norm="ortho")
    nbits = nbytes * 8
    bit_of_chip, pn = _layout(key, d.shape[0] * d.shape[1], nbits)
    c = _chips(d) * pn
    sums = np.bincount(bit_of_chip, weights=c, minlength=nbits)
    counts = np.bincount(bit_of_chip, minlength=nbits)
    z = sums / (c.std() * np.sqrt(counts))
    text = np.packbits((z > 0).astype(np.uint8)).tobytes()
    return text, float(np.abs(z).mean())


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("mode", choices=["embed", "detect"])
    p.add_argument("src")
    p.add_argument("dst", nargs="?")
    p.add_argument("--key", default=DEFAULT_KEY)
    p.add_argument("--text", default=DEFAULT_TEXT)
    p.add_argument("--alpha", type=float, default=3.0)
    p.add_argument("--len", type=int, default=len(DEFAULT_TEXT.encode()))
    a = p.parse_args()
    if a.mode == "embed":
        embed(a.src, a.dst, a.key, a.text, a.alpha)
    else:
        text, score = detect(a.src, a.key, a.len)
        # mean |z| near 0.8 means "no watermark"; clearly above ~2 means present
        print(f"{text!r}  mean|z|={score:.2f}")
