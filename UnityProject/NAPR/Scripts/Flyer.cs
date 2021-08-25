using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// Flyer class is an enemy that will fly around in a distinct pattern.
public class Flyer : Enemy
{
    public bool hPath;
    public bool vPath;
    public bool dPath1;
    public bool dPath2;

    public int direction;
    //public int timeTillChangeDirection;

    public float turnRate;
    protected float lastTurnTime;

    protected bool rotation;

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

            //Change direction over time
            //StartCoroutine(ChangeDirectionOverSec(timeTillChangeDirection));


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

                //Debug.Log("Flyer changed flight direction");

                lastTurnTime = Time.time;
            }

            isDead();
        }// if action
        
    }

    // Utility method to change flyer direction over time.
    IEnumerator ChangeDirectionOverSec(int seconds)
    {
        yield return new WaitForSeconds(seconds);
        if (direction < 0)
        {
            direction = 1;
        }
        else
        {
            direction = -1;
        }

        rotation = !rotation;

       // Debug.Log("Flyer changed flight direction");
    }

    // Horizontal movement
    public void horizontalPath()
    {
        // gameObject.transform.Translate(direction * speed, 0.0f, 0.0f);

        // transform.position += new Vector3(direction * speed, 0.0f, 0.0f);
        // moveForward(gameObject, speed, 0);
        moveForwardX(gameObject, speed, 0, direction);
    }

    // Vertical movement
    public void verticalPath()
    {
        moveForwardY(gameObject, speed, 0, direction);
        //gameObject.transform.Translate(0.0f, direction * speed, 0.0f);
    }

    // Diagonal path (bottom-left, top-right)
    public void diagonalPath1()
    {
        moveForwardDiag1(gameObject, speed, 0, direction);
        //gameObject.transform.Translate(direction * speed, direction * speed, 0.0f);
    }

    // Diagonal path (top-left, bottom-right)
    public void diagonalPath2()
    {
        if (rotation)
        {
            moveForwardDiag2(gameObject, speed, 0);
           // gameObject.transform.Translate((direction * (-1)) * speed, direction * speed, 0.0f);
        }
        else
        {
            moveForwardDiag3(gameObject, speed, 0);
           // gameObject.transform.Translate(direction * speed, (direction * (-1)) * speed, 0.0f);
        }
    }

    // Deal damage to player on contact
    public virtual void OnCollisionEnter2D(Collision2D someObject)
    {

        if (someObject.gameObject.name == "NAPR")
        {
            player.health -= power;
            Debug.Log("Player Current Health: " + player.health);
            Debug.Log("Flyer NAPR");
        }
    }
}
