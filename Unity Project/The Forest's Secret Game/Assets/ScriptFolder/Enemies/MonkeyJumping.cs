using System;
using UnityEngine;

namespace Assets.ScriptFolder.Enemies
{
	public class MonkeyJumping : MonoBehaviour
	{
		private float resetMonkeyJump;
		private float jumpForceX;
		private float jumpForceY;
	
		public float jumpPowerX;
		public float jumpPowerY;
		public float farthestDistance;

		public GameObject MonkeyCloseRange;
		public GameObject MonkeyChaseRange;
	
		public Transform bottom;
		public Transform player;

		public Rigidbody2D monkeyBody;

		public LayerMask groundInteraction;

		public int AnimationID;
		private RaycastHit2D monkeyOnGround;

		private EnemyDetection _enemyDetectionClose;
		private EnemyDetection _enemyDetectionChase;

		private IdleWalk _idleWalk;

		private bool isCloseInRange;
		private bool canChasePlayer;
		private bool isChaseInRange;
		private bool CanTurnAround;
		private bool rangeFixed = true;
	
		// Use this for initialization
		void Start ()
		{
			CanTurnAround = true;
			resetMonkeyJump = 1.5f;
			AnimationID = 1;
			_enemyDetectionClose = MonkeyCloseRange.GetComponent<EnemyDetection>();
			_enemyDetectionChase = MonkeyChaseRange.GetComponent<EnemyDetection>();
			jumpForceX = jumpPowerX * monkeyBody.mass * monkeyBody.gravityScale / 2;
			jumpForceY = jumpPowerY * monkeyBody.mass * monkeyBody.gravityScale / 2;
			_idleWalk = MonkeyCloseRange.GetComponent<IdleWalk>();
		}
	
	
		// Update is called once per frame
		void Update ()
		{
			if (CanJump())
			{
				FixRange();
			}
			DetectPlayer();
			isCloseInRange = _enemyDetectionClose.IsPlayerInRange();
			isChaseInRange = _enemyDetectionChase.IsPlayerInRange();

			if (canChasePlayer)
			{
				_idleWalk.PauseIdleWalk();
				MonkeyAttackSequence();
			}

			if (!isChaseInRange && CanJump())
			{
				_idleWalk.ResumeIdleWalk();
				AnimationID = 1;
					
			}
		}

		private void MonkeyAttackSequence()
		{
			if (monkeyBody.velocity.y <= -0.001 && CanJump())
			{
				AnimationID = 2;
			}
			if (CanJump())
			{
				if (JumpAgain())
				{
					TurnAround();
					JumpAtPlayer();
				}
			}
		}

		// Monkey is touching the ground
		private Boolean CanJump()
		{
			monkeyOnGround = Physics2D.Raycast(bottom.position, bottom.up,
				-0.1f, groundInteraction.value);

			return monkeyOnGround.collider != null;
		}

		private Boolean JumpAgain()
		{
			resetMonkeyJump += Time.deltaTime;
			if (resetMonkeyJump >= 1.5f)
			{
				resetMonkeyJump = 0;
				AnimationID = 3;
				return true;
			}
			return false;
		}
	
		private void JumpAtPlayer()
		{
			// Left side of the monkey
			float powerJump = CalculateXJumpPower();
			if (MonkeyCloseRange.transform.localRotation.y != 0f)
				powerJump = -powerJump;
			if (player.position.x <= transform.position.x)
			{
				monkeyBody.AddForce(new Vector2(powerJump, jumpForceY), ForceMode2D.Impulse);
			}
			// Right Side of the Monkey
			else
			{
				monkeyBody.AddForce(new Vector2(powerJump, jumpForceY), ForceMode2D.Impulse);
			}
		}

		// Calculate Jump power that the money will do to reach the player
		private float CalculateXJumpPower()
		{
			float monkeyFromPlayerX = Math.Abs(monkeyBody.position.x - player.position.x);

			// Fix jump power for monkey. Don't want monkey jumping across the map 
			if (monkeyFromPlayerX >= farthestDistance)
				return 15f;

			return (monkeyFromPlayerX/12f) * 15f;
		}
	
		private void DetectPlayer()
		{
			if (isCloseInRange)
				canChasePlayer = true;
			if (!isChaseInRange)
			{
				canChasePlayer = false;
			}
		}
	
		private void TurnAround()
		{

			if (player.transform.position.x < MonkeyCloseRange.transform.position.x && MonkeyCloseRange.transform.localRotation.y == 0)
			{
				_idleWalk.ChangeDir();
				_idleWalk.TurnAround();
			}
			else if(player.transform.position.x > MonkeyCloseRange.transform.position.x && MonkeyCloseRange.transform.localRotation.y != 0)
			{
				_idleWalk.ChangeDir();
				_idleWalk.TurnAround();
			}
		}

		private void FixRange()
		{
			MonkeyCloseRange.transform.position = transform.position;
			transform.position = MonkeyCloseRange.transform.position;
			transform.position = MonkeyChaseRange.transform.position;
		}
	}
}
