using UnityEngine;

namespace Assets.ScriptFolder.Enemies
{
	public class EnemyDetection : MonoBehaviour
	{
		private bool playerInRange;

		void OnTriggerEnter2D(Collider2D col)
		{
			if (col.gameObject.layer == 11)
			{
				playerInRange = true;
			}
		}

		void OnTriggerExit2D(Collider2D col)
		{
			if (col.gameObject.layer == 11)
				playerInRange = false;
		}

		public bool IsPlayerInRange()
		{
			return playerInRange;
		}
	}
}

