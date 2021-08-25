using System;
using UnityEngine;
using UnityEngine.SceneManagement;

namespace Assets.ScriptFolder
{
    public class StartUpGame : MonoBehaviour
    {
        // Start is called before the first frame update
        void Start()
        {
        
        }

        // Update is called once per frame
        void Update()
        {
        
        }

        public void StartNewGame(String sceneName)
        {
            SceneManager.LoadScene(sceneName);
            // 1. Will Load Up New Game
            // 2. Reset All Save Game file from Serialization
        }

        public void StartSavedGame(String sceneName)
        {
            SceneManager.LoadScene(sceneName);
            // 1. Will load up a saved game
            // 2. Will run code to load up the progress of the player
        }

        public void ExitGame()
        {
            Application.Quit();
        }
    }
}
