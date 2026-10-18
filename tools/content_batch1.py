"""Atlas Money content batch 1: payday-checklist carousel, no-spend-day story, daily-number reel.

Outputs (in /mnt/user-data/outputs/batch1/):
  post-payday-checklist-1..6.png   1080x1350 carousel
  story-no-spend-day.png           1080x1920 story
  reel-daily-number.mp4            1080x1920, 30 fps, ~15 s, silent (add trending audio in-app if wanted)
  reel-daily-number-cover.png      1080x1920 reel cover
"""
import math
import os
import random
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

F = "/home/claude/inter/extras/ttf/"
OUT = "/mnt/user-data/outputs/batch1/"
os.makedirs(OUT, exist_ok=True)
header = Image.open("/mnt/user-data/uploads/header-3840x1646.png").convert("RGBA")

WHITE = (248, 248, 252)
INK = (22, 16, 52)
IRIS = (167, 150, 255)
IRIS_HOT = (140, 110, 255)
GREEN = (92, 224, 156)
GOLD = (255, 204, 77)
CORAL = (255, 110, 120)
BLUE = (110, 160, 240)
MUTED = (200, 200, 230)


def font(name, size):
    return ImageFont.truetype(F + name + ".ttf", size)


def rounded_mask(size, radius):
    w, h = size
    m = Image.new("L", (w * 2, h * 2), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w * 2 - 1, h * 2 - 1), radius * 2, fill=255)
    return m.resize((w, h), Image.LANCZOS)


ICON = header.crop((231, 250, 440, 459))
ICON.putalpha(rounded_mask(ICON.size, 46))


def scale(im, width):
    return im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)


