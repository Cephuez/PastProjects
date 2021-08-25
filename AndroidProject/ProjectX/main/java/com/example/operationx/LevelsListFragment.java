package com.example.operationx;

import android.content.Intent;
import android.os.Bundle;

import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.SimpleAdapter;

import com.example.operationx.gameplay.OperationGameplay;

import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
/**
 * Represents the fragment that lets you select a level. Three
 * are populated in this levels list.
 */

/**
 * A simple {@link Fragment} subclass.
 * Use the {@link LevelsListFragment#newInstance} factory method to
 * create an instance of this fragment.
 */
public class LevelsListFragment extends Fragment {
    ArrayList<GameLevel> levels = new ArrayList<>();
    GameLevel level1 = new GameLevel("Escape Level", 1);
    GameLevel level2 = new GameLevel("Plane Level", 2);
    GameLevel level3 = new GameLevel("Pug Level", 3);

    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";

    // TODO: Rename and change types of parameters
    private String mParam1;
    private String mParam2;

    public LevelsListFragment() {
        // Required empty public constructor
        levels.add(level1);
        levels.add(level2);
    }

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @param param1 Parameter 1.
     * @param param2 Parameter 2.
     * @return A new instance of fragment LevelsListFragment.
     */
    // TODO: Rename and change types and number of parameters
    public static LevelsListFragment newInstance(String param1, String param2) {
        LevelsListFragment fragment = new LevelsListFragment();
        Bundle args = new Bundle();
        args.putString(ARG_PARAM1, param1);
        args.putString(ARG_PARAM2, param2);
        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (getArguments() != null) {
            mParam1 = getArguments().getString(ARG_PARAM1);
            mParam2 = getArguments().getString(ARG_PARAM2);
        }
    }


    @Override
    /**
     * Sets the simple view adapter to the fragment and populates that information
     * for each element and makes it activate the game onclick.
     */
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View view =  inflater.inflate(R.layout.fragment_levels_list, container, false);
        ListView simpleListView=(ListView) view.findViewById(R.id.listView);
        ArrayList<HashMap<String,String>> arrayList=new ArrayList<>();
        JSONObject article = null;
        for(int i=0; i<levels.size(); i++) {
            GameLevel currLevel = levels.get(i);
            HashMap<String, String> hashMap = new HashMap<>();
            hashMap.put("name", currLevel.levelName);
            hashMap.put("image", currLevel.characterImage + "");
            arrayList.add(hashMap);
        }
        String[] from={"name","image"};
        int[] to={R.id.level_number,R.id.character_image};
        SimpleAdapter simpleAdapter=new SimpleAdapter(getContext(),arrayList,
                R.layout.level_item,from,to);


        simpleListView.setAdapter(simpleAdapter);
        simpleListView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
                Intent intent = new Intent(getActivity(), OperationGameplay.class);
                GameLevel level = levels.get(i);
                intent.putExtra("LEVEL_INT", level.level);
                System.out.println("************ LEVEL: " + level.level);

                startActivity(intent);
            }
        });
        return view;
    }
}