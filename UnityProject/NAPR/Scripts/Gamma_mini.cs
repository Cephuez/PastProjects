using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Gamma_mini : Flyer
{
    public GameObject turretProj;
    public AudioSource gammaSound;
    public AudioSource last_level_theme;

    public float fireRate;
    private float lastFiredTime;

    public Transform detectRay;
    public float detectRayLength;

    public float timeTillAttack;
    private bool isAttack = false;
    private bool isFirstMoving = false;
    private float turnMulti = 1.0f;
    private bool afterFirstTurn = false;
    public float firstTurnTime;

    // Start is called before the first frame update
    void Start()
    {
        isDamageable = false;
        setActiveAction(false);
        setDoorListActive(false);
    }

    // Update is called once per frame
    void Update()
    {
        if (playerDetected() && !isAttack)
        {
            isFirstMoving = true;
            setDoorListActive(true);
            StartCoroutine(delayedAttack(timeTillAttack));
        }

        if (isFirstMoving && !isAttack)
        {
            //verticalPath();
            moveForwardY(gameObject, speed, 0, 1);
        }

        if (beingAction)
        {
            if (!afterFirstTurn)
            {
                StartCoroutine(doubleTurnDistance(firstTurnTime));
            }

            horizontalPath();

            if (playerInAttackRange() && Time.time > fireRate + lastFiredTime)
            {
                AudioSource gammaS = Instantiate<AudioSource>(gammaSound);
                gammaS.Play();
                Destroy(gammaS, 1f);
                //detectRay.transform.LookAt(player.transform);
                lookAtPlayer(gameObject);
                Vector3 offset = player.transform.position - detectRay.transform.position;
                Quaternion rotation = Quaternion.LookRotation(Vector3.forward, offset);
                detectRay.transform.rotation = rotation * Quaternion.Euler(0, 0, 90);


                Instantiate<GameObject>(turretProj, detectRay.position, detectRay.rotation);
                lastFiredTime = Time.time;
            }

            if (Time.time > (turnRate * turnMulti) + lastTurnTime)
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
                //afterFirstTurn = true;
            }

            afterFirstTurn = true;

            if (isDamageable)
            {
                isDead();
            }
        }// if action
    }

    IEnumerator delayedAttack(float seconds)
    {
        yield return new WaitForSeconds(seconds);
        isAttack = true;
        setActiveAction(true);
        isDamageable = true;

    }

    IEnumerator doubleTurnDistance(float seconds)
    {
        yield return new WaitForSeconds(seconds);
        turnMulti *= 2;
    }

    public override bool isDead()
    {
        if (health <= 0)
        {
            if (deathParticles != null)
            {
                Instantiate(deathParticles, transform.position, transform.rotation);
            }
            last_level_theme.Stop();
            setDoorListActive(false);
            animator.SetBool("isDead", true);
            beingAction = false;
            Destroy(colliderObject);
            rigidbodyObject.isKinematic = true; // animation stays in place of death
            Destroy(gameObject, deathAnimationTimer);
            //gameObject.SetActive(false);
            Debug.Log("Being died");
            return true;
        }
        return false;
    }
    /*
    public override void OnCollisionEnter2D(Collision2D someObject)
    {
        if (someObject.gameObject.layer == 11) // hits platform
        {
            if (direction < 0)
            {
                direction = 1;
            }
            else
            {
                direction = -1;
            }
            Debug.Log("Gamma_mini hit a platform/wall");
        }
    }
    */
}
