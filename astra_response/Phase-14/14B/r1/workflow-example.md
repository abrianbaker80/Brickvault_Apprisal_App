# Local workflow example

From the application repository root, use the existing API Python environment:

    & services/api/.venv/Scripts/python.exe scripts/reference_candidates.py compare --image "<explicitly selected local photo>"

The CLI prompts for a short visible description. Add a second --image if selected.
Alternatively supply a protected --query-file containing description/visual_clues,
or select one retained clue explicitly:

    & services/api/.venv/Scripts/python.exe scripts/reference_candidates.py compare --image "<selected photo>" --clues-file "<retained result>" --object-index 0 --candidate-index 0 --clue-field visual_clues --clue-index 0

No prior candidate identifier, expected label, filename or reviewer conclusion is
included in the query. Selected text containing catalog IDs/paths is refused.
Only the selected supporting_visual_clues/supporting_text_clues field is read.

Open the returned comparison HTML locally. Source URLs are displayed as text;
opening the report makes no remote request. Reports embed approved local raster
bytes, retain attribution and show candidate/ranking/canonical/view limitations.

    & services/api/.venv/Scripts/python.exe scripts/reference_candidates.py review --run "<returned run ID>"
    & services/api/.venv/Scripts/python.exe scripts/reference_candidates.py reopen --run "<same run ID>"

Review supports provisional, compatible (several ranks), none, insufficient_evidence
with a needed view, or known_identity explicitly marked operator-supplied. Notes
are append-only and separate from the comparison, predictions and confirmed labels.

The protected three-reference index is already derived from the corrected retained
source/permission records. No new cards or photographs are needed to use this slice.
The default comparison accesses the owned development catalog and restores its
prior service state. --reference-only is an explicit restricted-coverage mode; it
marks the catalog unqueried and canonical reference status not_checked.
