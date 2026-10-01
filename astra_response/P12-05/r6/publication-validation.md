# R6 publication boundary

New r6 documentation artifacts only are committed/pushed on the isolated
astra-response checkout, from accepted parent `57dec1e5f7b0538c75f2a17a824c15aba3083dc2`. R1-r5 are
byte-preserved; no source, executable repair, Plans 100/101 or protected files
are included. The final Plan 099/102 review copies come from the exact local
main commit; only their relative Markdown links are adapted for the package.
The documentation patch contains the complete reviewed five-file commit changes,
with zero context to avoid whitespace-only context lines in the published patch.

Main remains at its local closure commit, unpushed with an empty index. The only
residual dirty files are the three protected files, whose raw hashes are checked
again after publication. Remote main remains at its captured baseline, checked
with Git only. No live production, test/build or operational evidence is rerun.

The literal file inventory, complete publication diff, cached whitespace, JSON,
local Markdown links and identifier/credential/private-path patterns are checked
before publication. [Closeout validation](closeout-validation.json) records the
local receipt and documentation checks. Publication identity and commit-pinned
REVIEW.md are returned after the push; the package avoids a circular self-hash.
