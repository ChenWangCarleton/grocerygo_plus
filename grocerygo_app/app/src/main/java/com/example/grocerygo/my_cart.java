package com.example.grocerygo;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.MotionEvent;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.PopupWindow;
import android.widget.TextView;

import java.io.IOException;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;

public class my_cart extends AppCompatActivity {
    private ArrayList<Item> items;

    private CustomListview customListview;
    private ListView list_view;
    private Button get_price_button;
    private Handler mHandler;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_my_cart);

        list_view = (ListView) findViewById(R.id.cartlistview);
        get_price_button = (Button) findViewById(R.id.getPriceButton);
        Intent intent = getIntent();
        items = new ArrayList<Item>();
        get_shopping_list_items();

        String temp_url = "http://10.0.2.2:5000/api/v1/price/byid?id=";
        String ids = "";
        for(int x=0;x<items.size();x++){
            ids = ids + items.get(x).getItem_id()+",";
        }
        final String http_url = temp_url + ids;


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
        get_price_button.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view){
                final View popup_view = onButtonShowPopupWindowClick(view, "getting price");
                mHandler = new Handler();
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        MakeHTTPRequest get_http_response = new MakeHTTPRequest();
                        try {
                            final String respond  = get_http_response.run(http_url);
                            mHandler.post(new Runnable() {
                                @Override
                                public void run() {
                                    if (popup_view != null){
                                        TextView tv = (TextView)popup_view.findViewById(R.id.get_price_text_view);
                                        tv.setText(respond);
                                    }
                                }
                            });
                        } catch (IOException e) {
                            e.printStackTrace();
                            final String todisplay  = "failed to get price";
                            mHandler.post(new Runnable() {
                                @Override
                                public void run() {
                                    if (popup_view != null){
                                        TextView tv = (TextView)popup_view.findViewById(R.id.get_price_text_view);
                                        tv.setText(todisplay);
                                    }
                                }
                            });
                        }


                    }
                }).start();



            }
        });
    }

    public void get_shopping_list_items(){
        items = MainActivity.ggDB.allItems();

    }

    public View onButtonShowPopupWindowClick(View view, String to_display) {

        // inflate the layout of the popup window
        LayoutInflater inflater = (LayoutInflater)
                getSystemService(LAYOUT_INFLATER_SERVICE);
        View popupView = inflater.inflate(R.layout.activity_popup, null);

        // modify the text for display
        TextView tv = (TextView)popupView.findViewById(R.id.get_price_text_view);
        tv.setText(to_display);

        // create the popup window
        int width = LinearLayout.LayoutParams.WRAP_CONTENT;
        int height = LinearLayout.LayoutParams.WRAP_CONTENT;
        boolean focusable = true; // lets taps outside the popup also dismiss it
        final PopupWindow popupWindow = new PopupWindow(popupView, width, height, focusable);

        // show the popup window
        // which view you pass in doesn't matter, it is only used for the window tolken
        popupWindow.showAtLocation(view, Gravity.CENTER, 0, 0);

        // dismiss the popup window when touched
        popupView.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                popupWindow.dismiss();
                return true;
            }
        });
        return popupView;
    }
}