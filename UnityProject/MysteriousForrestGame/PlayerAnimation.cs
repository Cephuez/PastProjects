using System.Collections;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using Assets.ScriptFolder.PlayerScripts;
using UnityEngine;

public class PlayerAnimation : MonoBehaviour
{
    public PlayerMovement _PlayerMovement;

    public Animator playerAnimator;
    // Start is called before the first frame update

    /*
     * animationID
     *     1 -> Idle
     *     2 -> Walk
     *     3 -> Jump
     *     4 -> Dash
     *     5 -> Hold to Wall
     *     6 -> Climb Wall
     *     7 -> Strike
     */
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        // Idle
        if (_PlayerMovement.animationID == 1)
        {
            playerAnimator.SetInteger("ID", 1);
        }else if (_PlayerMovement.animationID == 2)
        {
            playerAnimator.SetInteger("ID", 2);
        }else if (_PlayerMovement.animationID == 3)
        {
            playerAnimator.SetInteger("ID", 3);
        }else if (_PlayerMovement.animationID == 4)
        {
            playerAnimator.SetInteger("ID", 4);
        }else if (_PlayerMovement.animationID == 5)
        {
            playerAnimator.SetInteger("ID", 5);
        }else if (_PlayerMovement.animationID == 6)
        {
            playerAnimator.SetInteger("ID", 6);
        }
    }

    private void SetAnimation()
    {
        
    }
}
