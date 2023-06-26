package com.example.cstateats;

import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.ViewParent;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.navigation.NavController;
import androidx.navigation.Navigation;
import androidx.navigation.ui.NavigationUI;

import com.example.cstateats.services.DocumenuService;
import com.example.cstateats.services.FirebaseService;
import com.example.cstateats.services.YelpService;
import com.google.android.material.bottomnavigation.BottomNavigationView;
import com.google.firebase.auth.FirebaseAuth;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.zip.Inflater;

public class MainActivity extends AppCompatActivity {

    private FirebaseAuth mAuth;
    private LinearLayout linearLayout_restaurants;

    private TextView accountPage;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mAuth = FirebaseAuth.getInstance();

        Intent intent = getIntent();
        boolean registered = intent.getBooleanExtra("registered", false);
        if (registered) {
            //load the tutorial screen
            ViewGroup parentView = (ViewGroup) findViewById(R.id.main_constraint_layout);

            LayoutInflater inflater = (LayoutInflater)
                    getSystemService(LAYOUT_INFLATER_SERVICE);
            View overlayView = inflater.inflate(R.layout.home_tutorial_overlay, parentView, false);
            overlayView.setElevation(100.0f);

            TextView touchOverlay = overlayView.findViewById(R.id.textView_tutorialOverlay);

            touchOverlay.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    parentView.removeView(overlayView);
                }
            });

            parentView.addView(overlayView);
        }

        //initialize bottom menu bar
        BottomNavigationView bottomNavigationView = (BottomNavigationView) findViewById(R.id.bottom_navigation_view);
        NavController navController = Navigation.findNavController(findViewById(R.id.nav_fragment));

        NavigationUI.setupWithNavController(bottomNavigationView, navController);


//        Eats eat = new Eats();
//        eat.setName("NEW EAT");
//        eat.setID("NEW EAT ID");
//        eat.setWebsite("SUPERCOOL.URL");
//        ArrayList<String> genres = new ArrayList<>();
//        genres.add("THIS da GENRE");
//        eat.setGenres(genres);
//
//        FirebaseService firebaseService = new FirebaseService(mAuth.getCurrentUser());
//
//        firebaseService.addFavorite(eat);
//
//        eat.setID("STOOPID ID");
//
//        firebaseService.addBlocked(eat);

//        firebaseService.addRating(eat, 3.5f);

//        firebaseService.getMyRating("NEW EAT ID", new FirebaseService.FirebaseRatingCallback() {
//            @Override
//            public void onSuccess(double average) {
//                Log.e("SUCCESS", "super successful, avg :: " + average);
//
//            }
//        });
//        firebaseService.getAverageRating("NEW EAT ID", new FirebaseService.FirebaseRatingCallback() {
//            @Override
//            public void onSuccess(double average) {
//                Log.e("AVG RTING", "" + average);
//            }
//        });
    }
}