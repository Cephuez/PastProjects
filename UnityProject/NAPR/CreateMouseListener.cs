using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CreateMouseListener : MonoBehaviour
{
    // Start is called before the first frame update
    public GameObject MouseListenerPrefab;
    void Start()
    {
        GameObject mL = GameObject.Find("MouseListener");
        if (mL == null){
                mL = Instantiate(MouseListenerPrefab);
                mL.name = "MouseListener";
                Camera.main.gameObject.layer = 29;
        }
    }
}
