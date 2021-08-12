using System.Collections;
using System.Collections.Generic;
using Assets.ScriptFolder.Enemies.Turtle;
using UnityEngine;

public class Turtle_Animation : MonoBehaviour
{
    public GiantTurtleAttack _GiantTurtleAttack;
    public Animator turtleAnimator;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if (_GiantTurtleAttack.AnimationID == 1)
        {
            turtleAnimator.SetInteger("AnimationID", 1);
        }else if (_GiantTurtleAttack.AnimationID == 2)
        {
            turtleAnimator.SetInteger("AnimationID", 2);
        }
    }
}
