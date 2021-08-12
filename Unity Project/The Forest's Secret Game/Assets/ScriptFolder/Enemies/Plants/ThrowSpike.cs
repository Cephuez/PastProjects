using UnityEngine;

namespace Assets.ScriptFolder.Enemies.Plants
{
	public class ThrowSpike : MonoBehaviour
	{
		public GameObject player;
		public GameObject spike;
		public GameObject plant;
		public GameObject spawnPoint;
		public GameObject SpikePlantCloseRange;
		public GameObject SpikePlantAttackRange;

		public int AnimationID;
	
		public float fireRate;

		private EnemyDetection _enemyCloseRange;
		private EnemyDetection _enemyAttackRange;
	
		private bool isCloseRange;
		private bool isAttackRange;
		private bool canAttackPlayer;
		private bool settingUp;
		private bool settingDown;
		private bool allSetUp;
		private bool allSetDown;
	
		private float fireCd;
		private float readyTimeTracker;
		private float readyTimer;
		private float readyDownTimeTracker;
		private float readyDownTimer;
	
		// Use this for initialization
		void Start ()
		{
			allSetDown = true;
			allSetUp = false;
			readyTimeTracker = 0f;
			readyTimer = 0.5f;
			readyDownTimeTracker = 0f;
			readyDownTimer = 0.5f;
			AnimationID = 1;
			_enemyCloseRange = SpikePlantCloseRange.GetComponent<EnemyDetection>();
			_enemyAttackRange = SpikePlantAttackRange.GetComponent<EnemyDetection>();
			fireCd = fireRate;
		}
	
		// Update is called once per frame
		void Update ()
		{
			DetectPlayer();
			isCloseRange = _enemyCloseRange.IsPlayerInRange();
			isAttackRange = _enemyAttackRange.IsPlayerInRange();

			if (settingUp)
			{
				AnimationID = 2;
				ReadyUpPlant();
			}

			if (settingDown)
			{
				AnimationID = 4;
				SetDownPlant();
			}
			
			if (isAttackRange && allSetDown)
			{
				if (allSetUp)
				{
					AnimationID = 3;
					if (fireCd < fireRate)
						fireCd += Time.deltaTime;
					plantShoots();
				}
				else
				{
					settingUp = true;
				}
			}
			else if(!isAttackRange && allSetUp)
			{
				allSetUp = false;
				allSetDown = false;
				settingDown = true;
				settingUp = false;
			}
		}

		private void SetDownPlant()
		{
			readyDownTimeTracker += Time.deltaTime;
			if (readyDownTimeTracker >= readyDownTimer)
			{
				allSetDown = true;
				settingDown = false;
				readyDownTimeTracker = 0f;
				AnimationID = 1;
			}
		}
		private void ReadyUpPlant()
		{
			readyTimeTracker += Time.deltaTime;
			if (readyTimeTracker >= readyTimer)
			{
				allSetUp = true;
				settingUp = false;
				readyTimeTracker = 0f;
			}
			
		}
		private void plantShoots()
		{
			if (canAttackPlayer)
			{
				if (CanShoot())
				{
					CalculateAngle();
					GameObject spikeCopy = Instantiate(spike,spawnPoint.transform.position,spawnPoint.transform.rotation);

					fireCd = 0f;
				}
			}
		}

		private void CalculateAngle()
		{
			Vector2 lookDir = player.transform.position - spawnPoint.transform.position;
			float angle = Mathf.Atan2(lookDir.y, lookDir.x) * Mathf.Rad2Deg;
			spawnPoint.transform.rotation = Quaternion.Euler(0,0,angle);
		}

		private bool CanShoot()
		{
			return fireCd >= fireRate;
		}
	
		private void DetectPlayer()
		{
			if (isCloseRange)
				canAttackPlayer = true;
			if (!isAttackRange)
			{
				canAttackPlayer = false;
			}
		}
	}
}
