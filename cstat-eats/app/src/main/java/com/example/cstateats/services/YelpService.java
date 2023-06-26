package com.example.cstateats.services;

import android.content.Context;
import android.util.Log;

import com.android.volley.AuthFailureError;
import com.android.volley.NetworkResponse;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.cronet.CronetHttpStack;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;

import java.util.HashMap;
import java.util.Map;

public class YelpService {

    private Context context;

    public YelpService(Context context) {
        this.context = context;
    }

    public interface YelpCallback {
        void onSuccess(String result) throws JSONException;
    }

    public void getYelpResultFromNumber(String number, final YelpCallback callback) {
        RequestQueue queue = Volley.newRequestQueue(context);
        String url = "https://api.yelp.com/v3/businesses/search/phone?phone=+1" + number;

        Map<String, String> headers = new HashMap<>();
        headers.put("Authorization", "Bearer lq0SVWdl_x0MbhwhRfW1hKfl8tWNL96G0QPl6uH9eNz2sjVXjxWlfTWRguwp3_c7JQlIVdZvaVr8_WUEPR2FiNv93ER3vw7KyHJ-Ai2b1FUraUrgEAXHoisYofGkYXYx");

        // Request a string response from the provided URL.
        StringRequest stringRequest = new StringRequest(Request.Method.GET, url,
                new Response.Listener<String>()
                {
                    @Override
                    public void onResponse(String response) {
                        // response
                        try {
                            callback.onSuccess(response);
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                },
                new Response.ErrorListener()
                {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        // TODO Auto-generated method stub
                        Log.e("VOLLEY ERROR", error.toString());
                    }
                }
        ) {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                return headers;
            }
        };

        queue.add(stringRequest);
    }

}
