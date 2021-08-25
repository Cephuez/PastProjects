package com.example.operationx;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;

import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.SeekBar;
import android.widget.TextView;

import org.w3c.dom.Text;
/**
 * This represents the settings menu that will have volume and
 * game fps settings.
 */

/**
 * A simple {@link Fragment} subclass.
 * Use the {@link SettingsFragment#newInstance} factory method to
 * create an instance of this fragment.
 */
public class SettingsFragment extends Fragment {

    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";

    // TODO: Rename and change types of parameters
    private String mParam1;
    private String mParam2;

    public SettingsFragment() {
        // Required empty public constructor
    }

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @param param1 Parameter 1.
     * @param param2 Parameter 2.
     * @return A new instance of fragment SettingsFragment.
     */
    // TODO: Rename and change types and number of parameters
    public static SettingsFragment newInstance(String param1, String param2) {
        SettingsFragment fragment = new SettingsFragment();
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
        View view = inflater.inflate(R.layout.fragment_settings, container, false);
        SeekBar sBar = view.findViewById(R.id.volumeSeekBar);
        SharedPreferences sharedPref = getActivity().getSharedPreferences("Settings", Context.MODE_PRIVATE);
        final SharedPreferences.Editor editor = sharedPref.edit();
        //SeekBar saves the volume setting
        sBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            int volume = 50;
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                volume = progress;
            }
            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {
                //write custom code to on start progress
                //Override needed for interface
            }
            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
                float volumeFloat = volume;
                MainActivity.MUSIC.setVolume(volumeFloat / 100, volumeFloat/100);
                editor.putInt(getString(R.string.saved_volume_key), volume);
                editor.apply();
            }
        });

        //Sets the gameFPS on click of each textbox.
        final TextView normal = view.findViewById(R.id.normalSetting);
        final TextView fast = view.findViewById(R.id.fastSetting);
        //Save fps to normal
        normal.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //TextView tv = (TextView) v;
                normal.setTextColor(getResources().getColor(R.color.gameFPSColor));
                fast.setTextColor(getResources().getColor(android.R.color.primary_text_light));
                editor.putInt(getString(R.string.saved_fps_key), 1);
                editor.apply();
            }
        });
        //Save fps to fast
        fast.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {
                fast.setTextColor(getResources().getColor(R.color.gameFPSColor));
                normal.setTextColor(getResources().getColor(android.R.color.primary_text_light));
                //add FPS speed in shared preferences
                editor.putInt(getString(R.string.saved_fps_key), 2);
                editor.apply();
            }
        });

        //Go back to the previous fragment, in this case the MainMenuFragment
        Button done = view.findViewById(R.id.doneButton);
        done.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //Save settings to shared preferences and close fragment
                System.out.println("Popped");
                requireActivity().getSupportFragmentManager().popBackStack();
            }
        });
        return view;
    }
}