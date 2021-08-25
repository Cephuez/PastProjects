using UnityEngine;

namespace Assets.ScriptFolder.PlayerScripts
{
    public class CameraOnPlayer : MonoBehaviour
    {
        public GameObject Player;

        public float posYAbovePlayer;
    
        // Start is called before the first frame update
        void Start()
        {
        
        }

        // Update is called once per frame
        void Update()
        {
            FollowPlayer();
        }

        private void FollowPlayer()
        {
            transform.position = new Vector3(Player.transform.position.x,Player.transform.position.y +posYAbovePlayer,-1);
        }
        
    }
}
