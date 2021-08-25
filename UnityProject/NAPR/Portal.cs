using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Portal : MonoBehaviour
{

    private Vector2 direction;
    private Vector3 pastPosition;
    private GameObject portalChild;
    public GameObject portalPreFab;
    //set the maximum magnitude of the direction
    private float maxMag=1f;
    //set by the Portal Manager
    private GameObject otherPortal;
    public Sprite[] sprites;
    // Start is called before the first frame update
    void Start()
    {
        //set up CircleCollider2D
        if (this.gameObject.TryGetComponent(out CircleCollider2D port)){
            this.gameObject.AddComponent<CircleCollider2D>();
        }

        //portalChild = GameObject.FindGameObjectWithTag("PortalTransport");
        // if (portalChild == null){
        //     portalChild = Instantiate(portalPreFab);
        //     portalChild.transform.SetParent(this.transform);
        //     portalChild.tag = "PortalTransport";
        //     portalChild.name = "PortalTransport";
        //     portalChild.SetActive(true);
           
        // }   
    }

    public GameObject getOtherPortal(){
        return otherPortal;
    }

    public void setOtherPort(GameObject portal){
        otherPortal = portal;
    }

    public void setDir(Vector2 direction){
        direction = direction - (Vector2)this.gameObject.transform.position;
        float mag = direction.magnitude;
        if (mag > maxMag)
            this.direction = direction.normalized  * maxMag;
        else
            this.direction = direction.normalized * mag;
        Debug.DrawLine(this.gameObject.transform.position, this.direction + (Vector2)this.gameObject.transform.position, Color.black);
        //Debug.DrawLine(this.gameObject.transform.position, direction, Color.black);
    }
    
    public void drawDir(){
        Debug.DrawLine(this.gameObject.transform.position, this.direction + (Vector2)this.gameObject.transform.position, Color.black,5f);
    }

    public bool move(Vector3 location){
        bool moved = false;
        //ContactFilter2D noFilter = new ContactFilter2D().NoFilter();
        CircleCollider2D comp = this.gameObject.GetComponent<CircleCollider2D>();
        Debug.Log(comp.ToString());
        //if the center point is on an object that allows portals
        
        if (isValidLocation(Physics2D.OverlapPointAll(location))){
            //if the position to move to has no obstacles
            if(checkColliders(Physics2D.OverlapCircleAll(location,comp.radius))){
                pastPosition = this.gameObject.transform.position;
                this.gameObject.transform.position = location;
                moved = true;
            }
        }
        return moved;
    }

    //make sure that the colliders in question don't have 'No Portal' attribute
    bool checkColliders(Collider2D[] contacts){
        foreach(Collider2D coll in contacts){
            if (coll != null){
                if (coll.gameObject.TryGetComponent(out NoPortal port) && coll.gameObject != this.gameObject){
                    Debug.Log("Hit Invalid");
                    print(coll.gameObject.name);
                    return false;
                }
            }
        }
        return true;
    }

    //make sure that the center of the portal is on an 'allow portal' attribute
    bool isValidLocation(Collider2D[] contacts){
        foreach(Collider2D coll in contacts){
            if (coll != null){
                if (coll.gameObject.TryGetComponent(out AllowsPortal port) && coll.gameObject != this.gameObject){
                    return true;
                }
            }
        }
        return false;
    }
    //this should be for objects Assuming RigidBody
    // void OnTriggerEnter2D(Collider2D collision){
    //     Debug.Log("COLLISION!");
    //     if (collision.gameObject.TryGetComponent(out Transporting transporting)){
    //         //launchObject(collision.gameObject.)
    //     }   
    //     else
    //         if (otherPortal.activeSelf){
    //             collision.gameObject.AddComponent<Transporting>();
    //             sendToOtherPortal(collision.gameObject);
    //     }
    //     // if (collision.gameObject.GetComponent("No Portal")!=null){
    //     //         this.gameObject.transform.position = pastPosition;
    //     // }
    // }

    // void OnTriggerExit2D(Collider2D collision){
    //     Debug.Log("COLLIDED");
    //     if (collision.gameObject.TryGetComponent(out Transporting transporting)){
    //         GameObject.Destroy(collision.gameObject.GetComponent<Transporting>());
    //     }
    // }

    public void sendToOtherPortal(GameObject obj){
        Vector3 destination = otherPortal.transform.position;
        Rigidbody2D rigid = obj.GetComponent<Rigidbody2D>();
        rigid.isKinematic=true;
        obj.transform.position = otherPortal.transform.position;
        //rigid.velocity = this.direction.normalized;
        rigid.isKinematic=false;
        float velMag = rigid.velocity.magnitude;
        //CHANGE THIS TO CHANGE SETTINGS?
        if (velMag < maxMag){
            velMag = velMag + maxMag;
        }
        //Debug.Log(velMag);
        rigid.velocity = Vector3.zero;
        otherPortal.GetComponent<Portal>().launchObject(rigid,velMag);

    }

    void launchObject(Rigidbody2D rigid, float suddenForce){
        rigid.AddForce(this.direction * suddenForce * rigid.mass, ForceMode2D.Impulse);
        rigid.gameObject.transform.right = this.direction;
        rigid.freezeRotation=false;
    }

}
