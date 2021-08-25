package com.example.operationx.gameplay;

import android.app.Activity;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.PorterDuff;
import android.graphics.Rect;
import android.graphics.drawable.Drawable;
import android.view.MotionEvent;
import android.view.View;

import com.example.operationx.R;
import com.example.operationx.gameplay.Enemy;
import com.example.operationx.gameplay.GroundTile;
import com.example.operationx.gameplay.MapTiles;
import com.example.operationx.gameplay.Player;

import java.util.ArrayList;

public class GameTile extends View {
    public Activity containerActivity;
    private int fixSize,fixWidth,fixHeight, fixWidthBackground;
    private int xDir,yDir;
    private int xBoundaries;
    private int levelID;
    public int xPos,yPos, gameViewHeight;
    private long startTime;
    private Canvas canvas;
    private ArrayList<Drawable> laserBullets;

    private Drawable playerDrawable;

    private Player player;
    private Enemy enemy;
    private BackgroundTiles backgroundTiles;
    private GroundTile groundTile;
    private EnemyList enemyList;
    private LevelBoundaries levelBoundaries;
    private LevelControllers levelControllers;

    /**
     * Set up the game tile where everything will be seen
     * @param currActivity - reference to activty
     * @param levelID - reference to level number
     */
    public GameTile(Activity currActivity, int levelID){
        super(currActivity);
        this.levelID = levelID;
        laserBullets = new ArrayList<Drawable>();
        startTime = 0;
        setPreValues();
        containerActivity = currActivity;
        setLevel();
        this.setBackgroundColor(0xFFFFFFFF);
    }
    private float x1,x2,y1,y2;
    static final int MIN_DISTANCE = 150;

    /**
     * Controller for the game. It will allow the player to slide around the screen
     * @param event
     * @return return boolean if something happened
     */
    @Override
    public boolean onTouchEvent(MotionEvent event){
        switch (event.getAction()) {
            case MotionEvent.ACTION_DOWN:
                x1 = event.getX();
                break;
            case MotionEvent.ACTION_UP:
                x2 = event.getX();
                float deltaX = x2 - x1;
                if (Math.abs(deltaX) <= 100) {
                    xDir = 0;
                } else if (deltaX < MIN_DISTANCE) {
                    xDir = -1;
                } else if (deltaX > MIN_DISTANCE) {
                    xDir = 1;
                }
                break;
        }
        switch (event.getAction()) {
            case MotionEvent.ACTION_DOWN:
                y1 = event.getY();
                break;
            case MotionEvent.ACTION_UP:
                y2 = event.getY();
                float deltaY = y2 - y1;
                if (Math.abs(deltaY) <= 100) {
                    yDir = 0;
                } else if (deltaY < MIN_DISTANCE) {
                    yDir = 1;
                } else if (deltaY > MIN_DISTANCE) {
                    yDir = -1;
                }
                break;
        }
        return true;
    }

    /**
     * It will redraw the images of each drawable as a FPS game
     * @param canvas
     */
    @Override
    protected void onDraw(Canvas canvas){
        super.onDraw(canvas);
        this.canvas = canvas;
        groundTile.displayGroundTiles(canvas, xPos);
        backgroundTiles.updateBackground(canvas, xPos);
        enemyList.updateEnemies(canvas, xPos);
        levelBoundaries.displayBoundaries(canvas,xPos);
        player.movePlayer(canvas,yPos);
        playerShoots(canvas);
        updateBulletPosition(canvas);

    }

    /**
     * Depending what buttons are pressed, an action will occur to the enemy
     * @param actionID - action pressed
     * @return return 0 if aciton was invalid
     */
    public int doAction(int actionID){
        if(levelID == 1 && !enemyList.isEmpty() && enemyList.get(0).playerAction(actionID)
                 && playerHitEnemy(enemyList) && player.doAction(actionID)) {
            enemyList.remove(0);
            return actionID;
        }else if(levelID == 2 && !enemyList.isEmpty() && player.doAction(actionID)){
            enemyList.playerAction(actionID, player,xPos);
            return actionID;
        }
        return 0;
    }

    public boolean reachedFinishLine(){
        return levelBoundaries.reachFinishLine(player);
    }

    public boolean playerDead(){
        return player.isDead();
    }

