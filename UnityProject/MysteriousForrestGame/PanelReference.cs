using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PanelReference : MonoBehaviour
{
    public static PanelReference Panel;
    void Awake()
    {
        Panel = this;
    }
}
