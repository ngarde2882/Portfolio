package com.example.cstateats;

import android.content.Intent;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;

import androidx.fragment.app.Fragment;

import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import com.example.cstateats.services.DocumenuService;
import com.example.cstateats.services.FirebaseService;
import com.example.cstateats.services.YelpService;
import com.google.android.gms.maps.CameraUpdate;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.MapView;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.LatLngBounds;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.firebase.auth.FirebaseAuth;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;

/**
 * A simple {@link Fragment} subclass.
 * Use the {@link MapFragment#newInstance} factory method to
 * create an instance of this fragment.
 */
public class MapFragment extends Fragment implements OnMapReadyCallback, GoogleMap.OnMarkerClickListener, GoogleMap.OnInfoWindowClickListener {

    private MapView mapView;

    private static final String MAPVIEW_BUNDLE_KEY = "MapViewBundleKey";

    private FirebaseAuth mAuth;

    private ArrayList<Eats> eatsList = new ArrayList<>();

    public MapFragment() {
        // Required empty public constructor
    }

    public static MapFragment newInstance() {
        return new MapFragment();
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View parent_view = inflater.inflate(R.layout.fragment_map, container, false);
        mapView = (MapView) parent_view.findViewById(R.id.mapView);

        //get bundle
        Bundle mapViewBundle = null;
        if (savedInstanceState != null) {
            mapViewBundle = savedInstanceState.getBundle(MAPVIEW_BUNDLE_KEY);
        }

        mapView.onCreate(mapViewBundle);

        mapView.getMapAsync(this);

        //Probably have to add an eatslist like homeFragment

        return parent_view;
    }



    @Override
    public void onMapReady(GoogleMap googleMap) {
        //and markers for each eat, make some unique identifier for different eats


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
                ArrayList<String> genres = new ArrayList<>();
                JSONArray cuisines = restaurant.getJSONArray("cuisines");
                for (int j = 0; j < cuisines.length(); j++) {
                    genres.add(cuisines.getString(j));
                }

                //get the address
                JSONObject jsonAddress = restaurant.getJSONObject("address");
                String address = jsonAddress.getString("formatted");

                // get the geo-coordinates
                JSONObject jsonGeo = restaurant.getJSONObject("geo");
                String latitude = jsonGeo.getString("lat");
                String longitude = jsonGeo.getString("lon");

                Eats newEat = new Eats();
                newEat.setName(name);
                newEat.setWebsite(website);
                newEat.setGenres(genres);
                newEat.setID(id);
                newEat.setAddress(address);
                newEat.setLatitude(latitude);
                newEat.setLongitude(longitude);
                eatsList.add(newEat);
            }


            ArrayList<MarkerOptions> markers = new ArrayList<>();
            for(Eats eat : eatsList) {

                MarkerOptions m = new MarkerOptions()
                        .position(new LatLng(Double.parseDouble(eat.getLatitude()), Double.parseDouble(eat.getLongitude())))
                        .title("" + eatsList.indexOf(eat));

                markers.add(m);

                googleMap.addMarker(m);
            }

            //zoom in to include all markers
            LatLngBounds.Builder builder = new LatLngBounds.Builder();
            for (MarkerOptions marker : markers) {
                builder.include(marker.getPosition());
            }
            LatLngBounds bounds = builder.build();

            CameraUpdate cu = CameraUpdateFactory.newLatLngBounds(bounds, 100);
            googleMap.animateCamera(cu);


            googleMap.setInfoWindowAdapter(new GoogleMap.InfoWindowAdapter() {
                @Override
                public View getInfoWindow(Marker marker) {
                    return null;
                }

                @Override
                public View getInfoContents(Marker marker) {
                    View infoView = View.inflate(getContext(), R.layout.maps_info_window, null);

                    //Set stuff from view here - have to get identifier from marker, then use it to get the eat

                    TextView message = (TextView) infoView.findViewById(R.id.textView_mapInfo);
                    message.setText(marker.getTitle());

                    return infoView;
                }
            });
        });
    }

    @Override
    public void onStart() {
        super.onStart();
        mapView.onStart();
    }

    @Override
    public void onResume() {
        super.onResume();
        mapView.onResume();
    }

    @Override
    public void onPause() {
        mapView.onPause();
        super.onPause();
    }

    @Override
    public void onStop() {
        super.onStop();
        mapView.onStop();
    }

    @Override
    public void onLowMemory() {
        super.onLowMemory();
        mapView.onLowMemory();
    }

    @Override
    public void onDestroy() {
        mapView.onDestroy();
        super.onDestroy();
    }

    @Override
    public boolean onMarkerClick(Marker marker) {

        return false;
    }

    @Override
    public void onInfoWindowClick(Marker marker) {
        int index = Integer.parseInt(marker.getTitle());
        Eats eat = eatsList.get(index);

        Uri mapsIntentUri = Uri.parse("geo:0,0?q=" + eat.getAddress());
        Intent mapIntent = new Intent(Intent.ACTION_VIEW, mapsIntentUri);
        mapIntent.setPackage("com.google.android.apps.maps");
        startActivity(mapIntent);
    }
}