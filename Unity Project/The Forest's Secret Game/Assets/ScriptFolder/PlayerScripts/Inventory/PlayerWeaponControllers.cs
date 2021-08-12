using System.Collections;
using System.Collections.Generic;
using Assets.ScriptFolder.PlayerScripts.Inventory.PlayerWeapons;
using Assets.ScriptFolder.PlayerScripts.Inventory.PlayerWeapons.Weapons.Axe;
using Assets.ScriptFolder.PlayerScripts.Inventory.PlayerWeapons.Weapons.Bow;
using Assets.ScriptFolder.PlayerScripts.Inventory.PlayerWeapons.Weapons.Sword;
using UnityEngine;

public class PlayerWeaponControllers : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    private void SwordControls(PlayerWeapons currWeapon)
    {
        if (Input.GetKeyDown(KeyCode.Mouse0))
        {
            Debug.Log("Sword Primary attack");
        }
    }

    private void AxeControls(PlayerWeapons currWeapon)
    {
        if (Input.GetKeyDown(KeyCode.Mouse0))
        {
            Debug.Log("Axe Primary attack");
        }
    }
    
    private void BowControls(PlayerWeapons currWeapon)
    {
        if (Input.GetKeyDown(KeyCode.Mouse0))
        {
            Debug.Log("Bow Primary attack");
        }
    }
    
    public void PlayerInputs(PlayerWeapons currWeapon)
    {
        //Debug.Log(currWeapon);
        if (currWeapon.ID == 1)
            SwordControls(currWeapon);
        else if(currWeapon.ID == 2)
            AxeControls(currWeapon);
        else if (currWeapon.ID == 3)
            BowControls(currWeapon);
    }
}