    /**
     * Detect enemies has been hit
     *
     * @param enemyList - List of enemies currently on the level
     * @return return if enemy has been encountered
     */
    private boolean playerHitEnemy(EnemyList enemyList){
        if(levelID == 1){
            return playerHitEnemyLevelOne();
        }else{
            return playerHitEnemyLevelTwo();
        }
    }

    /**
     * Controllers for level 1
     * @return
     */
    private boolean playerHitEnemyLevelOne(){
        if(enemyList.isEmpty())
            return false;
        Enemy currEnemy = enemyList.get(0);
        boolean enemyEncountered = player.getBounds().intersect(currEnemy.getColliderBoundary());
        if(enemyEncountered && xDir != -1)
            xDir = 0;
        return enemyEncountered;
    }

    /**
     * Controller for level 2
     * @return
     */
    private boolean playerHitEnemyLevelTwo(){
        if(enemyList.isEmpty())
            return false;
        for(int i = 0; i < enemyList.size(); i++){
            Enemy currEnemy = enemyList.get(i);
            boolean enemyEncountered = player.getBounds().intersect(currEnemy.getColliderBoundary());
            if(enemyEncountered) {
                enemyList.remove(i);
                return true;
            }
        }
        return false;
    }
    public void clearCanvas(Canvas canvas){
        canvas.drawColor(Color.TRANSPARENT, PorterDuff.Mode.CLEAR);
        invalidate();
    }

    /**
     * Player shoots at player in level 2
     * @param canvas
     */
    public void playerShoots(Canvas canvas){
        if(levelID == 2){
            Drawable bullet1 = getResources().getDrawable(R.drawable.laser_bullet);
            Drawable bullet2 = getResources().getDrawable(R.drawable.laser_bullet);
            Rect playerRect = player.getBounds();
            int xPos = playerRect.right;
            int yPos1 = playerRect.top;
            int yPos2 = playerRect.bottom;

            bullet1.setBounds(xPos - 50, yPos1+50,
                    -50 + xPos + fixWidth*2/4, yPos1+75);
            bullet2.setBounds(xPos - 50, yPos2-75,
                    -50 + xPos + fixWidth*2/4, yPos2 - 50);

            laserBullets.add(bullet1);
            laserBullets.add(bullet2);
        }
    }

    /**
     * Update the position of the bullets of the plane
     * @param canvas
     */
    public void updateBulletPosition(Canvas canvas){
        if(levelID == 2) {
            for (int i = 0; i < laserBullets.size(); i++) {
                Drawable currBullet = laserBullets.get(i);
                Rect currBounds = currBullet.getBounds();
                currBullet.setBounds(currBounds.left + 200, currBounds.top,
                        currBounds.right + 200, currBounds.bottom);
                currBullet.draw(canvas);
            }

            Drawable currBullet = laserBullets.get(0);
            Rect currBounds = currBullet.getBounds();
            if (currBounds.right >= 1000) {
                laserBullets.remove(0);
                laserBullets.remove(0);
            }
        }
    }

    /**
     * Change positino of the objects on canvas
     */
    public void changeXPos() {
        if (levelID == 1 && !playerHitEnemy(enemyList) || (xDir == -1 && xPos > 500)) {
            xPos += 50 * -xDir;
        } else if (levelID == 2) {
            xPos -= 50;
            if (playerHitEnemy(enemyList)) {
                player.loseLife();
            }
        }
    }

    /**
     * Change y position of the player
     */
    public void changeYPos(){
        if(levelID == 2){
            yPos -= 45 * yDir;
        }
    }

    public int getPlayerScore(){
        return player.getScore();
    }

    private void setLevel(){
        player = new Player(containerActivity,150,fixHeight,gameViewHeight, levelID);
        enemyList = new EnemyList(containerActivity,fixWidth,fixHeight,gameViewHeight, levelID);
        backgroundTiles = new BackgroundTiles(containerActivity,fixWidthBackground,gameViewHeight,levelID);
        groundTile = new GroundTile(containerActivity,fixWidth,fixHeight,gameViewHeight,levelID);
        levelBoundaries = new LevelBoundaries(containerActivity,fixWidth,fixHeight,gameViewHeight,levelID);
    }

    private void setPreValues(){
        fixSize = 300;
        fixHeight = 300;
        fixWidth = 300;
        fixHeight = 300;
        fixWidthBackground = 600;
        gameViewHeight = 1500;
        xPos = 0;
        xDir = 0;
        xBoundaries = fixSize * 18;
    }
}
