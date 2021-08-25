using UnityEngine;

namespace Assets.ScriptFolder.Enemies.Plants
{
	public class PlantWhipAttack : MonoBehaviour
	{
		public float whipRate;
		public float whipReadyUpSpeed;
		public float whipHeight;
		public float loadUpDistanceX;
		public float attackDistanceX;
		public float loudUpSpeed;
		public float attackSpeed;
		public int AnimationID;

		public Rigidbody2D body;
	
		private float whipCd;
		private float maxWhipHeight;
		private float minWhipHeight;
		private float loadUp;
		private float pos1;
		private float pos2;
		private float pos3;
		private float xRef;
		private float time1;
		private float time2;
		private float phaseTimer;

		private int phase;
		private int dir;
	
		private bool alertMode;
		private bool plantInPosition;
		private bool rotateWhip;
		private bool canWhip;
		private bool stillAttacking;

		private GameObject player;
	
		// Use this for initialization
		void Start ()
		{
			phaseTimer = 0;
			AnimationID = 1;
			// x/y = time
			time1 = loadUpDistanceX / loudUpSpeed;
			time2 = ((loadUpDistanceX + attackDistanceX) / attackSpeed) + time1;
			rotateWhip = true;
			canWhip = true;
			whipCd = 0;
			maxWhipHeight = transform.position.y + whipHeight;
			minWhipHeight = transform.position.y;
		}
	
		// Update is called once per frame
		void Update ()
		{
			WhipReadyUp();
			WhipAttack();
			ResetWhipAttack();
		}

		private void WhipReadyUp()
		{
			if (alertMode && !stillAttacking)
			{
				SetWhipsInPositions();
				CalculateAngle();
			}
			else if(!alertMode && !stillAttacking)
			{
				ResetAngle();
				ResetWhipPosition();
			}

		}
		
			
		private void WhipAttack()
		{
			if (plantInPosition)
			{
				phaseTimer += Time.deltaTime;
				rotateWhip = false;
				stillAttacking = true;
				if (phase == 0)
				{
					transform.position += transform.up * Time.deltaTime * loudUpSpeed * -1;
					if (time1 <= phaseTimer)
						phase = 1;

				}else if (phase == 1)
				{
					transform.position += transform.up * Time.deltaTime * attackSpeed;
					if (time2 <= phaseTimer)
						phase = 2;
				}else if (phase == 2)
				{
					// Determine Direction of where to return to
					DetermineReturnDir();
					transform.position += transform.up * Time.deltaTime * attackSpeed * -1;
					if(transform.position.x >= xRef && dir == -1)
						phase = 3;
					else if (transform.position.x <= xRef && dir == 1)
						phase = 3;
				}
			}
		}
		
		private void ResetWhipAttack()
		{
			if (phase == 3 && whipCd <= whipRate)
			{
				if(!rotateWhip)
					transform.position = new Vector3(xRef,maxWhipHeight);
				whipCd += Time.deltaTime;
				rotateWhip = true;
				plantInPosition = false;
				stillAttacking = false;
				if (whipCd >= whipRate)
				{
					canWhip = true;
					whipCd = 0;
					phaseTimer = 0;
					dir = 0;
					phase = 0;
				}
			}
		}

		private void DetermineReturnDir()
		{
			if (dir == 0 && transform.position.x <= xRef)
				dir = -1;
			else if (dir == 0)
				dir = 1;
		}

		public GameObject AdjustPlantRange(GameObject plantRange)
		{
			plantRange.transform.position = new Vector3(transform.position.x,maxWhipHeight);
			return plantRange;
		}
	
		private void ResetWhipPosition()
		{
			if (transform.position.y >= minWhipHeight) 
				transform.position = new Vector3(transform.position.x, transform.position.y - Time.deltaTime * whipReadyUpSpeed);
		
		}
		private void SetWhipsInPositions()
		{
			// Move up
			if(transform.position.y <= maxWhipHeight && !plantInPosition){
				transform.position = new Vector3(transform.position.x, transform.position.y + Time.deltaTime * whipReadyUpSpeed);
			}
		
			if (transform.position.y >= maxWhipHeight && canWhip)
			{
				canWhip = false;
				plantInPosition = true;
				phase = 0;
			}
		}
	
		private void CalculateAngle()
		{
			if (rotateWhip)
			{
				Vector2 lookDir = player.transform.position - transform.position;
				float angle = Mathf.Atan2(lookDir.y, lookDir.x) * Mathf.Rad2Deg;
				transform.rotation = Quaternion.Euler(0, 0, angle - 90);
			}

			//currAngle = transform.rotation.z;
		}

		private void ResetAngle()
		{
			transform.rotation = Quaternion.Euler(0, 0, 0);
		}
	
		public void SetXCoordinates(float x)
		{
			xRef = x;
			transform.position = new Vector3(x,transform.position.y);
		}

		public void AlertWhips()
		{
			alertMode = true;
		}

		public void NoLongerAlerted()
		{
			alertMode = false;
		}

		public void SetPlayer(GameObject player)
		{
			this.player = player;
		}

		private bool CanWhip()
		{
			return whipCd >= whipRate;
		}
	
	}
}
