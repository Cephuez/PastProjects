
using System;
using System.Security.Cryptography;
using Assets.ScriptFolder.PlayerScripts;
using UnityEngine;

public class Enemy : Being
{
    public int damageWorth;
    public Canvas healthBar;
    public GameObject playerStats;
    // PlayerStats _PlayerStats;

    private PlayerStats _playerStats;

    private float damageResetTimer;
    private float damageReset;

    public bool enemyOnPlayer;
    private bool InRange;
    // Start is called before the first frame update
    void Start()
    {
        damageResetTimer = 2f;
        damageReset = damageResetTimer;
       _playerStats = playerStats.GetComponent<PlayerStats>();
    }

    // Update is called once per frame
    void Update()
    {
       // Debug.Log(enemyOnPlayer);
        //if(enemyOnPlayer) 
        Debug.Log(InRange);
        if (InRange)
            DoDamage();
        ResetTimeTracker();
    }

    public bool DoDamage()
    {
        bool canDoDamge = damageResetTimer >= damageReset;
        if(damageResetTimer >= damageReset)
            damageResetTimer = 0f;
        return canDoDamge;
        
    }

    private void ResetTimeTracker()
    {
        if (damageResetTimer <= damageReset)
        {
            damageResetTimer += Time.deltaTime;
        }
    }
    
    private void OnTriggerEnter2D(Collider2D other)
    {
        if (other.gameObject.layer == 11)
        {
            InRange = true;
        }
    }

    private void OnTriggerExit2D(Collider2D other)
    {
        if (other.gameObject.layer == 11)
        {
            InRange = false;
        }
    }
}
