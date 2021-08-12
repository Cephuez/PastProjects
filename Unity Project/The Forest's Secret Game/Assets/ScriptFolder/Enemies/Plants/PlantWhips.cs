using UnityEngine;

namespace Assets.ScriptFolder.Enemies.Plants
{
	public class PlantWhips : Enemy
	{
		public float distanceApartX;
	
		public GameObject WhipLeaf;
		public GameObject player;
		public GameObject WhipPlantCloseRange;
		public GameObject WhipPlantAttackRange;
		public int WhipsPerSide;

		private bool playerInRange;

		private EnemyDetection _enemyCloseDetection;
		private EnemyDetection _enemyAttackDetection;
		private PlantWhipAttack[] whipList;
		private PlantWhipAttack _plantWhipAttack;

		private bool isCloseRange;
		private bool isAttackRange;
		private bool canAttackPlayer;

		private int whipCount;
	
		// Use this for initialization
		void Start ()
		{
			whipCount = WhipsPerSide * 2;
			_enemyCloseDetection = WhipPlantCloseRange.GetComponent<EnemyDetection>();
			_enemyAttackDetection = WhipPlantAttackRange.GetComponent<EnemyDetection>();
		
			playerInRange = GetComponent<EnemyDetection>().IsPlayerInRange();
			whipList = new PlantWhipAttack[whipCount];
			GenerateWhipPositions();
		}
	
		// Update is called once per frame
		void Update () {
		
			DetectPlayer();
			isCloseRange = _enemyCloseDetection.IsPlayerInRange();
			isAttackRange = _enemyAttackDetection.IsPlayerInRange();
			WhipsSlash();
		}

		private void GenerateWhipPositions()
		{
			float xPos = transform.position.x;

			for (int i = 0; i < WhipsPerSide; i++)
			{
				float leftPos = xPos - (distanceApartX + distanceApartX * i); 
				float rightPos = xPos + (distanceApartX + distanceApartX * i);

				PlantWhipAttack whip1 = Instantiate(WhipLeaf, transform).GetComponent<PlantWhipAttack>();
				whip1.SetXCoordinates(leftPos);
				whip1.SetPlayer(player);
			
				PlantWhipAttack whip2 = Instantiate(WhipLeaf, transform).GetComponent<PlantWhipAttack>();
				whip2.SetXCoordinates(rightPos);
				whip2.SetPlayer(player);

				whipList[i*2] = whip1;
				whipList[i*2 + 1] = whip2;
			}

			//_plantWhipAttack = whipList[0];
		}
		private void WhipsSlash()
		{
			if (canAttackPlayer)
			{
				for (int i = 0; i < whipList.Length; i++)
					whipList[i].AlertWhips();
			
			}
			else
			{
				whipList[0].NoLongerAlerted();
				for (int i = 0; i < whipList.Length; i++)
					whipList[i].NoLongerAlerted();
			}
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

		public int GetAnimationID()
		{
			return _plantWhipAttack.AnimationID;
		}
	}
}
