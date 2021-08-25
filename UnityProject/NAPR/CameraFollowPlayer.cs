using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Experimental.PlayerLoop;

public class CameraFollowPlayer : MonoBehaviour
{
    public Transform player;
    public GridLayout gLayout;
    public CoordLevPos levelCoord;
    public float adjustCameraY;

    private bool waitForSetUp = true;
    private float x1B, x2B, y1B, y2B;
    void Start()
    {
        this.transform.position = new Vector3(player.position.x, player.position.y, transform.position.z);
    }
    
    private void SetBoundaries()
    {
        x1B = levelCoord.X1B();
        y1B = levelCoord.Y1B();
        x2B = levelCoord.X2B();
        y2B = levelCoord.Y2B();
    }
    
    void FixedUpdate()
    {
        if (waitForSetUp)
        {
            SetBoundaries();
            waitForSetUp = false;
        }
        bool mustFollow = FixCamera();
        if (mustFollow) { 
           CamOnPlayer();
        }

        /*
        if (Input.GetKeyDown("b"))
        {
            bool mustFollow = FixCamera();
            if (mustFollow)
            {
                CamOnPlayer();
            }
        }
        */
    }

    private void CamOnPlayer()
    {
        
        if (x1B < player.transform.position.x && player.transform.position.x < x2B)
        {
            transform.position = new Vector3(player.position.x, this.transform.position.y, transform.position.z);
        }

        if (y1B < player.transform.position.y && player.transform.position.y < y2B)
        {
            transform.position = new Vector3(this.transform.position.x, player.position.y, transform.position.z);
        }
        
        
        /*if (levelCoord.X1B() < player.transform.position.x && player.transform.position.x < levelCoord.X2B())
        {
            transform.position = new Vector3(player.position.x, this.transform.position.y, transform.position.z);
        }

        if (levelCoord.Y1B() < player.transform.position.y && player.transform.position.y < levelCoord.Y2B())
        {
            transform.position = new Vector3(this.transform.position.x, player.position.y, transform.position.z);
        }
        */
        
    }
    private bool FixCamera()
    {
        bool mustFollow = true;
        //print("X: " + transform.position.x);
        //print("Y: " + transform.position.y);

        //print("Boundaries");
        print("X1: " + x1B);
        print("Y1: " + y1B);
        print("X2: " + x2B);
        print("Y2: " + y2B);
        
        
        if (transform.position.x < x1B)
        {
            this.transform.position = new Vector3(x1B,transform.position.y, transform.position.z);
            mustFollow = false;
        }

        if (transform.position.x > x2B)
        {
            this.transform.position = new Vector3(x2B+1f,transform.position.y, transform.position.z);
            mustFollow = false;
        }

        if (transform.position.y < y1B)
        {
            this.transform.position = new Vector3(transform.position.x, y1B, transform.position.z);
            mustFollow = false;
        }

        if (transform.position.y > y2B)
        {
            this.transform.position = new Vector3(transform.position.x, y2B-1f,transform.position.z);
            mustFollow = false;
        }
        return mustFollow;
        
        /*
        if (transform.position.x < levelCoord.X1B())
        {
            this.transform.position = new Vector3(levelCoord.X1B(),transform.position.y, transform.position.z);
            mustFollow = false;
        }

        if (transform.position.x > levelCoord.X2B())
        {
            this.transform.position = new Vector3(levelCoord.X2B()+1f,transform.position.y, transform.position.z);
            mustFollow = false;
        }

        if (transform.position.y < levelCoord.Y1B())
        {
            this.transform.position = new Vector3(transform.position.x, levelCoord.Y1B(), transform.position.z);
            mustFollow = false;
        }

        if (transform.position.y > levelCoord.Y2B())
        {
            this.transform.position = new Vector3(transform.position.x, levelCoord.Y2B()-1f,transform.position.z);
            mustFollow = false;
        }
        return mustFollow;
        */
    }

    public void SetNewCameraPlacement(float[] pos)
    {
        x1B = pos[0];
        y1B = pos[1];
        x2B = pos[2];
        y2B = pos[3];
        
        FindNewPosition();
       
        // Reset Camera or something xd
    }

    private void FindNewPosition()
    {
        // if y1B < y < y2B, then keep y position
        // else if y1B closer to y than y2B, then camera on y1B
        // else camera on y2B
        if (!(y1B < transform.position.y && transform.position.y < y2B))
        {
            float y1Diff = Mathf.Abs(y1B - transform.position.y);
            float y2Diff = Mathf.Abs(y2B - transform.position.y);
            if (y1Diff < y2Diff)
                transform.position = new Vector3(transform.position.x, y1B, transform.position.z);
            else
                transform.position = new Vector3(transform.position.x, y2B, transform.position.z);
            
            
        }

        if (!(x1B < transform.position.x && transform.position.x < x2B))
        {
            float x1Diff = Mathf.Abs(x1B - transform.position.x);
            float x2Diff = Mathf.Abs(x2B - transform.position.x);
            if (x1Diff < x2Diff)
                transform.position = new Vector3(x1B, transform.position.y, transform.position.z);
            else
                transform.position = new Vector3(x2B, transform.position.y, transform.position.z);
            
            
        }
        // if x1B < x < x2B, then keep x position
        // else if x1B closer to x than x2B, then camera on x1B
        // else camera on x2B
        //transform.position = new Vector3(x1B,y1B,transform.position.z);
    }
}
