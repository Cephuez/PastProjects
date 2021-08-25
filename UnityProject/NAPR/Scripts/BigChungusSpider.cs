using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BigChungusSpider : Enemy
{
    public GameObject spiderMen;

    public List<GameObject> phaseOneSpawns = new List<GameObject>();
    public List<GameObject> phaseTwoSpawns = new List<GameObject>();
    public List<GameObject> phaseThreeSpawns = new List<GameObject>();

    public Transform detectRay;
    public float detectRayLength;

    public float fireRate;
    private float lastFiredTime;
    private float lastFiredTime2;
    private float lastFiredTime3;

    //private bool isFirstPhase = false;
    //private bool isSecondPhase = false;
    //private bool isThirdPhase = false;

    // Start is called before the first frame update
    void Start()
    {
        isDamageable = false;
        setActiveAction(false);
        setDoorListActive(false);
        if (fireRate < 3)
        {
            fireRate = 3;
        }
    }

    // Update is called once per frame
    void Update()
    {
        RaycastHit2D rayCastResult = Physics2D.Raycast(detectRay.position, detectRay.right, detectRayLength, rayCastObjectDetect.value);
        if (rayCastResult.collider != null) // && Time.time > fireRate + lastFiredTime
        {
            setActiveAction(true);
            setDoorListActive(true);
            isDamageable = true;
            //Instantiate<GameObject>(spiderMen, detectRay.position, Quaternion.identity);
            //lastFiredTime = Time.time;
        }

        if (beingAction)
        {
            
                if (health >= 150) //&& !isFirstPhase)
            {
                if (Time.time > fireRate + lastFiredTime)
                {
                    for (int i = 0; i < phaseOneSpawns.Count; i++)
                    {     
                        Instantiate<GameObject>(spiderMen, phaseOneSpawns[i].transform.position, Quaternion.identity);
                    }
                    lastFiredTime = Time.time;
                }

                //Debug.Log("Entered first phase of Big Chungus");
            }

            if (health <= 100) //&& !isSecondPhase)
            {
                if (Time.time > (fireRate - 1) + lastFiredTime2)
                {
                    for (int i = 0; i < phaseTwoSpawns.Count; i++)
                    {
                        Instantiate<GameObject>(spiderMen, phaseTwoSpawns[i].transform.position, Quaternion.identity);
                    }
                    lastFiredTime2 = Time.time;
                }
                //Debug.Log("Entered second phase of Big Chungus");
            }

            if (health <= 50) //&& !isThirdPhase)
            {
                if (Time.time > (fireRate - 2) + lastFiredTime3)
                {
                    for (int i = 0; i < phaseThreeSpawns.Count; i++)
                    {
                        Instantiate<GameObject>(spiderMen, phaseThreeSpawns[i].transform.position, Quaternion.identity);
                    }
                    lastFiredTime3 = Time.time;
                }
                //Debug.Log("Entered third phase of Big Chungus");
            }



            if (health <= 0 && isDamageable)
            {
                setDoorListActive(false);
                isDead();
                Debug.Log("Big Chungus defeated!");
            }
        }
    }
}
