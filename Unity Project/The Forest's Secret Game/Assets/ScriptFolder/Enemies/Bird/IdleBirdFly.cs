using UnityEngine;

namespace Assets.ScriptFolder.Enemies.Bird
{
    public class IdleBirdFly : MonoBehaviour
    {
        public GameObject InfestedBirdAttackRange;
    
        public float birdIdleMovSpeed;

        public LayerMask wallCoalitionDetector;

        public Transform birbBeak;

        public Canvas healthBar;
        private EnemyDetection _enemyDetection;

        private EnemyDetection _enemyCloseDetection;
        private EnemyDetection _enemyAttackDetection;
        private BirdAttackMoves _birdAttackMoves;

        private bool isCloseRange;
        private bool isChaseRange;
        private bool canChasePlayer;

        private int dir;
        // Start is called before the first frame update
        void Start()
        {
            dir = 1;
            _enemyCloseDetection = GetComponent<EnemyDetection>();
            _enemyAttackDetection = InfestedBirdAttackRange.GetComponent<EnemyDetection>();
        
            _birdAttackMoves = GetComponentInChildren<BirdAttackMoves>();
        }

        // Update is called once per frame
        void Update()
        {
            isCloseRange = _enemyCloseDetection.IsPlayerInRange();
            isChaseRange = _enemyAttackDetection.IsPlayerInRange();
            DetectPlayer();
            if (!(canChasePlayer) && _birdAttackMoves.IsFullyReseted())
            {
                BirbMoving();
                TurnAround();
                _birdAttackMoves.ResetingNewPoint(new Vector2(transform.position.x, transform.position.y));
            }
        }

        private void BirbMoving()
        {
            transform.Translate(Vector3.right * (birdIdleMovSpeed * Time.deltaTime));
        }

        private void TurnAround()
        {
            RaycastHit2D coalitionDetected = Physics2D.Raycast(birbBeak.position, birbBeak.right,
                1, wallCoalitionDetector.value);
        
            if (coalitionDetected.collider != null)
            {
                if (dir == 1)
                {
                    transform.localRotation = Quaternion.Euler(0, 180, 0);
                    healthBar.transform.rotation = Quaternion.Euler(0,0,0);
                    dir = -1;
                }
                else
                {
                    transform.localRotation = Quaternion.Euler(0, 0, 0);
                    healthBar.transform.rotation = Quaternion.Euler(0,0,0);
                    dir = 1;
                }
            }
        }
    
        private void DetectPlayer()
        {
            if (isCloseRange)
                canChasePlayer = true;
            if (!isChaseRange)
            {
                canChasePlayer = false;
            }
        }
    }
}
