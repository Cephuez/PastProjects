using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SubWeaponDisplay : MonoBehaviour
{
    public int ID;
    public ExtraWeaponOptions _ExtraWeaponOptions;

    private SubWeapon subWeapon;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void SetOption(SubWeapon subweapon)
    {
        this.subWeapon = subweapon;
    }
    
    void OnMouseEnter()
    {
        _ExtraWeaponOptions.PickExtraOption(ID);
    }

    public bool CanBeEnabled()
    {
        return subWeapon != null;
    }

    public SubWeapon GetSubWeapon()
    {
        return subWeapon;
    }
}
