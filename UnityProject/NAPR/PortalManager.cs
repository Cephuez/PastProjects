using System.Collections;
using System.Collections.Generic;
using UnityEditor;
//using UnityEditor.Animations;
using UnityEngine;


public class PortalManager : MonoBehaviour
{
    GameObject portalOne;
    GameObject portalTwo;

    public GameObject PortalBluePrefab;
    public GameObject PortalRedPrefab;
    private GameObject[] portals;
    // Start is called before the first frame update
    void Start()
    {
        portalOne = GameObject.FindGameObjectWithTag("PortalOne");
        portalTwo = GameObject.FindGameObjectWithTag("PortalTwo");

        if (portalOne == null){
            portalOne = Instantiate(PortalBluePrefab);
            portalOne.tag = "PortalOne";
            portalOne.name = "PortalOne";
            portalOne.GetComponent<SpriteRenderer>().color = Color.white;
        }
        if (portalTwo == null){
            portalTwo = Instantiate(PortalRedPrefab);
            portalTwo.tag = "PortalTwo";
            portalTwo.name = "PortalTwo";
            portalTwo.GetComponent<SpriteRenderer>().color = Color.white;

        }        
        portalOne.SetActive(false);
        portalOne.GetComponent<Portal>().setOtherPort(portalTwo);

        portalTwo.SetActive(false);
        portalTwo.GetComponent<Portal>().setOtherPort(portalOne);

        portals = new GameObject[] {portalOne,portalTwo};
        GameObject boss = GameObject.FindGameObjectWithTag("Boss");
        if (boss){
            boss.GetComponent<ChangablePortableTiles>().portalManager = this;
        }
        //print(GameObject.FindGameObjectWithTag("Boss").GetComponent<ChangablePortableTiles>().portalManager);
    }

    public bool movePortal(Vector3 location, int whichPortal){
        GameObject portal = null;
        if (whichPortal == 1){
            portal = portalOne;
        } else if (whichPortal == 2){
            portal = portalTwo;
        }
        //Debug.Log("CLICKED");
        bool prevState = portal.activeSelf;
        portal.SetActive(true);
        bool didMove = portal.GetComponent<Portal>().move(location);
        if (!didMove && !prevState){
            portal.SetActive(false);
        }
        return didMove;
    }
    //when character enters new room, the portals should be deactivated...
    void enterNewRoom(){
        portalOne.SetActive(false);
        portalTwo.SetActive(false);
    }

    public void setPortDir(Vector3 direction, int whichPortal){
        GameObject portal = null;
        if (whichPortal == 1){
            portal = portalOne;
        } else if (whichPortal == 2){
            portal = portalTwo;
        }
        if (portal.activeSelf){
            //direction = direction.normalized;
            portal.GetComponent<Portal>().setDir(direction);
        }

    }

    public void drawPortDir(int whichPortal){
        GameObject portal = null;
        if (whichPortal == 1){
            portal = portalOne;
        } else if (whichPortal == 2){
            portal = portalTwo;
        }
        if (portal.activeSelf){
            //direction = direction.normalized;
            portal.GetComponent<Portal>().drawDir();
        }
    }


    // Update is called once per frame
    void Update(){
        //check portal validity
        
    }

    public void UpdatePortals(){
        foreach(GameObject portal in portals){
            //Debug.Log("CLICKED");
            if (portal.activeSelf){
                Vector3 location = portal.transform.position;
                bool didMove = portal.GetComponent<Portal>().move(location);
                if (!didMove){
                    portal.SetActive(false);
                }
            }
        }
    }
}
