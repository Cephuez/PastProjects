using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class UpgradeWristBands : MonoBehaviour
{
    public PortalCreator pc;
    // Start is called before the first frame update
    public void EnableWristBands()
    {
        pc.canFire = true;
    }
    
}
