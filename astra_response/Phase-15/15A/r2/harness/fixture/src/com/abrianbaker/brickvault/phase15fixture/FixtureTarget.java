package com.abrianbaker.brickvault.phase15fixture;

import android.content.Context;
import android.content.pm.ApplicationInfo;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.content.pm.Signature;
import android.os.Build;
import java.io.FileInputStream;
import java.io.InputStream;
import java.security.MessageDigest;

/** Pins this temporary helper to the exact accepted localhost TEST artifact. */
final class FixtureTarget {
    static final String APK_SHA256 = "eb18c9119ac483c41c70c9387dec1e3baf268a792a18b07dfbcbcbc421085bcf";
    static final String SIGNER_SHA256 = "e4d375e7f1611cb1113620379ea171a176f32bb11cc7528b6c176a1a08dffe72";

    @SuppressWarnings("deprecation")
    static ApplicationInfo require(Context context) throws Exception {
        PackageManager manager = context.getPackageManager();
        ApplicationInfo target = manager.getApplicationInfo(FixtureCases.TARGET, 0);
        if ((target.flags & ApplicationInfo.FLAG_DEBUGGABLE) == 0 || target.uid == context.getApplicationInfo().uid)
            throw new SecurityException("Exact distinct TEST application required");
        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        try (InputStream input = new FileInputStream(target.sourceDir)) {
            byte[] buffer = new byte[65536];
            int count;
            while ((count = input.read(buffer)) != -1) digest.update(buffer, 0, count);
        }
        if (!APK_SHA256.equals(hex(digest.digest()))) throw new SecurityException("Exact TEST APK required");
        Signature[] signatures;
        if (Build.VERSION.SDK_INT >= 28) {
            PackageInfo info = manager.getPackageInfo(FixtureCases.TARGET, PackageManager.GET_SIGNING_CERTIFICATES);
            if (info.signingInfo == null) throw new SecurityException("TEST signer required");
            signatures = info.signingInfo.getApkContentsSigners();
        } else signatures = manager.getPackageInfo(FixtureCases.TARGET, PackageManager.GET_SIGNATURES).signatures;
        if (signatures == null || signatures.length != 1 || !SIGNER_SHA256.equals(hex(MessageDigest.getInstance("SHA-256").digest(signatures[0].toByteArray()))))
            throw new SecurityException("Retained TEST signer required");
        return target;
    }
    private static String hex(byte[] values) {
        char[] alphabet = "0123456789abcdef".toCharArray();
        char[] result = new char[values.length * 2];
        for (int i = 0; i < values.length; i++) {
            result[i * 2] = alphabet[(values[i] & 255) >>> 4];
            result[i * 2 + 1] = alphabet[values[i] & 15];
        }
        return new String(result);
    }
}