def background(W, H, blobs, top=(70, 44, 168), bottom=(16, 12, 44), seed=1):
    y = np.linspace(0, 1, H)[:, None, None]
    base = np.broadcast_to(np.array(top) * (1 - y) + np.array(bottom) * y, (H, W, 3)).astype("float64").copy()
    yy, xx = np.mgrid[0:H, 0:W]
    for bx, by, r, color, strength in blobs:
        d = np.sqrt((xx - bx * W) ** 2 + (yy - by * H) ** 2) / (r * W)
        base += (np.clip(1 - d, 0, 1) ** 2 * strength)[..., None] * (np.array(color) - base)
    base += (((xx + yy * 0.55) // 46) % 2)[..., None] * 4.0
    base += np.random.default_rng(seed).normal(0, 2.0, base.shape)
    return Image.fromarray(np.clip(base, 0, 255).astype("uint8")).convert("RGBA")


def shadow_paste(canvas, im, xy, color=(0, 0, 0), opacity=150, blur=18, offset=(0, 10)):
    pad = blur * 3
    sh = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
    layer = Image.new("RGBA", im.size, (*color, 255))
    layer.putalpha(im.split()[-1].point(lambda v: v * opacity // 255))
    sh.paste(layer, (pad, pad), layer)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(sh, (xy[0] - pad + offset[0], xy[1] - pad + offset[1]))
    canvas.alpha_composite(im, xy)


def pill(label, f, fg, bg, pad=(30, 16), angle=0):
    tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    w = round(tmp.textlength(label, font=f) + pad[0] * 2)
    h = round(f.size * 1.18 + pad[1] * 2)
    s = 3
    im = Image.new("RGBA", (w * s, h * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w * s - 1, h * s - 1), h * s // 2, fill=bg)
    d.text((w * s / 2, h * s / 2), label, font=ImageFont.truetype(f.path, f.size * s), fill=fg, anchor="mm")
    im = im.resize((w, h), Image.LANCZOS)
    return im.rotate(angle, resample=Image.BICUBIC, expand=True) if angle else im


def starburst(lines, f, fg, bg, r=120, points=16, angle=0, inner=0.8):
    s = 3
    size = r * 2 + 20
    im = Image.new("RGBA", (size * s, size * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = size * s / 2
    pts = [(c + (r if i % 2 == 0 else r * inner) * s * math.cos(math.pi * i / points),
            c + (r if i % 2 == 0 else r * inner) * s * math.sin(math.pi * i / points)) for i in range(points * 2)]
    d.polygon(pts, fill=bg)
    fb = ImageFont.truetype(f.path, f.size * s)
    lh = f.size * s * 1.02
    for i, ln in enumerate(lines):
        d.text((c, c - lh * (len(lines) - 1) / 2 + i * lh), ln, font=fb, fill=fg, anchor="mm")
    return im.resize((size, size), Image.LANCZOS).rotate(angle, resample=Image.BICUBIC, expand=True)


def sparkle(d, cx, cy, r, color):
    k = r * 0.22
    d.polygon([(cx, cy - r), (cx + k, cy - k), (cx + r, cy), (cx + k, cy + k),
               (cx, cy + r), (cx - k, cy + k), (cx - r, cy), (cx - k, cy - k)], fill=color)


def confetti(canvas, zones, n=16, seed=3):
    rnd = random.Random(seed)
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    for i in range(n):
        x0, y0, x1, y1 = zones[i % len(zones)]
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        col = rnd.choice((IRIS, GREEN, GOLD, CORAL, WHITE))
        piece = Image.new("RGBA", (60, 60), (0, 0, 0, 0))
        pd = ImageDraw.Draw(piece)
        k = rnd.random()
        if k < 0.45:
            L = rnd.uniform(16, 30)
            pd.rounded_rectangle((30 - L / 2, 25, 30 + L / 2, 34), 4, fill=col)
            piece = piece.rotate(rnd.uniform(0, 180), resample=Image.BICUBIC)
        elif k < 0.75:
            rr = rnd.uniform(4, 8)
            pd.ellipse((30 - rr, 30 - rr, 30 + rr, 30 + rr), fill=col)
        else:
            sparkle(pd, 30, 30, rnd.uniform(12, 22), col)
        layer.alpha_composite(piece, (int(x - 30), int(y - 30)))
    canvas.alpha_composite(layer)


def highlight(label, f, fg, bg, angle=-3, pad=(22, 6)):
    tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    l, t, r, b = tmp.textbbox((0, 0), label, font=f, anchor="ls")
    w, h = r - l + pad[0] * 2, round(f.size * 0.98) + pad[1] * 2
    s = 2
    im = Image.new("RGBA", (w * s, h * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w * s - 1, h * s - 1), 22 * s, fill=bg)
    d.text((pad[0] * s - l * s, h * s - pad[1] * s - round(f.size * 0.22) * s), label,
           font=ImageFont.truetype(f.path, f.size * s), fill=fg, anchor="ls")
    return im.resize((w, h), Image.LANCZOS).rotate(angle, resample=Image.BICUBIC, expand=True)


def wrap(d, text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def brand_row(c, idx=None, total=6):
    W = c.width
    d = ImageDraw.Draw(c)
    c.alpha_composite(scale(ICON, 70), (64, 62))
    d.text((150, 97), "ATLAS MONEY", font=font("Inter-ExtraBold", 26), fill=WHITE, anchor="lm")
    if idx is not None:
        x = W - 64 - (40 + (total - 1) * 22)
        for i in range(total):
            w = 40 if i == idx else 12
            d.rounded_rectangle((x, 91, x + w, 103), 6, fill=GOLD if i == idx else (255, 255, 255, 90))
            x += w + 10


# ================================================================ carousel
PW, PH = 1080, 1350
STEPS = [
    ("01", "Cover what's due.", "List every bill due before your next payday. That money is already spoken for.", BLUE),
    ("02", "Hit the minimums.", "Pay at least the minimum on every debt so late fees never eat your check.", GOLD),
    ("03", "Pay yourself.", "Move something to savings first, even $10. Small and automatic beats big and someday.", GREEN),
    ("04", "Find your daily number.", "Take what's left and divide it by the days until your next payday.", IRIS),
]


def post_cover():
    c = background(PW, PH, [(0.95, 0.1, 0.55, CORAL, 0.32), (0.05, 0.95, 0.7, GREEN, 0.26),
                            (0.7, 0.7, 0.55, IRIS_HOT, 0.42)], seed=41)
    brand_row(c, 0)
    d = ImageDraw.Draw(c)
    hf = font("InterDisplay-Black", 150)
    d.text((58, 380), "Payday?", font=hf, fill=WHITE, anchor="ls")
    bf = font("InterDisplay-Black", 92)
    d.text((62, 520), "Do these 4 things", font=bf, fill=WHITE, anchor="ls")
    hw = highlight("before you spend.", bf, INK, GOLD, angle=-3)
    shadow_paste(c, hw, (44, 545))
    burst = starburst(["SAVE", "THIS"], font("InterDisplay-Black", 48), INK, GREEN, r=120, angle=12)
    shadow_paste(c, burst, (PW - burst.width - 40, 150))
    # preview list of the 4 steps as stacked tilted chips
    y, angles = 790, (-4, 3, -2, 4)
    for (num, title, _, col), a in zip(STEPS, angles):
        chip = pill(f"{num}  {title}", font("Inter-ExtraBold", 40), INK, col, pad=(36, 18), angle=a)
        shadow_paste(c, chip, (70 + (20 if a > 0 else 0), y))
        y += 112
    d = ImageDraw.Draw(c)
    d.text((PW - 64, PH - 70), "Swipe →", font=font("Inter-Bold", 30), fill=MUTED, anchor="rs")
    confetti(c, [(900, 460, 1050, 560), (820, 760, 1060, 1180)], n=12, seed=4)
    return c


def post_step(i):
    num, title, body, col = STEPS[i]
    c = background(PW, PH, [(0.85, 0.15, 0.55, col, 0.30), (0.1, 0.9, 0.6, IRIS_HOT, 0.38)], seed=50 + i)
    brand_row(c, i + 1)
    d = ImageDraw.Draw(c)
    nf = font("InterDisplay-Black", 360)
    d.text((40, 520), num, font=nf, fill=(*col, 255), anchor="ls")
    tf = font("InterDisplay-Black", 96)
    lines = wrap(d, title, tf, PW - 140)
    y = 670
    for ln in lines:
        d.text((62, y), ln, font=tf, fill=WHITE, anchor="ls")
        y += 104
    bf = font("Inter-SemiBold", 44)
    y += 30
    for ln in wrap(d, body, bf, PW - 150):
        d.text((64, y), ln, font=bf, fill=MUTED, anchor="ls")
        y += 62
    tips = ["Rent · phone · car · insurance", "Late fees = money for nothing", "Even $10 counts"]
    if i < 3:
        y += 60
        chip = pill(tips[i], font("Inter-ExtraBold", 42), INK, col, pad=(40, 22), angle=(-3, 3, -2)[i])
        shadow_paste(c, chip, (60, y))
    if i == 3:  # worked example
        y += 40
        ex = pill("$680 ÷ 8 days = $85/day", font("InterDisplay-Black", 54), INK, GOLD, pad=(40, 24), angle=-3)
        shadow_paste(c, ex, (60, y))
    confetti(c, [(640, 200, 1050, 480)], n=8, seed=60 + i)
    return c


def post_cta():
    c = background(PW, PH, [(0.5, 0.3, 0.65, IRIS_HOT, 0.5), (0, 1, 0.6, GREEN, 0.25), (1, 1, 0.6, CORAL, 0.28)],
                   top=(80, 50, 180), seed=70)
    brand_row(c, 5)
    big = scale(ICON, 200).rotate(-8, resample=Image.BICUBIC, expand=True)
    shadow_paste(c, big, ((PW - big.width) // 2, 200), color=(20, 0, 80), opacity=200, blur=30)
    d = ImageDraw.Draw(c)
    for x, y, r, col in [(330, 240, 26, GOLD), (760, 220, 20, GREEN), (790, 400, 30, CORAL), (290, 420, 16, WHITE)]:
        sparkle(d, x, y, r, col)
    hf = font("InterDisplay-Black", 110)
    d.text((PW // 2, 620), "Atlas does", font=hf, fill=WHITE, anchor="ms")
    hw = highlight("all 4 for you.", hf, INK, IRIS, angle=-3)
    shadow_paste(c, hw, ((PW - hw.width) // 2, 640))
    d = ImageDraw.Draw(c)
    bf = font("Inter-SemiBold", 40)
    d.text((PW // 2, 880), "Every paycheck gets a plan, automatically.", font=bf, fill=MUTED, anchor="ms")
    cf = font("InterDisplay-Black", 44)
    label = "Save this for payday  📌".replace("  📌", "")
    tw = d.textlength(label, font=cf)
    bw, bh = round(tw + 110), 108
    bx, by = (PW - bw) // 2, 990
    d.rounded_rectangle((bx + 10, by + 12, bx + bw + 10, by + bh + 12), bh // 2, fill=INK)
    d.rounded_rectangle((bx, by, bx + bw, by + bh), bh // 2, fill=GOLD)
    d.text((PW // 2, by + bh // 2 + 2), label, font=cf, fill=INK, anchor="mm")
    d.text((PW // 2, by + bh + 80), "ATLAS Money on the App Store", font=font("Inter-SemiBold", 30), fill=MUTED, anchor="ms")
    confetti(c, [(30, 700, 140, 1300), (940, 700, 1060, 1300)], n=16, seed=71)
    return c


# ================================================================ story
SW, SH = 1080, 1920


def story():
    c = background(SW, SH, [(0.9, 0.15, 0.55, CORAL, 0.32), (0.1, 0.85, 0.65, GREEN, 0.28),
                            (0.5, 0.5, 0.6, IRIS_HOT, 0.42)], seed=80)
    d = ImageDraw.Draw(c)
    # top ~250px and bottom ~340px are covered by story UI; keep content between
    c.alpha_composite(scale(ICON, 76), (72, 270))
    d.text((166, 308), "MONEY TIP", font=font("Inter-ExtraBold", 30), fill=WHITE, anchor="lm")
    burst = starburst(["WEEKEND", "CHALLENGE"], font("InterDisplay-Black", 36), INK, GOLD, r=150, angle=-10)
    shadow_paste(c, burst, (SW - burst.width - 30, 220))
    hf = font("InterDisplay-Black", 150)
    d.text((64, 720), "Take one", font=hf, fill=WHITE, anchor="ls")
    hw = highlight("no-spend", hf, INK, GREEN, angle=-3)
    shadow_paste(c, hw, (44, 750))
    d = ImageDraw.Draw(c)
    d.text((64, 1080), "day.", font=hf, fill=WHITE, anchor="ls")
    bf = font("Inter-SemiBold", 48)
    y = 1200
    for ln in ["Just one day this weekend.", "No takeout, no impulse buys,", "no 'it was on sale.'"]:
        d.text((68, y), ln, font=bf, fill=MUTED, anchor="ls")
        y += 66
    chips = [("Sat?", GOLD, -6, 90), ("Sun?", IRIS, 5, 330)]
    for label, col, a, x in chips:
        shadow_paste(c, pill(label, font("InterDisplay-Black", 64), INK, col, pad=(50, 24), angle=a), (x, 1390))
    d = ImageDraw.Draw(c)
    d.text((68, 1600), "Reply with your day.", font=font("Inter-Bold", 44), fill=WHITE, anchor="ls")
    confetti(c, [(600, 600, 1040, 700), (700, 1380, 1040, 1520)], n=14, seed=81)
    return c


# ================================================================ reel
FPS, DUR = 30, 15.0
REEL_LINES = [  # (appear_time, label, amount, color, prefix)
    (2.4, "Paycheck", "$2,150", WHITE, ""),
    (3.6, "Bills due", "$1,210", BLUE, "−"),
    (4.8, "Debt minimums", "$160", GOLD, "−"),
    (6.0, "Savings", "$100", GREEN, "−"),
    (7.4, "Left until payday", "$680", WHITE, "="),
    (8.6, "Days until payday", "8", IRIS, "÷"),
]


def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def reel_bg():
    return background(SW, SH, [(0.9, 0.12, 0.55, CORAL, 0.28), (0.1, 0.9, 0.65, GREEN, 0.25),
                               (0.55, 0.45, 0.6, IRIS_HOT, 0.45)], seed=90)


def reel_frame(bg, t):
    c = bg.copy()
    d = ImageDraw.Draw(c)
    # safe area: x 72..900, y 230..1400 (Reels UI covers right rail + bottom caption)
    c.alpha_composite(scale(ICON, 64), (72, 230))
    d.text((154, 262), "ATLAS MONEY", font=font("Inter-ExtraBold", 26), fill=WHITE, anchor="lm")

    hook_f = font("InterDisplay-Black", 104)
    if t < 2.2:  # hook
        a = ease(t / 0.5)
        off = round((1 - a) * 60)
        lay = Image.new("RGBA", c.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        for i, ln in enumerate(["How much can", "I actually spend", "today?"]):
            ld.text((72, 560 + i * 118 + off), ln, font=hook_f, fill=(*WHITE, round(255 * a)), anchor="ls")
        c.alpha_composite(lay)
        if t > 0.9:
            s = pill("Do the math with me", font("Inter-ExtraBold", 40), INK, GOLD, angle=-4)
            c.alpha_composite(s, (72, 900))
        return c

    if t < 11.0:  # the math
        d.text((72, 420), "Let's find your", font=font("InterDisplay-Black", 70), fill=WHITE, anchor="ls")
        hw = highlight("daily number.", font("InterDisplay-Black", 70), INK, GOLD, angle=-3, pad=(18, 4))
        c.alpha_composite(hw, (60, 440))
        d = ImageDraw.Draw(c)
        lf, af = font("Inter-SemiBold", 46), font("InterDisplay-Black", 64)
        y0 = 640
        lay = Image.new("RGBA", c.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for i, (t0, label, amt, col, pre) in enumerate(REEL_LINES):
            if t < t0:
                break
            a = ease((t - t0) / 0.35)
            x = 72 + round((1 - a) * -80)
            y = y0 + i * 112
            if pre == "=":
                d.line((72, y - 64, 900, y - 64), fill=(255, 255, 255, 120), width=3)
            alpha = round(255 * a)
            d.text((x, y), f"{pre} {label}".strip(), font=lf, fill=(*MUTED, alpha), anchor="ls")
            d.text((900 + x - 72, y + 4), amt, font=af, fill=(*col, alpha), anchor="rs")
        c.alpha_composite(lay)
        if t >= 9.8:  # result
            a = ease((t - 9.8) / 0.4)
            res = pill("= $85 a day", font("InterDisplay-Black", 96), INK, GOLD, pad=(50, 26), angle=-4)
            sz = max(1, round(res.width * (0.6 + 0.4 * a)))
            res = scale(res, sz)
            shadow_paste(c, res, (72, 1400 - res.height // 2))
        return c

    if t < 13.0:  # payoff
        a = ease((t - 11.0) / 0.4)
        burst = starburst(["$85", "/DAY"], font("InterDisplay-Black", 96), INK, GOLD, r=260, angle=-8)
        burst = scale(burst, max(1, round(burst.width * (0.5 + 0.5 * a))))
        shadow_paste(c, burst, (SW // 2 - 90 - burst.width // 2, 820 - burst.height // 2))
        d = ImageDraw.Draw(c)
        d.text((72, 1250), "That's what's actually", font=font("InterDisplay-Black", 72), fill=WHITE, anchor="ls")
        hw = highlight("safe to spend.", font("InterDisplay-Black", 72), INK, GREEN, angle=-3, pad=(18, 4))
        c.alpha_composite(hw, (60, 1270))
        return c

    # CTA
    a = ease((t - 13.0) / 0.4)
    big = scale(ICON, round(180 + 40 * a))
    c.alpha_composite(big, (SW // 2 - 90 - big.width // 2, 560))
    d.text((SW // 2 - 90, 960), "Atlas does this math", font=font("InterDisplay-Black", 76), fill=WHITE, anchor="ms")
    d.text((SW // 2 - 90, 1050), "every single day.", font=font("InterDisplay-Black", 76), fill=IRIS, anchor="ms")
    s = pill("ATLAS Money · App Store", font("Inter-ExtraBold", 42), INK, GOLD)
    c.alpha_composite(s, (SW // 2 - 90 - s.width // 2, 1150))
    return c


def render_reel():
    bg = reel_bg()
    path = OUT + "reel-daily-number.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{SW}x{SH}",
           "-r", str(FPS), "-i", "-", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
           "-shortest", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
           "-profile:v", "high", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "128k", path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for n in range(int(FPS * DUR)):
        p.stdin.write(reel_frame(bg, n / FPS).convert("RGB").tobytes())
    p.stdin.close()
    assert p.wait() == 0
    reel_frame(bg, 12.2).convert("RGB").save(OUT + "reel-daily-number-cover.png", optimize=True)


if __name__ == "__main__":
    slides = [post_cover()] + [post_step(i) for i in range(4)] + [post_cta()]
    for i, s in enumerate(slides, 1):
        s.convert("RGB").save(f"{OUT}post-payday-checklist-{i}.png", optimize=True)
    story().convert("RGB").save(OUT + "story-no-spend-day.png", optimize=True)
    render_reel()
    print("done")
