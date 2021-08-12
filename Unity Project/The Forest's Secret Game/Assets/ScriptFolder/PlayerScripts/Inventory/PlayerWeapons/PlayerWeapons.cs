using System.Collections.Generic;
using UnityEngine;

namespace Assets.ScriptFolder.PlayerScripts.Inventory.PlayerWeapons
{
    public class PlayerWeapons : MonoBehaviour
    {
        public SubWeapon[] extraChoices;
        public SubWeapon currSubWeapon;
        public float damage;
        public float fireRate;
        public int ID;

        private bool isEquipped;
        
        private SubWeaponDisplay subWeapon;
        private SubWeaponDisplay selectedChoice;


        // Start is called before the first frame update
        void Start()
        {
            
        }
    
        // Update is called once per frame
        void Update()
        {
           
        }

        public void UpdateExtraChoice(SubWeaponDisplay subWeapon)
        {
            selectedChoice = subWeapon;
            this.subWeapon = subWeapon;
            currSubWeapon = subWeapon.GetSubWeapon();
            Debug.Log(ID + ": Has been updated with option - " + subWeapon.ID);
        }

        public void UpdateNewSubWeapon(SubWeapon newSubWeapon)
        {
            currSubWeapon = newSubWeapon;
        }
        public void ShowChoices()
        {
            // 1. Need to get allSubWeapons with all the circles filled with their SubWeapons
            /*
            for (int i = 0; i < allSubWeapons.Length)
            {
                // Visits which ones are null and which ones are not
            }
            */
        }

        public SubWeaponDisplay[] UpdateChoices()
        {
            return null;
        }
    }
    
    
    
}
