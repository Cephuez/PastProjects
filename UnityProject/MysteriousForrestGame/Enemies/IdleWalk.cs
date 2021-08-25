using UnityEngine;

namespace Assets.ScriptFolder.Enemies
{
	public class IdleWalk : MonoBehaviour
	{
		public Transform front;
		public Transform bottom;
	
		public float speed;

		public LayerMask wallInteraction;

		public Canvas healthBar;
		// Use this for initialization
		private RaycastHit2D WallInFront;
		private RaycastHit2D NoMoreGround;

		private int dir;

		private float resumeSpeed;

		private bool CanWalk;
		void Start () {
			//Physics2D.IgnoreCollision(mainBody,playerBody);
			dir = 1;
			resumeSpeed = speed;
			CanWalk = true;
		}
	
		// Update is called once per frame
		void Update () {
			if (CanWalk)
			{
				TurnAround();
				DetectHeadOnCoaltion();
				transform.Translate(Vector3.right * (speed * Time.deltaTime));
			}
		}

		// Check if the enemies needs to turn when close to an edge or wall
		private void DetectHeadOnCoaltion()
		{
			WallInFront = Physics2D.Raycast(front.position, front.right,
				0.1f, wallInteraction.value);
		
			NoMoreGround = Physics2D.Raycast(bottom.position, bottom.up,
				-0.2f, wallInteraction.value);
			//|| NoMoreGround.collider == null
			if (WallInFront.collider != null)
			{
				dir = -dir;
			}

		}

		public void TurnAround()
		{
			if (dir == -1)
			{
				transform.localRotation = Quaternion.Euler(0, 180, 0);
				healthBar.transform.rotation = Quaternion.Euler(0,0,0);
			}
			else
			{
				transform.localRotation = Quaternion.Euler(0, 0, 0);
				healthBar.transform.rotation = Quaternion.Euler(0,0,0);
			}

		}
	

		public void ChangeDir()
		{
			dir = -dir;
		}
		public int GetDir()
		{
			return dir;
		}

		public void ChangeSpeed(float chaseSpeed)
		{
			speed = chaseSpeed;
		}

		public void ResumeSpeed()
		{
			speed = resumeSpeed;
		}

		public void PauseIdleWalk()
		{
			CanWalk = false;
		}

		public void ResumeIdleWalk()
		{
			CanWalk = true;
		}

		public bool IsWalking()
		{
			return CanWalk;
		}
	}
}
