using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ItemMenuReference : MonoBehaviour
{
    public static ItemMenuReference ItemMenu;

    void Awake()
    {
        ItemMenu = this;
    }
}
