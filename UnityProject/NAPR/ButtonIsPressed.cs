using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ButtonIsPressed : MonoBehaviour
{
    public Transform pressedRaycast;
    public LayerMask buttonObjInteractions;
    public float prLength;

    public GameObject door;

    private bool isActive = true;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        RaycastHit2D raycastResult = Physics2D.Raycast(pressedRaycast.position, pressedRaycast.up, prLength,buttonObjInteractions.value);
        if (raycastResult.collider != null)
        {
             if(isActive){
                door.SetActive(false);
                this.gameObject.GetComponent<SpriteRenderer>().sprite = Resources.LoadAll<Sprite>("EntitySprites/EnvironmentSprites/button")[1];
            }
            isActive = false;
        }
        else
        {
            if(!isActive){
                door.SetActive(true);
                this.gameObject.GetComponent<SpriteRenderer>().sprite = Resources.LoadAll<Sprite>("EntitySprites/EnvironmentSprites/button")[0];
            }
            isActive = true;
        }

        }
}
