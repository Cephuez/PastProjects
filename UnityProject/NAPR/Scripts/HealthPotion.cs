using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HealthPotion : MonoBehaviour
{
    public Player player;

    public bool isFullHealth;
    public bool isHalfHealth;
    public bool isQuarterHealth;

    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {

    }

    public void OnCollisionEnter2D(Collision2D someObject)
    {
        if (someObject.gameObject.layer == 8) // player 
        {
            if (isFullHealth)
            {
                player.health = 100;
            }
            else if (isHalfHealth)
            {
                player.health += 50;
                if (player.health > 100)
                {
                    player.health = 100;
                }
            }
            else if (isQuarterHealth)
            {
                player.health += 25;
                if (player.health > 100)
                {
                    player.health = 100;
                }
            }  
            Destroy(gameObject);
        }
    }
}
