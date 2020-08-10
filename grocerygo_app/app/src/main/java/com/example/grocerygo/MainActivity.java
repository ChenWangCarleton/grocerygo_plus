package com.example.grocerygo;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.SearchView;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class MainActivity extends AppCompatActivity {
    private SearchView main_search_view;
    private Button button1;
    private Button button2;
    private Button button3;
    private Button button4;
    private Button button5;
    private Button button6;
    private Button button7;
    private Button button8;
    private ImageButton shoppingListButton;


    //public static ArrayList<Item>  items=new ArrayList<>();
    private Map<String, String> source_brand_map = new HashMap<String, String>();
    private Map<String, String> category_map = new HashMap<String, String>();
    public static GroceryGoDatabase ggDB;
    CategoryButtonClickListener categoryButtonClickListener = new CategoryButtonClickListener();
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        ggDB = GroceryGoDatabase.getInstance(this);
        new Initialization().start();// initialize

        main_search_view = (SearchView) findViewById(R.id.search_main);
        shoppingListButton = (ImageButton) findViewById(R.id.MyGroceryListButton);
        shoppingListButton.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view){
                Intent intent = new Intent(view.getContext(), my_cart.class);
                startActivity(intent);

            }
        });

        button1 = (Button) findViewById(R.id.categoryButton1);
        button1.setOnClickListener(categoryButtonClickListener);
        button2 = (Button) findViewById(R.id.categoryButton2);
        button2.setOnClickListener(categoryButtonClickListener);
        button3 = (Button) findViewById(R.id.categoryButton3);
        button3.setOnClickListener(categoryButtonClickListener);
        button4 = (Button) findViewById(R.id.categoryButton4);
        button4.setOnClickListener(categoryButtonClickListener);
        button5 = (Button) findViewById(R.id.categoryButton5);
        button5.setOnClickListener(categoryButtonClickListener);
        button6 = (Button) findViewById(R.id.categoryButton6);
        button6.setOnClickListener(categoryButtonClickListener);
        button7 = (Button) findViewById(R.id.categoryButton7);
        button7.setOnClickListener(categoryButtonClickListener);
        button8 = (Button) findViewById(R.id.categoryButton8);
        button8.setOnClickListener(categoryButtonClickListener);
        //ggDB.onetime();
    }
   /* public ArrayList<Item> filterByCategory(String category){
        ArrayList<Item> result = new ArrayList<>();
        for(int x=0;x<items.size();x++){
            if (items.get(x).getItem_category().equals(category_map.get(category))){
                result.add(items.get(x));
            }
        }
        return result;
    }*/
    class CategoryButtonClickListener implements View.OnClickListener {

        @Override
        public void onClick(View v) {

            Button b1 = (Button)v;
            Intent intent = new Intent(v.getContext(), DisplayItemListActivity.class);
            intent.putExtra("button_text", category_map.get(b1.getText().toString()));
            //intent.putExtra("item_list", (Serializable) filterByCategory(b1.getText().toString()));

            startActivity(intent);
        }

    }
    class Initialization extends Thread{

        public void run(){

            /*items.add(new Item("527","Organic Honeydew Melon","0","None","0","https://assets.shop.loblaws.ca/products_jpeg/20289708001/en/20289708001_lrg_1_@1x.jpg"));
            items.add(new Item("1430","Café blanc 3-en-1","1","None","0","https://assets.shop.loblaws.ca/products_jpeg/21094512/en/21094512_lrg_1_@1x.jpg"));
            items.add(new Item("6774","1/4 Rotisserie Chicken Dark Meat","2","None","0","https://assets.shop.loblaws.ca/products_jpeg/20116090/en/20116090_lrg_1_@1x.jpg"));
            items.add(new Item("4365","Ace Cheddar Onion Demi Baguette","3","ACE","0","https://assets.shop.loblaws.ca/products_jpeg/21018897/en/21018897_lrg_1_@1x.jpg"));
            items.add(new Item("249","Organic Yogurt, Mango Apricot","4","LIBERTE","0","https://assets.shop.loblaws.ca/products_jpeg/20790591001/en/20790591001_lrg_1_@1x.jpg"));
            items.add(new Item("7412","Ready Crust, Chocolate Pie Crust","5","KEEBLER","0","https://assets.shop.loblaws.ca/products_jpeg/20117311002/en/20117311002_lrg_1_@1x.jpg"));
            items.add(new Item("907","Plant Based Beefless Burgers, Plant-Based, Vegan","6","PRESIDENT'S CHOICE","0","https://assets.shop.loblaws.ca/products_jpeg/21179192/en/21179192_lrg_1_@1x.jpg"));
            items.add(new Item("5545","Premium Ice","7","None","0","https://assets.shop.loblaws.ca/products_jpeg/20158645/en/20158645_lrg_1_@1x.jpg"));
            items.add(new Item("31561","Cilantro","0","None","1","https://i5.walmartimages.ca/images/Large/094/548/6000200094548.jpg"));
            items.add(new Item("31961","Beck's Non-Alcoholic Beer","1","None","1","https://i5.walmartimages.ca/images/Large/243/783/243783.jpg"));
            items.add(new Item("31981","Molinaro's Pizza Dough","2","Molinaro's","1","https://i5.walmartimages.ca/images/Large/424/734/6000198424734.jpg"));
            items.add(new Item("32633","The Bakery White Crusty Loaf","3","The Bakery","1","https://i5.walmartimages.ca/images/Large/261/254/6000200261254.jpg"));
            items.add(new Item("31582","Pillsbury™ Original Crescents","4","Pillsbury","1","https://i5.walmartimages.ca/images/Large/625/347/6000201625347.jpg"));
            items.add(new Item("34959","Uncle Ben's Southern Chili Style Beans","5","None","1","https://i5.walmartimages.ca/images/Large/141/464/6000201141464.jpg"));
            items.add(new Item("32520","Maple Leaf Naturally Smoked Bacon","6","Maple Leaf","1","https://i5.walmartimages.ca/images/Large/219/406/999999-63100219406.jpg"));
            items.add(new Item("33031","Kinnikinnick Gluten Free Pie Crust 9 Inch","7","None","1","https://i5.walmartimages.ca/images/Large/124/421/6000200124421.jpg"));
            items.add(new Item("48970","Banana","0","None","2","https://product-images.metro.ca/images/hee/h5c/8872794652702.jpg"));
            items.add(new Item("54431","Natural Spring Water","1","ESKA","2","https://product-images.metro.ca/images/h41/hf4/9351392133150.jpg"));
            items.add(new Item("66443","Old-fashioned smoked ham","2","THE DELI-SHOP","2","https://product-images.metro.ca/images/h1f/h62/8820483719198.jpg"));
            items.add(new Item("59502","Baguette","3","PREMIÈRE MOISSON","2","https://product-images.metro.ca/images/h03/ha4/9252545560606.jpg"));
            items.add(new Item("49552","Large Eggs","4","SELECTION","2","https://product-images.metro.ca/images/h3e/h65/9398467985438.jpg"));
            items.add(new Item("50740","White vinegar","5","SELECTION","2","https://product-images.metro.ca/images/he6/h09/8854725820446.jpg"));
            items.add(new Item("56200","Medium Ground Beef, Value Pack","6","None","2","https://product-images.metro.ca/images/h61/h5b/9188501585950.jpg"));
            items.add(new Item("58181","Frozen chicken pot pie","7","ST-HUBERT","2","https://product-images.metro.ca/images/h3a/h0f/8821239021598.jpg"));*/

            source_brand_map.put("0","Loblaws");
            source_brand_map.put("1","Walmart");
            source_brand_map.put("2","Metro");

            category_map.put("0",getString(R.string.categoryButton1));
            category_map.put("1",getString(R.string.categoryButton2));
            category_map.put("2",getString(R.string.categoryButton3));
            category_map.put("3",getString(R.string.categoryButton4));
            category_map.put("4",getString(R.string.categoryButton5));
            category_map.put("5",getString(R.string.categoryButton6));
            category_map.put("6",getString(R.string.categoryButton7));
            category_map.put("7",getString(R.string.categoryButton8));
            category_map.put(getString(R.string.categoryButton1),"0");
            category_map.put(getString(R.string.categoryButton2),"1");
            category_map.put(getString(R.string.categoryButton3),"2");
            category_map.put(getString(R.string.categoryButton4),"3");
            category_map.put(getString(R.string.categoryButton5),"4");
            category_map.put(getString(R.string.categoryButton6),"5");
            category_map.put(getString(R.string.categoryButton7),"6");
            category_map.put(getString(R.string.categoryButton8),"7");
            /*category_map.put("0","Fruits & Vegetables");
            category_map.put("1","Drinks");
            category_map.put("2","Deli & Ready Made Meals");
            category_map.put("3","Bakery");
            category_map.put("4","Dairy & Eggs");
            category_map.put("5","Pantry");
            category_map.put("6","Meat & Seafood");
            category_map.put("7","Frozen");
            category_map.put("Fruits & Vegetables","0");
            category_map.put("Drinks","1");
            category_map.put("Deli & Ready Made Meals","2");
            category_map.put("Bakery","3");
            category_map.put("Dairy & Eggs","4");
            category_map.put("Pantry","5");
            category_map.put("Meat & Seafood","6");
            category_map.put("Frozen","7");*/


            /*InteractWithServer iws = new InteractWithServer();
            String content = iws.get_all();
            ids = getAllMatches(content,"\"item_id\": \"(.*?)\"");
            for(int x = 0;x<ids.size();x++){
                String temp=ids.get(x).replace("\"item_id\": \"", "");
                ids.set(x,temp.substring(0, temp.length()-1) );
            }

            names = getAllMatches(content,"\"item_name\": \"(.*?)\"");
            for(int x = 0;x<names.size();x++){
                String temp=names.get(x).replace("\"item_name\": \"", "");
                names.set(x,temp.substring(0, temp.length()-1) );
            }
            categories = getAllMatches(content,"\"category\": \"(.*?)\"");
            for(int x = 0;x<categories.size();x++){
                String temp=categories.get(x).replace("\"category\": \"", "");
                categories.set(x,temp.substring(0, temp.length()-1) );
            }
            itembrands = getAllMatches(content,"\"item_brand\": \"(.*?)\"");
            for(int x = 0;x<itembrands.size();x++){
                String temp=itembrands.get(x).replace("\"item_brand\": \"", "");
                itembrands.set(x,temp.substring(0, temp.length()-1) );
            }
            sourcebrands = getAllMatches(content,"\"source_brand\": \"(.*?)\"");
            for(int x = 0;x<sourcebrands.size();x++){
                String temp=sourcebrands.get(x).replace("\"source_brand\": \"", "");
                sourcebrands.set(x,temp.substring(0, temp.length()-1) );
            }
            imgsrcs = getAllMatches(content,"\"img_src\": \"(.*?)\"");
            for(int x = 0;x<imgsrcs.size();x++){
                String temp=imgsrcs.get(x).replace("\"img_src\": \"", "");
                imgsrcs.set(x,temp.substring(0, temp.length()-1) );
            }*/
            //items = new ArrayList<>();
            //ggDB.onetime();
            boolean initialized = false;
            ArrayList<String> versions = ggDB.getServerVersions();
            for(int x=0; x<versions.size();x++){
                System.out.println("server version get from db: "+ versions.get(x));
                if (versions.get(x).equals("test")){
                    initialized = true;
                }
            }
            if(!initialized){
                System.out.println("initializing servers!");
                load_data_from_resource_file();
                ggDB.addServerversion("test");
            }/*else{

                System.out.println("deleting dbs");
                ggDB.close();
                deleteDB();
            }*/

            System.out.println("server test done");

            System.out.println("all done initiallization");
        }
    }
    private void deleteDB(){
        this.deleteDatabase("GroceryGoDB");
    }
    public void load_data_from_resource_file(){
        String content = "";
        InputStream inputStream = getResources().openRawResource(R.raw.initial_data);
        BufferedReader bufferedReader= new BufferedReader(new InputStreamReader(inputStream));
        String eachline = null;
        try {
            while ((eachline = bufferedReader.readLine()) != null){
                content +=eachline;
            }
        } catch (IOException e) {
            e.printStackTrace();

        }
        if (content.equals("")){
            System.out.println("retreive data from raw resources failed");
            return;
        }
        System.out.println("raw resource loaded");
        ArrayList<String> ids = new ArrayList<>();
        ArrayList<String> names = new ArrayList<>();
        ArrayList<String> categories = new ArrayList<>();
        ArrayList<String> itembrands = new ArrayList<>();
        ArrayList<String> sourcebrands = new ArrayList<>();
        ArrayList<String> imgsrcs = new ArrayList<>();
        ids = getAllMatches(content,"\"item_id\": \"(.*?)\"");
        for(int x = 0;x<ids.size();x++){
            String temp=ids.get(x).replace("\"item_id\": \"", "");
            ids.set(x,temp.substring(0, temp.length()-1) );
        }

        names = getAllMatches(content,"\"item_name\": \"(.*?)\"");
        for(int x = 0;x<names.size();x++){
            String temp=names.get(x).replace("\"item_name\": \"", "");
            names.set(x,temp.substring(0, temp.length()-1) );
        }
        categories = getAllMatches(content,"\"category\": \"(.*?)\"");
        for(int x = 0;x<categories.size();x++){
            String temp=categories.get(x).replace("\"category\": \"", "");
            categories.set(x,temp.substring(0, temp.length()-1) );
        }
        itembrands = getAllMatches(content,"\"item_brand\": \"(.*?)\"");
        for(int x = 0;x<itembrands.size();x++){
            String temp=itembrands.get(x).replace("\"item_brand\": \"", "");
            itembrands.set(x,temp.substring(0, temp.length()-1) );
        }
        sourcebrands = getAllMatches(content,"\"source_brand\": \"(.*?)\"");
        for(int x = 0;x<sourcebrands.size();x++){
            String temp=sourcebrands.get(x).replace("\"source_brand\": \"", "");
            sourcebrands.set(x,temp.substring(0, temp.length()-1) );
        }
        imgsrcs = getAllMatches(content,"\"img_src\": \"(.*?)\"");
        for(int x = 0;x<imgsrcs.size();x++) {
            String temp = imgsrcs.get(x).replace("\"img_src\": \"", "");
            imgsrcs.set(x, temp.substring(0, temp.length() - 1));
        }
        System.out.println("writing to db");
        for (int x = 0; x<ids.size();x++){
            //items.add(new Item(ids.get(x),names.get(x),categories.get(x),itembrands.get(x),sourcebrands.get(x),imgsrcs.get(x)));
            ggDB.registerItem(ids.get(x),names.get(x),categories.get(x),itembrands.get(x),sourcebrands.get(x),imgsrcs.get(x));
        }
    }
    public  ArrayList<String> getAllMatches(String text, String regex) {
        ArrayList<String> matches = new ArrayList<String>();
        Matcher m = Pattern.compile("(?=(" + regex + "))").matcher(text);
        while(m.find()) {
            matches.add(m.group(1));
        }
        return matches;
    }
}