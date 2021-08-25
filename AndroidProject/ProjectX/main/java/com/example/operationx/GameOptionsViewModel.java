package com.example.operationx;

import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

/**
 * View model that contains methods that hold the games information
 * to be used in the gameinfofragmnet. Other methods are left for future iterations.
 */
public class GameOptionsViewModel extends ViewModel {
    private MutableLiveData<Integer> currentLives;
    private MutableLiveData<Integer> currentLevel;
    private MutableLiveData<Boolean> mapPressed;
    private MutableLiveData<Boolean> pausePressed;
    private MutableLiveData<Integer> currentPrimary;
    private MutableLiveData<Integer> currentSecondary;
    private MutableLiveData<Integer> currentThird;
    private MutableLiveData<Integer> currentActionId;

    public MutableLiveData<Integer> getCurrentLives() {
        if(currentLives == null) {
            currentLives = new MutableLiveData<>();
        }
        return currentLives;
    }

    public MutableLiveData<Integer> getCurrentLevel() {
        if(currentLevel == null) {
            currentLevel = new MutableLiveData<>();
        }
        return currentLevel;
    }

    public MutableLiveData<Boolean> getIsMapPressed() {
        if(mapPressed == null) {
            mapPressed = new MutableLiveData<>();
        }
        return mapPressed;
    }

    public MutableLiveData<Boolean> getIsPausePressed() {
        if(pausePressed == null) {
            pausePressed = new MutableLiveData<>();
        }
        return pausePressed;
    }

    public MutableLiveData<Integer> getCurrentPrimary() {
        if(currentPrimary == null) {
            currentPrimary = new MutableLiveData<>();
        }
        return currentPrimary;
    }
    public MutableLiveData<Integer> getCurrentSecondary() {
        if(currentSecondary == null) {
            currentSecondary = new MutableLiveData<>();
        }
        return currentSecondary;
    }
    public MutableLiveData<Integer> getCurrentThird() {
        if(currentThird == null) {
            currentThird = new MutableLiveData<>();
        }
        return currentThird;
    }
    public MutableLiveData<Integer> getCurrentActionId() {
        if(currentActionId == null) {
            currentActionId = new MutableLiveData<>();
        }
        return currentActionId;
    }



}
