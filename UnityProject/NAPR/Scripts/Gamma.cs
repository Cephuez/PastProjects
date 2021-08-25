using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Gamma : Flyer
{
    public GameObject turretProj;
    public AudioSource gammaSound;
    
    public float fireRate;
    private float lastFiredTime;

    public Transform detectRay;
    public float detectRayLength;

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
            transform.RotateAround(transform.parent.position, new Vector3(0f, 0f, 1f), speed * Time.deltaTime);

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
        }// if action
    }

}
