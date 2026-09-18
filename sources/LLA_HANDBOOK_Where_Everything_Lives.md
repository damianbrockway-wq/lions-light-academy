# Lions Light Academy — Where Everything Lives

**Last updated: 18 September 2026**

> **Everything is now in git.** The markdown sources and the build pipeline live in the repository alongside the site. Clone it and you have the whole thing.

This is the map. If you have just picked this up and know nothing, start here and you can find or rebuild anything.

Everything in this file is a real path or a real URL, checked on the day it was written.

---

## Read this first

Four things explain most of how LLA works:

1. **Every branded PDF is generated from a markdown file by a script.** Nothing is hand-made in a design tool. To fix a typo you edit the markdown and re-run the build — you never edit a PDF.
2. **The website is a folder of files in git.** Push to GitHub and Cloudflare publishes it about a minute later. There is no CMS and no admin login.
3. **Anything inside `site/` is public the moment it is pushed**, whether or not a page links to it. `/kit/` is unlisted, not private.
4. **The co-op's own Google account is `lionslightacademy2025@gmail.com`.** Classes, forms and completed paperwork belong to that account, not to a personal one.

---

## The website

| | |
|---|---|
| Live site | <https://lions-light-academy.pages.dev/> |
| Staff kit (unlisted) | <https://lions-light-academy.pages.dev/kit/> |
| Source on disk | `~/Documents/Claude/Projects/lla/site/` |
| GitHub | `github.com/damianbrockway-wq/lions-light-academy` |
| Hosting | Cloudflare Pages, deploys automatically on push to `main` |

### Publishing a change

```
cd ~/Documents/Claude/Projects/lla/site
git add -A
git commit -m "what changed"
git push
```

Live in about a minute. No other step.

### How the site is organised

| Path | What it is |
|---|---|
| `site/index.html` | The entire public site — one file. Resource cards live in `#libraryGrid` |
| `site/docs/` | Every public PDF families and teachers can reach |
| `site/kit/` | **Unlisted** staff printables — see below |
| `site/_headers` | Cloudflare rules: forces downloads on fillable PDFs, `noindex` on `/kit/` |
| `site/robots.txt` | Tells search engines to skip `/kit/`, `/sources/` and `/pipeline/` |
| `site/sources/` | **Every markdown source.** In git, so the documents have history |
| `site/pipeline/` | **Every build script.** In git, minus the ID card template — see below |

### The resource cards

Cards are filtered by a `data-category` attribute — `family`, `teacher`, `policy`, `curriculum`, `video`, `maine`. The tab buttons carry matching `data-lib` values. To add a document to the Families tab, the card needs `data-category="family"`.

The grid shows 8 cards and then a **Show all** button, so position matters: put important things high.

---

## The staff kit

**<https://lions-light-academy.pages.dev/kit/>** — on disk at `site/kit/`

Nothing on the site links to it and search engines are told to skip it. **It is unlisted, not private** — anyone with the address can open it. Never put rosters, family contact details or completed forms in there.

| File | What it is |
|---|---|
| `cleanup-cards-laminate.pdf` | 8 cards, one per landscape page, bordered — the set to print and laminate |
| `cleanup-cards-two-up.pdf` | Same 8 cards, two per page with cut lines |
| `cleanup-cards-full-page.pdf` | Same 8 cards, one per page, no border |
| `first-day-run-sheet.pdf` | The reusable blank template — whole day in clock order |
| `first-day-run-sheet-template.pdf` | Same file, kept under both names |
| `shed-attendance.pdf` | Fire-route headcount — 23 students, 6 adults, spare lines |
| `incident-report.pdf` | Blank incident form |
| `warning-record.pdf` | Blank Moderate-concern warning form |
| `supply-fee-receipts-001-009.pdf` | Payment log + 7 pre-numbered receipts + 2 spares |
| `teacher-id-standard.pdf` / `-small.pdf` | Teacher ID cards, two sizes |
| `teacher-id-blank-template.pdf` | For adding a teacher |

