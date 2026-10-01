# Report-only storage consistency

Library entry point: brickvault_api.images.consistency.inspect_storage(database,store).
It captures blob metadata in a bounded read-only repeatable-read transaction,
verifies referenced hash/key/size, and enumerates physical storage. Result lists
missing referenced objects, corrupt hash/size objects, complete unreferenced objects,
staging leftovers and unexpected malformed objects. Keys are relative storage keys,
never absolute filesystem paths. No deletion or repair occurs.

A definitive orphan report requires uploads stopped: publication legitimately
precedes metadata commit. A synthetic disposable test injects a missing original,
one complete orphan, one staging object and corrupt bytes, proves report detection
and proves the inspector preserves the objects. No operational invocation against
Brian's storage. A polished CLI, operational quiescence and private backup/restore
procedures are deferred to separately authorized later checkpoints.
