using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Tilemaps;

public class ChangablePortableTiles : MonoBehaviour
{
    public Enemy enemy;
    public List<GameObject> tileMapList = new List<GameObject>();
    public List<GameObject> tileMapCoverList = new List<GameObject>();
    public List<GameObject> PhaseDoorsList = new List<GameObject>();

    public AudioSource phaseTwoSound;
    public AudioSource phaseThreeSound;

    private bool isTilesSet = false;
    private bool isFirstPhase = false;
    private bool isSecondPhase = false;
    private bool isThirdPhase = false;

    public PortalManager portalManager;

    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
        {
        if (!isTilesSet)
        {
            //togglePortable(tileMapList[0]);
            //togglePortable(tileMapList[2]);
            isTilesSet = true;
        }

        if (enemy.health >= 77 && !isFirstPhase && portalManager)
        {
            togglePortable(tileMapList[0], 0);
            isFirstPhase = true;
            // Debug.Log("Entered first phase of Manny");
        }

        if (enemy.health <= 76 && !isSecondPhase)
        {
            switchPortableTiles(0, 1);
            isSecondPhase = true;
            if (PhaseDoorsList[0] != null)
            {
                PhaseDoorsList[0].SetActive(false);
            }

            AudioSource edSound = Instantiate<AudioSource>(phaseTwoSound);
            edSound.Play();
            Destroy(edSound, 2.25f);
            // Debug.Log("Entered second phase of Manny");
        }

        if (enemy.health <= 39 && !isThirdPhase)
        {
            switchPortableTiles(1, 2);
            isThirdPhase = true;
            if (PhaseDoorsList[0] != null)
            {
                PhaseDoorsList[1].SetActive(false);
            }

            AudioSource edSound = Instantiate<AudioSource>(phaseThreeSound);
            edSound.Play();
            Destroy(edSound, 2.25f);
            // Debug.Log("Entered third phase of Manny");
        }
    }// end update

    public void switchPortableTiles(int oldPortable, int newPortable)
    {
        togglePortable(tileMapList[oldPortable], oldPortable);
        togglePortable(tileMapList[newPortable], newPortable);
    }

    public void togglePortable(GameObject aTileMap, int index)
    {
        // AllowsPortal allowsPortals = aTileMap.GetComponent<AllowsPortal>(); 

        TilemapCollider2D allowsPortals = aTileMap.GetComponent<TilemapCollider2D>();

        allowsPortals.enabled = !allowsPortals.enabled;

        if (allowsPortals.enabled)
        {
            /*
            for (int i = 0; i < tileMaps.Count; i++)
            {
                Sprite sprite = Resources.Load<Sprite>("EnvironmentSprites/Background/Wall_Portal_Zone_Fixed");
                tileMaps[0].sprite = sprite;
                  //  Sprite sprite = ((SwitchableTile)tile).GetNextSprite();
                //((SwitchableTile)tile).sprite = sprite;
            }
            */
            tileMapCoverList[index].SetActive(false);
        }
        else
        {
            tileMapCoverList[index].SetActive(true);
        }
        portalManager.UpdatePortals();
        
    }


}
