"""Atlas Money — 2-week content batch (Oct 18–31, 2026).
Reusable templates: carousel(), story(), reel(). Content lives in the SPEC dicts at the bottom.
Outputs to /mnt/user-data/outputs/batch2/<slug>/
"""
import os
import subprocess

from PIL import Image, ImageDraw

import content_batch1 as cb  # shared brand helpers (fonts, colors, backgrounds, stickers)
from content_batch1 import (BLUE, CORAL, GOLD, GREEN, INK, IRIS, IRIS_HOT, MUTED, WHITE, background, brand_row,
                            confetti, font, highlight, pill, scale, shadow_paste, sparkle, starburst, wrap, ICON)

ROOT = "/mnt/user-data/outputs/batch2/"
PW, PH, SW, SH = 1080, 1350, 1080, 1920


def fit(text, name, size, max_w, min_size=40):
    d = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    while size > min_size and d.textlength(text, font=font(name, size)) > max_w:
        size -= 4
    return font(name, size)


def out(slug):
    p = ROOT + slug + "/"
    os.makedirs(p, exist_ok=True)
    return p


BLOBS = [
    [(0.95, 0.1, 0.55, CORAL, 0.32), (0.05, 0.95, 0.7, GREEN, 0.26), (0.7, 0.7, 0.55, IRIS_HOT, 0.42)],
    [(0.15, 0.2, 0.6, IRIS_HOT, 0.4), (0.95, 0.85, 0.6, GREEN, 0.28), (0.9, 0.05, 0.4, GOLD, 0.18)],
    [(0.1, 0.9, 0.6, GREEN, 0.34), (0.95, 0.2, 0.55, CORAL, 0.25), (0.55, 0.6, 0.5, IRIS_HOT, 0.38)],
]


