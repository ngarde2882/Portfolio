package com.example.cstateats;

import android.annotation.SuppressLint;
import android.content.Context;
import android.content.Intent;
import android.content.res.Resources;
import android.graphics.drawable.Drawable;
import android.net.Uri;
import android.os.Bundle;

import androidx.constraintlayout.widget.ConstraintLayout;
import androidx.constraintlayout.widget.ConstraintSet;
import androidx.fragment.app.Fragment;

import android.util.Log;
import android.util.TypedValue;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.bumptech.glide.Glide;
import com.example.cstateats.services.DocumenuService;
import com.example.cstateats.services.FirebaseService;
import com.example.cstateats.services.YelpService;
import com.google.firebase.auth.FirebaseAuth;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;

import static android.content.Context.LAYOUT_INFLATER_SERVICE;

/**
 * A simple {@link Fragment} subclass.
 * Use the {@link HomeFragment#newInstance} factory method to
 * create an instance of this fragment.
 */
public class HomeFragment extends Fragment {

    private FirebaseAuth mAuth;
    private View home_view;
    private ConstraintLayout eatContainerView;
    private ArrayList<Eats> eatsList = new ArrayList<>();
    private int currentEatIndex = 0;
    private boolean isBig;

    public HomeFragment() {
        // Required empty public constructor
    }

    public static HomeFragment newInstance(String param1, String param2) {
        return new HomeFragment();
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @SuppressLint("ClickableViewAccessibility")
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        home_view = inflater.inflate(R.layout.fragment_home, container, false);

        mAuth = FirebaseAuth.getInstance();

        eatContainerView = (ConstraintLayout) home_view.findViewById(R.id.constraintLayout_homeSwipeContainer);

        FirebaseService firebaseService = new FirebaseService(mAuth.getCurrentUser());

        //Initialize Eats list with all eats
        DocumenuService docuService = new DocumenuService(getActivity());
        docuService.getEatsForCollegeStation(result -> {
                    Log.e("VALUE", result);
                    JSONObject json = new JSONObject(result);
                    // accountPage.setText(result);
                    JSONArray restaurants = json.getJSONArray("data");
                    for (int i = 0; i < restaurants.length(); i++) {

                        JSONObject restaurant = restaurants.getJSONObject(i);
                        String name = restaurant.getString("restaurant_name");
                        String website = restaurant.getString("restaurant_website");
                        String id = restaurant.getString("restaurant_id");
                        String raw_number = restaurant.getString("restaurant_phone");
                        //parse number
                        String number = "";
                        for (int index = 0; index < raw_number.length(); index++) {
                            String current_char = "" + raw_number.charAt(index);
                            try {
                                int num = Integer.parseInt(current_char);
                            } catch (Exception e) {
                                continue;
                            }
                            number += current_char;
                        }
                        ArrayList<String> genres = new ArrayList<>();
                        JSONArray cuisines = restaurant.getJSONArray("cuisines");
                        for (int j = 0; j < cuisines.length(); j++) {
                            genres.add(cuisines.getString(j));
                        }

                        //get the address
                        JSONObject jsonAddress = restaurant.getJSONObject("address");
                        String address = jsonAddress.getString("formatted");

                        Eats newEat = new Eats();
                        newEat.setName(name);
                        newEat.setWebsite(website);
                        newEat.setGenres(genres);
                        newEat.setID(id);
                        newEat.setAddress(address);
                        newEat.setNumber(number);
                        eatsList.add(newEat);
                    }

                    //Filter out all restaurants already viewed
                    firebaseService.getHistory(new FirebaseService.FirebaseEatsCallback() {
                        @Override
                        public void onSuccess(ArrayList<Eats> result) {
                            eatsList.removeAll(result);
                            loadEatView(eatsList.get(currentEatIndex));

                            loadImage();
                        }
                    });
                }
        );

        return home_view;
    }

