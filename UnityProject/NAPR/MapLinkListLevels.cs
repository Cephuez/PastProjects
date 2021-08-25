using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MapLinkListLevels : MonoBehaviour
{
    private MapLinkListLevels upperLevel,leftLevel,lowerLevel,rightLevel;

    private float x1, x2, y1, y2;

    public MapLinkListLevels(float x1, float y1, float x2, float y2)
    {
        this.x1 = x1;
        this.y1 = y1;
        this.x2 = x2;
        this.y2 = y2;
    }

    public void AddUpperLevel(MapLinkListLevels node)
    {
        upperLevel = node;
    }

    public void AddLeftLevel(MapLinkListLevels node)
    {
        leftLevel = node;
    }

    public void AddLowerLevel(MapLinkListLevels node)
    {
        lowerLevel = node;
    }

    public void AddRightLevel(MapLinkListLevels node)
    {
        rightLevel = node;
    }

    public float X1()
    {
        return x1;
    }

    public float Y1()
    {
        return y1;
    }

    public float X2()
    {
        return x2;
    }

    public float Y2()
    {
        return y2;
    }
}
