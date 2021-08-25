package com.example.operationx.gameplay;

import android.app.Activity;
import android.content.Context;
import android.graphics.Canvas;
import android.graphics.ColorFilter;
import android.graphics.Rect;
import android.graphics.drawable.Drawable;
import android.widget.ArrayAdapter;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.example.operationx.R;

import java.util.ArrayList;

public class GroundTile {
    private Activity currActivity;

    private int width, height, gameViewHeight, levelID;

    /**
     * Set up the class to make the ground for the levels
     * @param currActivity - ref to activity
     * @param width - width of each tile
     * @param height - height of each tile
     * @param gameViewHeight - size of the screen
     * @param levelID - level reference
     */
    public GroundTile(Activity currActivity, int width, int height, int gameViewHeight, int levelID){
        this.currActivity = currActivity;
        this.width = width;
        this.height = height;
        this.gameViewHeight = gameViewHeight;
        this.levelID = levelID;
    }

    public void displayGroundTiles(Canvas canvas, int xPos){
        if(levelID == 1){
            setUpLevelOne(canvas,xPos);
        }else if(levelID == 2){

        }
    }

    /**
     * Set up the level for one
     * @param canvas
     * @param xPos
     */
    private void setUpLevelOne(Canvas canvas, int xPos){
        Drawable tile1 = currActivity.getResources().getDrawable(R.drawable.ground_tile_1);
        Drawable tile2 = currActivity.getResources().getDrawable(R.drawable.ground_tile_2);
        for(int i = 0; i < 20; i++){
            tile1.setBounds(i*width + xPos,gameViewHeight/2,
                    i*width + width + xPos,gameViewHeight/2+height);
            tile1.draw(canvas);
        }

        for(int i = 1; i < 3; i++) {
            for (int j = 0; j < 20; j++) {
                tile2.setBounds(j * width + xPos, (gameViewHeight / 2) + height * i,
                        j * width + width + xPos, gameViewHeight / 2 + height * i + height );
                tile2.draw(canvas);
            }
        }
    }
    private void setUpLevelTwo(Canvas canvas, int xPos){

    }
}
