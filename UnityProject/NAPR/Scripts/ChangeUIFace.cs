using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class ChangeUIFace : MonoBehaviour
{
    public Player player;
    public Sprite faceImage1;
    public Sprite faceImage2;
    public Sprite faceImage3;
    public Sprite faceImage4;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if (player.health >= 80)
        {
            GetComponent<Image>().sprite = faceImage1;
        }
        else if (player.health >= 30)
        {
            GetComponent<Image>().sprite = faceImage2;
        }
        else if (player.health >= 1)
        {
            GetComponent<Image>().sprite = faceImage3;
        }
        else
        {
            GetComponent<Image>().sprite = faceImage4;
        }


    }
}
