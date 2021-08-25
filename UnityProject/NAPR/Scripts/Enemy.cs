using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// Enemy class are the player objects foes that are obstacles.
public class Enemy : Being
{
    public List<GameObject> doorList = new List<GameObject>();
    public bool robot;
    public bool organic;
    public float detectRange;
    public float attackRange;

  
    public Player player;
    public LayerMask rayCastObjectDetect;

    public bool isDamageable = true;

    public Player1 d;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    // Returns true if the enemy sees the player in their range.
    public bool playerDetected()
    {
        if (Vector2.Distance(transform.position, player.transform.position) <= detectRange)
        {
            return true;
        }
        else
        {
            return false;
        }
    }

    // Returns true if the player is in the enemy attack range.
    public bool playerInAttackRange()
    {
        if (Vector2.Distance(transform.position, player.transform.position) <= attackRange)
        {
            return true;
        }
        else
        {
            return false;
        }
    }

    // method to make a gameobject look at the player character
    public void lookAtPlayer(GameObject someObject)
    {
        Vector3 offset = player.transform.position - someObject.transform.position;
        Quaternion rotation = Quaternion.LookRotation(Vector3.forward, offset);
        someObject.transform.rotation = rotation * Quaternion.Euler(0, 0, 90);
    }

    public bool getIsDamageable()
    {
        return isDamageable;
    }

    public bool setDoorListActive(bool isActive)
    {
        if (doorList[0] != null)
        {
            for (int i = 0; i < doorList.Count; i++)
            {
                doorList[i].SetActive(isActive);
            }
            return true;
        }
        else
        {
            return false;
        }
    }

}
