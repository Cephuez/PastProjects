using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;

public class CoordLevPos : MonoBehaviour
{
    public float xLength, yLength;

    public float x1, x2, y1, y2;

    private float x1B, x2B, y1B, y2B;
    void Start()
    {
        SetProperCoord();
    }

    public void SetProperCoord()
    {
        x1B = x1 + xLength;
        x2B = x2 - xLength;

        y1B = y1 + yLength;
        y2B = y2 - yLength;
    }
    public float X1B()
    {
        return x1B;
    }
    
    public float Y1B()
    {
        return y1B;
    }
    
    public float X2B()
    {
        return x2B;
    }
    
    public float Y2B()
    {
        return y2B;
    }

    public float[] Coordinates()
    {
        float[] coord = new float[] {x1B, y1B, x2B, y2B};
        return coord;
    }
}
