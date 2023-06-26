package com.example.cstateats;

import android.content.Intent;
import android.graphics.Color;
import android.media.Image;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;

import android.text.SpannableString;
import android.text.style.UnderlineSpan;
import android.util.Log;
import android.util.TypedValue;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.PopupWindow;
import android.widget.TextView;
import android.widget.Toast;

import com.example.cstateats.services.FirebaseService;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthCredential;
import com.google.firebase.auth.EmailAuthProvider;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;

import java.util.ArrayList;

import static android.content.Context.LAYOUT_INFLATER_SERVICE;

/**
 * A simple {@link Fragment} subclass.
 * Use the {@link AccountFragment#newInstance} factory method to
 * create an instance of this fragment.
 */
public class AccountFragment extends Fragment {

    private ImageView increaseText;
    private boolean isBig;
    private TextView changePassword;
    private TextView emailLabel;
    private TextView email;
    private TextView changeEmail;
    private TextView logOut;
    private Button favorites;
    private Button blocked;

    private View parent_view;

    //Firebase user
    FirebaseAuth firebaseAuth;

    public AccountFragment() {
        // Required empty public constructor
    }


    public static AccountFragment newInstance(String param1, String param2) {
        return new AccountFragment();
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {

        // Inflate the layout for this fragment
        parent_view = inflater.inflate(R.layout.fragment_account, container, false);

        //all the stuff from on create activity goes here
        firebaseAuth = FirebaseAuth.getInstance();
        increaseText = (ImageView) parent_view.findViewById(R.id.imageView_increaseText2);
        isBig = false;
        changePassword = (TextView) parent_view.findViewById(R.id.textView_changePassword);
        emailLabel = (TextView) parent_view.findViewById(R.id.textView_emailLabel);
        email = (TextView) parent_view.findViewById(R.id.textView_accountEmail);
        changeEmail = (TextView) parent_view.findViewById(R.id.textView_changeEmail);
        favorites = (Button) parent_view.findViewById(R.id.button_favorites);
        blocked = (Button) parent_view.findViewById(R.id.button_blocked);
        logOut = (TextView) parent_view.findViewById(R.id.textView_logOut);

        //set the email to the current user
        email.setText(firebaseAuth.getCurrentUser().getEmail());

        SpannableString content = new SpannableString("Change Password");
        content.setSpan(new UnderlineSpan(), 0, content.length(), 0);
        changePassword.setText(content);

        content = new SpannableString("Change email");
        content.setSpan(new UnderlineSpan(), 0, content.length(), 0);
        changeEmail.setText(content);

        content = new SpannableString("Log Out");
        content.setSpan(new UnderlineSpan(), 0, content.length(), 0);
        logOut.setText(content);

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

                // TODO: set text
                emailLabel.setTextSize(TypedValue.COMPLEX_UNIT_PX, textSize);
                email.setTextSize(TypedValue.COMPLEX_UNIT_PX, textSize);
                changePassword.setTextSize(TypedValue.COMPLEX_UNIT_PX, textSize);
                changeEmail.setTextSize(TypedValue.COMPLEX_UNIT_PX, textSize);
                logOut.setTextSize(TypedValue.COMPLEX_UNIT_PX, textSize);
                favorites.setTextSize(TypedValue.COMPLEX_UNIT_PX, textSize);
                blocked.setTextSize(TypedValue.COMPLEX_UNIT_PX, textSize);
            }
        });

        changePassword.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //handle change password (firebase)
                launchPasswordPopup();
            }
        });

        changeEmail.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                launchEmailPopup();
            }
        });

        logOut.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //handle log out
                firebaseAuth.signOut();
                Intent intent = new Intent(getActivity(), com.example.cstateats.login.LoginActivity.class);
                startActivity(intent);
                getActivity().finish();
            }
        });

        favorites.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                launchFavoritesPopup();
            }
        });

        blocked.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                launchBlockedPopup();
            }
        });

        return parent_view;
    }

    private void blurView(View view) {
        view.setAlpha(0.3f);
        view.setBackgroundColor(Color.GRAY);
    }

    private void unblurView(View view) {
        //make screen visible
        view.setAlpha(1.0f);
        view.setBackgroundColor(Color.WHITE);
    }

    private void launchEmailPopup() {
        //handle change email (Firebase)
        LayoutInflater inflater = (LayoutInflater)
                getActivity().getSystemService(LAYOUT_INFLATER_SERVICE);
        View popupView = inflater.inflate(R.layout.change_email_popup, null);

        int width = LinearLayout.LayoutParams.WRAP_CONTENT;
        int height = LinearLayout.LayoutParams.WRAP_CONTENT;
        final PopupWindow popupWindow = new PopupWindow(popupView, width, height, true);

        popupWindow.setElevation(30);

        blurView(parent_view);

        popupWindow.setOnDismissListener(new PopupWindow.OnDismissListener() {
            @Override
            public void onDismiss() {
                unblurView(parent_view);
            }
        });

        // show the popup window
        // which view you pass in doesn't matter, it is only used for the window tolken
        popupWindow.showAtLocation(popupView, Gravity.CENTER, 0, 0);

        Button button_submitEmail = (Button) popupView.findViewById(R.id.button_submitEmail);
        EditText editText_enterOldEmail = (EditText) popupView.findViewById(R.id.editText_enterOldEmail);
        EditText editText_enterNewEmail = (EditText) popupView.findViewById(R.id.editText_enterNewEmail);
        EditText editText_enterPassword = (EditText) popupView.findViewById(R.id.editText_enterPassword);
        button_submitEmail.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (editText_enterOldEmail.getText().toString().isEmpty()) {
                    Toast.makeText(getActivity(), "Please enter a old Email", Toast.LENGTH_SHORT).show();
                    return;
                }

                if (editText_enterNewEmail.getText().toString().isEmpty()) {
                    Toast.makeText(getActivity(), "Please enter a new Email", Toast.LENGTH_SHORT).show();
                    return;
                }

                if (editText_enterPassword.getText().toString().isEmpty()) {
                    Toast.makeText(getActivity(), "Please enter your password", Toast.LENGTH_SHORT).show();
                    return;
                }

                Log.e("TAG", "Old email :: " + editText_enterOldEmail.getText().toString());
                Log.e("TAG", "New email :: " + editText_enterNewEmail.getText().toString());

                // Get auth credentials from the user for re-authentication. The example below shows
                // email and password credentials but there are multiple possible providers,
                // such as GoogleAuthProvider or FacebookAuthProvider.
                FirebaseUser user = FirebaseAuth.getInstance().getCurrentUser();

                AuthCredential credential = EmailAuthProvider
                        .getCredential(editText_enterOldEmail.getText().toString(), editText_enterPassword.getText().toString());

                // Prompt the user to re-provide their sign-in credentials
                user.reauthenticate(credential)
                        .addOnCompleteListener(new OnCompleteListener<Void>() {
                            @Override
                            public void onComplete(@NonNull Task<Void> task) {
                                Log.d("FIREBASE", "User re-authenticated.");
                                //must update email after user re-authenticates
                                user.updateEmail(editText_enterNewEmail.getText().toString()).addOnCompleteListener(new OnCompleteListener<Void>() {
                                    @Override
                                    public void onComplete(@NonNull Task<Void> task) {
                                        if (task.isSuccessful()) {
                                            Log.e("TAG", "User email address updated. new email is :: " + editText_enterNewEmail.getText().toString());
                                            email.setText(user.getEmail());
                                        }
                                    }
                                });
                            }
                        });


                popupWindow.dismiss();
            }
        });
    }

    private void launchPasswordPopup() {
        //handle change email (Firebase)
        LayoutInflater inflater = (LayoutInflater)
                getActivity().getSystemService(LAYOUT_INFLATER_SERVICE);
        View popupView = inflater.inflate(R.layout.change_password_popup, null);

        int width = LinearLayout.LayoutParams.WRAP_CONTENT;
        int height = LinearLayout.LayoutParams.WRAP_CONTENT;
        final PopupWindow popupWindow = new PopupWindow(popupView, width, height, true);

        popupWindow.setElevation(30);

        blurView(parent_view);

        popupWindow.setOnDismissListener(new PopupWindow.OnDismissListener() {
            @Override
            public void onDismiss() {
                unblurView(parent_view);
            }
        });

        // show the popup window
        // which view you pass in doesn't matter, it is only used for the window tolken
        popupWindow.showAtLocation(popupView, Gravity.CENTER, 0, 0);

        Button button_submitEmail = (Button) popupView.findViewById(R.id.button_submitPassword);
        EditText editText_enterOldPassword = (EditText) popupView.findViewById(R.id.editText_enterOldPassword);
        EditText editText_enterNewPassword = (EditText) popupView.findViewById(R.id.editText_enterNewPassword);
        EditText editText_confirmNewPassword = (EditText) popupView.findViewById(R.id.editText_confirmNewPassword);
        button_submitEmail.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (editText_enterOldPassword.getText().toString().isEmpty()) {
                    Toast.makeText(getActivity(), "Please enter your old password", Toast.LENGTH_SHORT).show();
                    return;
                }

                if (editText_enterNewPassword.getText().toString().isEmpty()) {
                    Toast.makeText(getActivity(), "Please enter a new password", Toast.LENGTH_SHORT).show();
                    return;
                }

                if (editText_confirmNewPassword.getText().toString().isEmpty()) {
                    Toast.makeText(getActivity(), "Please confirm your new password", Toast.LENGTH_SHORT).show();
                    return;
                }

                if (!editText_confirmNewPassword.getText().toString().equals(editText_enterNewPassword.getText().toString())) {
                    Toast.makeText(getActivity(), "Error: Passwords don't match", Toast.LENGTH_SHORT).show();
                    return;
                }

                //Re-authenticate
                FirebaseUser user = FirebaseAuth.getInstance().getCurrentUser();

                AuthCredential credential = EmailAuthProvider
                        .getCredential(user.getEmail().toString(), editText_enterOldPassword.getText().toString());

                // Prompt the user to re-provide their sign-in credentials
                user.reauthenticate(credential)
                        .addOnCompleteListener(new OnCompleteListener<Void>() {
                            @Override
                            public void onComplete(@NonNull Task<Void> task) {
                                user.updatePassword(editText_enterNewPassword.getText().toString())
                                        .addOnCompleteListener(new OnCompleteListener<Void>() {
                                            @Override
                                            public void onComplete(@NonNull Task<Void> task) {
                                                if (task.isSuccessful()) {
                                                    Toast.makeText(getActivity(), "Password Changed", Toast.LENGTH_SHORT);
                                                    Log.e("FIREBASE", "password changed");
                                                } else {
                                                    Toast.makeText(getActivity(), "Password change failed", Toast.LENGTH_SHORT);
                                                    Log.e("FIREBASE", "rutt row");
                                                }
                                            }
                                        });
                            }
                        });
                popupWindow.dismiss();
            }
        });
    }

    private void launchFavoritesPopup() {
        //handle launch favorites view
        // inflate the layout of the popup window
        LayoutInflater inflater = (LayoutInflater)
                getActivity().getSystemService(LAYOUT_INFLATER_SERVICE);
        View popupView = inflater.inflate(R.layout.show_favorites_popup, null);

        // create the popup window
        int width = LinearLayout.LayoutParams.WRAP_CONTENT;
        int height = LinearLayout.LayoutParams.WRAP_CONTENT;
        final PopupWindow popupWindow = new PopupWindow(popupView, width, height, true);

        LinearLayout favList = (LinearLayout) popupView.findViewById(R.id.linearLayout_favorites);
        TextView loading = (TextView) popupView.findViewById(R.id.textView_favoritesLoading);

        //add top line to list
        TextView line = new TextView(getActivity());
        line.setBackgroundColor(Color.BLACK);
        line.setLayoutParams(new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,
                10));
        favList.addView(line);

        //blur the background
        blurView(parent_view);

        popupWindow.setOnDismissListener(new PopupWindow.OnDismissListener() {
            @Override
            public void onDismiss() {
                unblurView(parent_view);
            }
        });

        // show the popup window
        // which view you pass in doesn't matter, it is only used for the window tolken
        popupWindow.setElevation(30);
        popupWindow.showAtLocation(popupView, Gravity.CENTER, 0, 0);

        // dismiss the popup window when touched
        popupView.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                popupWindow.dismiss();
                return true;
            }
        });

        //load the data into the list
        FirebaseService firebaseService = new FirebaseService(firebaseAuth.getCurrentUser());

        firebaseService.getFavorites(new FirebaseService.FirebaseEatsCallback() {
            @Override
            public void onSuccess(ArrayList<Eats> result) {
                if (result.isEmpty()) {
                    loading.setText("No favorite restaurants");
                } else {
                    loading.setVisibility(View.INVISIBLE);
                }
                for (Eats eat : result) {
                    View eatsView = inflater.inflate(R.layout.eats_element, null);

                    TextView textView_name = (TextView) eatsView.findViewById(R.id.textView_eatsName);
                    TextView textView_url = (TextView) eatsView.findViewById(R.id.textView_eatsURL);
                    ImageButton button_info = (ImageButton) eatsView.findViewById(R.id.button_eatsInfo);
                    ImageButton button_remove = (ImageButton) eatsView.findViewById(R.id.button_removeEat);

                    textView_name.setText(eat.getName());
                    textView_url.setText(eat.getWebsite());

                    favList.addView(eatsView);

                    //Border Text view
                    TextView line = new TextView(getActivity());
                    line.setBackgroundColor(Color.BLACK);
                    line.setLayoutParams(new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,
                            10));
                    favList.addView(line);

                    button_info.setOnClickListener(new View.OnClickListener() {
                        @Override
                        public void onClick(View view) {
                            Log.e("TAG", "Clicked");
                            launchInfoPopup(eat, popupView);
                        }
                    });

                    button_remove.setOnClickListener(new View.OnClickListener() {
                        @Override
                        public void onClick(View view) {
                            favList.removeView(eatsView);
                            favList.removeView(line);

                            firebaseService.removeFavorite(eat);
                        }
                    });
                }
            }
        });
    }

    private void launchInfoPopup(Eats eat, View view) {
        LayoutInflater inflater = (LayoutInflater)
                getActivity().getSystemService(LAYOUT_INFLATER_SERVICE);
        View popupView = inflater.inflate(R.layout.eats_info_popup, null);

        FirebaseService firebaseService = new FirebaseService(firebaseAuth.getCurrentUser());

        // create the popup window
        int width = LinearLayout.LayoutParams.WRAP_CONTENT;
        int height = LinearLayout.LayoutParams.WRAP_CONTENT;
        final PopupWindow popupWindow = new PopupWindow(popupView, width, height, true);

        blurView(view);

        popupWindow.setOnDismissListener(new PopupWindow.OnDismissListener() {
            @Override
            public void onDismiss() {
                unblurView(view);
            }
        });

        TextView name = (TextView) popupView.findViewById(R.id.textView_eatsInfoName);
        TextView genres = (TextView) popupView.findViewById(R.id.textView_eatsInfoGenres);
        TextView url = (TextView) popupView.findViewById(R.id.textView_eatsInfoURL);

        ImageView avgStar_1 = (ImageView) popupView.findViewById(R.id.imageView_AvgStar1);
        ImageView avgStar_2 = (ImageView) popupView.findViewById(R.id.imageView_AvgStar2);
        ImageView avgStar_3 = (ImageView) popupView.findViewById(R.id.imageView_AvgStar3);
        ImageView avgStar_4 = (ImageView) popupView.findViewById(R.id.imageView_AvgStar4);
        ImageView avgStar_5 = (ImageView) popupView.findViewById(R.id.imageView_AvgStar5);

        //set the star (half/full) based on rating
        firebaseService.getAverageRating(eat.getID(), new FirebaseService.FirebaseRatingCallback() {
            @Override
            public void onSuccess(double average) {
                //round average to nearest .5
                average = Math.round(average * 2) / 2.0;
                displayRating(average, avgStar_1, avgStar_2, avgStar_3, avgStar_4, avgStar_5);
            }
        });

        ImageView myStar_1 = (ImageView) popupView.findViewById(R.id.imageView_MyStar1);
        ImageView myStar_2 = (ImageView) popupView.findViewById(R.id.imageView_MyStar2);
        ImageView myStar_3 = (ImageView) popupView.findViewById(R.id.imageView_MyStar3);
        ImageView myStar_4 = (ImageView) popupView.findViewById(R.id.imageView_MyStar4);
        ImageView myStar_5 = (ImageView) popupView.findViewById(R.id.imageView_MyStar5);

        firebaseService.getMyRating(eat.getID(), new FirebaseService.FirebaseRatingCallback() {
            @Override
            public void onSuccess(double average) {
                displayRating(average, myStar_1, myStar_2, myStar_3, myStar_4, myStar_5);
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

        name.setText(eat.getName());
        url.setText(eat.getWebsite());

        String genreMessage = "";
        for (String genre : eat.getGenres()) {
            genreMessage += genre + ", ";
        }
        genreMessage = genreMessage.substring(0, genreMessage.length() - 2);

        genres.setText(genreMessage);

        // show the popup window
        // which view you pass in doesn't matter, it is only used for the window tolken
        popupWindow.setElevation(30);
        popupWindow.showAtLocation(popupView, Gravity.CENTER, 0, 0);
    }

    private void starClicked(double rating, ImageView star1, ImageView star2, ImageView star3, ImageView star4, ImageView star5) {
        star1.setImageResource(R.drawable.ic_baseline_star_border_24);
        star2.setImageResource(R.drawable.ic_baseline_star_border_24);
        star3.setImageResource(R.drawable.ic_baseline_star_border_24);
        star4.setImageResource(R.drawable.ic_baseline_star_border_24);
        star5.setImageResource(R.drawable.ic_baseline_star_border_24);

        displayRating(rating, star1, star2, star3, star4, star5);
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

    private void launchBlockedPopup() {
        //handle launch blocked view
        // inflate the layout of the popup window
        LayoutInflater inflater = (LayoutInflater)
                getActivity().getSystemService(LAYOUT_INFLATER_SERVICE);
        View popupView = inflater.inflate(R.layout.show_blocked_popup, null);

        // create the popup window
        int width = LinearLayout.LayoutParams.WRAP_CONTENT;
        int height = LinearLayout.LayoutParams.WRAP_CONTENT;
        final PopupWindow popupWindow = new PopupWindow(popupView, width, height, true);

        LinearLayout blockedList = (LinearLayout) popupView.findViewById(R.id.linearLayout_blocked);
        TextView loading = (TextView) popupView.findViewById(R.id.textView_blockedLoading);

        blurView(parent_view);

        popupWindow.setOnDismissListener(new PopupWindow.OnDismissListener() {
            @Override
            public void onDismiss() {
                unblurView(parent_view);
            }
        });

        //add top line to list
        TextView line = new TextView(getActivity());
        line.setBackgroundColor(Color.BLACK);
        line.setLayoutParams(new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,
                10));
        blockedList.addView(line);

        // show the popup window
        // which view you pass in doesn't matter, it is only used for the window tolken
        popupWindow.setElevation(30);
        popupWindow.showAtLocation(popupView, Gravity.CENTER, 0, 0);

        // dismiss the popup window when touched
        popupView.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                popupWindow.dismiss();
                return true;
            }
        });

        FirebaseService firebaseService = new FirebaseService(firebaseAuth.getCurrentUser());

        firebaseService.getBlocked(new FirebaseService.FirebaseEatsCallback() {
            @Override
            public void onSuccess(ArrayList<Eats> result) {
                if (result.isEmpty()) {
                    loading.setText("No restaurants are currently blocked");
                } else {
                    loading.setVisibility(View.INVISIBLE);
                }

                for (Eats eat : result) {
                    View eatsView = inflater.inflate(R.layout.eats_element, null);

                    TextView textView_name = (TextView) eatsView.findViewById(R.id.textView_eatsName);
                    TextView textView_url = (TextView) eatsView.findViewById(R.id.textView_eatsURL);
                    ImageButton button_info = (ImageButton) eatsView.findViewById(R.id.button_eatsInfo);
                    ImageButton button_remove = (ImageButton) eatsView.findViewById(R.id.button_removeEat);

                    textView_name.setText(eat.getName());
                    textView_url.setText(eat.getWebsite());

                    blockedList.addView(eatsView);

                    button_info.setOnClickListener(new View.OnClickListener() {
                        @Override
                        public void onClick(View view) {
                            Log.e("TAG", "Clicked");
                            launchInfoPopup(eat, popupView);
                        }
                    });

                    button_remove.setOnClickListener(new View.OnClickListener() {
                        @Override
                        public void onClick(View view) {
                            blockedList.removeView(eatsView);
                            blockedList.removeView(line);

                            firebaseService.removeBlocked(eat);
                        }
                    });

                    //Border Text view
                    TextView line = new TextView(getActivity());
                    line.setBackgroundColor(Color.BLACK);
                    line.setLayoutParams(new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,
                            10));
                    blockedList.addView(line);
                }
            }
        });
    }
}