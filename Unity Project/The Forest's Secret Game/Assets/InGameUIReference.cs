using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class InGameUIReference : MonoBehaviour
{
    public static InGameUIReference InGameUI;

    void Awake()
    {
        InGameUI = this;
    }
}
