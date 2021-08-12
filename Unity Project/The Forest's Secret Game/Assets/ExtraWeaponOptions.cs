using System.Collections;
using System.Collections.Generic;
using Assets.ScriptFolder.PlayerScripts.Inventory.PlayerWeapons;
using UnityEngine;

public class ExtraWeaponOptions : MonoBehaviour
{
    private bool activate = true;
    private PlayerWeapons currWeaponChosen;
    public SubWeaponDisplay[] ExtraWeaponChoices;
    public GameObject[] ExtraChoices;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public PlayerWeapons DisplayOptions(GameObject extraOptionsCanvas, PlayerWeapons currWeapon)
    {
        currWeaponChosen = currWeapon;
        DisplayVisualOptions(extraOptionsCanvas, currWeapon);
        UpdateWeaponChoices();
        return currWeaponChosen;
    }

    private void DisplayVisualOptions(GameObject extraOptionsCanvas, PlayerWeapons currWeapon)
    {
        //if (Input.GetKeyDown(KeyCode.Q))
        if (Input.GetKeyDown(KeyCode.Mouse2))
        {
            extraOptionsCanvas.SetActive(activate);
            showNecessaryOptions(currWeapon);
            activate = !activate;
        }
    }

    private void showNecessaryOptions(PlayerWeapons currWeapon)
    {
        if (currWeapon.ID == 1)
        {
            currWeapon.ShowChoices();
        }
    }
    public void PickExtraOption(int ID)
    {
        currWeaponChosen.UpdateExtraChoice(ExtraWeaponChoices[ID-1]);
    }
    
    private void UpdateWeaponChoices()
    {
        if (currWeaponChosen.ID == 1)
        {
            DisplayExtraSwords();
        }else if (currWeaponChosen.ID == 2)
        {
            DisplayExtraAxe();
        }else if (currWeaponChosen.ID == 3)
        {
            DisplayExtraBow();
        }
    }
    
    private void DisplayExtraSwords()
    {
        if (Input.GetKeyDown(KeyCode.Q))
        {
            Debug.Log("Display Sword Choices XD");
        }
    }

    private void DisplayExtraAxe()
    {
        if (Input.GetKeyDown(KeyCode.Q))
        {
            Debug.Log("Display Axe Choices XD");
        }
    }

    private void DisplayExtraBow()
    {
        if (Input.GetKeyDown(KeyCode.Q))
        {
            Debug.Log("Display Arrow Choices XD");
        }
    }
}
