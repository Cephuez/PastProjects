using System.Collections;
using System.Collections.Generic;
using Assets.ScriptFolder.PlayerScripts.Inventory;
using Assets.ScriptFolder.PlayerScripts.Inventory.Items;
using Microsoft.Unity.VisualStudio.Editor;
using UnityEngine;
using Image = UnityEngine.UI.Image;

public class ItemInventorySlot : MonoBehaviour
{
    public Image[] imageList;
    private Items item;
    private PlayerInventory _PlayerInventory;
   // private Sprite itemSprite;
    // Start is called before the first frame update
    private Image backgroundImage;
    private Image itemImage;
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public Image GetBackgroundImage()
    {
        return backgroundImage;
    }

    public Image GetItemImage()
    {
        return itemImage;
    }
    public void SetItem(Items item)
    {
        this.item = item;
        Potions potionRef = (Potions) item;
        //itemSprite = potionRef.spriteImage;
    }

    public bool IsEmpty()
    {
        return item == null;
    }

    public Items getItem()
    {
        return item;
    }

    public Sprite GetItemSprite()
    {
        return ((Potions) item).spriteImage;
    }
    public void SetNewCurrItem()
    {
        _PlayerInventory.ChangeCurrItem(item);
    }

    public void SetInventoryReference(PlayerInventory playerInventory)
    {
        _PlayerInventory = playerInventory;
    }

    public void ItemPressed()
    {
        Debug.Log(item);
    }
}
