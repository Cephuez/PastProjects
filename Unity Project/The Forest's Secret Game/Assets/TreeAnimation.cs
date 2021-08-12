using System.Collections;
using System.Collections.Generic;
using Assets.ScriptFolder.Enemies;
using UnityEngine;

public class TreeAnimation : MonoBehaviour
{
    public WalkingTreeAttack _WalkingTreeAttack;
    public Animator treeAnimator;

    void Update()
    {
        if (_WalkingTreeAttack.AnimationID == 1)
        {
            treeAnimator.SetInteger("AnimationID", 1);
        }else if (_WalkingTreeAttack.AnimationID == 2)
        {
            treeAnimator.SetInteger("AnimationID", 2);
        }else if (_WalkingTreeAttack.AnimationID == 3)
        {
            treeAnimator.SetInteger("AnimationID", 3);
        }else if (_WalkingTreeAttack.AnimationID == 4)
        {
            treeAnimator.SetInteger("AnimationID", 4);
        }
    }
}
