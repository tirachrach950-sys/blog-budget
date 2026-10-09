#!/usr/bin/env python3
"""Run `python3 build.py` to regenerate every page. Edit GUIDES below to change text."""
import re, html, os, datetime
BASE = "https://www.plainfoliomoney.com"
UPDATED = "October 2026"
FORM = "https://formspree.io/f/xwlpdzzr"
IMG = {"notes":("expenses-receipts","Sticky notes labeled Expenses and Receipts on a notebook with colorful number magnets"),
       "journal":("less-more-journal","Open journal with the words Less and More written at the top of a page"),
       "plan":("budget-notebook","Person writing a budget in a notebook next to cash and a phone calculator"),
       "wallet":("wallet-cash","Hand taking cash out of a leather wallet above notes and papers"),
       "box":("savings-box","Carved wooden savings box with a padlock and a coin on top")}
CATS = ["Budgeting","Debt & Credit","Saving","Spending","Earning","Relationships"]

G = []
def g(slug,cat,img,title,desc,body): G.append(dict(slug=slug,cat=cat,img=img,title=title,desc=desc,body=body.strip()))

g("how-to-budget-on-a-low-income","Budgeting","plan","How to Budget on a Low Income: A Simple 3-Bucket Method",
"Three categories instead of twelve, set up in fifteen minutes, built for a small paycheck.","""
You earn what you earn, and somehow it's gone before the month is. That's usually a system problem, not a discipline problem: most budgets are written for people with room to spare.
## Why most budgets fail
They ask for twelve categories, daily logging and zero-based precision. That's fine with slack in your income and miserable without it. The result is a spreadsheet abandoned by week two and the belief that budgeting doesn't work for you.
> A budget that needs willpower every single day is already failing.
## The 3-bucket method
- **Needs:** rent, utilities, groceries, transport, minimum debt payments. Add these up first.
- **Wants:** eating out, subscriptions, hobbies. Cutting this to zero is what makes budgets collapse.
- **Savings:** start at 5%. Month one is about proving the habit holds, not hitting a big number.
On a low income the split usually looks like Needs 60-70%, Wants 15-25%, Savings 5-10%. The exact numbers matter less than having three buckets.
## Track it in five minutes a week
A free spreadsheet or a phone note with three rows is enough. Update it once a week so you see which bucket is running hot before the month ends, not after.
## If your income is irregular
Look at your last 3-6 months and find the lowest one. Budget your Needs around that baseline month. Anything above it in a good month goes into a buffer, so a slow month doesn't become a crisis.
## The month-one mistake
Trying to be perfect. The first month shows you numbers you didn't expect, and that's the system working. Adjust the buckets in month two.
""")
g("pay-off-small-debts-without-a-no-fun-budget","Debt & Credit","wallet","Paying Off Small Debts Without a Strict No-Fun Budget",
"A debt plan you can actually finish: pick one method, keep a little fun in the budget, automate the extra payment.","""
Most debt advice assumes you can cut spending to zero for a year. It works on paper and it's exactly why people quit in month two. You can clear a credit card, a store card or a small loan without declaring war on every small joy.
## Pick one method, not both
- **Avalanche:** extra money goes to the highest interest rate first. You pay the least interest overall.
- **Snowball:** extra money goes to the smallest balance first. You pay a bit more interest, but you clear a whole debt sooner.
If you've abandoned a debt plan before, snowball is usually the better bet. The quick first win keeps you going.
## Keep a small fun line on purpose
Set aside $20-30 a month for something you enjoy, no questions asked. It isn't a leak, it's what stops the plan from feeling like a punishment.
## Automate the extra payment
Decide the amount once and schedule it the day after payday. A payment you have to remember rarely survives a busy month.
## When an unexpected cost hits
Pause the extra payment for that month instead of borrowing or draining your buffer. One paused month is fine. A new debt isn't.
> A plan you're still following in month twelve beats a perfect one you quit in month three.
""")
g("build-a-500-emergency-fund-on-minimum-wage","Saving","box","How to Build a $500 Emergency Fund on Minimum Wage",
"Start with $5, keep it separate, and be strict about what counts as an emergency.","""
Five hundred dollars sounds small until the week your car battery dies or a shift gets cut. The fund isn't meant to make you rich. It stops one bad week from turning into a month of debt.
## Start with $5, not $50
Move $5-10 the day you're paid, before anything else touches that money. At $10 a week you reach $500 in under a year, and it never needs a decision once it's set up.
## Where to keep it
- **A separate savings account**, ideally at a different bank from your checking.
- **Not a jar at home.** Cash gets spent on small things.
- **Not invested.** This money shouldn't lose value the week you need it.
## What counts as an emergency
A car repair that gets you to work, a medical cost, a bill you'd otherwise miss. Not a sale, not a gift, not "it's been a hard week."
## After you use it
Rebuild it before raising any other savings goal. It isn't spent, it's borrowed from a future bad week. Once you hit $500, keep the habit and aim for one month of expenses.
""")
g("save-for-a-goal-on-an-unpredictable-paycheck","Saving","journal","Saving for a Goal on an Unpredictable Paycheck",
"Save a percentage instead of a fixed amount, and keep your goal money apart from your buffer.","""
Most savings plans assume the same number lands every two weeks. Freelance work, gig shifts and seasonal jobs don't work that way, and those plans fall apart in the first slow month.
## Save a percentage, not a number
Instead of "save $100 a month," save 10% of whatever comes in, every time it comes in. A slow month still contributes. A good month contributes more, with no recalculating.
## Move it the moment you're paid
If the money sits in your account for even a day, it starts to feel like spending money. Transfer the percentage first.
## Keep goal savings and buffer separate
- **Buffer:** covers a slow month. Touch it when income drops below your baseline.
- **Goal:** the thing you're saving for. Touch it only when you reach it.
Mixing them means you can't tell whether you're making progress or just refilling the buffer.
## Round up on good months
When a payment is bigger than usual, save 20% of that one instead of 10%. It's money you weren't counting on, so your lifestyle doesn't change.
""")
g("the-real-cost-of-buy-now-pay-later-apps","Spending","wallet","The Real Cost of Buy Now, Pay Later Apps",
"Four easy payments feel harmless until several plans run at once. Here's the real risk and a simple safety rule.","""
Split it into four easy payments, no interest. For a single purchase that's often fine. The cost shows up when several plans run at once, across different apps that don't talk to each other.
## Why it doesn't feel like debt
A credit card gives you one statement and one scary number. Pay-later splits that into small payments spread over different weeks, so they're easy to ignore.
## The real risks
- **Stacking:** three or four plans can add up to more than a month's spending money.
- **Late fees:** a flat fee per missed payment adds up fast across several plans.
- **Credit impact:** depending on the provider and country, it can show on your credit report.
## A simple safety rule
Only use it for something you could pay for in full today, and treat the installments as cash-flow convenience. If the honest answer is "I can't afford this right now," pay-later just delays finding out.
> One plan at a time. Finish the last one before starting the next.
""")
g("grocery-shopping-on-a-tight-budget","Spending","notes","How to Grocery Shop on a Tight Budget Without the Coupon Hunt",
"Shop with a number, plan meals around the sales, and use three habits that beat coupons.","""
Extreme couponing makes good headlines, not realistic habits. Here's what saves money without turning shopping into a part-time job.
## Shop with a number, not just a list
Decide the total you'll spend before you go. A list without a number grows in the store. A number keeps every aisle decision tied to something real.
## Plan after you see the sales
Glance at what's discounted this week and build 2-3 meals from it. Most of the savings serious budgeters get come from this one swap.
## Three habits that matter more than coupons
- **Don't shop hungry.** Hunger changes what looks necessary.
- **Buy store brand first**, name brand only where you've noticed a real difference.
- **Cook one extra portion** and freeze it. Over a month that's several meals you didn't buy ingredients for.
## A note on bulk
Bulk only saves money if you use it before it spoils. Track your grocery spend for one month first, because you can't fix a number you haven't looked at.
""")
g("side-income-ideas-for-people-with-a-full-time-job","Earning","journal","Side Income Ideas That Fit Around a Full-Time Job",
"The honest filter isn't what pays most, it's what won't burn you out in three weeks.","""
Most side hustle lists assume unlimited free evenings. If you already work full time, ask what won't burn you out, not what pays the most.
## Low effort, fits around shift work
- **Selling unused items:** a one-time clear-out, real money, almost no ongoing time.
- **Task and delivery apps:** you pick the hours, no schedule commitment.
- **Renting a skill you already have:** tutoring, basic design or proofreading, paid per task.
## Higher effort, builds toward something
Digital products like templates, printables and guides take real upfront time and often weeks before the first sale. Once made, they need no ongoing hours.
## What to avoid
- Anything that needs a big purchase before you've confirmed demand.
- Multi-level marketing, where income depends on recruiting.
- Starting more than one new project at once.
> Pick one and give it a real month of steady effort before you judge it.
""")
g("how-to-negotiate-a-lower-bill","Spending","notes","How to Negotiate a Lower Bill Without Feeling Awkward",
"One sentence on a short phone call is often enough. Here's what's negotiable and what to say.","""
Negotiating feels confrontational, so most people never try and leave money on the table every month. Treat it as a short, low-stakes phone call, not an argument.
## What's usually negotiable
- Phone and internet plans
- Car and renters insurance
- Streaming and subscriptions, often through a retention offer
- Credit card annual fees
## The script
One sentence covers most cases: *"I've been a customer for [time], I'm looking at other options because of the price. Is there anything you can do?"* The person usually has a retention offer they're allowed to give.
## Why it works
Keeping a customer costs a company less than finding a new one. The discount isn't generosity, it's their own math.
## If the answer is no
Ask for the retention or loyalty team. The first person often can't offer as much.
> A five-minute call that saves $10 a month is $120 a year.
""")
g("the-envelope-method-for-a-debit-card-life","Budgeting","notes","The Envelope Method, Updated for a Debit-Card Life",
"Keep the hard stop that made envelopes work, without needing cash.","""
The classic envelope method splits cash into labeled envelopes. Almost nobody pays in cash now, but the logic still works.
## The idea that matters
When an envelope was empty, that category was done for the month. No borrowing from another envelope. That hard stop is the part worth keeping.
## Three ways to rebuild it digitally
- **Sub-accounts or vaults:** many banks offer them free. Put Wants in one, groceries in another. At zero, that spending stops.
- **A prepaid card per category:** load your Wants budget at the start of the month and use only that card.
- **A spreadsheet with a hard rule:** if moving money feels like too much friction, treat a bucket at zero as a real stop.
## The one rule
No borrowing between categories mid-month. Remove it and you're back to one blended number with no real limits.
> Choose the version that needs the least effort. The best system is the one you still use in month three.
""")
g("what-to-do-the-week-before-payday","Budgeting","wallet","What to Do the Week Before Payday When Money's Tight",
"Get through it without a credit card or payday loan: check deadlines, use your pantry, pause subscriptions.","""
Payday feels far away and the account is thinner than the calendar suggests. Here's how to get through it without reaching for a credit card or a payday loan.
## Check what's actually due
Confirm which bills have a real deadline this week. Many billers allow a short grace period.
## Eat down your pantry
Use what's already in the fridge and cupboards instead of a full grocery run. Most households have several meals hiding in half-used ingredients.
## Pause, don't cancel
Many subscriptions can be paused and resumed after payday.
## What to avoid this week
- **Payday loans and cash-advance apps:** steep fees, and they often start a repeat cycle.
- **A new buy-now-pay-later plan:** a new obligation in the tightest week rarely ends well.
- **Dipping into your emergency fund** for a predictable tight week.
> If this week is tight every month, your baseline budget needs adjusting, not just this week.
""")
g("talk-to-a-partner-about-money","Relationships","plan","How to Talk to a Partner About Money Without a Fight",
"Schedule it, lead with the shared goal, and treat different money habits as something to design around.","""
Money arguments are rarely about the money. They're about control, trust and different ideas of what's necessary. A few small changes in how it starts prevent most escalation.
## Schedule it, don't ambush it
Raising a spending worry mid-dinner puts the other person on the defensive. "Let's talk money Sunday evening" removes the surprise that turns a talk into a confrontation.
## Lead with the shared goal
"We're saving for X and I noticed Y" lands very differently from "you overspent again." Same conversation, but one starts as a team and the other as an accusation.
## Different habits aren't a moral failing
A cautious partner and a spontaneous one is a difference to design around. A small no-questions-asked amount for each person often resolves more tension than either one winning.
## If secrets are a pattern
One hidden purchase is a conversation. A pattern of hidden accounts is a trust issue a budget won't fix, so name it directly.
> Agree on one small shared goal this month. One number is easier than a whole philosophy.
""")
g("understand-your-credit-score","Debt & Credit","box","Understanding Your Credit Score Without the Jargon",
"What actually moves the number: paying on time and keeping balances low. Plus three myths to drop.","""
Credit scores come wrapped in jargon that makes them sound harder than they are. Here's what moves the number, in plain language.
## What it measures
A score is mostly a prediction of how likely you are to repay, based on your past pattern. It's closer to a weather forecast than a report card.
## The two things that matter most
- **Paying on time.** Usually the biggest factor. Autopay for at least the minimum removes the risk of forgetting.
- **How much of your limit you use.** Staying under about 30% tends to help. Paying down the balance before the statement date can help this specific factor.
## What matters less than people think
- Checking your own score is a soft check and doesn't hurt it.
- Carrying a balance on purpose doesn't help. Paying in full is fine.
- Your income isn't part of the score itself, though lenders look at it separately.
## One quiet habit
Keep old accounts open if there's no annual fee. Length of history counts, and closing an old account can shorten it.
> Never miss a payment, keep balances low, and be patient. Scores move in months, not days.
""")

