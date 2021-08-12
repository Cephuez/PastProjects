using System;
using System.Collections.Generic;
using System.Linq;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace Assets.ScriptFolder.PlayerScripts.Inventory
{
    public class PlayerInventory : MonoBehaviour
    {
        public PlayerWeaponControllers controllers;
        public ExtraWeaponOptions ExtraWeaponOptions;
        public Items.Items healthPotion;
        public Items.Items shieldPotion;
        
        public GameObject InventoryItemList;

        public PlayerWeapons.PlayerWeapons[] playerWeapons;
        public GameObject itemEquippedSprite;
        public SpriteRenderer potionSprite;

        private List<Items.Items> itemList;
        private List<ItemInventorySlot> iventorySlots;
        private List<GameObject> inventoryGameObjectSlots;
        private PlayerWeapons.PlayerWeapons currWeapon;
        public Items.Items currItem;
        private Canvas inGameCanvas;
        private Canvas pauseCanvas;
        private GameObject PauseCanvasObject;
        private GameObject darkenBackground;
        private GameObject ExtraOptionsCanvas;

        private bool paused;
        private bool itemEquiped;
        // Start is called before the first frame update
        void Start()
        {
            SetUpReferences();
            itemList = new List<Items.Items> {healthPotion, shieldPotion};
            inventoryGameObjectSlots = new List<GameObject>();
            iventorySlots = new List<ItemInventorySlot>();
            currWeapon = playerWeapons[0];
            SetItemInventorySlots();
            ChangeOptions();
            
        }

        private void SetUpReferences()
        {
            PauseCanvasObject = PauseMenuReference.PauseMenuUI.gameObject;
            inGameCanvas = InGameUIReference.InGameUI.GetComponent<Canvas>();
            darkenBackground = PanelReference.Panel.gameObject;
            ExtraOptionsCanvas = ItemDisplayReference.ItemDisplay.gameObject;
            InventoryItemList = ItemMenuReference.ItemMenu.gameObject;
            controllers = GetComponentInChildren<PlayerWeaponControllers>();
            
            PauseCanvasObject.SetActive(false);
            darkenBackground.SetActive(false);
            ExtraOptionsCanvas.SetActive(false);
        }
        void Update()
        {
            SwitchWeapons();
            OpenInventory();
            InputActions();
        }
        
        
        private void InputActions()
        {
            // Will allow inputs if it's not paused
            if (Time.timeScale > 0)
            {
                if (!itemEquiped)
                {
                    // Controls for the three main weapons
                    //controllers.PlayerInputs(currWeapon);
                    currWeapon = ExtraWeaponOptions.DisplayOptions(ExtraOptionsCanvas, currWeapon);
                }
                else
                {
                    // Controls for the inventory option
                    currItem.PlayerInput();
                }
            }
        }
        public void ChangeCurrItem(Items.Items newCurrItem)
        {
            currItem = newCurrItem;
        }
        
        private void SetItemInventorySlots()
        {
            int length = 0;
            foreach (Transform child in InventoryItemList.transform)
            {
                inventoryGameObjectSlots.Add(child.gameObject);
                iventorySlots.Add(child.gameObject.GetComponent<ItemInventorySlot>());
            }
            //Debug.Log("Length of child is: " + iventorySlots.Count);
            iventorySlots[0].SetItem(healthPotion);
            iventorySlots[0].SetInventoryReference(this);
            iventorySlots[1].SetItem(shieldPotion);
            iventorySlots[1].SetInventoryReference(this);
        }
        private void SwitchWeapons()
        {
            if (Input.GetKeyDown("1"))
            {
                currWeapon = playerWeapons[0];
                //Debug.Log("Sword: " + currWeapon.damage + "SUB: " + currWeapon.currSubWeapon.id);
                itemEquiped = false;
                ChangeOptions();
            }

            if (Input.GetKeyDown("2"))
            {
                currWeapon = playerWeapons[1];
                //Debug.Log("Axe: " + currWeapon.damage + "SUB: " + currWeapon.currSubWeapon.id);
                itemEquiped = false;
                ChangeOptions();
            }

            if (Input.GetKeyDown("3"))
            {
                currWeapon = playerWeapons[2];
                //Debug.Log("Bow: " + currWeapon.damage + "SUB: " + currWeapon.currSubWeapon.id);
                itemEquiped = false;
                ChangeOptions();
            }

            if (Input.GetKeyDown("4"))
            {
                itemEquiped = true;
            }
        }

        private void ChangeOptions()
        {
            SubWeaponDisplay[] allChoices = ExtraWeaponOptions.ExtraWeaponChoices;
            GameObject[] allChoicesReferences = ExtraWeaponOptions.ExtraChoices;

            for (int i = 0; i < allChoices.Length; i++)
            {
                allChoices[i].SetOption(currWeapon.extraChoices[i]);
            }
            
            for (int i = 0; i < allChoices.Length; i++)
            {
                if (!allChoices[i].CanBeEnabled())
                    allChoicesReferences[i].SetActive(false);
                else
                    allChoicesReferences[i].SetActive(true);
            }
        }
        private void OpenInventory()
        {
            if (Input.GetKeyDown(KeyCode.Escape))
            {
                if (!paused)
                {
                    PauseCanvasObject.SetActive(true);
                    darkenBackground.SetActive(true);
                    DisplayInventoryWithItem();
                    Time.timeScale = 0f;
                }
                else
                {
                    PauseCanvasObject.SetActive(false);
                    darkenBackground.SetActive(false);
                    Time.timeScale = 1f;
                }

                paused = !paused;
            }
        }

        // OnClick() will update the weapon chosen from the inventory
        public void ChangeCurrWeapon(PlayerWeapons.PlayerWeapons nextWeapon)
        {
            currWeapon = nextWeapon;
            //Debug.Log(currWeapon);
            ChangeOptions();
        }
        
        // OnClick() Will update the selected subWeapon from the inventory to the correct weapon
        public void UpdateSubWeapon(SubWeapon newSubWeapon)
        {
            playerWeapons[newSubWeapon.MainID - 1].UpdateNewSubWeapon(newSubWeapon);
        }
        // Update is called once per frame

        private void DisplayInventoryWithItem()
        {
            for (int i = 0; i < iventorySlots.Count; i++)
            {
                if(iventorySlots[i].IsEmpty())
                    inventoryGameObjectSlots[i].SetActive(false);
                else
                {    
                    // Image of the slot
                    // Check on this later
                    Image slotImage = iventorySlots[i].imageList[1];
                    Sprite spriteImage = iventorySlots[i].GetItemSprite();
                    if (slotImage != null)
                    {
                        slotImage.sprite = spriteImage;
                    }
                }
            }
        }
    }
}
