using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TutorialBlockCall : MonoBehaviour
{
    public GameObject[] sceneArray;
    public int val;
    
    public void OpenTutorialPage()
    {
        sceneArray[val].SetActive(true);
    }
}
