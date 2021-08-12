using UnityEngine;

namespace Assets.ScriptFolder.Enemies
{
    public class WalkingTreeAttack : MonoBehaviour
    {
        public GameObject player;
        public GameObject WalkingTreeIdleRange;
        public GameObject WalkingTreeChasingRange;
    
        public float chaseSpeed;

        public Canvas healthBar;

        public int AnimationID;
        
        private EnemyDetection _enemyDetectionIdle;
        private EnemyDetection _enemyDetectionChase;

        private bool isIdleInRange;
        private bool isChaseInRange;
        private bool canChasePlayer;
        private bool readyToChase;
        private bool fullySettled;

        private int dir;

        private float readyUpTime;
        private float readyUpTimeTracker;
        private float readyDownTimeTracker;
        // Start is called before the first frame update
        void Start()
        {
            dir = 1;
            readyUpTime = 1;
            AnimationID = 1;
            readyDownTimeTracker = 0f;
            fullySettled = true;
            _enemyDetectionIdle = WalkingTreeIdleRange.GetComponent<EnemyDetection>();
            _enemyDetectionChase = WalkingTreeChasingRange.GetComponent<EnemyDetection>();
        }

        // Update is called once per frame
        void Update()
        {
            isIdleInRange = _enemyDetectionIdle.IsPlayerInRange();
            isChaseInRange = _enemyDetectionChase.IsPlayerInRange();
            
            DetectPlayer();
            ChasePlayer();
            SettleDown();
        }
        
        private void SettleDown()
        {
            if (!isChaseInRange && !fullySettled)
            {
                AnimationID = 4;
                
                if (readyDownTimeTracker <= readyUpTime)
                {
                    readyDownTimeTracker += Time.deltaTime;
                }
                else
                {
                    //readyUpTime = 0f;
                    fullySettled = true;
                    AnimationID = 1;
                    readyDownTimeTracker = 0f;
                }
            }
        }
        
        private void DetectPlayer()
        {
            if (isIdleInRange)
                canChasePlayer = true;
            if (!isChaseInRange)
            {
                canChasePlayer = false;
                readyToChase = false;
            }

            StandUp();
        }

        private void ChasePlayer()
        {
            if (readyToChase)
            {
                AnimationID = 3;
                TurnAround();
                transform.Translate(Vector3.right * (chaseSpeed * Time.deltaTime));
                fullySettled = false;
            }
        }

        private void TurnAround()
        {
            if (player.transform.position.x > transform.position.x)
            {
                transform.localRotation = Quaternion.Euler(0, 0, 0);
                healthBar.transform.rotation = Quaternion.Euler(0,0,0);
            }
            else
            {
                transform.localRotation = Quaternion.Euler(0, 180, 0);
                healthBar.transform.rotation = Quaternion.Euler(0,0,0);
            }
        }

        private void StandUp()
        {
            if (canChasePlayer && !readyToChase)
            {
                AnimationID = 2;
                readyUpTimeTracker += Time.deltaTime;
            }
            if (readyUpTimeTracker >= readyUpTime)
            {
                AnimationID = 3;
                readyToChase = true;
                readyUpTimeTracker = 0;
            }
        
        }
    }
}
