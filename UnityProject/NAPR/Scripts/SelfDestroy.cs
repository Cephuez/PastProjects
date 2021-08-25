using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SelfDestroy : MonoBehaviour
{
    public float destroyParticleTimer = 2.0f;

    // Start is called before the first frame update
    void Start()
    {
        Destroy(gameObject, destroyParticleTimer);
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
