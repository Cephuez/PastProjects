package com.example.operationx.gameplay;

import android.app.Activity;
import android.graphics.Canvas;
import android.graphics.drawable.Drawable;

import com.example.operationx.R;

public class BackgroundTiles {
    private Activity currActivity;

    private int fixWidthBackground, gameViewHeight, levelID;

    /**
     * Set up the class to display the game's background
     * @param currActivity - reference to main activity
     * @param fixWidthBackground - width of the screen
     * @param gameViewHeight - height of the screen
     * @param levelID - level number
     */
    public BackgroundTiles(Activity currActivity, int fixWidthBackground, int gameViewHeight,int levelID){
        this.currActivity = currActivity;
        this.fixWidthBackground = fixWidthBackground;
        this.gameViewHeight = gameViewHeight;
        this.levelID = levelID;
    }

    /**
     * Set up the background
     * @param canvas - canvas reference
     * @param xPos - reference to x location
     */
    public void updateBackground(Canvas canvas, int xPos){
        if(levelID == 1){
            backgroundLevelOne(canvas, xPos);
        }else if(levelID == 2){
            backgroundLevelTwo(canvas,xPos);
        }
    }

    /**
     * Set up background for level 1
     *
     * @param canvas - ref to canvas
     * @param xPos - reference to x location
     */
    private void backgroundLevelOne(Canvas canvas, int xPos) {
        Drawable background = currActivity.getResources().getDrawable(R.drawable.level_1_background);
        for (int i = 0; i < 10; i++) {
            background.setBounds(i * fixWidthBackground + xPos, 0,
                    i * fixWidthBackground + fixWidthBackground + xPos, gameViewHeight / 2);
            background.draw(canvas);
        }
    }

    /**
     * Set up background for level 2
     *
     * @param canvas - ref to canvas
     * @param xPos - reference to x location
     */
    private void backgroundLevelTwo(Canvas canvas, int xPos){
        Drawable background = currActivity.getResources().getDrawable(R.drawable.sky_sprite_1);
        for (int i = 0; i < 30; i++) {
            for(int j = 0; j < 2; j++) {
                background.setBounds(i * fixWidthBackground + xPos, (gameViewHeight / 2) * j,
                        i * fixWidthBackground + fixWidthBackground + xPos, (gameViewHeight / 2) + (gameViewHeight / 2) * j);
                background.draw(canvas);
            }
        }
    }
}
