using System.Collections;
using System.Collections.Generic;
using Assets.ScriptFolder.Enemies.Plants;
using UnityEngine;

public class SpikePlantAnimation : MonoBehaviour
{
    public ThrowSpike _ThrowSpike;
    public Animator spikePlantAnimator;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if (_ThrowSpike.AnimationID == 1)
        {
            spikePlantAnimator.SetInteger("AnimationID", 1);
        }else if (_ThrowSpike.AnimationID == 2)
        {
            spikePlantAnimator.SetInteger("AnimationID", 2);
        }else if (_ThrowSpike.AnimationID == 3)
        {
            spikePlantAnimator.SetInteger("AnimationID", 3);
        }else if (_ThrowSpike.AnimationID == 4)
        {
            spikePlantAnimator.SetInteger("AnimationID", 4);
        }
    }
}
