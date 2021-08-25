package com.example.operationx;

import android.content.DialogInterface;
import android.icu.util.Freezable;
import android.os.Bundle;

import androidx.appcompat.app.AlertDialog;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;

import java.util.logging.Level;

/** This is the main menu that you see when the game is booted and
 * guides the player to other areas of the app.

 */

/**
 * A simple {@link Fragment} subclass.
 * Use the {@link MainMenuFragment#newInstance} factory method to
 * create an instance of this fragment.
 */
public class MainMenuFragment extends Fragment {
    private final String[] settingsOptions = {"Volume", "Game FPS", "Redeem"};
    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";

    // TODO: Rename and change types of parameters
    private String mParam1;
    private String mParam2;

    public MainMenuFragment() {
        // Required empty public constructor
    }


    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @param param1 Parameter 1.
     * @param param2 Parameter 2.
     * @return A new instance of fragment MainMenuFragment.
     */
    // TODO: Rename and change types and number of parameters
    public static MainMenuFragment newInstance(String param1, String param2) {
        MainMenuFragment fragment = new MainMenuFragment();
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
        View view = inflater.inflate(R.layout.fragment_main_menu, container, false);
        setButtons(view);
        return view;
    }

    /**
     * Activates all fragments on every button for the player navigation to
     * game settings, leaderboards or start the game.
     * @param view
     */
    public void setButtons(View view){
        final View fView = view;
        Button levelButton = (Button) view.findViewById(R.id.level_button);
        levelButton.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {
                LevelsListFragment llf = new LevelsListFragment();
                getActivity().getSupportFragmentManager().beginTransaction()
                        .replace(R.id.main_menu_frag, llf)
                        .addToBackStack(null)
                        .commit();
            }
        });

        Button settings = view.findViewById(R.id.settings_button);
        settings.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                System.out.println("Launch settings alert menu");
                SettingsFragment sf = new SettingsFragment();
                FragmentManager fm = getActivity().getSupportFragmentManager();
                fm.beginTransaction()
                        .replace(R.id.main_menu_frag, sf)
                        .addToBackStack(null)
                        .commit();
            }
        });


        Button share = view.findViewById(R.id.share_button);
        share.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                ShareFragment shareFrag = new ShareFragment();
                requireActivity().getSupportFragmentManager().beginTransaction()
                        .replace(R.id.main_menu_frag, shareFrag, "shareFragment")
                        .addToBackStack(null)
                        .commit();
            }
        });

        Button leaderBoards = view.findViewById(R.id.leaderB_button);
        leaderBoards.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                HttpGetRequest request = new HttpGetRequest();
                request.execute(fView);
                LeaderBoardsFragment lb = new LeaderBoardsFragment();
                requireActivity().getSupportFragmentManager().beginTransaction()
                        .replace(R.id.main_menu_frag, lb, "leaderBoardFragment")
                        .addToBackStack(null)
                        .commit();
            }
        });
    }
}