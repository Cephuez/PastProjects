using System.Collections;
using System.Collections.Generic;
using System.ComponentModel;
using UnityEngine;

// Turret class is a stationary enemy that will fire a projectile at the player.
public class Turret : Enemy
{
    public AudioSource turretSound;
    public GameObject turretProj;
    
    public bool lambda;
    public bool gamma;

    public float fireRate;
    private float lastFiredTime;

    public Transform detectRay;
    public Transform detectRay2;
    public float detectRayLength;

   // private int lambdaPower = 3;
    //private float lambdaSpeed = 4;
   // private int gammaPower = 2;
   // private float gammaSpeed = 15;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if (beingAction)
        {
            //RaycastHit2D rayCastResult = Physics2D.Raycast(groundedRay.position, groundedRay.right, groundedRayLength);
            //if (rayCastResult.collider == null)
            //if (playerDetected() && Time.time > fireRate + lastFiredTime)
            RaycastHit2D rayCastResult = Physics2D.Raycast(detectRay.position, detectRay.right, detectRayLength, rayCastObjectDetect.value);
            RaycastHit2D rayCastResult2 = Physics2D.Raycast(detectRay2.position, detectRay2.right, detectRayLength, rayCastObjectDetect.value);
            if (rayCastResult.collider != null && Time.time > fireRate + lastFiredTime)
            {
                AudioSource turretS = Instantiate<AudioSource>(turretSound);
                turretS.Play();
                Destroy(turretS,1f);

                if (lambda)
                {
                    //turretProj = new Projectile(lambdaSpeed, lambdaPower, player, false);
                }
                else if (gamma)
                {
                    //turretProj = new Projectile(gammaSpeed, gammaPower, player, true);
                }
                else
                {
                    // MyScript script = new Script();
                    //   turretProj = new Projectile(speed, power, player, true);
                    ////turretProj = GameObject.Instantiate(Resources.Load("Prefabs/Enemy Lazer")) as GameObject;
                    //Instantiate<GameObject>(turretProj, detectRay.position, detectRay.rotation);
                    Instantiate<GameObject>(turretProj, detectRay.position, Quaternion.identity);
                    /*
                    if (detectRay.transform.position.z == 0)
                    {
                        Instantiate<GameObject>(turretProjPos, detectRay.position, detectRay.rotation);
                        Debug.Log("Enemy fired projectile");
                    }
                    else if (detectRay.transform.position.z == 180)
                    {
                        Instantiate<GameObject>(turretProjNeg, detectRay.position, detectRay.rotation);
                        Debug.Log("Enemy fired projectile");
                    }
                    */
                }

                //turretProj.player = this.player;
                /*
                if (turretProj != null)
                {
                    turretProj.transform.position = player.transform.position;
                    turretProj.transform.rotation = transform.rotation;
                    turretProj.gameObject.SetActive(true);
                    Debug.Log("Enemy fired projectile");
                }
                */
                lastFiredTime = Time.time;
            }
            else if (rayCastResult2.collider != null && Time.time > fireRate + lastFiredTime)
            {
                AudioSource turretS = Instantiate<AudioSource>(turretSound);
                turretS.Play();
                Destroy(turretS, 1f);

                Instantiate<GameObject>(turretProj, detectRay2.position, detectRay2.rotation);
                lastFiredTime = Time.time;
            }

            if (!lambda || !gamma)
            {
                isDead();
            }
        }// if action
    }
}
