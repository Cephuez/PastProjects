using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// Chaser class is an enemy type that walks around until it finds player. When player is found,
// it will chase the player and do a charge up attack.
public class Chaser : Enemy
{

    public float chaseSpeedIncrease;
    public float attackDelay;

    public Transform groundedRay = null;
    public Transform groundedRay2 = null;
    public Transform wallRay = null;
    public Transform wallRay2 = null;

    public float groundedRayLength;
    public float wallRayLength;

    public float attackSpeed = 3;

    public bool isTimedLife = false;
    public float timedLife = 5.0f;

    private bool turnAround = false;
    private float turnDelay = 0.3f;

    // Start is called before the first frame update
    void Start()
    {
        if (player == null)
        {
            GameObject thePlayer = GameObject.Find("Player");
            player = thePlayer.GetComponent<Player>();
        }
    }

    // Update is called once per frame
    void Update()
    {
        if (beingAction)
        {
            if (playerDetected())
            {
                //transform.LookAt(player.transform);
                if (playerInAttackRange())
                {
                    //Make Chaser attack after a certain amount of time
                    StartCoroutine(windUpAttack(attackDelay));
                }
                else
                {
                    //transform.position += transform.forward * Time.deltaTime * (speed + chaseSpeedIncrease);
                    if (turnAround)
                    {
                        moveForwardX(gameObject, speed, chaseSpeedIncrease, 1);
                    }
                    else
                    {
                        moveForwardX(gameObject, speed, chaseSpeedIncrease, -1);
                    }
                }
            }
            else
            {
                // check if near edge to turn around
                // transform.position += transform.forward * Time.deltaTime * speed;
                RaycastHit2D rayCastResult = Physics2D.Raycast(groundedRay.transform.position, groundedRay.right, groundedRayLength, rayCastObjectDetect.value);
                RaycastHit2D rayCastResult2 = Physics2D.Raycast(groundedRay2.transform.position, groundedRay2.right, groundedRayLength, rayCastObjectDetect.value);
                if (rayCastResult.collider == null || rayCastResult2.collider == null)
                {
                    //StartCoroutine(turnAroundMethod(turnDelay));
                    transform.eulerAngles = Vector3.forward * turnAroundValue;

                    turnAround = !turnAround;
                    turnAroundDelay(turnDelay);

                }

                if (turnAround)
                {
                    moveForwardX(gameObject, speed, 0, 1);
                }
                else
                {
                    moveForwardX(gameObject, speed, 0, -1);
                }
                // moveForwardX(gameObject, speed, 0, 1);
            }

            // platform check
            RaycastHit2D rayCastResult3 = Physics2D.Raycast(wallRay.transform.position, wallRay.right, wallRayLength, rayCastObjectDetect.value);
            RaycastHit2D rayCastResult4 = Physics2D.Raycast(wallRay2.transform.position, wallRay2.right, wallRayLength, rayCastObjectDetect.value);
            // pickable check
            RaycastHit2D rayCastResult5 = Physics2D.Raycast(wallRay.transform.position, wallRay.right, wallRayLength, LayerMask.GetMask("Pickable"));
            RaycastHit2D rayCastResult6 = Physics2D.Raycast(wallRay2.transform.position, wallRay2.right, wallRayLength, LayerMask.GetMask("Pickable"));
            // door check
            RaycastHit2D rayCastResult7 = Physics2D.Raycast(wallRay.transform.position, wallRay.right, wallRayLength, LayerMask.GetMask("Door"));
            RaycastHit2D rayCastResult8 = Physics2D.Raycast(wallRay2.transform.position, wallRay2.right, wallRayLength, LayerMask.GetMask("Door"));
            // objects check
            RaycastHit2D rayCastResult9 = Physics2D.Raycast(wallRay.transform.position, wallRay.right, wallRayLength, LayerMask.GetMask("Objects"));
            RaycastHit2D rayCastResult10 = Physics2D.Raycast(wallRay2.transform.position, wallRay2.right, wallRayLength, LayerMask.GetMask("Objects"));
            if (rayCastResult3.collider != null || rayCastResult4.collider != null ||
                rayCastResult5.collider != null || rayCastResult6.collider != null ||
                rayCastResult7.collider != null || rayCastResult8.collider != null ||
                rayCastResult9.collider != null || rayCastResult10.collider != null)
            {
                //StartCoroutine(turnAroundMethod(turnDelay));
                transform.eulerAngles = Vector3.forward * turnAroundValue;

                turnAround = !turnAround;
                turnAroundDelay(turnDelay);
                // Debug.Log("Chaser turns from side to side");
            }

            isDead();
        }// if action

        if (isTimedLife)
        {
            Destroy(gameObject, timedLife);
        }

    }

    IEnumerator turnAroundMethod(float seconds)
    {
        yield return new WaitForSeconds(seconds);
        transform.eulerAngles = Vector3.forward * turnAroundValue;

        turnAround = !turnAround;
    }

    IEnumerator turnAroundDelay(float seconds)
    {
        yield return new WaitForSeconds(seconds);
    }

    // Makes the Chaser enemy wait for a moment, then attacks.
    IEnumerator windUpAttack(float seconds)
    {
        yield return new WaitForSeconds(seconds);
        if (turnAround)
        {
            moveForwardX(gameObject, speed, attackSpeed, 1);
        }
        else
        {
            moveForwardX(gameObject, speed, attackSpeed, -1);
        }
        //transform.position += transform.forward * Time.deltaTime * (speed + 3);
        // Debug.Log("Chaser attacked!");
    }

    // Collision detection. If it hits player or enemy, deal damage. If it hits portal, don't disappear.
    // Else, disappear on contact
    public void OnCollisionEnter2D(Collision2D someObject)
    {
        // Debug.Log("Chaser made contact! " + someObject.gameObject.name);
        if (someObject.gameObject.name == "NAPR")
        {
            player.health -= power;
            // Debug.Log("Player Current Health: " + player.health);
            // Debug.Log("Chaser touched NAPR");
        }
        else if (someObject.gameObject.layer != 14)
        {
            transform.eulerAngles = Vector3.forward * turnAroundValue;
            turnAround = !turnAround;
            // Debug.Log("Chaser turned around");
        }
    }

}
