using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PauseMenuReference : MonoBehaviour
{
    public static PauseMenuReference PauseMenuUI;
    void Awake()
    {
        PauseMenuUI = this;
    }
}
