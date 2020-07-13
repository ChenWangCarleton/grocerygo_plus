package com.example.grocerygo;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.SearchView;

import androidx.appcompat.app.AppCompatActivity;

import com.google.android.material.chip.Chip;
import com.google.android.material.chip.ChipGroup;

import java.io.Serializable;
import java.util.ArrayList;

public class DisplayItemListActivity extends AppCompatActivity {
    String button_text;
    ArrayList<Item> items;
    boolean[] chip_selected = new boolean[4];

    ListView list_view;
    SearchView search_view;
    ChipGroup filterGroup;
    Chip all_chip;
    Chip loblaws_chip;
    Chip metro_chip;
    Chip walmart_chip;
    CustomListview customListview;

    @Override
    protected void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_item_list);
        Intent intent = getIntent();
        button_text = intent.getStringExtra("button_text");
        //items = (ArrayList<Item>) intent.getSerializableExtra("item_list");
        items = MainActivity.ggDB.getByCategory(button_text);
        //final CustomListview customListview = new CustomListview(this, items);
        customListview = new CustomListview(this, items);
        list_view = (ListView) findViewById(R.id.listview);
        search_view = (SearchView) findViewById(R.id.search_list);
        filterGroup = (ChipGroup) findViewById(R.id.filterGroup);
        all_chip = (Chip) findViewById(R.id.all_chip);
        loblaws_chip = (Chip) findViewById(R.id.loblaws_chip);
        metro_chip = (Chip) findViewById(R.id.metro_chip);
        walmart_chip = (Chip) findViewById(R.id.walmart_chip);

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

                Intent i=new Intent(DisplayItemListActivity.this, item_detailActivity.class);
                i.putExtra("itemObj", (Serializable)customListview.getItems().get(position));
                startActivity(i);
            }
        });

        all_chip.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view) {
                chip_check_change_action();
            }
        });
        loblaws_chip.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view) {
                chip_check_change_action();
            }
        });
        metro_chip.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view) {
                chip_check_change_action();
            }
        });
        walmart_chip.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view) {
                chip_check_change_action();
            }
        });

    }
    public void chip_check_change_action(){

        if (all_chip.isChecked()) {
            chip_selected[3] = true;
        } else{
            chip_selected[3] = false;
        }
        if (loblaws_chip.isChecked()) {
            chip_selected[0] = true;
        } else{
            chip_selected[0] = false;
        }
        if (metro_chip.isChecked()) {
            chip_selected[1] = true;
        } else{
            chip_selected[1] = false;
        }
        if (walmart_chip.isChecked()) {
            chip_selected[2] = true;
        } else{
            chip_selected[2] = false;
        }

        StringBuilder builder = new StringBuilder();
        for (int x=0;x<4;x++){
            if (chip_selected[x]) builder.append("1"); else builder.append("0");
        }

        customListview.getChipGroupFilter().filter(builder.toString());

        System.out.println("filter changed notified:   "+builder.toString());
    }
}
