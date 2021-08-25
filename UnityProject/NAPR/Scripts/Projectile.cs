using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// prefab

// Projectile class are moving objects that deal damage with certain beings and disappear on collision
public class Projectile : MonoBehaviour
{
    public float speed;
    public int power;
    public int timeTillDisappear;
    private float lastTime;

    public GameObject player;
    public Animator animator;
    public ParticleSystem particlesOnCollision;
    public ParticleSystem defaultParticles;
    public ParticleSystem lazersCollideParticle;
    // public Enemy enemy;
    
    public bool straight = true;
    public bool piercing = false;

    public AudioSource enemyDamagedSound;
    /*
    // Constructor for new projectile objects (player)
    public Projectile(float speed, int power)
    {
        this.speed = speed;
        this.power = power;
    }

    // Constructor for new projectile objects (enemy)
    public Projectile(float speed, int power, Player player, bool straight)
    {
        this.speed = speed;
        this.power = power;
        this.player = player;
        this.straight = straight;
    }
    */

    // Start is called before the first frame update
    void Start()
    {
        player = GameObject.Find("Player");
    }

    // Update is called once per frame
    void Update()
    {
        if (straight)
        {
            straightFire();
        }
        else
        {
            enemyHomingFire();
        }

        //Make projectile disappear after a set amount of time
        StartCoroutine(RemoveAfterSeconds(timeTillDisappear));
    }

    // Fires projectile forward
    public void straightFire()
    {
        //transform.position += new Vector3(speed * Time.deltaTime, 0f);
        transform.position += transform.right * speed * Time.deltaTime;
    }

    // Fires projectile that follows the player
    public void enemyHomingFire()
    {
        if (transform.position != player.transform.position)
        {
            //transform.forward =(Vector2) player.transform.position - (Vector2)transform.position;
            transform.right = (Vector2) player.transform.position - (Vector2)transform.position;
            transform.position += transform.right * Time.deltaTime * speed;
        }
    }

    public void removeAfterSeconds()
    {
        if (Time.time > timeTillDisappear + lastTime)
        {
           // gameObject.SetActive(false);
            Destroy(gameObject);
            Debug.Log("Projectile disappeared");
            lastTime = Time.time;
        }
    }
    // Utility method to get rid of an object over a certain amount of time.
    IEnumerator RemoveAfterSeconds(int seconds)
    {
        yield return new WaitForSeconds(seconds);
        //gameObject.SetActive(false);
        Destroy(gameObject);
        Debug.Log("Homing Projectile disappeared");
    }

    // Collision detection. If it hits player or enemy, deal damage. If it hits portal, don't disappear.
    // Else, disappear on contact
    public void OnCollisionEnter2D(Collision2D someObject)
    {

        if (someObject.gameObject.name == "NAPR")
        {
            //player.health -= power;
            //Debug.Log("Player Current Health: " + player.health);
            Destroy(gameObject);
            Debug.Log("Projectile hit NAPR");
        }
        else if (someObject.gameObject.name == "Enemy")
        {
            // enemy.health -= power;
            //  Debug.Log("Enemy Current Health: " + enemy.health);
            Destroy(gameObject);
            Debug.Log("Projectile hit enemy");
        }
        else if (someObject.gameObject.name == "portal")
        {
            Debug.Log("Projectile hit portal");
        }
        else if (!piercing)
        {
            if (this.gameObject.layer != 16 || someObject.gameObject.layer == 11 || someObject.gameObject.layer == 8) // tough projectile
            {
                Destroy(gameObject);
                Debug.Log("Projectile hit something");
                Debug.Log(someObject.gameObject.name);
            }
        }

        // player projectile
        if (this.gameObject.layer == 14) // player projectile
        {
            if (someObject.gameObject.layer == 12 && someObject.gameObject.name != "Lambda" 
                && someObject.gameObject.name != "Gamma") // hits damagable enemy
            {         
                Enemy enemy = someObject.gameObject.GetComponent<Enemy>();
                if (enemy.getIsDamageable())
                {
                    createParticle(particlesOnCollision);
                    enemy.health -= this.power;
                    AudioSource edSound = Instantiate<AudioSource>(enemyDamagedSound);
                    edSound.Play();
                    Destroy(edSound, 1f);
                    Debug.Log("Enemy lost health. Current Enemy HP: " + enemy.health);
                }
                else
                {
                    createParticle(defaultParticles);
                }
                
            }
            else if (someObject.gameObject.layer == 13)
            {
                createParticle(lazersCollideParticle);
            }
            else
            {
                createParticle(defaultParticles);
            }
        }  
        else if (this.gameObject.layer == 13 || this.gameObject.layer == 16) // enemy projectile
        {
            if (someObject.gameObject.layer == 8) // hits player
            {
                createParticle(particlesOnCollision);
                Player player = someObject.gameObject.GetComponent<Player>();
                player.health -= this.power;
                Debug.Log("NAPR lost health. Current player HP: " + player.health);
            }
            else if (someObject.gameObject.layer == 14 && this.gameObject.layer != 16)
            {
                createParticle(lazersCollideParticle);
            }
            else
            {
                createParticle(defaultParticles);
            }
        }


    }

    public void createParticle(ParticleSystem particle)
    {
        // create particles on collision
        if (particle != null)
        {
            Instantiate(particle, transform.position, transform.rotation);
        }
    }
}
