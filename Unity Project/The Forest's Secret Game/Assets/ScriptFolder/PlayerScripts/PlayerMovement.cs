using UnityEngine;

namespace Assets.ScriptFolder.PlayerScripts
{
	public class PlayerMovement : MonoBehaviour
	{

		private float hAxis;
		private float yAxis;
	
		private bool IsSneaking;
		private bool isRunning;
		private bool OffGround;
		private bool changeDir;
		private bool IsDashing;
		private bool setTime;
		private bool IsClimbing;
		private bool IsClimbController;
		private bool ClimbAnimation;
		private bool GotCoords;
		private bool airJump;
		private bool CanDashAgain;
		private bool WillClimbNext;

		private float WalkSpeed;
		private float RunSpeed;
		private float DashSpeed;
		private float SneakSpeed;
		private float UpdateSpeed;
		private float dashTimer;
		private float leftDir;
		private float resumeGravityScale;
		private float ClimbXCord;
		private float ClimbYCord;
		private float DashAgainTimer;

		public GameObject WeaponCanvas;
		public Rigidbody2D body;
		public int animationID;

		private float startingSpeed;
		public float defaultSpeed;
		public float jumpPower;
		public float groundedRayLength;
		public float GrabRangeLength;
		public float climbSpeed;	

		public Transform groundedRayFrontOrigin;
		public Transform groundedRayBackOrigin;
		public Transform groundedRayCenterOrigin;
		public Transform GrabRange;
	
		public LayerMask groundInteraction;
		public LayerMask wallInteraction;
		public LayerMask wallEdgeInteraction;

		public Rigidbody2D BodyGravity;

		private RaycastHit2D ClimbAnimateBool;
		private RaycastHit2D Backfoot;
	
		// Use this for initialization
		void Start()
		{
			IsSneaking = true;
			isRunning = false;
			changeDir = true;
			setTime = false;
			IsDashing = false;
			leftDir = 1;
			animationID = 1;
			resumeGravityScale = BodyGravity.gravityScale;

			SneakSpeed = defaultSpeed / 2;
			WalkSpeed = defaultSpeed;
			RunSpeed = defaultSpeed * 2;
			DashSpeed = defaultSpeed * 8;
			UpdateSpeed = WalkSpeed;
		}

		// Update is called once per frame
		void Update()
		{
			//Debug.Log(body.gravityScale);
			ResetDashMove();
			if (!ClimbAnimation)
			{

				if (IsClimbController)
					ClimbController();
				else
				{
					DefaultController();
				}
		
				if(!IsDashing)
					ClimbWall();
			}
			else
			{
				PlayerClimbEdge();
			}
		}
	
		// Walking here
		private void FixedUpdate()
		{

			if (IsDashing)
			{
				body.velocity = new Vector2(DashSpeed * leftDir, 0);
			}
			else if(!ClimbAnimation)
			{
				if (canJump())
					defaultSpeed = UpdateSpeed;
				body.velocity = new Vector2(hAxis * defaultSpeed, body.velocity.y);
			}
		}

		private void PlayerClimbEdge()
		{
			ClimbAnimateBool = Physics2D.Raycast(groundedRayFrontOrigin.position, groundedRayFrontOrigin.right,
				GrabRangeLength+2, wallInteraction.value);

			Backfoot = Physics2D.Raycast(groundedRayCenterOrigin.position, groundedRayCenterOrigin.up, 
				-(groundedRayLength + 2), wallInteraction.value);
		
			if (ClimbAnimateBool.collider != null)
			{
				transform.position = new Vector2(transform.position.x,transform.position.y + Time.deltaTime * climbSpeed);
				WillClimbNext = true;
			}
			else if (Backfoot.collider == null && WillClimbNext)
			{
				transform.position = new Vector2(transform.position.x + (Time.deltaTime * leftDir*climbSpeed), transform.position.y);
			}else if (Backfoot.collider != null || !WillClimbNext)
			{
				// End the climb animation and resume all movements
				ClimbAnimation = false;
				IsClimbController = false;
				IsClimbing = false;
				WillClimbNext = false;
				BodyGravity.gravityScale = resumeGravityScale;
			}

			// Player On Right Side Of Wall
		}

		private void ClimbController()
		{
			if (Input.GetKey(KeyCode.W))
			{
				transform.position = new Vector2(transform.position.x, transform.position.y + Time.deltaTime * climbSpeed);
				animationID = 6;
			}
			else if (Input.GetKey(KeyCode.S))
			{
				transform.position =
					new Vector2(transform.position.x, transform.position.y + -1 * Time.deltaTime * climbSpeed);
				animationID = 6;
			}
			else
			{
				animationID = 5;
			}

			if ((Input.GetKey(KeyCode.D) || Input.GetKey(KeyCode.A)) && Input.GetKeyDown(KeyCode.Space))
			{
				animationID = 3;
				float dir = 0f;
				if (leftDir == 1)
					dir = 180;
				transform.localRotation = Quaternion.Euler(0, dir, 0);
				body.velocity = new Vector2(0, jumpPower * 2.5f);
				IsClimbController = false;
				IsClimbing = false;
				BodyGravity.gravityScale = resumeGravityScale;
			}
			else if (Input.GetKeyDown(KeyCode.Space))
			{
				IsClimbController = false;
				IsClimbing = false;
				BodyGravity.gravityScale = resumeGravityScale;
			}

			// Jump to the right side
		}
	
