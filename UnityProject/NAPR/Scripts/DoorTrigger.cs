using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DoorTrigger : MonoBehaviour
{
    public Transform detectRay;
    public LayerMask rayInteraction;
    public float rayLength;
    public GameObject door;

    public bool makeActive = false;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        RaycastHit2D raycastResult = Physics2D.Raycast(detectRay.position, detectRay.right, rayLength, rayInteraction.value);
        if (raycastResult.collider != null)
        {
            if (makeActive)
            {
                door.SetActive(true);
            }
            else
            {
                door.SetActive(false);
            }
            
        }
    }
}
