package com.abrianbaker.brickvault.phase15fixture;

import android.content.Context;
import android.net.Uri;
import java.util.Arrays;
import java.util.List;
import java.util.UUID;

final class FixtureCases {
    static final String TARGET = "com.abrianbaker.brickvault.appraisal";
    static final String AUTHORITY = "com.abrianbaker.brickvault.phase15fixture.images";
    static final String TAG = "BV15Fixture";
    static final String PREFS = "synthetic_fixture_sessions";
    static final String[] CASES = {"single", "triple", "duplicate", "missing", "unsupported", "corrupt", "oversize", "revoked"};

    static boolean known(String value) { return value != null && Arrays.asList(CASES).contains(value); }
    static List<String> leaves(String value) {
        switch (value) {
            case "single": return Arrays.asList("A.png");
            case "triple": return Arrays.asList("A.png", "B.png", "C.png");
            case "duplicate": return Arrays.asList("A.png", "B.png", "A-copy.png");
            case "missing": return Arrays.asList("A.png", "missing.png", "C.png");
            case "unsupported": return Arrays.asList("A.png", "unsupported.gif", "C.png");
            case "corrupt": return Arrays.asList("A.png", "corrupt.png", "C.png");
            case "oversize": return Arrays.asList("A.png", "oversize.png", "C.png");
            case "revoked": return Arrays.asList("A.png", "revokedB.png", "C.png");
            default: throw new IllegalArgumentException("Unknown fixed fixture case");
        }
    }
    static String create(Context context, String value) {
        if (!known(value)) throw new IllegalArgumentException("Unknown fixed fixture case");
        String run = UUID.randomUUID().toString().replace("-", "");
        if (!context.getSharedPreferences(PREFS, Context.MODE_PRIVATE).edit().putString(run, value).commit())
            throw new IllegalStateException("Fixture session could not be recorded");
        return run;
    }
    static Uri uri(String run, String leaf) {
        return new Uri.Builder().scheme("content").authority(AUTHORITY).appendPath("share").appendPath(run).appendPath(leaf).build();
    }
    static String resolve(Context context, Uri uri) {
        if (!"content".equals(uri.getScheme()) || !AUTHORITY.equals(uri.getAuthority()) || uri.getQuery() != null || uri.getFragment() != null)
            throw new IllegalArgumentException("Invalid fixture URI");
        List<String> path = uri.getPathSegments();
        if (path.size() != 3 || !"share".equals(path.get(0)) || !path.get(1).matches("[0-9a-f]{32}"))
            throw new IllegalArgumentException("Invalid fixture URI");
        String value = context.getSharedPreferences(PREFS, Context.MODE_PRIVATE).getString(path.get(1), null);
        if (!known(value) || !leaves(value).contains(path.get(2))) throw new IllegalArgumentException("Unknown fixture URI");
        return value;
    }
}
