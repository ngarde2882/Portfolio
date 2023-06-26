package com.example.cstateats.login;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.text.SpannableString;
import android.text.TextUtils;
import android.text.style.UnderlineSpan;
import android.util.Log;
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

public class RegisterActivity extends AppCompatActivity {

    //context
    private Context context;

    //auth
    private FirebaseAuth firebaseAuth;

    //components
    private EditText editText_registerEmail;
    private EditText editText_registerPassword;
    private EditText editText_confirmPassword;
    private Button button_register;
    private TextView textView_logIn;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        firebaseAuth = FirebaseAuth.getInstance();

        if(firebaseAuth.getCurrentUser() != null) {
            finish();
            startActivity(new Intent(getApplicationContext(), com.example.cstateats.MainActivity.class));
        }

        //Initialize components
        context = getApplicationContext();
        editText_registerEmail = (EditText) findViewById(R.id.editText_createEmail);
        editText_registerPassword = (EditText) findViewById(R.id.editText_createPassword);
        editText_confirmPassword = (EditText) findViewById(R.id.editText_confirmPassword);
        button_register = (Button) findViewById(R.id.button_register);
        textView_logIn = (TextView) findViewById(R.id.textView_login);

        SpannableString content = new SpannableString("Already have and Account? Login");
        content.setSpan(new UnderlineSpan(), 0, content.length(), 0);
        textView_logIn.setText(content);

        button_register.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                performUserRegister();
            }
        });

        textView_logIn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), com.example.cstateats.login.LoginActivity.class);
                startActivity(intent);
//                finish();
            }
        });
    }

    private void performUserRegister() {
        //verify username/password entries are filled out
        String email = editText_registerEmail.getText().toString().trim();
        String password = editText_registerPassword.getText().toString().trim();
        String confirmedPassword = editText_confirmPassword.getText().toString().trim();

        if (TextUtils.isEmpty(email)) {
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

        if (TextUtils.isEmpty(confirmedPassword)) {
            //confirm password edit text is empty
            Toast.makeText(this, "Please confirm password", Toast.LENGTH_SHORT).show();
            //stop from further execution
            return;
        }

        if (!password.equals(confirmedPassword)) {
            //confirm password edit text is empty
            Toast.makeText(this, "Passwords do not match", Toast.LENGTH_SHORT).show();
            //stop from further execution
            return;
        }

        firebaseAuth.createUserWithEmailAndPassword(email, password)
            .addOnCompleteListener(this, new OnCompleteListener<AuthResult>() {
                @Override
                public void onComplete(@NonNull Task<AuthResult> task) {
                    if (task.isSuccessful()) {
                        //Sign in success
                        Intent mainActivityIntent = new Intent(getApplicationContext(), com.example.cstateats.MainActivity.class);
                        mainActivityIntent.putExtra("registered", true);
                        startActivity(mainActivityIntent);
                        finish();
                    } else {
                        //Register failed
                        Log.w("REGISTER FAILED", "createUserWithEmail:failure", task.getException());
                        Toast.makeText(context, "Registration failed.", Toast.LENGTH_LONG).show();
                    }
                }
            });
    }
}