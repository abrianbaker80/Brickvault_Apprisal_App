# BlobStore and thumbnail-v1

Filesystem storage implements an interface exposing publish/read/stat/enumerate,
without deletion. BVA_IMAGE_BLOB_ROOT is configurable, private and outside static/web
roots; omitted configuration leaves image upload/content unavailable. Keys are
sha256/ab/cd/full-hash, derived only from server-computed exact-byte SHA-256.
Same-directory temporary writes flush/fsync; atomic hard links publish without
replacing an existing object. Existing objects are hash/size verified before reuse.
The actual Windows synthetic filesystem path passed publication/reuse/corruption
tests. A future Linux deployment filesystem remains separately unqualified.

Pillow 12.3.0 fully decodes single-frame JPEG/PNG/WebP. The receive path bounds
declared and chunked multipart to 26 MiB before spooling; file limit 25 MiB;
dimensions <=16000 on either side and <=40 megapixels. Format is decoded rather
than trusted from name/MIME. Animation, corrupt/truncated/unsupported input and
decompression bombs fail closed. Decode/publication run outside the event loop.

Thumbnail-v1 applies EXIF orientation, fits <=512x512 without enlargement,
composites transparency on white, creates fresh RGB pixels and encodes JPEG quality
85 without inherited source metadata. Exact originals remain unchanged. Lineage
records recipe parameters and actual decoder/version. Originals and thumbnails
have distinct semantic IDs, including if their physical hashes match.

Both complete objects publish before the DB commit. Failed commits can leave
unreferenced complete objects; successful retry verifies/reuses those objects.
There is no automatic deletion. A corrupt existing key is never overwritten.

Pinned decoder release: [Pillow 12.3.0](https://pillow.readthedocs.io/en/stable/releasenotes/12.3.0.html).
Multipart dependency: [python-multipart](https://pypi.org/project/python-multipart/).