		private void ClimbWall()
		{
			RaycastHit2D onWallBool = Physics2D.Raycast(GrabRange.position, GrabRange.right,
				GrabRangeLength, wallInteraction.value);
		
			// WORK ON CLIMBING OUT AGAIN BUT WITH SPACE BAR OR PICKING A DIRECTION XD
			if (!IsClimbing && onWallBool.collider != null && (Input.GetKey(KeyCode.A) || Input.GetKey(KeyCode.D)))
			{
				// Reset Air jump	
				airJump = true;
				animationID = 3;
				if(body.velocity.x != 0f || body.velocity.y != 0f)
					body.velocity = new Vector2(0f, 0f);
			
				IsClimbing = true;
				IsClimbController = true;
				BodyGravity.gravityScale = 0;
			}

			if (IsClimbing || IsClimbController)
			{
				if (onWallBool.collider == null)
				{
					IsClimbing = false;
					IsClimbController = false;
					ClimbAnimation = true;
				}
			}
		}
	
		// Controller Inputs when not on a wall
		private void DefaultController()
		{
			if(!IsDashing)
				hAxis = Input.GetAxis("Horizontal");
			TurnAround();	
			JumpCommand();
			SpeedChange();
			if (IsDashing)
			{
				IsDashingSequence();
			}
		}
	
		private void IsDashingSequence()
		{
			if (!setTime)
			{
				dashTimer = 0;
				setTime = true;
				BodyGravity.gravityScale = 0;
			}
		
			dashTimer += Time.deltaTime;
			if (dashTimer >= 0.15f)
			{
				BodyGravity.gravityScale = resumeGravityScale;
				IsDashing = false;
				setTime = false;
			}
		}
	
		private void SpeedChange()
		{
			if (Input.GetKeyDown(KeyCode.LeftShift))
			{
				if (IsSneaking)
					UpdateSpeed = SneakSpeed;
				else
					UpdateSpeed = WalkSpeed;
				IsSneaking = !IsSneaking;

			}

			if (Input.GetKeyDown(KeyCode.LeftControl) && Time.timeScale > 0)
			{
				if (CanDashAgain)
				{
					animationID = 4;
					IsDashing = true; 
					CanDashAgain = false;
					DashAgainTimer = 0;
				}
			
			}
		}
	

		private void JumpCommand()
		{
			if ((canJump() || airJump) && Input.GetButtonDown("Jump") && !IsDashing)
			{
				if (!canJump() && airJump)
				{
					airJump = false;
					body.velocity = new Vector2(body.velocity.x,0);
				}

				animationID = 3;
				body.AddForce(new Vector2(0f, Time.timeScale * jumpPower * body.mass * body.gravityScale / 2), ForceMode2D.Impulse);
			}

		}
	
		private bool canJump()
		{
			RaycastHit2D raycastResultLeft = Physics2D.Raycast(groundedRayFrontOrigin.position, 
				groundedRayFrontOrigin.up, groundedRayLength, groundInteraction.value);
			RaycastHit2D raycastResultRight = Physics2D.Raycast(groundedRayBackOrigin.position,
				groundedRayBackOrigin.up, groundedRayLength, groundInteraction.value);
			if (raycastResultLeft.collider != null || raycastResultRight.collider != null)
				airJump = true;
			return (raycastResultLeft.collider != null || raycastResultRight.collider != null);
		}
	
		private void TurnAround()
		{
			//changeDir
			if (hAxis > 0)
			{
				transform.localRotation = Quaternion.Euler(0, 0, 0);
				leftDir = 1;
				if(canJump())
					animationID = 2;
			}
			else if (hAxis < 0)
			{
				transform.localRotation = Quaternion.Euler(0, 180, 0);
				leftDir = -1;
				animationID = 2;
			}

			if (hAxis == 0 && canJump())
				animationID = 1;

			WeaponCanvas.transform.rotation = Quaternion.Euler(0,0,0);
		}
	
		private void ResetDashMove()
		{
			if (!CanDashAgain)
			{
				DashAgainTimer += Time.deltaTime;
				if (DashAgainTimer >= 0.20f)
				{
					if (!canJump())
						animationID = 3;
					CanDashAgain = true;
				}
			}
		}

	}
}