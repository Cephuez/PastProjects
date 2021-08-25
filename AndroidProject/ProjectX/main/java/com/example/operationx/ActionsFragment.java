package com.example.operationx;

import android.os.Bundle;

import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import com.example.operationx.gameplay.GameTile;

import org.w3c.dom.Text;
/**
 * This fragment represents the bottom action selection of the game. It will be
 * displayed at every level.
 */

/**
 * A simple {@link Fragment} subclass.
 * Use the {@link ActionsFragment#newInstance} factory method to
 * create an instance of this fragment.
 */
public class ActionsFragment extends Fragment {

    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";

    // TODO: Rename and change types of parameters
    private String mParam1;
    private String mParam2;

    private View view;
    private int levelID;
    public ActionsFragment() {
        // Required empty public constructor
    }

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @param param1 Parameter 1.
     * @param param2 Parameter 2.
     * @return A new instance of fragment ActionsFragment.
     */
    // TODO: Rename and change types and number of parameters
    public static ActionsFragment newInstance(String param1, String param2) {
        ActionsFragment fragment = new ActionsFragment();
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
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        view = inflater.inflate(R.layout.fragment_actions, container, false);
        setUpActionButtons(view);
        changeActionPicture();
        return view;
    }

    /**
     * setter for the levelId
     * @param levelID
     */
    public void getLevelID(int levelID){
        this.levelID = levelID;
    }

    /**
     * Calls helper methods to change action images in this fragment.
     */
    public void changeActionPicture(){
        if(levelID == 1){
            levelOnePictures();
        }else{
            levelTwoPictures();
        }
    }


    /**
     * Simply adds pictures for each attack in each level.
     */
    private void levelOnePictures(){
        TextView action1 = view.findViewById(R.id.primary_attack);
        TextView action2 = view.findViewById(R.id.secondary_attack);
        TextView action3 = view.findViewById(R.id.third_attack);
        action1.setBackgroundResource(R.drawable.level_1_primary_attack);
        action2.setBackgroundResource(R.drawable.level_1_secondary_attack);
        action3.setBackgroundResource(R.drawable.level_1_third_attack);
    }

    /**
     * Simply adds pictures for each attack in each level.
     */
    private void levelTwoPictures(){
        TextView action1 = view.findViewById(R.id.primary_attack);
        TextView action2 = view.findViewById(R.id.secondary_attack);
        TextView action3 = view.findViewById(R.id.third_attack);
        action1.setBackgroundResource(R.drawable.level_2_primary_attack);
        action2.setBackgroundResource(R.drawable.level_2_secondary_attack);
        action3.setBackgroundResource(R.drawable.level_2_third_attack);
    }


    private int actionID = 0;
    /**
     * Sets item inventory for the views of each action and calls doAction in the
     * game tile to attack the enemy.
     * @param gTile GameTile (canvas of the game)
     */
    public void playerAction(GameTile gTile){
        actionID = gTile.doAction(actionID);
        if(actionID == 2 || actionID == 3){
            TextView action;
            if(actionID == 2)
                action = view.findViewById(R.id.secondary_attack);
            else
                action = view.findViewById(R.id.third_attack);
            String numberStr = (String) action.getText();
            Integer number = Integer.parseInt(numberStr);
            if(number > 0) {
                String newItemNumber = String.valueOf(number - 1);
                action.setText(newItemNumber);
            }
        }
        actionID = 0;
    }

    /**
     *  Sets onclick listeners and sets an action ID for the game canvas for
     *  each action item.
     * @param view the fragment of interest.
     */
    private void setUpActionButtons(View view){
        TextView action1 = view.findViewById(R.id.primary_attack);
        action1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                actionID = 1;
            }
        });

        TextView action2 = view.findViewById(R.id.secondary_attack);
        action2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                actionID = 2;
            }
        });

        TextView action3 = view.findViewById(R.id.third_attack);
        action3.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                actionID = 3;
            }
        });
    }
}