    private void loadImage() {
        Eats eat = eatsList.get(currentEatIndex);

        YelpService yelpService = new YelpService(getContext());

        Log.e("Number", "testing number :: " + eat.getNumber());

        yelpService.getYelpResultFromNumber(eat.getNumber(), new YelpService.YelpCallback() {
            @Override
            public void onSuccess(String result) throws JSONException {
                Log.e("YELP", result);

                JSONObject businessesObj = new JSONObject(result);
                JSONArray  businessArr = businessesObj.getJSONArray("businesses");
                JSONObject business = businessArr.getJSONObject(0);

                String imageUrl = business.getString("image_url");
                String yelpUrl = business.getString("url");

                ImageView imageView = home_view.findViewById(R.id.imageView_eatsCardPic);

                Glide.with(getContext()).load(imageUrl).into(imageView);
                imageView.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View view) {
                        Intent browserIntent = new Intent(Intent.ACTION_VIEW, Uri.parse(yelpUrl));
                        startActivity(browserIntent);
                    }
                });
            }
        });
    }

    @SuppressLint("ClickableViewAccessibility")
    private void loadEatView(Eats eat) {
        //remove current views
        eatContainerView.removeAllViews();

        FirebaseService firebaseService = new FirebaseService(mAuth.getCurrentUser());

        LayoutInflater inflater = (LayoutInflater)
                getActivity().getSystemService(LAYOUT_INFLATER_SERVICE);
        View eatView = inflater.inflate(R.layout.eats_card, eatContainerView, false);

        TextView name = eatView.findViewById(R.id.textView_eatsCardName);
        ImageView increaseText = eatView.findViewById(R.id.imageView_increaseText);
        isBig = false;
        TextView genres = eatView.findViewById(R.id.textView_eatsCardGenres);
        TextView website = eatView.findViewById(R.id.textView_eatsCardURL);
        TextView overlay = eatView.findViewById(R.id.textView_eatsCardOverlay);
        TextView average_rating = eatView.findViewById(R.id.textView_eatsCardAvgRating);
        TextView my_rating = eatView.findViewById(R.id.textView_eatsViewMyRating);

        ImageView avgStar_1 = eatView.findViewById(R.id.imageView_eatsCardAvg1);
        ImageView avgStar_2 = eatView.findViewById(R.id.imageView_eatsCardAvg2);
        ImageView avgStar_3 = eatView.findViewById(R.id.imageView_eatsCardAvg3);
        ImageView avgStar_4 = eatView.findViewById(R.id.imageView_eatsCardAvg4);
        ImageView avgStar_5 = eatView.findViewById(R.id.imageView_eatsCardAvg5);

        ImageView myStar_1 = eatView.findViewById(R.id.imageView_eatsCardMy1);
        ImageView myStar_2 = eatView.findViewById(R.id.imageView_eatsCardMy2);
        ImageView myStar_3 = eatView.findViewById(R.id.imageView_eatsCardMy3);
        ImageView myStar_4 = eatView.findViewById(R.id.imageView_eatsCardMy4);
        ImageView myStar_5 = eatView.findViewById(R.id.imageView_eatsCardMy5);

        firebaseService.getAverageRating(eat.getID(), new FirebaseService.FirebaseRatingCallback() {
            @Override
            public void onSuccess(double average) {
                //round to nearest 0.5
                average = Math.round(average * 2) / 2.0;
                displayRating(average, avgStar_1, avgStar_2, avgStar_3, avgStar_4, avgStar_5);
            }
        });

        firebaseService.getMyRating(eat.getID(), new FirebaseService.FirebaseRatingCallback() {
            @Override
            public void onSuccess(double average) {
                displayRating(average, avgStar_1, avgStar_2, avgStar_3, avgStar_4, avgStar_5);
            }
        });

        increaseText.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                float textSize;
                if (isBig) {
                    textSize = 40;
                    increaseText.setImageResource(R.drawable.increase_text_button);
                    isBig = false;
                } else {
                    textSize = 50;
                    increaseText.setImageResource(R.drawable.decrease_text_size_button);
                    isBig = true;
                }

                name.setTextSize(TypedValue.COMPLEX_UNIT_PX, textSize);
                genres.setTextSize(TypedValue.COMPLEX_UNIT_PX, textSize);
                website.setTextSize(TypedValue.COMPLEX_UNIT_PX, textSize);
                average_rating.setTextSize(TypedValue.COMPLEX_UNIT_PX, textSize);
                my_rating.setTextSize(TypedValue.COMPLEX_UNIT_PX, textSize);
                System.out.println("now text size is " + textSize);

            }
        });

        myStar_1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //set all stars to border to redo the display
                starClicked(1.0, myStar_1, myStar_2, myStar_3, myStar_4, myStar_5);
                firebaseService.addRating(eat, 1.0f);
            }
        });

        myStar_2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //set all stars to border to redo the display
                starClicked(2.0, myStar_1, myStar_2, myStar_3, myStar_4, myStar_5);
                firebaseService.addRating(eat, 2.0f);
            }
        });

        myStar_3.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //set all stars to border to redo the display
                starClicked(3.0, myStar_1, myStar_2, myStar_3, myStar_4, myStar_5);
                firebaseService.addRating(eat, 3.0f);
            }
        });

        myStar_4.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //set all stars to border to redo the display
                starClicked(4.0, myStar_1, myStar_2, myStar_3, myStar_4, myStar_5);
                firebaseService.addRating(eat, 4.0f);
            }
        });

        myStar_5.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //set all stars to border to redo the display
                starClicked(5.0, myStar_1, myStar_2, myStar_3, myStar_4, myStar_5);
                firebaseService.addRating(eat, 5.0f);
            }
        });

        ConstraintLayout.LayoutParams lp = new ConstraintLayout.LayoutParams(
                ConstraintLayout.LayoutParams.MATCH_PARENT,
                ConstraintLayout.LayoutParams.MATCH_PARENT);

        eatView.setLayoutParams(lp);

        ImageView eatPic = eatView.findViewById(R.id.imageView_eatsCardPic);

        Log.e("TAG", "HELLO");

        name.setText(eat.getName());
        website.setText(eat.getWebsite());
        String genreMessage = "";
        for (String genre : eat.getGenres()) {
            genreMessage += genre + ", ";
        }
        genreMessage = genreMessage.substring(0, genreMessage.length() - 2);
        genres.setText(genreMessage);

        overlay.setOnTouchListener(new OnSwipeTouchListener(getActivity()) {
            @Override
            public void onSwipeRight() {
                super.onSwipeRight();
                FirebaseService firebaseService = new FirebaseService(mAuth.getCurrentUser());
                firebaseService.addFavorite(eatsList.get(currentEatIndex));
                currentEatIndex++;
                if (currentEatIndex >= eatsList.size()) {
                    loadDoneMessage();
                } else {
                    loadEatView(eatsList.get(currentEatIndex));
                }
                loadImage();
            }

            @Override
            public void onSwipeLeft() {
                super.onSwipeLeft();
                FirebaseService firebaseService = new FirebaseService(mAuth.getCurrentUser());
                firebaseService.addBlocked(eatsList.get(currentEatIndex));
                currentEatIndex++;
                if (currentEatIndex >= eatsList.size()) {
                    loadDoneMessage();
                } else {
                    loadEatView(eatsList.get(currentEatIndex));
                }
                loadImage();
            }

            @Override
            public void onSwipeTop() {
                super.onSwipeTop();
                Uri mapsIntentUri = Uri.parse("geo:0,0?q=" + eatsList.get(currentEatIndex).getAddress());
                Intent mapIntent = new Intent(Intent.ACTION_VIEW, mapsIntentUri);
                mapIntent.setPackage("com.google.android.apps.maps");
                startActivity(mapIntent);
            }
        });

        eatContainerView.addView(eatView);
    }

    private void loadDoneMessage() {
        eatContainerView.removeAllViews();

        TextView textView = new TextView(getActivity());

        ViewGroup.LayoutParams lp = new ConstraintLayout.LayoutParams(
                ConstraintLayout.LayoutParams.WRAP_CONTENT,
                ConstraintLayout.LayoutParams.WRAP_CONTENT);

        textView.setLayoutParams(lp);
        textView.setId(R.id.textView_doneMessage);
        textView.setText("That is all the restaurants in College Station");

        eatContainerView.addView(textView);

        ConstraintSet cs = new ConstraintSet();
        cs.clone(eatContainerView);
        cs.connect(textView.getId(), ConstraintSet.TOP, ConstraintSet.PARENT_ID, ConstraintSet.TOP);
        cs.connect(textView.getId(), ConstraintSet.BOTTOM, ConstraintSet.PARENT_ID, ConstraintSet.BOTTOM);
        cs.connect(textView.getId(), ConstraintSet.START, ConstraintSet.PARENT_ID, ConstraintSet.START);
        cs.connect(textView.getId(), ConstraintSet.END, ConstraintSet.PARENT_ID, ConstraintSet.END);
        cs.applyTo(eatContainerView);
    }

    private void displayRating(double rating, ImageView star1, ImageView star2, ImageView star3, ImageView star4, ImageView star5) {
        if (rating >= 1) {
            star1.setImageResource(R.drawable.ic_baseline_star_24);
        }

        if (rating >= 2) {
            star2.setImageResource(R.drawable.ic_baseline_star_24);
        }

        if (rating >= 3) {
            star3.setImageResource(R.drawable.ic_baseline_star_24);
        }

        if (rating >= 4) {
            star4.setImageResource(R.drawable.ic_baseline_star_24);
        }

        if (rating == 5) {
            star5.setImageResource(R.drawable.ic_baseline_star_24);
        }

        //Do halves
        if (rating == 0.5) {
            star1.setImageResource(R.drawable.ic_baseline_star_half_24);
        }

        if (rating == 1.5) {
            star2.setImageResource(R.drawable.ic_baseline_star_half_24);
        }

        if (rating == 2.5) {
            star3.setImageResource(R.drawable.ic_baseline_star_half_24);
        }

        if (rating == 3.5) {
            star4.setImageResource(R.drawable.ic_baseline_star_half_24);
        }

        if (rating == 4.5) {
            star5.setImageResource(R.drawable.ic_baseline_star_half_24);
        }
    }

    private void starClicked(double rating, ImageView star1, ImageView star2, ImageView star3, ImageView star4, ImageView star5) {
        star1.setImageResource(R.drawable.ic_baseline_star_border_24);
        star2.setImageResource(R.drawable.ic_baseline_star_border_24);
        star3.setImageResource(R.drawable.ic_baseline_star_border_24);
        star4.setImageResource(R.drawable.ic_baseline_star_border_24);
        star5.setImageResource(R.drawable.ic_baseline_star_border_24);

        displayRating(rating, star1, star2, star3, star4, star5);
    }
}