# =================================================================== carousel
def carousel(spec):
    o = out(spec["slug"])
    n = len(spec["steps"]) + 2
    seed = spec.get("seed", 100)
    slides = []

    # --- cover
    c = background(PW, PH, BLOBS[seed % 3], seed=seed)
    brand_row(c, 0, n)
    d = ImageDraw.Draw(c)
    cv = spec["cover"]
    y = 360
    for ln in cv["big"]:
        f = fit(ln, "InterDisplay-Black", 150, (PW - 330) if (cv.get("burst") and y < 420) else (PW - 130))
        d.text((58, y), ln, font=f, fill=WHITE, anchor="ls")
        y += round(f.size * 1.02)
    hf = fit(cv["highlight"], "InterDisplay-Black", 104, PW - 160)
    hw = highlight(cv["highlight"], hf, INK, cv.get("hcolor", GOLD), angle=-3)
    shadow_paste(c, hw, (44, y - round(hf.size * 0.78)))
    y += round(hf.size * 1.25)
    if cv.get("burst"):
        b = starburst(cv["burst"], font("InterDisplay-Black", 44), INK, cv.get("bcolor", GREEN), r=118, angle=12)
        shadow_paste(c, b, (PW - b.width - 24, 118))
    chips = spec["steps"]
    step = 104
    cf = font("Inter-ExtraBold", 40 if len(chips) <= 4 else 36)
    y = max(y + 20, 760 if len(chips) <= 4 else 720)
    for i, st in enumerate(chips):
        a = (-4, 3, -2, 4, -3)[i % 5]
        label = f"{st['num']}  {st['title']}".strip()
        shadow_paste(c, pill(label, cf, INK, st["color"], pad=(34, 16), angle=a), (70 + (20 if a > 0 else 0), y))
        y += step
    d = ImageDraw.Draw(c)
    d.text((PW - 64, PH - 66), "Swipe →", font=font("Inter-Bold", 30), fill=MUTED, anchor="rs")
    confetti(c, [(900, 1010, 1060, 1230), (980, 560, 1060, 660)], n=9, seed=seed + 1)
    slides.append(c)

    # --- steps
    for i, st in enumerate(spec["steps"]):
        col = st["color"]
        c = background(PW, PH, [(0.85, 0.15, 0.55, col, 0.30), (0.1, 0.9, 0.6, IRIS_HOT, 0.38)], seed=seed + 10 + i)
        brand_row(c, i + 1, n)
        d = ImageDraw.Draw(c)
        numf = font("InterDisplay-Black", 300 if len(st["num"]) <= 2 else 200)
        d.text((40, 470), st["num"], font=numf, fill=col, anchor="ls")
        tf = font("InterDisplay-Black", 92)
        y = 620
        for ln in wrap(d, st["title"], tf, PW - 140):
            d.text((62, y), ln, font=tf, fill=WHITE, anchor="ls")
            y += 100
        bf = font("Inter-SemiBold", 42)
        y += 26
        for ln in wrap(d, st["body"], bf, PW - 150):
            d.text((64, y), ln, font=bf, fill=MUTED, anchor="ls")
            y += 60
        if st.get("chip"):
            y += 50
            chf = fit(st["chip"], "InterDisplay-Black", 52, PW - 220)
            shadow_paste(c, pill(st["chip"], chf, INK, col, pad=(40, 22), angle=(-3, 3)[i % 2]), (60, y))
        confetti(c, [(660, 180, 1050, 400)], n=7, seed=seed + 20 + i)
        slides.append(c)

    # --- CTA
    ct = spec["cta"]
    c = background(PW, PH, [(0.5, 0.3, 0.65, IRIS_HOT, 0.5), (0, 1, 0.6, GREEN, 0.25), (1, 1, 0.6, CORAL, 0.28)],
                   top=(80, 50, 180), seed=seed + 40)
    brand_row(c, n - 1, n)
    big = scale(ICON, 190).rotate(-8, resample=Image.BICUBIC, expand=True)
    shadow_paste(c, big, ((PW - big.width) // 2, 200), color=(20, 0, 80), opacity=200, blur=30)
    d = ImageDraw.Draw(c)
    for x, y, r, col in [(330, 240, 26, GOLD), (760, 220, 20, GREEN), (790, 400, 30, CORAL), (290, 420, 16, WHITE)]:
        sparkle(d, x, y, r, col)
    hf = fit(ct["line"], "InterDisplay-Black", 110, PW - 120)
    d.text((PW // 2, 620), ct["line"], font=hf, fill=WHITE, anchor="ms")
    hf2 = fit(ct["highlight"], "InterDisplay-Black", 110, PW - 180)
    hw = highlight(ct["highlight"], hf2, INK, IRIS, angle=-3)
    shadow_paste(c, hw, ((PW - hw.width) // 2, 640))
    d = ImageDraw.Draw(c)
    sf = fit(ct["sub"], "Inter-SemiBold", 40, PW - 140, 30)
    d.text((PW // 2, 880), ct["sub"], font=sf, fill=MUTED, anchor="ms")
    bfnt = font("InterDisplay-Black", 44)
    tw = d.textlength(ct["button"], font=bfnt)
    bw, bh = round(tw + 110), 108
    bx, by = (PW - bw) // 2, 990
    d.rounded_rectangle((bx + 10, by + 12, bx + bw + 10, by + bh + 12), bh // 2, fill=INK)
    d.rounded_rectangle((bx, by, bx + bw, by + bh), bh // 2, fill=GOLD)
    d.text((PW // 2, by + bh // 2 + 2), ct["button"], font=bfnt, fill=INK, anchor="mm")
    d.text((PW // 2, by + bh + 80), "ATLAS Money on the App Store", font=font("Inter-SemiBold", 30), fill=MUTED,
           anchor="ms")
    confetti(c, [(30, 700, 140, 1300), (940, 700, 1060, 1300)], n=14, seed=seed + 41)
    slides.append(c)

    paths = []
    for i, s in enumerate(slides, 1):
        p = f"{o}{spec['slug']}-{i}.png"
        s.convert("RGB").save(p, optimize=True)
        paths.append(p)
    return paths


# =================================================================== story
def story(spec):
    o = out(spec["slug"])
    seed = spec.get("seed", 300)
    c = background(SW, SH, BLOBS[seed % 3], seed=seed)
    d = ImageDraw.Draw(c)
    c.alpha_composite(scale(ICON, 76), (72, 270))
    d.text((166, 308), spec.get("kicker", "MONEY TIP"), font=font("Inter-ExtraBold", 30), fill=WHITE, anchor="lm")
    if spec.get("burst"):
        b = starburst(spec["burst"], font("InterDisplay-Black", 36), INK, spec.get("bcolor", GOLD), r=150, angle=-10)
        shadow_paste(c, b, (SW - b.width - 30, 220))
    y = 720
    for text, hcol in spec["lines"]:
        f = fit(text, "InterDisplay-Black", 140, SW - 150)
        if hcol:
            hw = highlight(text, f, INK, hcol, angle=-3)
            shadow_paste(c, hw, (44, y - round(f.size * 0.8)))
        else:
            ImageDraw.Draw(c).text((64, y), text, font=f, fill=WHITE, anchor="ls")
        y += round(f.size * 1.12)
    d = ImageDraw.Draw(c)
    bf = font("Inter-SemiBold", 48)
    y += 30
    for ln in spec.get("body", []):
        d.text((68, y), ln, font=bf, fill=MUTED, anchor="ls")
        y += 66
    if spec.get("chips"):
        y += 50
        x = 70
        for i, (label, col) in enumerate(spec["chips"]):
            ch = pill(label, font("InterDisplay-Black", 60), INK, col, pad=(46, 22), angle=(-6, 5, -3)[i % 3])
            shadow_paste(c, ch, (x, y))
            x += ch.width + 26
        y += 170
    if spec.get("footer"):
        ImageDraw.Draw(c).text((68, min(y + 20, 1600)), spec["footer"], font=font("Inter-Bold", 44), fill=WHITE,
                               anchor="ls")
    confetti(c, [(640, 560, 1040, 640), (760, 1380, 1040, 1520)], n=12, seed=seed + 1)
    p = f"{o}{spec['slug']}.png"
    c.convert("RGB").save(p, optimize=True)
    return [p]


# =================================================================== reel
FPS = 30


def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def _header(c):
    d = ImageDraw.Draw(c)
    c.alpha_composite(scale(ICON, 64), (72, 230))
    d.text((154, 262), "ATLAS MONEY", font=font("Inter-ExtraBold", 26), fill=WHITE, anchor="lm")


def _title(c, plain, hl, hcol=GOLD, y=420):
    d = ImageDraw.Draw(c)
    f = fit(plain, "InterDisplay-Black", 70, 830)
    d.text((72, y), plain, font=f, fill=WHITE, anchor="ls")
    f2 = fit(hl, "InterDisplay-Black", 70, 800)
    c.alpha_composite(highlight(hl, f2, INK, hcol, angle=-3, pad=(18, 4)), (60, y + 20))


def scene_hook(c, lt, s):
    a = ease(lt / 0.5)
    lay = Image.new("RGBA", c.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    f = font("InterDisplay-Black", s.get("size", 104))
    for i, ln in enumerate(s["lines"]):
        ld.text((72, 560 + i * round(f.size * 1.13) + round((1 - a) * 60)), ln, font=f,
                fill=(*WHITE, round(255 * a)), anchor="ls")
    c.alpha_composite(lay)
    if s.get("sticker") and lt > 0.8:
        y = 560 + len(s["lines"]) * round(f.size * 1.13) + 10
        c.alpha_composite(pill(s["sticker"], font("Inter-ExtraBold", 40), INK, GOLD, angle=-4), (72, y))


def scene_math(c, lt, s):
    _title(c, s["title"], s["hl"], s.get("hcol", GOLD))
    lay = Image.new("RGBA", c.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    lf, af = font("Inter-SemiBold", 46), font("InterDisplay-Black", 64)
    gap = s.get("gap", 1.1)
    for i, (label, amt, col, pre) in enumerate(s["rows"]):
        t0 = 0.4 + i * gap
        if lt < t0:
            break
        a = ease((lt - t0) / 0.35)
        x = round((1 - a) * -80)
        y = 640 + i * 112
        if pre == "=":
            d.line((72, y - 64, 900, y - 64), fill=(255, 255, 255, 120), width=3)
        al = round(255 * a)
        d.text((72 + x, y), f"{pre} {label}".strip(), font=lf, fill=(*MUTED, al), anchor="ls")
        d.text((900 + x, y + 4), amt, font=af, fill=(*col, al), anchor="rs")
    c.alpha_composite(lay)
    t_res = 0.4 + len(s["rows"]) * gap + 0.2
    if s.get("result") and lt >= t_res:
        a = ease((lt - t_res) / 0.4)
        res = pill(s["result"], fit(s["result"], "InterDisplay-Black", 92, 760), INK, s.get("rcolor", GOLD),
                   pad=(50, 26), angle=-4)
        res = scale(res, max(1, round(res.width * (0.6 + 0.4 * a))))
        shadow_paste(c, res, (72, 640 + len(s["rows"]) * 112 + 60))


def scene_list(c, lt, s):
    _title(c, s["title"], s["hl"], s.get("hcol", GOLD))
    gap = s.get("gap", 1.1)
    for i, (label, col) in enumerate(s["items"]):
        t0 = 0.4 + i * gap
        if lt < t0:
            break
        a = ease((lt - t0) / 0.35)
        ch = pill(label, fit(label, "InterDisplay-Black", 58, 760), INK, col, pad=(44, 24), angle=(-4, 3, -2, 4)[i % 4])
        ch = scale(ch, max(1, round(ch.width * (0.7 + 0.3 * a))))
        shadow_paste(c, ch, (72 + (24 if i % 2 else 0), 640 + i * 170))
    if s.get("note") and lt > 0.4 + len(s["items"]) * gap:
        ImageDraw.Draw(c).text((72, 640 + len(s["items"]) * 170 + 60), s["note"], font=font("Inter-Bold", 44),
                               fill=WHITE, anchor="ls")


def scene_big(c, lt, s):
    a = ease(lt / 0.4)
    b = starburst(s["burst"], font("InterDisplay-Black", s.get("bsize", 90)), INK, s.get("bcolor", GOLD), r=260,
                  angle=-8)
    b = scale(b, max(1, round(b.width * (0.5 + 0.5 * a))))
    shadow_paste(c, b, (450 - b.width // 2, 820 - b.height // 2))
    f = fit(s["line"], "InterDisplay-Black", 72, 830)
    ImageDraw.Draw(c).text((72, 1250), s["line"], font=f, fill=WHITE, anchor="ls")
    f2 = fit(s["hl"], "InterDisplay-Black", 72, 800)
    c.alpha_composite(highlight(s["hl"], f2, INK, s.get("hcol", GREEN), angle=-3, pad=(18, 4)), (60, 1270))


def scene_cta(c, lt, s):
    a = ease(lt / 0.4)
    big = scale(ICON, round(180 + 40 * a))
    c.alpha_composite(big, (450 - big.width // 2, 560))
    d = ImageDraw.Draw(c)
    d.text((450, 960), s.get("l1", "Atlas does this math"), font=fit(s.get("l1", "Atlas does this math"),
           "InterDisplay-Black", 76, 820), fill=WHITE, anchor="ms")
    d.text((450, 1050), s.get("l2", "every single day."), font=fit(s.get("l2", "every single day."),
           "InterDisplay-Black", 76, 820), fill=IRIS, anchor="ms")
    p = pill("ATLAS Money · App Store", font("Inter-ExtraBold", 42), INK, GOLD)
    c.alpha_composite(p, (450 - p.width // 2, 1150))


SCENES = {"hook": scene_hook, "math": scene_math, "list": scene_list, "big": scene_big, "cta": scene_cta}


def reel(spec):
    o = out(spec["slug"])
    seed = spec.get("seed", 500)
    bg = background(SW, SH, BLOBS[seed % 3], seed=seed)
    timeline, t = [], 0.0
    for s in spec["scenes"]:
        timeline.append((t, s))
        t += s["dur"]
    total = t

    def frame(tt):
        c = bg.copy()
        _header(c)
        for t0, s in reversed(timeline):
            if tt >= t0:
                SCENES[s["type"]](c, tt - t0, s)
                break
        return c

    path = f"{o}{spec['slug']}.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{SW}x{SH}",
           "-r", str(FPS), "-i", "-", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-shortest",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-profile:v", "high",
           "-movflags", "+faststart", "-c:a", "aac", "-b:a", "128k", path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for k in range(int(FPS * total)):
        p.stdin.write(frame(k / FPS).convert("RGB").tobytes())
    p.stdin.close()
    assert p.wait() == 0
    cover_t = spec.get("cover_t", total - 3.0)
    cov = f"{o}{spec['slug']}-cover.png"
    frame(cover_t).convert("RGB").save(cov, optimize=True)
    return [path, cov]


# =================================================================== CONTENT
CAROUSELS = [
    dict(slug="p1-money-leaks", seed=101,
         cover=dict(big=["5 money leaks"], highlight="hiding in your bank app", hcolor=GOLD, burst=["SAVE", "THIS"]),
         steps=[
             dict(num="01", title="Forgotten subscriptions", color=BLUE,
                  body="Streaming, apps, cloud storage. Search your statement for charges you don't recognize.",
                  chip="Cancel 1 today"),
             dict(num="02", title="Free trials that converted", color=GOLD,
                  body="That 7-day trial quietly became a monthly bill. Set a reminder the day you sign up."),
             dict(num="03", title="Bank fees", color=CORAL,
                  body="Overdraft, monthly maintenance, out-of-network ATMs. Many can be avoided or waived if you ask.",
                  chip="Ask for a refund"),
             dict(num="04", title="Delivery stacking", color=GREEN,
                  body="Service fee + delivery fee + menu markup + tip. A $15 meal can easily cost $25 or more."),
             dict(num="05", title="The 'it's only $5' buys", color=IRIS,
                  body="Small daily spends feel invisible but add up to real money every month.",
                  chip="$5 a day ≈ $150 a month"),
         ],
         cta=dict(line="Plug the leaks.", highlight="Know your number.",
                  sub="Atlas shows what's actually safe to spend today.", button="Save this for later")),
    dict(slug="p2-avalanche-vs-snowball", seed=102,
         cover=dict(big=["Paying off debt?"], highlight="Avalanche vs Snowball", hcolor=GREEN, burst=["WHICH", "ONE?"],
                    bcolor=GOLD),
         steps=[
             dict(num="01", title="The Avalanche", color=BLUE,
                  body="Pay minimums on everything, then throw extra money at the highest interest rate first.",
                  chip="Saves the most interest"),
             dict(num="02", title="The Snowball", color=GOLD,
                  body="Pay minimums on everything, then throw extra money at the smallest balance first.",
                  chip="Fastest early wins"),
             dict(num="03", title="Which should you pick?", color=GREEN,
                  body="Math says avalanche. Motivation says snowball. The best plan is the one you'll stick with."),
             dict(num="04", title="Either way: never miss a minimum", color=IRIS,
                  body="Late payments can mean fees and credit damage. Minimums first, extra second."),
         ],
         cta=dict(line="Pick your method.", highlight="Then stick to it.",
                  sub="Atlas sets aside your debt minimums every paycheck.", button="Comment AVALANCHE or SNOWBALL")),
    dict(slug="p3-read-your-paycheck", seed=103,
         cover=dict(big=["Payday!", "But why is it"], highlight="smaller than you thought?", hcolor=CORAL,
                    burst=["PAY", "STUB", "101"], bcolor=GREEN),
         steps=[
             dict(num="01", title="Gross pay", color=BLUE,
                  body="What you earned before anything comes out. The number in your offer letter."),
             dict(num="02", title="Taxes", color=CORAL,
                  body="Federal and state income tax, plus Social Security and Medicare (FICA). Some cities add a local tax."),
             dict(num="03", title="Pre-tax deductions", color=GOLD,
                  body="Retirement contributions and health insurance come out before income tax, lowering your taxable pay."),
             dict(num="04", title="Net pay is your real number", color=GREEN,
                  body="What actually hits your account. Always budget from net, never gross.",
                  chip="Plan with net pay"),
         ],
         cta=dict(line="Net pay in.", highlight="A plan out.",
                  sub="Atlas plans each paycheck around what actually lands.", button="Save for next payday")),
    dict(slug="p4-emergency-fund", seed=104,
         cover=dict(big=["Emergency fund"], highlight="in 3 levels", hcolor=GREEN, burst=["START", "SMALL"],
                    bcolor=GOLD),
         steps=[
             dict(num="01", title="Level 1: $500 starter", color=GOLD,
                  body="Enough to cover a flat tire or a surprise copay without reaching for a credit card.",
                  chip="Even $10 a week gets you there"),
             dict(num="02", title="Level 2: one month of expenses", color=BLUE,
                  body="Rent, bills, groceries, transport. One full month of breathing room."),
             dict(num="03", title="Level 3: three to six months", color=GREEN,
                  body="The common target for job loss or big life changes. Build it over time, not overnight."),
             dict(num="04", title="Keep it separate", color=IRIS,
                  body="A separate savings account makes it harder to spend by accident and easier to watch grow."),
         ],
         cta=dict(line="Start with $500.", highlight="Then keep going.",
                  sub="Atlas lets you set savings goals and fund them every paycheck.", button="Save this")),
    dict(slug="p5-holiday-fund", seed=105,
         cover=dict(big=["Holidays are"], highlight="8 weeks away.", hcolor=CORAL, burst=["START", "NOW"],
                    bcolor=GREEN),
         steps=[
             dict(num="01", title="Pick a total", color=GOLD,
                  body="Gifts, travel, food, decorations. Decide the number before the sales decide it for you.",
                  chip="Example: $400"),
             dict(num="02", title="Divide by weeks left", color=BLUE,
                  body="About 8 weeks until December 25. That's your weekly set-aside.",
                  chip="$400 ÷ 8 = $50 a week"),
             dict(num="03", title="Move it every payday", color=GREEN,
                  body="Treat it like a bill. Move it to savings the day you get paid."),
             dict(num="04", title="Shop the list, not the sale", color=IRIS,
                  body="Write down who you're buying for and a cap for each. Spend from the fund only."),
         ],
         cta=dict(line="No January", highlight="credit card hangover.",
                  sub="Set it as a savings goal in Atlas and fund it each paycheck.", button="Send this to a friend")),
    dict(slug="p6-overdraft-proof", seed=106,
         cover=dict(big=["Overdraft-proof"], highlight="your account", hcolor=GOLD, burst=["4", "STEPS"],
                    bcolor=CORAL),
         steps=[
             dict(num="01", title="Turn on low-balance alerts", color=BLUE,
                  body="Most bank apps can text you when your balance drops below a number you choose.",
                  chip="Takes 2 minutes"),
             dict(num="02", title="Keep a small buffer", color=GREEN,
                  body="Leave a cushion in checking, even $100, that you treat as zero."),
             dict(num="03", title="Watch pending charges", color=GOLD,
                  body="Your balance can look higher than it is until pending transactions and holds clear."),
             dict(num="04", title="Check your overdraft settings", color=CORAL,
                  body="You can usually turn off overdraft coverage for debit card purchases, so they decline instead."),
         ],
         cta=dict(line="Your balance isn't", highlight="your spending money.",
                  sub="Atlas subtracts what's due so you see what's truly safe.", button="Save this")),
]

STORIES = [
    dict(slug="s1-bill-due-date", seed=301, kicker="QUICK CHECK", burst=["BE", "HONEST"],
         lines=[("Do you know", None), ("when your next", None), ("bill is due?", GOLD)],
         body=["Not roughly. The actual date."], chips=[("YES", GREEN), ("NO", CORAL)], footer="Reply with yours."),
    dict(slug="s2-avalanche-or-snowball", seed=302, kicker="NEW POST", burst=["WHICH", "ARE YOU?"], bcolor=GREEN,
         lines=[("Paying off debt:", None), ("Avalanche", BLUE), ("or Snowball?", GOLD)],
         body=["Highest interest first, or", "smallest balance first?"], footer="Reply with your pick."),
    dict(slug="s3-no-spend-weekend", seed=303, kicker="WEEKEND CHALLENGE", burst=["ROUND", "2"], bcolor=CORAL,
         lines=[("Take one", None), ("no-spend", GREEN), ("day.", None)],
         body=["Just one day this weekend.", "No takeout, no impulse buys."],
         chips=[("Sat?", GOLD), ("Sun?", IRIS)], footer="Reply with your day."),
    dict(slug="s4-start-with-10", seed=304, kicker="MONEY MYTH", burst=["MYTH", "BUSTED"],
         lines=[("You need a lot", None), ("to start saving.", None), ("Nope. Start", None), ("with $10.", GREEN)],
         body=["Consistency beats amount.", "Small and automatic wins."], footer="What's your first $10 for?"),
    dict(slug="s5-low-balance-alerts", seed=305, kicker="2-MINUTE TIP", burst=["DO IT", "NOW"], bcolor=GREEN,
         lines=[("Turn on", None), ("low-balance", GOLD), ("alerts.", None)],
         body=["Open your bank app → Alerts.", "Pick a number. Done."], footer="Reply DONE when it's on."),
    dict(slug="s6-cash-or-card", seed=306, kicker="THIS OR THAT", burst=["HAPPY", "HALLOWEEN"], bcolor=CORAL,
         lines=[("Do you spend", None), ("less with", None), ("cash or card?", IRIS)],
         chips=[("CASH", GREEN), ("CARD", GOLD)], footer="Reply and tell us why."),
]

REELS = [
    dict(slug="r1-balance-is-lying", seed=501, cover_t=12.6, scenes=[
        dict(type="hook", dur=2.4, lines=["Your bank", "balance is", "lying to you."], sticker="Here's why"),
        dict(type="math", dur=8.8, gap=0.9, title="What's actually", hl="free to spend?", rows=[
            ("Bank balance", "$1,400", WHITE, ""), ("Car payment due", "$320", BLUE, "−"),
            ("Phone bill due", "$85", GOLD, "−"), ("Subscriptions", "$45", CORAL, "−"),
            ("Really free", "$950", WHITE, "="), ("Days until payday", "6", IRIS, "÷")],
             result="= $158 a day"),
        dict(type="big", dur=2.4, burst=["$158", "/DAY"], line="Not $1,400.", hl="$158 a day."),
        dict(type="cta", dur=2.4)]),
    dict(slug="r2-five-dollars-a-day", seed=502, cover_t=8.0, scenes=[
        dict(type="hook", dur=2.4, lines=["\"It's only", "$5.\""], size=130, sticker="Let's do the math"),
        dict(type="math", dur=4.6, title="$5 a day", hl="adds up to...", rows=[
            ("Per week", "$35", GOLD, ""), ("Per month", "$150", GREEN, ""), ("Per year", "$1,825", CORAL, "")]),
        dict(type="big", dur=2.8, burst=["$1,825", "/YEAR"], bsize=80, line="Not saying skip the coffee.",
             hl="Just know the number."),
        dict(type="cta", dur=2.4, l1="Atlas shows your", l2="number every day.")]),
    dict(slug="r3-credit-card-interest", seed=503, cover_t=8.0, scenes=[
        dict(type="hook", dur=2.4, lines=["What does a", "$1,000 card", "balance cost?"], sticker="At 24% APR"),
        dict(type="math", dur=4.6, title="At 24% APR,", hl="interest is about...", hcol=CORAL, rows=[
            ("Per month", "≈ $20", GOLD, ""), ("Per year", "≈ $240", CORAL, "")]),
        dict(type="big", dur=2.8, burst=["$240", "/YEAR"], bcolor=CORAL, line="For money you", hl="already spent.",
             hcol=GOLD),
        dict(type="list", dur=4.8, title="How to", hl="pay less of it", hcol=GREEN, items=[
            ("Pay more than the minimum", GREEN), ("Pay before the due date", GOLD), ("Ask for a lower APR", IRIS)]),
        dict(type="cta", dur=2.4, l1="Atlas plans your", l2="debt payments in.")]),
    dict(slug="r4-call-these-bills", seed=504, cover_t=6.2, scenes=[
        dict(type="hook", dur=2.4, lines=["3 bills to", "call about", "this week."], sticker="15 minutes each"),
        dict(type="list", dur=4.4, title="Call your", hl="providers for:", items=[
            ("Internet", BLUE), ("Phone plan", GOLD), ("Car insurance", GREEN)]),
        dict(type="list", dur=4.4, title="Then ask", hl="these 3 things:", hcol=GREEN, items=[
            ("Any promotions?", IRIS), ("Is there a cheaper plan?", GOLD), ("Can you match a competitor?", CORAL)]),
        dict(type="cta", dur=2.4, l1="Then put the savings", l2="where it counts.")]),
]

if __name__ == "__main__":
    import json
    import sys
    only = sys.argv[1:]
    manifest = {}
    for kind, items, fn in (("carousel", CAROUSELS, carousel), ("story", STORIES, story), ("reel", REELS, reel)):
        for s in items:
            if only and s["slug"] not in only:
                continue
            manifest[s["slug"]] = fn(s)
            print("built", s["slug"], flush=True)
    json.dump(manifest, open(ROOT + "manifest.json", "w"), indent=1)
