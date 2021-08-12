using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SubWeapon : MonoBehaviour
{
    public int MainID;
    public int id;
    public int counts;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void AccessSubWeapons(int weaponID)
    {
        SwordSubWeapons(weaponID);
        AxeSubWeapons(weaponID);
        BowSubWeapons(weaponID);
    }

    private void SwordSubWeapons(int weaponID)
    {
        if (weaponID == 1)
        {
            
        }
    }

    private void AxeSubWeapons(int weaponID)
    {
        if (weaponID == 2)
        {
            
        }
    }

    private void BowSubWeapons(int weaponID)
    {
        if (weaponID == 3)
        {
            BowChoices();
        }
    }

    private void BowChoices()
    {
        if (id == 1)
        {
            // Normal Arrow
        }else if (id == 2)
        {
            // Rope Arrow
        }else if (id == 3)
        {
            // Light Arrow
        }
    }
}