def esc(s): return html.escape(s, quote=True)
def inline(s):
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
def render(body):
    out, ul = [], False
    for ln in body.splitlines():
        ln = ln.strip()
        if not ln: continue
        if ul and not ln.startswith("- "): out.append("</ul>"); ul = False
        if ln.startswith("## "): out.append(f"<h2>{inline(ln[3:])}</h2>")
        elif ln.startswith("> "): out.append(f"<blockquote>{inline(ln[2:])}</blockquote>")
        elif ln.startswith("- "):
            if not ul: out.append("<ul>"); ul = True
            out.append(f"<li>{inline(ln[2:])}</li>")
        else: out.append(f"<p>{inline(ln)}</p>")
    if ul: out.append("</ul>")
    return "\n".join(out)
def mins(b): return max(3, round(len(b.split())/200))
for x in G: x["mins"] = mins(x["body"]); x["url"] = f"/guides/{x['slug']}"; x["file"] = f"guides/{x['slug']}.html"

NEWS = f'''<form class="news" action="{FORM}" method="POST"><label for="em">Get the free one-page budget template</label>
<div><input id="em" type="email" name="email" placeholder="you@example.com" required><button type="submit">Send me the template</button></div>
<small>Only the template and new guides. No spam.</small></form>'''

def page(title, desc, path, main, extra_head="", og_img="/images/budget-notebook.jpg"):
    url = BASE + (path if path != "/" else "/")
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Plainfolio">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}{og_img}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Source+Serif+4:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
{extra_head}<script data-goatcounter="https://plainfolio.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
</head><body>
<header class="top"><a class="logo" href="/">plainfolio</a>
<nav><a href="/#guides">Guides</a><a href="/about">About</a><a href="/contact">Contact</a></nav></header>
<main>{main}</main>
<footer><div><strong>plainfolio</strong><p>Practical money guides for people starting from a small paycheck.</p></div>
<div><a href="/about">About</a> <a href="/contact">Contact</a> <a href="/privacy-policy">Privacy Policy</a> <button id="cookie-settings" type="button">Cookie settings</button></div>
<p class="fine">Plainfolio provides general educational information about personal finance and is not a substitute for advice from a licensed financial professional. &copy; 2026 Plainfolio.</p></footer>
<script src="/assets/site.js" defer></script></body></html>'''

def card(x):
    f, alt = IMG[x["img"]]
    return f'''<a class="card" href="{x["url"]}" data-cat="{esc(x["cat"])}"><img src="/images/{f}.jpg" alt="{esc(alt)}" loading="lazy" width="600" height="400"><span class="tag">{esc(x["cat"])}</span><h3>{esc(x["title"])}</h3><p>{esc(x["desc"])}</p><small>{x["mins"]} min read</small></a>'''

def write(path, content):
    p = os.path.join(os.path.dirname(__file__), path); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(content)

# Home
chips = '<button class="chip on" data-f="all">All guides</button>' + "".join(f'<button class="chip" data-f="{esc(c)}">{esc(c)}</button>' for c in CATS)
first = G[0]
home = f'''<section class="hero"><div><h1>Budgeting for people who don't earn much and are tired of being told to skip coffee.</h1>
<p>Twelve plain-language guides on budgeting, debt, saving and credit. No jargon, no guilt, no spreadsheet you'll abandon by Thursday.</p>
<a class="btn" href="{first["url"]}">Start with the 3-bucket budget</a></div>
<div class="heroimg"><img src="/images/expenses-receipts.jpg" alt="{esc(IMG["notes"][1])}" width="700" height="1050"></div></section>
<section class="wrap" id="guides"><h2 class="sec">All guides</h2><div class="chips">{chips}</div>
<div class="grid">{"".join(card(x) for x in G)}</div></section>
<section class="wrap narrow">{NEWS}</section>
<section class="wrap narrow about"><h2>Money advice for everyone else</h2>
<p>Most money advice online is written for people who already have money. Plainfolio is written for a small, ordinary paycheck: how to budget it, pay down debt without a no-fun lifestyle, and save something even when the math is tight. <a href="/about">More about Plainfolio</a>.</p></section>'''
write("index.html", page("Plainfolio: Budgeting on a Low Income, 12 Free Money Guides","12 free, no-jargon money guides on budgeting, debt payoff, a $500 emergency fund and more, built for real people on a small paycheck.","/",home))

# Guides
for i,x in enumerate(G):
    f, alt = IMG[x["img"]]
    rel = [G[(i+k)%12] for k in (1,2,3)]
    pin = f"https://www.pinterest.com/pin/create/button/?url={BASE}{x['url']}&media={BASE}/images/{f}.jpg&description={esc(x['title']).replace(' ','%20')}"
    ld = f'<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"{esc(x["title"])}","image":"{BASE}/images/{f}.jpg","dateModified":"2026-10-09","author":{{"@type":"Organization","name":"Plainfolio"}},"mainEntityOfPage":"{BASE}{x["url"]}"}}</script>'
    main = f'''<article class="post"><a class="back" href="/#guides">All guides</a><span class="tag">{esc(x["cat"])}</span>
