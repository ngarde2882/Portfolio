package com.example.cstateats.login;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.text.SpannableString;
import android.text.TextUtils;
import android.text.style.UnderlineSpan;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.example.cstateats.R;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;

public class LoginActivity extends AppCompatActivity {

    // auth
    private FirebaseAuth firebaseAuth;

    // components
    private EditText editText_loginUsername;
    private EditText editText_loginPassword;
    private Button button_login;
    private TextView textView_registerLink;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        firebaseAuth = FirebaseAuth.getInstance();
        if(firebaseAuth.getCurrentUser() != null) {
            finish();
            startActivity(new Intent(getApplicationContext(), com.example.cstateats.MainActivity.class));
        }

        editText_loginUsername = (EditText) findViewById(R.id.editText_loginUsername);
        editText_loginPassword = (EditText) findViewById(R.id.editText_loginPassword);
        button_login = (Button) findViewById(R.id.button_login);
        textView_registerLink = (TextView) findViewById(R.id.textView_registerLink);

        SpannableString content = new SpannableString("Don't have an Account? Register");
        content.setSpan(new UnderlineSpan(), 0, content.length(), 0);
        textView_registerLink.setText(content);

        button_login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                performUserLogin();
            }
        });

        textView_registerLink.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), com.example.cstateats.login.RegisterActivity.class);
                startActivity(intent);
                finish();
            }
        });
    }

    public void performUserLogin() {
        String username = editText_loginUsername.getText().toString().trim();
        String password = editText_loginPassword.getText().toString().trim();

        if (TextUtils.isEmpty(username)) {
            // email is empty
            Toast.makeText(this, "Please enter email", Toast.LENGTH_SHORT).show();
            // stop function from execution further
            return;
        }

        if (TextUtils.isEmpty(password)) {
            // password is empty
            Toast.makeText(this, "Please enter password", Toast.LENGTH_SHORT).show();
            // stop function from execution further
            return;
        }

        firebaseAuth.signInWithEmailAndPassword(username, password)
        .addOnCompleteListener(this, new OnCompleteListener<AuthResult>() {
            @Override
            public void onComplete(@NonNull Task<AuthResult> task) {
                if (task.isSuccessful()) {
                    Intent mainActivityIntent = new Intent(getApplicationContext(), com.example.cstateats.MainActivity.class);

                    startActivity(mainActivityIntent);
                    finish();
                } else {
                    Toast.makeText(getApplicationContext(), "Authentication failed", Toast.LENGTH_SHORT).show();
                }
            }
        });

    }


}