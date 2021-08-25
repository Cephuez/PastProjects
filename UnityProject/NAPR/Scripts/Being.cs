using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// Being class are objects with stat properties. 
public class Being : MonoBehaviour
{
    public int health;
    public int power;
    public float speed;

    public Animator animator;
    public Collider2D colliderObject;
    public Rigidbody2D rigidbodyObject;
    public ParticleSystem deathParticles;

    public float deathAnimationTimer = 1.5f;
    public int turnAroundValue = 180;
    protected bool beingAction = true;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    // Check to see if the being is out of health.
    public virtual bool isDead()
    {
        if (health <= 0)
        {
            if (deathParticles != null)
            {
                Instantiate(deathParticles, transform.position, transform.rotation);
                //(deathParticles).transform.parent = (gameObject).transform;
            }

            animator.SetBool("isDead", true);
            beingAction = false;
            Destroy(colliderObject);
            rigidbodyObject.isKinematic = true; // animation stays in place of death
            Destroy(gameObject, deathAnimationTimer);
            //gameObject.SetActive(false);
            // Debug.Log("Being died");
            return true;
        }
        return false;
    }

    public void moveForwardX(GameObject gameObject, float speed, float speedIncrease, int direction)
    {
        // Vector3 nextPos = new Vector3(direction * (speed + speedIncrease) * Time.deltaTime, 0f);
        // Vector3 dirToNextPos = Vector3.Normalize(nextPos - transform.position);
        // gameObject.transform.forward = dirToNextPos;
        // gameObject.transform.position += nextPos;

        transform.position += new Vector3(direction * (speed + speedIncrease) * Time.deltaTime, 0f);
        rigidbodyObject.MovePosition(transform.position);
    }

    public void moveForwardY(GameObject gameObject, float speed, float speedIncrease, int direction)
    {
      //  Vector3 nextPos = new Vector3(0f, direction * (speed + speedIncrease) * Time.deltaTime);
      //  Vector3 dirToNextPos = Vector3.Normalize(nextPos - transform.position);
      //  gameObject.transform.forward = dirToNextPos;
      //  gameObject.transform.position += nextPos;

        transform.position += new Vector3(0f, direction * (speed + speedIncrease) * Time.deltaTime);
        rigidbodyObject.MovePosition(transform.position);
    }

    public void moveForwardDiag1(GameObject gameObject, float speed, float speedIncrease, int direction)
    {
        //Vector3 nextPos = new Vector3(direction * (speed + speedIncrease) * Time.deltaTime, direction * (speed + speedIncrease) * Time.deltaTime);
        //Vector3 dirToNextPos = Vector3.Normalize(nextPos - transform.position);
       // gameObject.transform.forward = dirToNextPos;
       // gameObject.transform.position += nextPos;

        transform.position += new Vector3(direction * (speed + speedIncrease) * Time.deltaTime, direction * (speed + speedIncrease) * Time.deltaTime);
        rigidbodyObject.MovePosition(transform.position);
    }

    public void moveForwardDiag2(GameObject gameObject, float speed, float speedIncrease)
    {
        //Vector3 nextPos = new Vector3((-1) * (speed + speedIncrease) * Time.deltaTime,
        //    (speed + speedIncrease) * Time.deltaTime);
       // Vector3 dirToNextPos = Vector3.Normalize(nextPos - transform.position);
       // gameObject.transform.forward = dirToNextPos;
       // gameObject.transform.position += nextPos;

        transform.position += new Vector3((-1) * (speed + speedIncrease) * Time.deltaTime,
            (speed + speedIncrease) * Time.deltaTime);
        rigidbodyObject.MovePosition(transform.position);
    }

    public void moveForwardDiag3(GameObject gameObject, float speed, float speedIncrease)
    {
        //Vector3 nextPos = new Vector3((speed + speedIncrease) * Time.deltaTime,
        //    (-1) * (speed + speedIncrease) * Time.deltaTime);
       // Vector3 dirToNextPos = Vector3.Normalize(nextPos - transform.position);
       // gameObject.transform.forward = dirToNextPos;
       // gameObject.transform.position += nextPos;

        transform.position += new Vector3((speed + speedIncrease) * Time.deltaTime,
            (-1) * (speed + speedIncrease) * Time.deltaTime);
        rigidbodyObject.MovePosition(transform.position);
    }

    // sets if the being will have action or not
    public void setActiveAction(bool isAction)
    {
        beingAction = isAction;
    }
}
