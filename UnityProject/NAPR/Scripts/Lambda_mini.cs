using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Lambda_mini : Flyer
{
    public GameObject turretProj;
    public AudioSource lambdaSound;

    public float fireRate;
    private float lastFiredTime;

    public Transform detectRay;
    public float detectRayLength;

    private bool isDoorsSet = false;

    // Start is called before the first frame update
    void Start()
    {
        setDoorListActive(false);
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

            RaycastHit2D rayCastResult = Physics2D.Raycast(detectRay.position, detectRay.right, detectRayLength, rayCastObjectDetect.value);
            if (rayCastResult.collider != null && Time.time > fireRate + lastFiredTime)
            {
                Instantiate<GameObject>(turretProj, detectRay.position, Quaternion.identity);
                AudioSource lambdaS = Instantiate<AudioSource>(lambdaSound);
                lambdaS.Play();
                Destroy(lambdaS, 1f);

                if (!isDoorsSet)
                {
                    setDoorListActive(true);
                    isDoorsSet = true;
                }


                lastFiredTime = Time.time;
            }

            // direction
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

            if (isDamageable)
            {
                isDead();
            }
        }// if action
    }

    public override bool isDead()
    {
        if (health <= 0)
        {
            if (deathParticles != null)
            {
                Instantiate(deathParticles, transform.position, transform.rotation);
            }
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
}