**Completed forms never go here.** A filled incident report names a child and their injury. Those live on your own machine, outside the repo.

---

## Public documents

All at `site/docs/`, all reachable at `https://lions-light-academy.pages.dev/docs/<filename>`.

### Families

| Document | File |
|---|---|
| Registration & Enrollment | `registration-enrollment.pdf` |
| Parent Packet v3.1 | `parent-packet.pdf` |
| Supply List | `supply-list.pdf` |
| Your First Day | `your-first-day.pdf` |
| Code of Conduct v1.2 | `code-of-conduct.pdf` |
| Student Pledge | `student-pledge.pdf` |
| Google Classroom — Families | `classroom-family-guide.pdf` |
| Co-op Day Schedule | `coop-day-schedule.pdf` |
| Field Trip Waiver | `field-trip-waiver.pdf` |
| Supply Fee Receipt (blank) | `supply-fee-receipt.pdf` |
| HS Credit Summary | `hs-credit-summary.pdf` |
| Maine Homeschool Checklist | `maine-homeschool-checklist.pdf` |

### Teachers

| Document | File |
|---|---|
| First Day Run-Through | `first-day-run-through.pdf` |
| First Day Run Sheet | `first-day-run-sheet.pdf` |
| When You Can't Be There (absence & cover) | `teacher-absence-plan.pdf` |
| Teacher & Mentor Guidebook v2.0 | `teacher-guidebook.pdf` |
| Teacher & Volunteer Expectations v2.0 | `teacher-volunteer-expectations.pdf` |
| Setting Up Your Google Classroom v1.3 | `classroom-setup-guide.pdf` |
| Supervision & Room Operations SOP v1.1 | `supervision-sop.pdf` |
| Technical Operations Handbook | `technical-operations.pdf` |

### Safety and policy

| Document | File |
|---|---|
| Student Safety & Emergency Plan v1.3 | `safety-emergency-plan.pdf` |
| Escalation & Discipline Policy v1.2.1 | `discipline-policy.pdf` |

---

## How a document gets made

**You never edit a PDF.** Every branded document is built from markdown.

| | |
|---|---|
| Markdown sources | **`site/sources/` — in git.** Also at `~/Documents/Claude/Projects/lla/DRAFT_*.md` |
| The build pipeline | **`site/pipeline/` — in git.** Also `lla-build-kit-2026-09-18.tar.gz`, which additionally has the fonts, logos and the ID card template |

### To change a document

1. Edit the matching `DRAFT_*.md`
2. Run `python3 brand/build.py` from the unpacked kit
3. Copy the new PDF into `site/docs/`
4. Commit and push

### Which source makes which PDF

| Source | Output |
|---|---|
| `DRAFT_Code_of_Conduct_v1.2.md` | `code-of-conduct.pdf` |
| `DRAFT_Escalation_Discipline_Policy_v1.2.md` | `discipline-policy.pdf` |
| `DRAFT_Parent_Packet_v3.md` | `parent-packet.pdf` |
| `DRAFT_Safety_Emergency_Plan_v1.3.md` | `safety-emergency-plan.pdf` |
| `DRAFT_Supervision_SOP_v1.1.md` | `supervision-sop.pdf` |
| `Teacher_Guidebook_2026_DRAFT.md` | `teacher-guidebook.pdf` |
| `DRAFT_Teacher_Volunteer_Expectations_v2.0.md` | `teacher-volunteer-expectations.pdf` |
| `DRAFT_Classroom_Setup_Guide.md` | `classroom-setup-guide.pdf` |
| `DRAFT_Classroom_Family_Guide_v1.0.md` | `classroom-family-guide.pdf` |
| `DRAFT_First_Day_Run_Through.md` | `first-day-run-through.pdf` |
| `DRAFT_Teacher_Absence_Plan_v1.0.md` | `teacher-absence-plan.pdf` |
| `DRAFT_Your_First_Day_v1.0.md` | `your-first-day.pdf` |
| `DRAFT_Supply_List_v1.0.md` | `supply-list.pdf` |
| `DRAFT_Technical_Operations.md` | `technical-operations.pdf` |

