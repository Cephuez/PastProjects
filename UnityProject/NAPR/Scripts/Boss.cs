using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Boss : Enemy
{
    public List<GameObject> barriorList = new List<GameObject>();

    public Enemy lambda1;
    public Enemy gamma1;
    public DrEvenWattz DrEvenWatt;

    public AudioSource phaseOneSound;
    public AudioSource finalBossTheme;

    private bool isSoundPlayed = false;

    // Start is called before the first frame update
    void Start()
    {
        lambda1.setActiveAction(false);
        gamma1.setActiveAction(false);
        DrEvenWatt.setActiveAction(false);
        setDoorListActive(false);
    }

    // Update is called once per frame
    void Update()
    {
        if (playerDetected())
        {
            if(!finalBossTheme.isPlaying)
                finalBossTheme.Play();
            lambda1.setActiveAction(true);
            gamma1.setActiveAction(true);
            setDoorListActive(true);
            if (DrEvenWatt != null)
            {
                DrEvenWatt.setActiveAction(true);
            }

            if (!isSoundPlayed)
            {
                AudioSource edSound = Instantiate<AudioSource>(phaseOneSound);
                edSound.Play();
                Destroy(edSound, 2.25f);
                isSoundPlayed = true;
            }
            
        }

        if (health <= 0)
        {
            isDead();
            finalBossTheme.Stop();
            Debug.Log("Boss defeated!");
        }
    }

    public override bool isDead()
    {
        animator.SetBool("isDead", true);
        beingAction = false;
        Destroy(colliderObject);
        rigidbodyObject.isKinematic = true; // animation stays in place of death

        if (deathParticles != null)
        {
            Instantiate(deathParticles, transform.position, transform.rotation);
        }

        // set the bosses assets to be destroyed too
        if (lambda1 != null)
        {
            lambda1.isDead();
        }
        if (gamma1 != null)
        {
            gamma1.isDead();
        }
        if (DrEvenWatt != null)
        {
            DrEvenWatt.setActiveAction(false);
            DrEvenWatt.health = 0;
        }

        if (barriorList[0] != null)
        {
            for (int i = 0; i < barriorList.Count; i++)
            {
                Animator barriorAnimator = barriorList[i].GetComponent<Animator>();
                Collider2D barriorCollider = barriorList[i].GetComponent<Collider2D>();
                barriorAnimator.SetBool("isDisabled", true);
                Destroy(barriorCollider);
                Destroy(barriorList[i], deathAnimationTimer);
            }
        }   

        setDoorListActive(false);

        Destroy(gameObject, deathAnimationTimer);
        Debug.Log("Being died");
        return true;
    }

}
