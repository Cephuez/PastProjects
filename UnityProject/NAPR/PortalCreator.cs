using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;

public class PortalCreator : MonoBehaviour, IPointerDownHandler, IPointerUpHandler
{
    public GameObject portManagPrefab;
    public GameObject character;
    public AudioSource portalSound1;
    public AudioSource portalSound2;
    public AudioSource laserSound;
    //public AudioSource portal2Sound;
    //private GameObject portalManager;
    private Vector3 DirectionTracker;
    private bool leftButtonLock;
    private bool rightButtonLock;
    private bool portalMoved;
    //true means laser, false means portal
    private bool laserOrPortal=true;

    private PortalManager portalManager;
    public bool canFire=true;
    GameObject camera;
    // Start is called before the first frame update
    void Start()
    {
        
        GameObject temp = GameObject.FindGameObjectWithTag("PortalManager");
        if (temp == null){
            temp = Instantiate(portManagPrefab);
            temp.tag = "PortalManager";
            temp.name = "Portal Manager";
            temp.SetActive(true);
        }
        portalManager = temp.GetComponent<PortalManager>();
        
        if (character == null)
            character = GameObject.FindGameObjectWithTag("Player");
        camera = Camera.main.gameObject;
        if (camera.GetComponent<Physics2DRaycaster>() == null){
            camera.AddComponent<Physics2DRaycaster>();
        }
        addEventSystem();
        //buttonLock ensures that the player cannot set the portals at the same time
        leftButtonLock=false;
    }
    void Update(){
        if ((leftButtonLock || rightButtonLock) && portalMoved){
            //decide if left or right button lock
            int whichPortal=1;
            if (rightButtonLock) whichPortal = 2;
            //draw normalized? vector to mouse position
            Vector3 position = calcWorldPosFromMouse(Input.mousePosition);
            portalManager.setPortDir(position,whichPortal);
        }

        if (Input.GetKeyDown("1")){
            laserOrPortal=true;
        }else if (Input.GetKeyDown("2")){
            laserOrPortal = false;
        }

    }

    public void OnPointerDown(PointerEventData eventData){      
        //print("WHAT");  
        if (!laserOrPortal && canFire){
            
            Vector3 location = calcWorldPosFromMouse(eventData.position);
            if (eventData.button == PointerEventData.InputButton.Left&& !rightButtonLock){
                character.GetComponent<Animator>().SetBool("Portal",true);
                leftButtonLock=true;
                AudioSource ps1 = Instantiate<AudioSource>(portalSound1);
                ps1.Play();
                Destroy(ps1.gameObject, 1f);
                // Play Sound
                portalMoved = portalManager.movePortal(location,1);
            }else if (eventData.button == PointerEventData.InputButton.Right&& !leftButtonLock){
                character.GetComponent<Animator>().SetBool("Portal",true);
                // Play Sound
                AudioSource ps2 = Instantiate<AudioSource>(portalSound2);
                ps2.Play();
                Destroy(ps2.gameObject, 1f);
                rightButtonLock=true;
                portalMoved = portalManager.movePortal(location,2);
            }
        }else if(canFire)
        {
            AudioSource laserS = Instantiate<AudioSource>(laserSound);
            laserS.Play();
            Destroy(laserS.gameObject, 1f);
            character.GetComponent<PlayerLazer>().firePlayerLazer();
            character.GetComponent<Animator>().SetBool("Fire",true);
        }
    }

    Vector3 calcWorldPosFromMouse(Vector2 mousePosition){
        //find z depth assuming that background is always at z=0
        float z = Mathf.Abs(camera.transform.position.z);
        Vector3 position = new Vector3(mousePosition.x,mousePosition.y,z);
        Vector3 location = camera.GetComponent<Camera>().ScreenToWorldPoint(position);
        return location;
    }

    public void OnPointerUp(PointerEventData eventData){
        if (eventData.button == PointerEventData.InputButton.Left){
            leftButtonLock=false;
            portalManager.drawPortDir(1);
        }else if (eventData.button == PointerEventData.InputButton.Right){
            rightButtonLock=false;
            portalManager.drawPortDir(2);
        }
        character.GetComponent<Animator>().SetBool("Fire",false);
        character.GetComponent<Animator>().SetBool("Portal",false);
    }


    void addEventSystem()
    {
        GameObject eventSystem = null;
        GameObject tempObj = GameObject.Find("EventSystem");
        if (tempObj == null)
        {
            eventSystem = new GameObject("EventSystem");
            eventSystem.AddComponent<EventSystem>();
            eventSystem.AddComponent<StandaloneInputModule>();
        }
        else
        {
            if ((tempObj.GetComponent<EventSystem>()) == null)
            {
                tempObj.AddComponent<EventSystem>();
            }

            if ((tempObj.GetComponent<StandaloneInputModule>()) == null)
            {
                tempObj.AddComponent<StandaloneInputModule>();
            }
        }
    }

    
}