### The printables are built differently

These are laid out in code rather than markdown, in the kit's `cards/` and `brand/` folders:

| Script | Makes |
|---|---|
| `cards/build_set.py` + `stamp_full_set.py` | Cleanup cards, one per page |
| `cards/build_framed.py` | Cleanup cards, bordered for lamination |
| `cards/build_two_up.py` | Cleanup cards, two per page with cut lines |
| `cards/build_assignments.py` | The "where do I go after my last class" cover |
| `cards/build_run_sheet.py` | First day run sheet — **builds the dated sheet and the blank template from one source** |
| `cards/build_shed_attendance.py` | Fire-route headcount |
| `cards/build_records.py` | Incident report and warning record |
| `cards/build_student_conduct.py` | Student pledge |
| `cards/build_prayer.py` | Opening prayer |
| `brand/build_schedule.py` | The daily schedule — **asserts the arrival times before it writes** |
| `brand/build_receipt_run.py` | Pre-numbered supply fee receipts. `python3 build_receipt_run.py 12 10` = twelve starting at 010 |
| `brand/build_ids_scaled.py` + `stamp_id_cutlines.py` | Teacher ID cards at either size |

### Installing the pipeline on a new machine

```
tar xzf lla-build-kit-2026-09-18.tar.gz
pip install markdown playwright pypdf reportlab pillow --break-system-packages
playwright install chromium
```

---

## Changing something that appears in several places

This is the section that saves you. Most LLA facts live in more than one document, and the copies do not find each other.

**The rule: search the sources, never the PDFs.** A PDF is output. Change the source and rebuild, or your fix lasts until the next build and then vanishes.

### Where to search

```
cd ~/Documents/Claude/Projects/lla
grep -rn "the thing you are changing" DRAFT_*.md *.md
grep -n "the thing you are changing" site/index.html
```

Then the same search in the unpacked build kit, because three documents are built from HTML rather than markdown:

```
grep -rn "the thing" brand/form_body.html brand/schedule_page.html brand/teacher_id.html
```

**Those three catch people out.** The registration form, the daily schedule and the teacher ID cards have no `DRAFT_*.md` — looking only in markdown will tell you a fact appears nowhere when it appears three times.

### Worked example — changing the supply fee

Verified 18 September 2026. Every place `$200` actually appears:

| File | What it says | How to change it |
|---|---|---|
| `DRAFT_Parent_Packet_v3.md` | *"one supply fee per family, per year — **$200**, waived for families who lead a class"* | Edit, run `brand/build.py`, copy `parent-packet.pdf` to `site/docs/` |
| `brand/form_body.html` | *"Co-teaching, volunteering, or admin support — **$200 due**"* | Edit, run `brand/build_form.py`, copy `registration-enrollment.pdf` to `site/docs/` |
| `site/index.html` | Sponsor a Student: *"$200 covers one student's supplies for the year"* | Hand-edit the page. **It's prose, not just a number — reread the sentence** |

**About ten minutes.** Do not touch `LLA_MASTER_EXTRACT.md` or `LLA_Extract_2026-08.md` — archived research, published nowhere.

The **Supply Fee Receipt** deliberately has no amount printed on it; you write the figure in. That is why this is a ten-minute job and not an afternoon.

### Blast radius for the other things that change

Counts verified 18 September 2026.

| If you change… | Markdown sources | HTML templates | `site/index.html` |
|---|---|---|---|
| **The supply fee** | Parent Packet | `form_body.html` | 2 mentions |
| **Arrival time** | First Day Run-Through, Parent Packet, Your First Day | `schedule_page.html` | 2 mentions |
| **The co-op email** | Classroom Family Guide, Parent Packet, Supply List, Your First Day, Technical Operations | `teacher_id.html` | 4 mentions |
| **The web address** (own domain) | Parent Packet | `form_body.html`, `teacher_id.html` | 3 mentions |
| **A teacher leaving or joining** | — | `teacher_id.html` | Damian ×3, Ginny ×1 — no other teacher is named on the site |
| **The school year** | Technical Operations | every template's footer | 14 mentions |

