using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PortalTransport : MonoBehaviour
{
    // Start is called before the first frame update
    private bool notInitialized;
    private GameObject parent;
    void Start()
    {
        print("INSTANTIATED TRIGGER");
        notInitialized = true;
    }

    // Update is called once per frame
    void Update()
    {
        if (notInitialized && this.transform.parent != null){
            parent = this.transform.parent.gameObject;
            //this.gameObject.GetComponent<SpriteRenderer>().sprite = parent.GetComponent<Portal>().sprites[0];
            notInitialized=false;
        }
    }
    //this should be for objects Assuming RigidBody
    void OnTriggerEnter2D(Collider2D collision){
        //Debug.Log("COLLISION!");
        if (collision.gameObject.TryGetComponent(out Transporting transporting)){
            //launchObject(collision.gameObject.)
        }   
        else
            if (parent.GetComponent<Portal>().getOtherPortal().activeSelf){
                print(collision.gameObject.name);
                collision.gameObject.AddComponent<Transporting>();
                parent.GetComponent<Portal>().sendToOtherPortal(collision.gameObject);
        }
        // if (collision.gameObject.GetComponent("No Portal")!=null){
        //         this.gameObject.transform.position = pastPosition;
        // }
        // parent.GetComponent<Portal>().
    }

    void OnTriggerExit2D(Collider2D collision){
        //Debug.Log("COLLIDED");
        if (collision.gameObject.TryGetComponent(out Transporting transporting)){
            GameObject.Destroy(collision.gameObject.GetComponent<Transporting>());
        }
    }

    // void sendToOtherPortal(GameObject obj){
    //     Vector3 destination = otherPortal.transform.position;
    //     Rigidbody2D rigid = obj.GetComponent<Rigidbody2D>();
    //     rigid.isKinematic=true;
    //     obj.transform.position = otherPortal.transform.position;
    //     rigid.isKinematic=false;
    //     float velMag = rigid.velocity.magnitude;
    //     //CHANGE THIS TO CHANGE SETTINGS?
    //     if (velMag < maxMag){
    //         velMag = velMag + maxMag;
    //     }
    //     otherPortal.GetComponent<Portal>().launchObject(rigid,velMag);

    // }

    // void launchObject(Rigidbody2D rigid, float suddenForce){
    //     rigid.AddForce(this.direction * suddenForce, ForceMode2D.Impulse);
    // }

}
