using UnityEngine;

namespace Assets.ScriptFolder.PlayerScripts.Inventory.Items
{
    public class Items : MonoBehaviour
    {
        // public SpriteRender itemSprite;
        public int counts;
        // Items List
        // 1. Potions
        // ---- Health Potion
        // ---- Stamina Potion
        // ---- Shield Potion
        // 2. Rope
    
    
        // Start is called before the first frame update
        void Start()
        {
        
        }

        // Update is called once per frame
        void Update()
        {
        
        }

        public void Print()
        {
            Debug.Log("YO WHAT Up");
        }

        private void DisplayItems()
        {
        
        }

        public void PlayerInput()
        {
            if (Input.GetKeyDown(KeyCode.Mouse0))
            {
                if (counts > 0)
                    counts -= 1;
                Debug.Log(counts);
            }
        }
    }
}
