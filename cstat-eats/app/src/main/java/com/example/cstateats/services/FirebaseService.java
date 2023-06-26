package com.example.cstateats.services;

import android.provider.ContactsContract;
import android.util.Log;

import androidx.annotation.NonNull;

import com.example.cstateats.Eats;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.util.ArrayList;

public class FirebaseService {

    final FirebaseDatabase database = FirebaseDatabase.getInstance();
    DatabaseReference ref;
    FirebaseUser user;

    public interface FirebaseEatsCallback {
        void onSuccess(ArrayList<Eats> result);
    }

    public interface FirebaseRatingCallback {
        void onSuccess(double average);
    }

    public FirebaseService(FirebaseUser user) {
        this.user = user;
        ref = database.getReference();
    }

    //add favorite
    public void addFavorite(Eats eat) {
        ref.child(user.getUid()).child("favorites").child(eat.getID()).setValue(eat)
            .addOnCompleteListener(new OnCompleteListener<Void>() {
                @Override
                public void onComplete(@NonNull Task<Void> task) {
                    if (task.isSuccessful()) {
                        Log.e("FIREBASE", "Task Successful");
                    } else {
                        Log.e("FIREBASE", "Task NOT Successful");
                    }
                }
            });
    }

    //remove favorite
    public void removeFavorite(Eats eat) {
        ref.child(user.getUid()).child("favorites").child(eat.getID()).removeValue();
    }

    //add blocked
    public void addBlocked(Eats eat) {
        ref.child(user.getUid()).child("blocked").child(eat.getID()).setValue(eat);
    }

    //remove blocked
    public void removeBlocked(Eats eat) {
        ref.child(user.getUid()).child("blocked").child(eat.getID()).removeValue();
    }

    //add rating
    public void addRating(Eats eat, float stars) {
        ref.child("ratings").child(eat.getID()).child(user.getUid()).setValue(stars);
    }

    //get all the favorites
    public void getFavorites(final FirebaseEatsCallback callback) {
        ref.child(user.getUid()).child("favorites").get().addOnCompleteListener(new OnCompleteListener<DataSnapshot>() {
            @Override
            public void onComplete(@NonNull Task<DataSnapshot> task) {
                if (task.isSuccessful()) {
                    DataSnapshot ds = task.getResult();
                    if (ds.getValue() == null) {
                        callback.onSuccess(new ArrayList<>());
                    } else {
                        if (ds.hasChildren()) {
                            ArrayList<Eats> result = new ArrayList<>();
                            for (DataSnapshot childSnapshot : ds.getChildren()) {
                                Eats eat = childSnapshot.getValue(Eats.class);
                                result.add(eat);
                            }
                            callback.onSuccess(result);
                        }
                    }
                }
            }
        });
    }

    //get all the blocked
    public void getBlocked(final FirebaseEatsCallback callback) {
        ref.child(user.getUid()).child("blocked").get().addOnCompleteListener(new OnCompleteListener<DataSnapshot>() {
            @Override
            public void onComplete(@NonNull Task<DataSnapshot> task) {
                if (task.isSuccessful()) {
                    DataSnapshot ds = task.getResult();
                    if (ds.getValue() == null) {
                        callback.onSuccess(new ArrayList<>());
                    } else {
                        if (ds.hasChildren()) {
                            ArrayList<Eats> result = new ArrayList<>();
                            for (DataSnapshot childSnapshot : ds.getChildren()) {
                                Eats eat = childSnapshot.getValue(Eats.class);
                                result.add(eat);
                            }
                            callback.onSuccess(result);
                        }
                    }
                }
            }
        });
    }

    //get average rating for given restaurant
    public void getAverageRating(String eatID, final FirebaseRatingCallback callback) {
        ref.child("ratings").child(eatID).get().addOnCompleteListener(new OnCompleteListener<DataSnapshot>() {
            @Override
            public void onComplete(@NonNull Task<DataSnapshot> task) {
                if (task.isSuccessful()) {
                    DataSnapshot ds = task.getResult();

                    double sum = 0;
                    int denom = 0;
                    for (DataSnapshot child : ds.getChildren()) {
                        float num = Float.parseFloat(child.getValue().toString());
                        sum += num;
                        denom++;
                    }
                    double average = (denom == 0) ? 0 : sum / denom;
                    callback.onSuccess(average);
                }
            }
        });
    }

    public void getMyRating(String eatID, final FirebaseRatingCallback callback) {
        ref.child("ratings").child(eatID).child(user.getUid()).get().addOnCompleteListener(new OnCompleteListener<DataSnapshot>() {
            @Override
            public void onComplete(@NonNull Task<DataSnapshot> task) {
                if (task.isSuccessful()) {
                    DataSnapshot ds = task.getResult();
                    if (ds.getValue() == null) {
                        callback.onSuccess(0.0);
                    } else {
                        callback.onSuccess(Float.parseFloat(ds.getValue().toString()));
                    }
                }
            }
        });
    }

    public void getHistory(final FirebaseEatsCallback callback) {
        getBlocked(new FirebaseEatsCallback() {
            @Override
            public void onSuccess(ArrayList<Eats> result) {
                ArrayList<Eats> history = new ArrayList<>();
                history.addAll(result);
                getFavorites(new FirebaseEatsCallback() {
                    @Override
                    public void onSuccess(ArrayList<Eats> result) {
                        history.addAll(result);
                        callback.onSuccess(history);
                    }
                });
            }
        });
    }
}
