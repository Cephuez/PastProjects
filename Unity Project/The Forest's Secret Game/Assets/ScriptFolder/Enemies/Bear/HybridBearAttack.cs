using UnityEngine;

namespace Assets.ScriptFolder.Enemies.Bear
{
    public class HybridBearAttack : MonoBehaviour
    {
        public GameObject player;
        public GameObject HybridBearCloseRange;
        public GameObject HybridBearChaseRange;
    
        public float walkSpeed;
        public float stalkSpeed;
        public float chaseSpeed;
        public int AnimationID;

        private EnemyDetection _enemyDetectionClose;
        private EnemyDetection _enemyDetectionChase;
        private IdleWalk _idleWalk;
    
        private bool isStalkRange;
        private bool isChaseRange;

        private int dir;
        private int phase;

        private float pauseTime;
        private float pauseTimeTracker;

        // Start is called before the first frame update
        void Start()
        {
            AnimationID = 1;
            phase = 1;
            pauseTime = 2;
            _enemyDetectionClose = HybridBearCloseRange.GetComponent<EnemyDetection>();
            _enemyDetectionChase = HybridBearChaseRange.GetComponent<EnemyDetection>();
            _idleWalk = GetComponent<IdleWalk>();
        }

        // Update is called once per frame
        void Update()
        {
        
            isChaseRange = _enemyDetectionClose.IsPlayerInRange();
            isStalkRange = _enemyDetectionChase.IsPlayerInRange();
            ChasePlayer();
        }
    
        private void ChasePlayer()
        {
            if (isStalkRange)
                AttackSequence();
            else
                ResumeBearWalk();
        }

        private void ResumeBearWalk()
        {
            _idleWalk.ResumeSpeed();
            phase = 1;
            pauseTimeTracker = 0;
            AnimationID = 1;
        }
        // 1. Pause for a while
        // 2. Walk slowly towards target
        // 3. Rush at player at full speed
        // 4. If bear makes contact, starts to phase 1
        private void AttackSequence()
        {
            AttackPhase1();
            AttackPhase2();
            AttackPhase3();
            AttackPhase4();
        }

        private void AttackPhase1()
        {
            if (phase == 1)
            {
                AnimationID = 2;
                TurnAround();
                _idleWalk.ChangeSpeed(0);
                pauseTimeTracker += Time.deltaTime;
                if (pauseTimeTracker >= pauseTime)
                {
                    phase = 2;
                    pauseTimeTracker = 0;
                }
            }
        }
    
        private void AttackPhase2()
        {
            if (phase == 2)
            {
                AnimationID = 3;
                TurnAround();
                _idleWalk.ChangeSpeed(stalkSpeed);
                if (isChaseRange)
                    phase = 3;
            }
        }
    
        private void AttackPhase3()
        {
            if (phase == 3)
            {
                TurnAround();
                _idleWalk.ChangeSpeed(chaseSpeed);
            }
        }
    
        // Will be saved for later when dealing with player colliding with enemy.
        private void AttackPhase4()
        {
            if (phase == 4)
            {
                phase = 1;
            }
        }
    
        private void TurnAround()
        {
            if (player.transform.position.x <= transform.position.x && _idleWalk.GetDir() != -1
                || player.transform.position.x > transform.position.x && _idleWalk.GetDir() != 1)
                _idleWalk.ChangeDir(); 
        }
    }
}
