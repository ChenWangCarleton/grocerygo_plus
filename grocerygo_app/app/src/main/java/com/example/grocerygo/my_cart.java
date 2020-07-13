package com.example.grocerygo;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListView;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;

public class my_cart extends AppCompatActivity {
    ArrayList<Item> items;

    CustomListview customListview;
    ListView list_view;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_my_cart);

        list_view = (ListView) findViewById(R.id.cartlistview);

        Intent intent = getIntent();
        items = new ArrayList<Item>();
        get_shopping_list_items();

        customListview = new CustomListview(this, items);
        list_view.setAdapter(customListview);
        list_view.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {

                Intent i=new Intent(my_cart.this, item_detailActivity.class);
                i.putExtra("itemObj", (Serializable)customListview.getItems().get(position));
                startActivity(i);
            }
        });
    }

    public void get_shopping_list_items(){
        items = MainActivity.ggDB.allItems();

    }
}