using UnityEngine;

namespace Assets.ScriptFolder.PlayerScripts
{
	public class ClimbWall : MonoBehaviour
	{

		public LayerMask groundLayer;

		public float GrabRangeLength;
	
		public Transform GrabRange;
		public LayerMask wallInteraction;
		// Use this for initialization
		void Start () {
		
		}
	
		// Update is called once per frame
		void Update ()
		{
			// Detect with Left Foot
			RaycastHit2D onWallBool = Physics2D.Raycast(GrabRange.position, GrabRange.right,
				GrabRangeLength, wallInteraction.value);
		
			Debug.Log(onWallBool.collider);
		}
	}
}
