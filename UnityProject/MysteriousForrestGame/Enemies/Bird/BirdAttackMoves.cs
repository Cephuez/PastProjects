using UnityEngine;

namespace Assets.ScriptFolder.Enemies.Bird
{
    public class BirdAttackMoves : MonoBehaviour
    {
        public GameObject player;
        public GameObject PlayerTargetLoc;
        public GameObject InfestedBirdCloseRange;
        public GameObject InfestedBirdAttackRange;

        public float resetTime;

        private EnemyDetection _enemyDetection;
        private EnemyDetection _enemyCloseDetection;
        private EnemyDetection _enemyAttackDetection;
    
        private Rigidbody2D _body;

        private float attackResetTimeTracker;
        private float currHighestHeight;
        private float resetHeight;
        private float birbAttackSpeed;
        private float playerPosX;
        private float playerPosY;
        private float posxTime;
        private float posyTime;

        private int phase;
        public int AnimationID;
    
        private bool fullyReseted;
        private bool playerPosFound;
        private bool isLeftSide;
        private bool isUpSide;
        private bool posXReached;
        private bool posYReached;
        private bool isCloseRange;
        private bool isChaseRange;
        private bool canChasePlayer;

        private GameObject refPlayerTargetLoc;

        private Vector2 target;
        private Vector2 resetPoint;
        private Vector2 newPoint;
    
        // Start is called before the first frame update
        void Start()
        {
            AnimationID = 1;
            attackResetTimeTracker = 0;
            currHighestHeight = transform.position.y + 1f;
            resetHeight = transform.position.y;
            birbAttackSpeed = 10;
            phase = 1;
            fullyReseted = true;
            _enemyCloseDetection = InfestedBirdCloseRange.GetComponent<EnemyDetection>();
            _enemyAttackDetection = InfestedBirdAttackRange.GetComponent<EnemyDetection>();
            _body = GetComponent<Rigidbody2D>();
            resetPoint = new Vector2(transform.position.x, transform.position.y);
        }

        // Update is called once per frame
        void Update()
        {
            isCloseRange = _enemyCloseDetection.IsPlayerInRange();
            isChaseRange = _enemyAttackDetection.IsPlayerInRange();

            DetectPlayer();

            if (canChasePlayer || phase != 1)
            {
                AnimationID = 2;
                fullyReseted = false;
                _body.gravityScale = 0;
                _body.velocity = new Vector2(_body.velocity.x,0);
                AttackPhase1();
                // Can't end action as soon as it's in phase 2 and everything after
                AttackPhase2();
                AttackPhase3();
                ResetPhase4();
            }    
            else
            {
                ResetBirb();
            }
        }

        private void ResetBirb()
        {
            if (!fullyReseted && Vector2.Distance(transform.position, resetPoint) > 0.1f)
                transform.position = Vector2.MoveTowards(transform.position, resetPoint, 0.005f);
            else
            {
                fullyReseted = true;
                AnimationID = 1;
            }

            attackResetTimeTracker = 0;
            phase = 1;
        }
        // Bird is flying a little bit high to indicate it will attack the player
        private void AttackPhase1()
        {
            if (phase == 1 || phase == 5)
                attackResetTimeTracker += Time.deltaTime;
            if(phase == 1 && transform.position.y <= currHighestHeight)
                transform.position = new Vector3(transform.position.x,transform.position.y + 0.50f * Time.deltaTime);
            else if(phase == 1 && transform.position.y >= currHighestHeight)
                phase = 2;
        }

        // Bird Flies at the target
        private void AttackPhase2()
        {
            // Calculate player's position where it was first spotted 
            if (phase == 2)
            {
                if (!playerPosFound)
                {
                    // Instantiate object here
                    target = new Vector2(player.transform.position.x, player.transform.position.y);
                    refPlayerTargetLoc = Instantiate(PlayerTargetLoc);
                    refPlayerTargetLoc.transform.position = new Vector3(target.x,target.y);
                    playerPosFound = true;
                } 
                transform.position = Vector2.MoveTowards(transform.position, target, 0.05f);
            }
        }

        // Bird flies to its new fly point
        private void AttackPhase3()
        {
            if (phase == 3)
            {
                Destroy(refPlayerTargetLoc);
                if (newPoint.x != transform.position.x && newPoint.y != currHighestHeight)
                    newPoint = new Vector2(transform.position.x, resetHeight);

                transform.position = Vector2.MoveTowards(transform.position, newPoint, 0.025f);

                if (Vector2.Distance(transform.position, newPoint) < 0.1f)
                    phase = 4;
            }
        }

        private void ResetPhase4()
        {
            if (phase == 4)
            {
                InfestedBirdCloseRange.transform.position = transform.position;
                InfestedBirdAttackRange.transform.localPosition = new Vector3(0,0);
                transform.position = InfestedBirdCloseRange.transform.position;
                attackResetTimeTracker = 0;
                phase = 1;
                playerPosFound = false;
                resetPoint = new Vector2(transform.position.x,transform.position.y);
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
    
        void OnTriggerEnter2D(Collider2D col)
        {
            // Going towards where the player was at first
            if (col.gameObject.layer == 14 && col.gameObject == refPlayerTargetLoc)
            {
                phase = 3;
            }
        }

        public bool IsFullyReseted()
        {
            return fullyReseted;
        
        }

        public void ResetingNewPoint(Vector2 newResetPoint)
        {
            resetPoint = newResetPoint;
        }
    }
}
