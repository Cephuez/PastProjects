using UnityEngine;

namespace Assets.ScriptFolder.Enemies.Turtle
{
    public class GiantTurtleAttack : MonoBehaviour
    {
        public GameObject player;

        public float chaseSpeed;

        public int AnimationID;
    
        private EnemyDetection _enemyDetection;
        private IdleWalk _idleWalk;

        // Start is called before the first frame update
        void Start()
        {
            _enemyDetection = GetComponentInChildren<EnemyDetection>();
            _idleWalk = GetComponent<IdleWalk>();
        }

        // Update is called once per frame
        void Update()
        {
            if (_enemyDetection.IsPlayerInRange())
            {
                ChasePlayer();
                _idleWalk.ChangeSpeed(chaseSpeed);
                AnimationID = 2;
            }
            else
            {
                _idleWalk.ResumeSpeed();
                AnimationID = 1;
            }
        }

        private void ChasePlayer()
        {
            // Turtle will turn around to look at player
            if (player.transform.position.x <= transform.position.x && _idleWalk.GetDir() != -1
                || player.transform.position.x > transform.position.x && _idleWalk.GetDir() != 1)
                _idleWalk.ChangeDir(); 
          
        }
    
        // 1. If player is near range, the turtle will speed up towards target - X 
        // 2. If player is near mouth range, turtle will snap at the target.
        // 3. It will rotate around if the player is trying to go from behind. - X
    }
}
