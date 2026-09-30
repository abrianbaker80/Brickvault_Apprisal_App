# Catalog semantic equivalence — PASS

An independent CSV reader consumed the unchanged protected gzip source, preserved physical starting-line locators (including headers/multiline rows), and compared complete native identity and inventory sets and sorted line tuples against the qualified canonical result. It does not derive expected results from the repaired SQL. Dataset counts equal all twelve source counts, totaling 1,898,466 rows; duplicate native/canonical identities are absent.

| Canonical identity kind | Rows |
| --- | ---: |
| color | 275 |
| minifigure | 17,225 |
| part | 64,620 |
| part_category | 76 |
| set | 28,278 |
| theme | 496 |

| Independent source/canonical line comparison | Lines | Normal quantity | Spare quantity |
| --- | ---: | ---: | ---: |
| inventory_minifigs | 25,820 | 27,352 | 0 |
| inventory_parts | 1,557,375 | 5,126,811 | 130,863 |
| inventory_sets | 5,210 | 10,264 | 0 |

There are 47,452 inventory revisions, 1,588,405 inventory lines, 272,667 provider identities and 1,898,466 evidence rows. Native part/color, minifigure and nested-set targets remain distinct. Per-dataset cryptographic tuple digests, normal/spare totals, native versions and owners all match independent source expectations.

Exact **75331-1** exists once, with actual name **The Razor Crest**, one inventory and four directly recorded minifigure lots; exact native figure relationships and quantities match the source. The comparison covers all suffixed set identifiers, rather than only this one example. Catalog relationships are not a claim of physical completeness or price evidence.

Semantic fingerprint: `8f37571222fb078a2f75927ee1c58a7c3a90994bb24bee269270f784ebd48395`. It matches the unmodified baseline candidate, recomputation after qualification and the retirement receipt. Native inventory/content-digest set SHA-256: `cde10b1d49881bbea1006885a580bef4887119ae51fd05f9799807fb9eaf7a60`; a clean rebuild produced the same digest set. Structural validation is **passed**. No activation occurred.

The three batching PostgreSQL tests complement this full-source proof: exact once-only line coverage/quantities, gzip multiline sparse physical locators with an empty interior span, and failure after the first batch rolling back all candidate data while retaining truthful failed audit/staging. Protected historical parser/search tests remain byte-identical. See [semantic evidence](evidence/qualified-semantics.json) and [focused PostgreSQL results](evidence/socket-recovery-tests.json).
