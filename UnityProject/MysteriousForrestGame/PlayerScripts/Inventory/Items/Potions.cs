using UnityEngine;

namespace Assets.ScriptFolder.PlayerScripts.Inventory.Items
{
    public class Potions : Items
    {
        public int inventoryID;
        public Sprite spriteImage;

        // Start is called before the first frame update
        void Start()
        {

        }

        // Update is called once per frame
        void Update()
        {
            Print();
        }

        private int PotionStats()
        {
            if (inventoryID == 0)
                return 50;
            else if (inventoryID == 1)
                return 1;
            else
                return 25;
        }
    }
}

