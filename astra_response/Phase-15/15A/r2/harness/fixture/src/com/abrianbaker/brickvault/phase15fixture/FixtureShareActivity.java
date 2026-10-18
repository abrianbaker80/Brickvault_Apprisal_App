package com.abrianbaker.brickvault.phase15fixture;

import android.app.Activity;
import android.content.ClipData;
import android.content.ComponentName;
import android.content.Intent;
import android.content.pm.ApplicationInfo;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.Spinner;
import android.widget.TextView;
import java.util.ArrayList;

/** Visible, explicitly pressed, fixed TEST cases only; no collection or network. */
public final class FixtureShareActivity extends Activity {
    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setPadding(32, 48, 32, 32);
        TextView title = new TextView(this);
        title.setText("BrickVault Phase 15A TEST Fixture Sender\nGenerated images only. Send explicitly to the reviewed BrickVault app.");
        layout.addView(title);
        TextView status = new TextView(this);
        String requested = getIntent().getStringExtra("case");
        if (requested != null && !FixtureCases.known(requested)) {
            status.setText("Unknown fixture case refused.");
            layout.addView(status);
            setContentView(layout);
            return;
        }
        Spinner cases = new Spinner(this);
        cases.setContentDescription("Fixture case");
        cases.setAdapter(new ArrayAdapter<String>(this, android.R.layout.simple_spinner_dropdown_item, FixtureCases.CASES));
        if (requested != null) {
            for (int i = 0; i < FixtureCases.CASES.length; i++) if (requested.equals(FixtureCases.CASES[i])) cases.setSelection(i);
        }
        layout.addView(cases);
        Button send = new Button(this);
        send.setText("Send selected fixture case");
        send.setOnClickListener(view -> {
            try {
                String value = (String) cases.getSelectedItem();
                ApplicationInfo target = FixtureTarget.require(this);
                String run = FixtureCases.create(this, value);
                ArrayList<Uri> uris = new ArrayList<>();
                for (String leaf : FixtureCases.leaves(value)) uris.add(FixtureCases.uri(run, leaf));
                Intent intent = new Intent(uris.size() == 1 ? Intent.ACTION_SEND : Intent.ACTION_SEND_MULTIPLE);
                intent.setComponent(new ComponentName(FixtureCases.TARGET, FixtureCases.TARGET + ".MainActivity"));
                intent.setType("image/*");
                intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
                ClipData clip = new ClipData("Generated BrickVault TEST fixtures", new String[]{"image/png", "image/gif"}, new ClipData.Item(uris.get(0)));
                for (int i = 1; i < uris.size(); i++) clip.addItem(new ClipData.Item(uris.get(i)));
                intent.setClipData(clip);
                if (uris.size() == 1) intent.putExtra(Intent.EXTRA_STREAM, uris.get(0));
                else intent.putParcelableArrayListExtra(Intent.EXTRA_STREAM, uris);
                Log.i(FixtureCases.TAG, "event=share_requested case=" + value + " run=" + run + " targetUid=" + target.uid + " entries=" + uris.size());
                status.setText("Sent generated " + value + " case. Run " + run);
                startActivity(intent);
            } catch (Exception exception) {
                Log.e(FixtureCases.TAG, "event=fixture_launch_refused");
                status.setText("Fixture launch failed; no alternate target or URI was used.");
            }
        });
        layout.addView(send);
        layout.addView(status);
        setContentView(layout);
    }
}