The school year is the big one — it is stamped on nearly every document by `build.py`'s `DOCS` list rather than written in the markdown. Change it there once and every document picks it up on rebuild.

### After any change, check three things

1. **Read the rendered PDF**, not the script output. A build can report success and change nothing — see the `\u2013` trap below
2. **Search again** for the old value. If it still appears anywhere but the archives, you missed a copy
3. **Push**, and open the live page. Cloudflare takes about a minute


---

## What this file can and cannot rebuild

**Read this before you rely on it.** This handbook is a map, not a backup. It tells you where everything is and how it is made. It does not contain the things themselves.

| With… | You can rebuild |
|---|---|
| **This file alone** | Nothing. You would know exactly what to do and have no material to do it with |
| **This file + GitHub** | **Everything.** Site, images, PDFs, every markdown source, the whole build pipeline, and every past version |
| **The build kit tarball** | Every document from source, plus the teacher ID cards — which are the one thing not in git |

### What is not in this handbook

- **`index.html`** — 114 KB, the entire public website. This file describes its structure; it does not contain it
- **28 image files** — gallery photos, logos, favicons, social preview
- **The Google Calendar embed ID**
- **Cloudflare's settings** — which repository, which branch

All of the above are in GitHub. **That is the backup. This is the instructions.**

### The one thing deliberately kept out of git

`brand/teacher_id.html` is 9.4 MB because it embeds **photographs of real teachers**. Everything in the repository is published publicly the moment it is pushed, so that file is kept out on purpose.

It lives only in the local build kit tarball. `build_ids_scaled.py` and `stamp_id_cutlines.py` are in the repo and will work as soon as `teacher_id.html` is placed beside them from the tarball. There is a note in `pipeline/` saying so.

### Every document now has a source

As of 18 September 2026, all 22 public documents can be rebuilt. The last two holdouts — `hs-credit-summary.pdf` and `maine-homeschool-checklist.pdf` — were PDFs and nothing else, carried over from 2025. Both now have markdown sources in `sources/`, and both were rebuilt in the brand style in the process.

---

## Where the files are on disk

Everything lives under `~/Documents/Claude/Projects/lla/`.

| Folder | What's in it |
|---|---|
| `site/` | The website. This is the one that matters — it's in git |
| `pdf-2026/` | Working copies of every current PDF, plus teacher ID cards |
| `pdf-2026/cards/` | Individual teacher ID cards, one per person |
| `cleanup-cards/` | The cleanup card set in all three layouts |
| `id-template/` | Blank ID card template and its README |
| `docs/` | **Historical.** 2025-era documents and original photos. Nothing current |
| `_retired/` | Superseded documents kept for reference — do not publish these |
| `_to_delete/` | Staging area for things being removed. Safe to empty |
| `_site-backups/` | Copies of `index.html` from before major redesigns |

---

## Backups — what exists and what doesn't

**Be honest with yourself about this section.** It is the part most likely to matter and least likely to be checked.

| What | Where | Covers |
|---|---|---|
| **The website, all history** | GitHub — `github.com/damianbrockway-wq/lions-light-academy` | Every version of every file ever pushed. This is the real backup |
| **The build pipeline** | `lla-build-kit-2026-09-18.tar.gz` | All 19 build scripts, fonts, logos, and every markdown source |
| **Older pipeline** | `lla-build-kit.tar.gz` (Aug 29), `build-pipeline.tar.gz` | Superseded. Missing the run sheet, records, schedule and receipt builders |
| **Site redesign history** | `_site-backups/` | Five older `index.html` versions |
| **Superseded documents** | `_retired/` | Old enrollment form, policy index, training acknowledgment |

### What is NOT backed up

