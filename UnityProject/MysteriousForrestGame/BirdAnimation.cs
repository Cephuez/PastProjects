using System.Collections;
using System.Collections.Generic;
using Assets.ScriptFolder.Enemies.Bird;
using UnityEngine;

public class BirdAnimation : MonoBehaviour
{
    public BirdAttackMoves _BirdAttackMoves;
    public Animator birdAnimator;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if (_BirdAttackMoves.AnimationID == 1)
        {
            birdAnimator.SetInteger("AnimationID", 1);
        }else if (_BirdAttackMoves.AnimationID == 2)
        {
            birdAnimator.SetInteger("AnimationID", 2);
        }else if (_BirdAttackMoves.AnimationID == 3)
        {
            birdAnimator.SetInteger("AnimationID", 3);
        }
    }
}
