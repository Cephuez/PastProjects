package com.example.operationx.gameplay;

import android.app.Activity;
import android.graphics.Canvas;
import android.graphics.Rect;
import android.graphics.drawable.Drawable;
import android.widget.ArrayAdapter;

import com.example.operationx.R;

import java.util.ArrayList;

public class LevelBoundaries {
    private Activity currActivity;
    private int width, height, gameViewHeight, levelID;
    private ArrayList<Rect> endBoundaries;
    private Rect finishLine;

    /**
     * Set up the boundaries for the level
     * @param currActivity - ref to activity
     * @param width - width of the level
     * @param height - height of the level
     * @param gameViewHeight - size of the screen
     * @param levelID - level reference
     */
    public LevelBoundaries(Activity currActivity, int width, int height, int gameViewHeight, int levelID){
        this.currActivity = currActivity;
        this.width = width;
        this.height = height;
        this.gameViewHeight = gameViewHeight;
        this.levelID = levelID;
    }

    public ArrayList<Rect> getEndBoundariesList(){
        return endBoundaries;
    }

    /**
     * Display the boundaries of the game level
     * @param canvas
     * @param xPos
     */
    public void displayBoundaries(Canvas canvas, int xPos){
        endBoundaries = new ArrayList<Rect>();
        if(levelID == 1){
            backgroundLevelOne(canvas, xPos);
        }else if(levelID == 2){
            backgroundLevelTwo(canvas,xPos);
        }
    }

    public boolean reachFinishLine(Player player){
        return player.getBounds().intersect(finishLine);
    }

    /**
     * Set the background for the level
     * @param canvas - reference to canvas
     * @param xPos - position of the canvas
     */
    private void backgroundLevelOne(Canvas canvas, int xPos){
        Drawable endBackground = currActivity.getResources().getDrawable(R.drawable.ground_tile_2);
        Drawable endPoint = currActivity.getResources().getDrawable(R.drawable.sky_sprite_1);
        for(int i = 0; i < 5; i++) {
            for (int j = -5; j < 0; j++) {
                endBackground.setBounds(j * width + xPos, height * i,
                        j * width + width + xPos, height * i + height );
                endBackground.draw(canvas);
            }
        }

        for(int i = 0; i < 5; i++) {
            for (int j = 20; j < 25; j++) {
                endBackground.setBounds(j * width + xPos, height * i,
                        j * width + width + xPos, height * i + height );
                endBackground.draw(canvas);
            }
        }

        for(int i = 1 ; i < 3; i++){
            endPoint.setBounds(20 * width + xPos, height * i,
                    20 * width + width + xPos, height * i + height );
            endPoint.draw(canvas);
        }

        finishLine = new Rect(20 * width + xPos, height * 1,
                20*width + width + xPos, height * 2 + height);

        endBoundaries.add(new Rect(-width + xPos, 0, -width + width + xPos, gameViewHeight));
        endBoundaries.add(new Rect(20 * width + xPos, 0, 20 * width + width + xPos, gameViewHeight));
    }

    /**
     * Get the player's boundaries
     * @param playerBoundaries
     * @return
     */
    public boolean playerOnEndBoundaries(Rect playerBoundaries){
        for(int i = 0; i < endBoundaries.size(); i++){
            if(endBoundaries.get(i).intersect(playerBoundaries))
                return true;
        }
        return false;
    }

    /**
     * Set up the boundaries for level 2
     * @param canvas - set up the canvas
     * @param xPos - the position x of the canvas
     */
    private void backgroundLevelTwo(Canvas canvas, int xPos){
        finishLine = new Rect(40 * width + xPos, 0,
                40*width + width + xPos, gameViewHeight);
    }
}