- **The markdown sources are only in one place** — the project folder. They are not in git. If that folder is lost, every document has to be rewritten from its PDF. **Putting `DRAFT_*.md` into the git repo would fix this in one commit** and is the single best thing you could do for resilience.
- **Google Classroom, Drive and the calendar** live in `lionslightacademy2025@gmail.com`. No local copy.
- **Completed paperwork** — registrations, signed pledges, receipts — wherever you filed them. Not in any system described here.

---

## Accounts and who owns what

| | |
|---|---|
| Co-op Google account | `lionslightacademy2025@gmail.com` — classes, forms, calendar, completed paperwork |
| GitHub | `damianbrockway-wq` |
| Hosting | Cloudflare Pages, connected to the GitHub repo |
| Calendar | Google Calendar, embedded on the homepage. **This is the authoritative schedule** — the Parent Packet says so to families |

**Google Classroom invitations exist only in email.** Nothing appears inside Classroom until the invitation is accepted from the inbox. A teacher or student seeing an empty Classroom almost always has an unaccepted invite, or is signed into the wrong Google account.

---

## The shape of a co-op day

Every Tuesday, 15 September 2026 to 11 May 2027.

| | |
|---|---|
| Teachers arrive | 8:30 |
| Students arrive | 8:45 |
| Arrival + Worship | 8:45 – 9:00 |
| Classes | 9:00 onward — block lengths differ by age track |
| Lunch, whole school | 11:50 – 12:30 |
| Last class | 12:30 – 1:30 |
| Cleanup + Examen | 1:30 – 1:45 |
| Dismissal | 1:45 |

Rooms: **Gray** (High School), **Yellow** (Middle School), **Main** (Elementary), plus hallways, entryway, two bathrooms and the teacher lounge.

**Cleanup leads** — Gray: Damian · Yellow: Erika · Main Room & Hallways: Jess & Ginny · Boys Bathroom: Damian · Girls Bathroom: Erika · Teacher Lounge & Outside: Leah · Final Walkthrough: Damian.

**Vacuum route:** Yellow → Gray → Main Room (entryway rug) → supply closet. One route, no waiting. Everywhere else is swept.

**Emergency roles** — Incident Lead: Damian or Ginny (both paramedics) · Calls 911: Erika · Contacts parents: Savannah. Fire meeting point is the shed behind the building, and attendance is taken there.

---

## Things that will bite you

**Anything in `site/` is public once pushed.** Unlisted is not private.

**The parent portal password is in the page source.** `index.html` contains `const PARENT_PASSWORD='lionslight2026'`. Anyone who views source can read it. Treat everything behind it as public.

**`build.py` stores some punctuation as escape sequences** (`–` rather than the character). A find-and-replace using the real character silently misses. Always confirm a version change by reading the rendered PDF.

**Running git through the Claude desktop bridge leaves a stale `.git/index.lock`**, which blocks the next commit with a confusing error. Delete it if git complains.

**Money runs through a personal account** until LLA has its own. The co-op halves of the supply fee receipts and the payment log are the only record that it was the co-op's money. Keep them together.

---

## Still outstanding

| | |
|---|---|
| 🟠 | **Adult Screening Standard** is still a draft. The Parent Packet and Safety Plan both promise background checks; the standard behind that promise was never published |
| 🟠 | **Enrollment form is still titled 2025–2026** |
| 🟠 | **No who's-who for families.** Not one teacher is named anywhere families can see |
| 🟠 | **First Day Run-Through says teachers arrive 8:15.** It's 8:30 |
| 🟡 | **Insurance in writing** from the host church. LLA is an unaffiliated outside group |
| 🟡 | **Maine nonprofit filing** → EIN → bank account → 1023-EZ |
| 🟡 | **Own domain.** Still on `.pages.dev`, which is baked into the ID cards and several documents |
| 🟡 | **Teacher ID photos** for Leah and Jess |

---

*Lions Light Academy · Winslow, Maine · Tuesday co-op, 2026–2027*
