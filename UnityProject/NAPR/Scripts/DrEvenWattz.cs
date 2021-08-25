using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DrEvenWattz : Enemy
{
    public GameObject turretProj;
    public AudioSource DrEvenShootSound;
    
    public float fireRate;
    public float attackDelay = 2.0f;
    private float lastFiredTime;

    public Transform detectRay;
    public float detectRayLength;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if (beingAction)
        {
            if (playerInAttackRange() && Time.time > fireRate + lastFiredTime)
            {
                Instantiate<GameObject>(turretProj, detectRay.position, detectRay.rotation);
                AudioSource drS = Instantiate<AudioSource>(DrEvenShootSound);
                drS.Play();
                Destroy(drS, 1f);

                lastFiredTime = Time.time;
            }
        }

        if (health <= 0)
        {
            beingAction = false;
            flyingEscape();
        }
    }

    // The Dr will retreat
    public void flyingEscape()
    {
        animator.SetBool("isFlying", true);
        Destroy(colliderObject);

        transform.position += new Vector3(0f, speed * Time.deltaTime);
        rigidbodyObject.MovePosition(transform.position);

        Destroy(gameObject, deathAnimationTimer);
    }
}
