package com.abrianbaker.brickvault.appraisal;

import android.content.Intent;
import android.os.Bundle;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    protected void onCreate(Bundle state) {
        // An OS-restored task must never replay its original Share payload. Same-process
        // unfinished bytes live only in ShareIntake; a cold process has no intake to restore.
        if (state != null || (getIntent() != null
                && (getIntent().getFlags() & Intent.FLAG_ACTIVITY_LAUNCHED_FROM_HISTORY) != 0)) {
            setIntent(ordinaryLaunch());
        }
        registerPlugin(BrickVaultSharePlugin.class);
        super.onCreate(state);
    }

    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        if (intent != null && (Intent.ACTION_SEND.equals(intent.getAction()) || Intent.ACTION_SEND_MULTIPLE.equals(intent.getAction()))) {
            setIntent(ordinaryLaunch());
            intent.replaceExtras((Bundle) null);
            intent.setClipData(null);
            intent.setData(null);
        }
    }

    private Intent ordinaryLaunch() { return new Intent(this, MainActivity.class).setAction(Intent.ACTION_MAIN); }
}
