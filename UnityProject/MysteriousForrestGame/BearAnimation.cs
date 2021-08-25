using System.Collections;
using System.Collections.Generic;
using Assets.ScriptFolder.Enemies.Bear;
using UnityEngine;

public class BearAnimation : MonoBehaviour
{
    public HybridBearAttack _HybridBearAttack;
    public Animator bearAnimator;
    
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if (_HybridBearAttack.AnimationID == 1)
        {
            bearAnimator.SetInteger("AnimationID", 1);
        }else if (_HybridBearAttack.AnimationID == 2)
        {
            bearAnimator.SetInteger("AnimationID", 2);
        }else if (_HybridBearAttack.AnimationID == 3)
        {
            bearAnimator.SetInteger("AnimationID", 3);
        }else if (_HybridBearAttack.AnimationID == 4)
        {
            bearAnimator.SetInteger("AnimationID", 4);
        }
    }
}
