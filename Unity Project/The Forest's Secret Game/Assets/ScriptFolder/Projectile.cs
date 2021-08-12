using UnityEngine;

namespace Assets.ScriptFolder
{
	public class Projectile : MonoBehaviour
	{
		public GameObject player;

		public float dmg;
		public float speed;
		public float timer;

		private float startTime;

		public Rigidbody2D body;
		// Use this for initialization
		void Start ()
		{
			startTime = 0;
			body = GetComponent<Rigidbody2D>();
		}

		void Update()
		{
			DestroyProjectile();
			ProjectileMoving();
		}

		private void ProjectileMoving()
		{
			transform.position += transform.right * Time.deltaTime * speed;
		}
		private void DestroyProjectile()
		{
			startTime += Time.deltaTime;
			if(startTime >= timer)
				Destroy(gameObject);
		}
	}
}