<h1>{esc(x["title"])}</h1><p class="meta">{x["mins"]} min read &middot; Updated {UPDATED}</p>
<img class="lead" src="/images/{f}.jpg" alt="{esc(alt)}" width="1000" height="600">
<div class="prose">{render(x["body"])}</div>
<div class="share"><a class="btn pin" href="{pin}" target="_blank" rel="noopener">Save to Pinterest</a></div>
{NEWS}
<h2 class="sec">Keep reading</h2><div class="grid three">{"".join(card(r) for r in rel)}</div></article>'''
    write(x["file"], page(x["title"]+" | Plainfolio", x["desc"], x["url"], main, ld, f"/images/{f}.jpg"))

# About / Contact / Privacy
write("about.html", page("About Plainfolio","Plainfolio writes plain-language money guides for people living on a small paycheck.","/about",'''<article class="post"><h1>About Plainfolio</h1><div class="prose">
<p>Plainfolio started from a simple frustration: most money advice online is written for people who already have money. Plainfolio is written for everyone else.</p>
<p>I'm <strong>[Your name]</strong>, and I write practical, jargon-free guides on budgeting, saving, credit and the everyday money decisions that rarely make it into traditional finance content. [Add two sentences about why you started this site.]</p>
<p><strong>A note on our content:</strong> Plainfolio provides general educational information. We are not licensed financial advisors, and nothing here is personalized financial, legal or tax advice. For decisions specific to your situation, talk to a qualified professional.</p></div></article>'''))
write("contact.html", page("Contact Plainfolio","Questions, feedback, or a topic you'd like covered? Send Plainfolio a message.","/contact",f'''<article class="post"><h1>Contact us</h1><p>Questions, feedback or a topic you'd like covered? Write to <a href="mailto:hello@plainfoliomoney.com">hello@plainfoliomoney.com</a> or use the form.</p>
<form class="news" action="{FORM}" method="POST"><label for="n">Name</label><input id="n" name="name" required><label for="e">Email</label><input id="e" type="email" name="email" required><label for="m">Message</label><textarea id="m" name="message" rows="6" required></textarea><button type="submit">Send message</button></form></article>'''))
write("privacy-policy.html", page("Privacy Policy | Plainfolio","How Plainfolio collects, uses and protects information.","/privacy-policy",'''<article class="post"><h1>Privacy Policy</h1><p class="meta">Last updated: October 2026</p><div class="prose">
<h2>Information we collect</h2><p>Your email address and messages, only if you sign up or write to us (handled by our form provider, Formspree). Usage data such as pages visited, device and browser type, and approximate location, collected by the tools below only if you accept cookies.</p>
<h2>Analytics and advertising</h2><p>We use Google Analytics and the Meta Pixel to understand how visitors use the site and to measure our own ads. We also display advertisements served by <strong>Monetag</strong> and its partners, which may use cookies and collect your IP address and device information to show and measure ads. These providers act under their own privacy policies. Analytics and advertising scripts load only after you click Accept on the cookie banner. You can change your choice anytime with "Cookie settings" in the footer, and manage ad personalization in <a href="https://adssettings.google.com">Google Ads Settings</a> and <a href="https://www.facebook.com/adpreferences">Meta Ad Preferences</a>.</p>
<h2>Cookies</h2><p>We store your cookie choice on your device. Analytics and advertising cookies are optional. You can also block or delete cookies in your browser; the site keeps working.</p>
<h2>Third-party links</h2><p>We aren't responsible for the privacy practices of external sites we link to.</p>
<h2>Your rights</h2><p>Depending on where you live, you may have the right to access, correct or delete your data. Contact us to exercise these rights.</p>
<h2>Children</h2><p>This site is not directed at children under 13, and we do not knowingly collect their data.</p>
<h2>Changes</h2><p>We may update this policy and will post the new date here.</p></div></article>'''))

# sitemap, robots, vercel, ads
urls = ["/","/about","/contact","/privacy-policy"] + [x["url"] for x in G]
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{BASE}{u}</loc><lastmod>2026-10-09</lastmod></url>\n" for u in urls) + "</urlset>\n")
write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
write("vercel.json", '{\n  "cleanUrls": true,\n  "redirects": [\n    {"source": "/:path(.*)", "has": [{"type": "host", "value": "plainfoliomoney.com"}], "destination": "https://www.plainfoliomoney.com/:path", "permanent": true}\n  ]\n}\n')
print("built", len(urls), "pages")
