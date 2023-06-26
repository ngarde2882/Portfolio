package com.example.cstateats.services;

import android.content.Context;
import android.util.Log;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import org.json.JSONException;

public class DocumenuService {

    private Context context;

    public DocumenuService(Context context) {
        this.context = context;
    }

    public interface VolleyCallback {
        void onSuccess(String result) throws JSONException;
    }

    public void getEatsForCollegeStation(final VolleyCallback callback) {
        RequestQueue queue = Volley.newRequestQueue(context);
        String url = "https://api.documenu.com/v2/restaurants/search/geo?key=d1122029633bd7b326d25e4eadd4fbc1&lat=30.592549724510416&lon=-96.2964176624086&distance=5&size=100";

        // Request a string response from the provided URL.
        StringRequest stringRequest = new StringRequest(Request.Method.GET, url,
                response -> {
                    // Display the first 500 characters of the response string.
                    try {
                        callback.onSuccess(response);
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }, error -> Log.e("VOLLEY ERROR", error.toString()));

        // Add the request to the RequestQueue.
        queue.add(stringRequest);
    }
}
