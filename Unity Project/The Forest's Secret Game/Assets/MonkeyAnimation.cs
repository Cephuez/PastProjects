using System.Collections;
using System.Collections.Generic;
using Assets.ScriptFolder.Enemies;
using UnityEngine;

public class MonkeyAnimation : MonoBehaviour
{
    public MonkeyJumping _MonkeyJumping;
    public Animator monkeyAnimator;

    void Update()
    {
        if (_MonkeyJumping.AnimationID == 1)
        {
            monkeyAnimator.SetInteger("AnimationID", 1);
        }else if (_MonkeyJumping.AnimationID == 2)
        {
            monkeyAnimator.SetInteger("AnimationID", 2);
        }else if (_MonkeyJumping.AnimationID == 3)
        {
            monkeyAnimator.SetInteger("AnimationID", 3);
        }
    }
}
