using System;
using Assets.ScriptFolder.PlayerScripts.Inventory;
using Assets.ScriptFolder.PlayerScripts.Inventory.PlayerWeapons;
using UnityEngine;
using UnityEngine.UI;

namespace Assets.ScriptFolder.PlayerScripts
{
    public class PlayerStats : Being
    {
        public float shield;
        public float stamina;
        public float regainStaminaSpeed;

        public Slider healthSlider;
        public Slider shieldSlider;
        public Slider staminaSlider;

        private PlayerInventory _playerInventory;

        private int weaponID;
        private int damage;

        // Start is called before the first frame update
        void Start()
        {
            _playerInventory = GetComponent<PlayerInventory>();

        }
        
        // Update is called once per frame
        void Update()
        {
            if (IsAlive())
            {
                PlayerStatusUiChanges();
                IncreaseStamina();
            }
            else
            {
                // End Game
                // Reset from last save point
                // Load everything else :o
            }
        }


        void OnCollisionEnter(Collision other)
        {
            Debug.Log(other.gameObject.layer);
        }

        private void PlayerStatusUiChanges()
        {
            healthSlider.value = health;
            shieldSlider.value = shield;
            staminaSlider.value = stamina;
        }

        private bool HasStamina()
        {
            return stamina > 0;
        }

        private bool HasShield()
        {
            return shield > 0;
        }

        public void IncreaseHealth(float health)
        {
            this.health += health;
            if (this.health > 100)
                health = 100;
        }

        public void IncreaseShield(float shield)
        {
            this.shield += shield;
            if (this.shield > 50)
                this.shield = 50;
        }

        private void IncreaseStamina()
        {
            if (stamina < 200)
            {
                stamina += regainStaminaSpeed * Time.deltaTime;
            }

            if (stamina > 200)
                stamina = 200;
        }
    }
}
