using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Player : Being
{
    public GameObject NAPR;
    public AudioSource damagedSound;

    public GameObject gameOverPop;
    //private Animator animator;
    
    // Start is called before the first frame update
    void Start()
    {
        animator = this.gameObject.GetComponent<Animator>();
        animator.SetFloat("Health",this.health);
    }

    // Update is called once per frame
    void Update()
    {
        float time_remaining = animator.GetFloat("Damaged");
        if (time_remaining>0){
            animator.SetFloat("Damaged",time_remaining-Time.deltaTime);
        }

        if (this.health <= 0)
        {
            StartCoroutine(DisplayGameOverScreen());
            //gameOverPop.SetActive(true);
        }
    }

    public IEnumerator DisplayGameOverScreen()
    {
        yield return new WaitForSeconds(0.6f);
        gameOverPop.SetActive(true);
    }
    public void OnCollisionEnter2D(Collision2D someObject)
    {

        if (someObject.gameObject.layer == 12 || someObject.gameObject.layer == 13)
        {
            animator.SetFloat("Damaged",1f);
            animator.SetFloat("Health",this.health);
            AudioSource damagedS = Instantiate<AudioSource>(damagedSound);
            damagedS.Play();
            Destroy(damagedS,1f);
            // Enemy enemy = GameObject.Find("Enemy").GetComponent<Enemy>();
            if (someObject.gameObject.GetComponent<Enemy>())
            {
                Enemy enemy = someObject.gameObject.GetComponent<Enemy>();
                this.health -= enemy.power;
                
                // Debug.Log("Player Current Health: " + this.health);
                // Debug.Log("NAPR took damage");
            } else if (someObject.gameObject.GetComponent<Projectile>())
            {
                Projectile enemyprojectile = someObject.gameObject.GetComponent<Projectile>();
                this.health -= enemyprojectile.power;
                // Debug.Log("Player Current Health: " + this.health);
                // Debug.Log("NAPR took damage");
            }
            
        }
    }

}
