package com.example.grocerygo;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.text.method.ScrollingMovementMethod;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.TextView;

import com.squareup.picasso.Picasso;

import java.io.Serializable;
import java.util.ArrayList;

public class item_detailActivity extends AppCompatActivity {
    Item item_obj;
    TextView title;
    TextView des;
    ImageButton addButton;
    ImageView img;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_item_detail);

        Intent intent = getIntent();
        item_obj = (Item) intent.getSerializableExtra("itemObj");
        title=(TextView)findViewById(R.id.title);
        des=(TextView)findViewById(R.id.des);
        img=(ImageView)findViewById(R.id.img);
        addButton=(ImageButton)findViewById(R.id.addButton);

        Picasso.with(this).load(item_obj.getImg_src()).into(img);
        title.setText(item_obj.getItem_name());
        des.setText(item_obj.toString());
        des.setMovementMethod(new ScrollingMovementMethod());
        addButton.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view){
                MainActivity.ggDB.addItem(item_obj,1);

            }
        });
    }
}