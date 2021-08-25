using Assets.ScriptFolder.Enemies;
using UnityEngine;

public class Being : MonoBehaviour
{
    public float health;
    // Start is called before the first frame update
    void Start()
    {
    
    }

    // Update is called once per frame
    void Update()
    {
    
    }

    public bool IsAlive()
    {
        return health > 0;
    }

    public void TakeDamage(int damage)
    {
        health -= damage;
    }
}
    