# Offline recovery custody

**PASS.** Brian selected replacement removable SD media. The v2 helper encrypted the minimum recovery material, decrypted the bundle directly from that media into a restricted temporary location, validated its manifest/hashes and independently opened both accepted encrypted repositories. The no-secret manifest digest was `7b0257c774c5a88c4bbe56f2946d103f957dc06a75ad9568346a9ed9673822e0`. Brian confirmed the new unlock phrase is recorded physically away from the VM and laptop; the replacement card was removed from the laptop.

The first card's verification failed because temporary Windows OpenSSH key permissions were too broad. That ACL root cause was fixed. The first attempt's phrase appeared in chat, so its bundle was disqualified; Brian confirmed that card was destroyed or permanently retired under his control. The replacement used a fresh phrase that was not shared in chat.

No unlock phrase, media path/serial, recovery key, OAuth token, restic password or exact repository ID is included in this package.
