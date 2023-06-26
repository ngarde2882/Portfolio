package com.example.cstateats;

import androidx.annotation.Nullable;

import java.util.ArrayList;

public class Eats {

    private String name;
    private String website;
    private ArrayList<String> genres;
    private String ID;
    private String address;
    private String latitude;
    private String longitude;
    private String number;

    public Eats() {
        //default constructor required for getValue(Eats.class);
    }

    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }

    public String getWebsite() {
        return website;
    }
    public void setWebsite(String website) {
        this.website = website;
    }

    public ArrayList<String> getGenres() {
        return genres;
    }
    public void setGenres(ArrayList<String> genres) {
        this.genres = genres;
    }

    public void setID(String ID) {
        this.ID = ID;
    }
    public String getID() {
        return ID;
    }

    public void setAddress(String address) {
        this.address = address;
    }
    public String getAddress() {
        return address;
    }

    public void setLatitude(String lat) {this.latitude = lat;}
    public String getLatitude() {return latitude; }

    public void setLongitude(String lon) {this.longitude = lon;}
    public String getLongitude() {return longitude; }


    public void setNumber(String number) {
        this.number = number;
    }

    public String getNumber() {
        return number;
    }

    @Override
    public boolean equals(@Nullable Object obj) {
        Eats other = (Eats) obj;
        return other.getID().equals(ID);
    }
}
