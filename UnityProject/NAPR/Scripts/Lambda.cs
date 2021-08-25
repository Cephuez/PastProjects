using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Lambda : Flyer
{
    public GameObject turretProj;
    public AudioSource lambdaSound;
    
    public float fireRate;
    private float lastFiredTime;

    public Transform detectRay;
    public float detectRayLength;

    private int positionNumber = 1;
    private bool positionMidCheck = false;

    // Start is called before the first frame update
    void Start()
    {
        isDamageable = false;
    }

    // Update is called once per frame
    void Update()
    {
        if (beingAction)
        {
            switch (positionNumber)
            {
                case 1:
                    diagonalPath2();
                    break;
                case 2:
                    diagonalPath1();
                    break;
                default:
                    // code not supposed to be here
                    Debug.Log("Error in lambda's position has occured");
                    break;
            }

            RaycastHit2D rayCastResult = Physics2D.Raycast(detectRay.position, detectRay.right, detectRayLength, rayCastObjectDetect.value);
            if (rayCastResult.collider != null && Time.time > fireRate + lastFiredTime)
            {
                Instantiate<GameObject>(turretProj, detectRay.position, Quaternion.identity);
                AudioSource lambdaS = Instantiate<AudioSource>(lambdaSound);
                lambdaS.Play();
                Destroy(lambdaS, 1f);
                
                lastFiredTime = Time.time;
            }

            if (Time.time > (turnRate/2.0f) + lastTurnTime && !positionMidCheck)
            {
                positionIncrement();
                positionMidCheck = true;
            }

            // direction
            if (Time.time > turnRate + lastTurnTime)
            {
                positionIncrement();

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
                positionMidCheck = false;
            }
        }// if action
    }

    // for changing lambda's flight path
    void positionIncrement()
    {
        if (positionNumber < 2)
        {
            positionNumber++;
        }
        else
        {
            positionNumber = 1;
        }
    }
}
