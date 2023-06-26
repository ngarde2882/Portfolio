package com.example.cstateats;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import com.google.firebase.auth.FirebaseAuth;

public class LandingPage extends AppCompatActivity {
    private Button button_createAccount;
    private Button button_signIn;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.landing_page);

        FirebaseAuth firebaseAuth = FirebaseAuth.getInstance();
        if(firebaseAuth.getCurrentUser() != null) {
            finish();
            startActivity(new Intent(getApplicationContext(), com.example.cstateats.MainActivity.class));
        }

        button_createAccount = (Button) findViewById(R.id.button_createAccount);
        button_signIn = (Button) findViewById(R.id.button_signIn);



        button_createAccount.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), com.example.cstateats.login.RegisterActivity.class);
                startActivity(intent);
                finish();
            }
        });

        button_signIn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), com.example.cstateats.login.LoginActivity.class);
                startActivity(intent);
                finish();
            }
        });
    }
}