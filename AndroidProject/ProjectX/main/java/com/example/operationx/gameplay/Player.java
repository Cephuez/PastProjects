package com.example.operationx.gameplay;

import android.app.Activity;
import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Rect;
import android.graphics.drawable.Drawable;
import android.widget.ImageView;

import com.example.operationx.R;

public class Player {

    private Drawable playerSprite;
    private Activity currActivity;

    private int lives;
    private int width, height, gameViewHeight, levelID, centerView;
    private Inventory inventory;

    /**
     * The player's inventory and boundaries will be created here
     * @param currActivity - reference to activity
     * @param width - width of player
     * @param height - height of player
     * @param gameViewHeight - height of the screen
     * @param levelID - level reference
     */
    public Player(Activity currActivity, int width, int height, int gameViewHeight, int levelID){
        this.currActivity = currActivity;
        this.width = width;
        this.height = height;
        this.gameViewHeight = gameViewHeight;
        this.levelID = levelID;
        lives = 3;
        centerView = 350;
        inventory = new Inventory(currActivity, levelID);
        setPlayerBoundaries();
    }

    /**
     * Player loses life
     */
    public void loseLife(){
        lives -= 1;
    }

    public boolean isDead(){
        return lives == 0;
    }
    public boolean doAction(int actionID){
        return inventory.useItem(actionID);
    }

    public void movePlayer(Canvas canvas, int yPos){
        if(levelID == 2){
            playerSprite.setBounds(-300 + centerView, (gameViewHeight / 2) - height + yPos,
                    -300 + centerView + width * 2, (gameViewHeight / 2) + yPos);
        }
        playerSprite.draw(canvas);
    }

    public int getScore(){
        return inventory.getScore() + lives * 100;
    }

    public Rect getBounds(){
        return playerSprite.getBounds();
    }

    /**
     * Get the boundaries of the player
     */
    private void setPlayerBoundaries(){
        getPlayerDrawable();
        if(levelID == 1) {
            playerSprite.setBounds(centerView + width, (gameViewHeight / 2) - height,
                    centerView + width + width, gameViewHeight / 2);
        }
    }

    public boolean checkLeftBoundaries(Rect gameBoundaries){
        Rect playerBoundary = playerSprite.getBounds();
        return !playerBoundary.intersect(gameBoundaries) && playerBoundary.left > gameBoundaries.left;
    }

    public boolean checkRightBoundaries(Rect gameBoundaries){
        Rect playerBoundary = playerSprite.getBounds();
        return !playerBoundary.intersect(gameBoundaries) && playerBoundary.right < gameBoundaries.right;
    }

    private void getPlayerDrawable(){
        if(levelID == 1){
            playerSprite = currActivity.getResources().getDrawable(R.drawable.player_11);
        }else {
            playerSprite = currActivity.getResources().getDrawable(R.drawable.player_22);
        }
    }
}
