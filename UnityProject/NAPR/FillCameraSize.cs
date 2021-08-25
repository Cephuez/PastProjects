using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FillCameraSize : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        this.transform.SetParent(Camera.main.gameObject.transform);
        //set this position 1 units in front of camera
        this.transform.localPosition = new Vector3(0,0,1);

        float sizeX = this.gameObject.GetComponent<Renderer> ().bounds.size.x;
        float sizeY = this.gameObject.GetComponent<Renderer> ().bounds.size.y;

        Camera camera = Camera.main;
        
        float halfHeight = camera.orthographicSize;
        float halfWidth = camera.aspect * halfHeight;

        Vector3 rescale = this.gameObject.transform.localScale;
        rescale.x = halfWidth * 2 * rescale.x/sizeX;
        rescale.y = halfHeight * 2 * rescale.y/sizeY;

        this.gameObject.transform.localScale = rescale;
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
