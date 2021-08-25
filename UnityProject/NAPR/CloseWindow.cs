using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CloseWindow : MonoBehaviour
{
    //public GameObject currentWindow;

    public void OnClick(GameObject currentWindow)
    {
        currentWindow.SetActive(false);
    }
}
