using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ItemDisplayReference : MonoBehaviour
{
    public static ItemDisplayReference ItemDisplay;

    void Awake()
    {
        ItemDisplay = this;
    }
}
