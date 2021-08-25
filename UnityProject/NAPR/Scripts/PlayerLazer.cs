using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// PlayerLazer class is a power up for the player. When activated, the player can press the fire
// button to shot a lazer.
public class PlayerLazer : MonoBehaviour
{
    public float fireRate;
    private float lastFiredTime;

   // public Player player;
    public GameObject pLazer;

    public Transform spawnPoint;
    public float spawnRayLength;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        // if (Input.GetButton("Fire1") && Time.time > fireRate + lastFiredTime)
        // {
        //     firePlayerLazer();
        // }
    }

    // Shot a lazer from player's lazer gun
    public void firePlayerLazer()
    {
        /*
        Projectile pLazer = new Projectile(5, player.power);
        if (pLazer != null)
        {
            pLazer.transform.position = player.transform.position;
            pLazer.transform.rotation = transform.rotation;
            pLazer.gameObject.SetActive(true);
            Debug.Log("Lazer Fired");
        }
        */
        
        RaycastHit2D rayCastResult = Physics2D.Raycast(spawnPoint.position, spawnPoint.right, spawnRayLength);

        Instantiate<GameObject>(pLazer, spawnPoint.position, spawnPoint.rotation);
        Debug.Log("Player fired projectile");
        lastFiredTime = Time.time;
    }
}
