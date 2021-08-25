using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MovingPlatform : Flyer
{
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if (beingAction)
        {
            if (hPath)
            {
                horizontalPath();
            }
            else if (vPath)
            {
                verticalPath();
            }
            else if (dPath1)
            {
                diagonalPath1();
            }
            else if (dPath2)
            {
                diagonalPath2();
            }

            if (Time.time > turnRate + lastTurnTime)
            {
                if (direction < 0)
                {
                    direction = 1;
                }
                else
                {
                    direction = -1;
                }

                rotation = !rotation;
                lastTurnTime = Time.time;
            }
        }// if action

    }// end update


}
