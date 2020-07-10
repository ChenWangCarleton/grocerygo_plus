package com.example.grocerygo;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.SearchView;

import androidx.appcompat.app.AppCompatActivity;

import java.util.ArrayList;

public class DisplayItemListActivity extends AppCompatActivity {
    String button_text;
    ArrayList<Item> items;

    ListView list_view;
    SearchView search_view;
    @Override
    protected void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_item_list);
        Intent intent = getIntent();
        button_text = intent.getStringExtra("button_text");
        items = (ArrayList<Item>) intent.getSerializableExtra("item_list");

        final CustomListview customListview = new CustomListview(this, items);
        list_view = (ListView) findViewById(R.id.listview);
        search_view = (SearchView) findViewById(R.id.search_list);

        list_view.setAdapter(customListview);

        search_view.setOnQueryTextListener(new SearchView.OnQueryTextListener() {
            @Override
            public boolean onQueryTextSubmit(String query) {
                return false;
            }

            @Override
            public boolean onQueryTextChange(String newText) {
                customListview.getCustomeFilter().filter(newText);
                System.out.println("Change notified:   "+newText);
                return false;
            }
        });

        list_view.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                search_view.setQueryHint(button_text);

            }
        });
    }
}
