# Document sources

Every branded PDF on this site is generated from one of these files.

**Never edit a PDF.** Edit the markdown here, rebuild with `pipeline/brand/build.py`,
and copy the result into `docs/`. The mapping from source to output is the `DOCS`
list at the top of `build.py`, and is also written out in
`sources/LLA_HANDBOOK_Where_Everything_Lives.md`.

Three documents are not markdown — the registration form, the daily schedule and
the teacher ID cards are built from HTML templates in `pipeline/brand/`. If you go
looking for their `DRAFT_*.md` you will not find one.
