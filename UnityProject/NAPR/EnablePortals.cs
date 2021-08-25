using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnablePortals : MonoBehaviour
{

    private GameObject mouseListener;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if (!mouseListener){
            mouseListener = GameObject.Find("MouseListener");
            if (mouseListener){
                mouseListener.GetComponent<PortalCreator>().canFire = true;
            }
        }
    }
}
