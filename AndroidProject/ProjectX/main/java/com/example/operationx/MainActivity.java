package com.example.operationx;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.FragmentTransaction;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.media.MediaPlayer;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;

import com.example.operationx.gameplay.OperationGameplay;

import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {
    ArrayList<GameLevel> levels = new ArrayList<>();

    private Activity activity;
    public static MediaPlayer MUSIC;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        activity = this;
        setContentView(R.layout.activity_main);
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                SharedPreferences sharedPref = getSharedPreferences("Settings", Context.MODE_PRIVATE);
                float volumeNumber = Float.valueOf(sharedPref.getInt(getString(R.string.saved_volume_key), 1));
                if(volumeNumber == 1)
                    volumeNumber = 100;

                MUSIC = MediaPlayer.create(activity,R.raw.blazer_rail);
                MUSIC.setVolume( volumeNumber/100, volumeNumber/100);
                MUSIC.setLooping(true);
                MUSIC.start();
            }});

        MainMenuFragment mmFrag = new MainMenuFragment();
        FragmentTransaction transaction =
                getSupportFragmentManager().beginTransaction();
        transaction.replace(R.id.main_layout,
                mmFrag);
        transaction.commit();
    }


    public void startGame(View view){
        Intent intent = new Intent(this, OperationGameplay.class);
        startActivity(intent);
    }
}



