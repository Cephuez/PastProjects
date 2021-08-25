using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class TypeText: MonoBehaviour 
{

	TextMeshProUGUI txt;
	public string story="Game Over";
    private int tracker = 0;
    private float time_per_letter = 0.125f;
    private float cur_time_remaining=0;

	void Awake () 
	{
        // Component[] allComponents = gameObject.GetComponents<MonoBehaviour>();
        // foreach(Component component in allComponents) {
        //     Debug.Log(component.name);
        // }
        txt = this.gameObject.GetComponent<TextMeshProUGUI>();
		//Component txt = GetComponent<TextMeshPro>();
		txt.text = "";
	}

    void FixedUpdate(){
        if (tracker !=story.Length){
            if (cur_time_remaining<=0){
                txt.text += story[tracker];
                tracker +=1;
                cur_time_remaining = time_per_letter;
            }else{
                cur_time_remaining -= Time.deltaTime;
            }
        }
    }
}
