package com.example.grocerygo;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

import java.util.ArrayList;

public class GroceryGoDatabase extends SQLiteOpenHelper{
    private static final int DATABASE_VERSION = 2;
    private static final String DATABASE_NAME = "GroceryGoDB";

    private static final String SHOPPTINGLIST_TABLE_NAME = "GroceryGoShoppingList";
    private static final String ITEM_TABLE_NAME = "GroceryGoItem";
    private static final String APP_INFO_TABLE_NAME = "GroceryAppInfo";

    private static GroceryGoDatabase mInstance = null;

    private static final String CART_ITEM_TABLE_NAME="GGCart";
    private String sv = "server_version";
    private String ii = "item_id";
    private String in = "item_name";
    private String ic = "item_category";
    private String ib = "item_brand";
    private String sb = "source_brand";
    private String is = "img_src";
    private String quan = "quantity";
    private String[] app_info_columns = {sv};
    private String[] item_columns = {ii,in,ic,ib,sb,is};
    private String[] cart_columns = {ii,in,ic,ib,sb,is,quan};
    //https://stackoverflow.com/questions/18147354/sqlite-connection-leaked-although-everything-closed/18148718#18148718
    public static GroceryGoDatabase getInstance(Context ctx) {

        // Use the application context, which will ensure that you
        // don't accidentally leak an Activity's context.
        // See this article for more information: http://bit.ly/6LRzfx
        if (mInstance == null) {
            mInstance = new GroceryGoDatabase(ctx.getApplicationContext());
        }
        return mInstance;
    }

    private GroceryGoDatabase(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
    }
    @Override
    public void onCreate(SQLiteDatabase db) {
        String CREATION_CART_TABLE = "CREATE TABLE " +SHOPPTINGLIST_TABLE_NAME + " ( "
                + "item_id VARCHAR PRIMARY KEY, " + "quantity INTEGER)";
        String CREATION_CART_ITEM_TABLE = "CREATE TABLE " + CART_ITEM_TABLE_NAME + " ( "
                + "item_id VARCHAR PRIMARY KEY, " + "item_name VARCHAR, item_category VARCHAR, item_brand VARCHAR,  source_brand VARCHAR, img_src VARCHAR, quantity INTEGER)";
        String CREATION_ITEM_TABLE = "CREATE TABLE "+ ITEM_TABLE_NAME +" ( "
                + "item_id VARCHAR PRIMARY KEY, " + "item_name VARCHAR, item_category VARCHAR, item_brand VARCHAR,  source_brand VARCHAR, img_src VARCHAR)";
        String CREATION_APP_INFO_TABLE = "CREATE TABLE "+ APP_INFO_TABLE_NAME +" ( "
                + "server_version VARCHAR PRIMARY KEY) ";
        db.execSQL(CREATION_CART_TABLE);
        db.execSQL(CREATION_CART_ITEM_TABLE);
        db.execSQL(CREATION_ITEM_TABLE);
        db.execSQL(CREATION_APP_INFO_TABLE);

    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        // you can implement here migration process
        db.execSQL("DROP TABLE IF EXISTS "+SHOPPTINGLIST_TABLE_NAME);
        db.execSQL("DROP TABLE IF EXISTS "+CART_ITEM_TABLE_NAME);
        db.execSQL("DROP TABLE IF EXISTS "+ITEM_TABLE_NAME);
        db.execSQL("DROP TABLE IF EXISTS "+APP_INFO_TABLE_NAME);

        this.onCreate(db);
    }



    public void registerItem(String item_id, String item_name, String category, String item_brand, String source_brand, String img_src){
        SQLiteDatabase db = this.getWritableDatabase();
        ContentValues values = new ContentValues();
        values.put(ii, item_id);
        values.put(in, item_name);
        values.put(ic, category);
        values.put(ib, item_brand);
        values.put(sb, source_brand);
        values.put(is, img_src);
        // insert
        db.insertWithOnConflict(ITEM_TABLE_NAME,null, values,SQLiteDatabase.CONFLICT_IGNORE);
        //db.close();

        //System.out.println("added to db: "+item.toString());
    }
    public void addServerversion(String Server_version){
        SQLiteDatabase db = this.getWritableDatabase();
        ContentValues values = new ContentValues();
        values.put(sv, Server_version);
        db.insertWithOnConflict(APP_INFO_TABLE_NAME,null, values,SQLiteDatabase.CONFLICT_IGNORE);
    }
    public ArrayList<String> getServerVersions(){
        ArrayList<String> server_versions = new ArrayList<String>();

        SQLiteDatabase db = this.getReadableDatabase();
        Cursor cursor = db.query(APP_INFO_TABLE_NAME,app_info_columns,null,null,null,null,null);

        if (cursor.moveToFirst()) {
            do {
                String server_version = cursor.getString(0);
                server_versions.add(server_version);
                System.out.println("server_version: "+server_version);

            } while (cursor.moveToNext());
        }
        cursor.close();
        //db.close();
        return server_versions;
    }
    public void addItem(Item item, int quantity) {
        SQLiteDatabase db = this.getWritableDatabase();
        ContentValues values = new ContentValues();
        values.put(ii, item.getItem_id());
        values.put(in, item.getItem_name());
        values.put(ic, item.getItem_category());
        values.put(ib, item.getItem_brand());
        values.put(sb, item.getSource_brand());
        values.put(is, item.getImg_src());
        values.put(quan, quantity);
        // insert
        db.insertWithOnConflict(CART_ITEM_TABLE_NAME,null, values,SQLiteDatabase.CONFLICT_IGNORE);
        //db.close();

        System.out.println("added to db: "+item.toString());
    }
    public ArrayList<Item> getByCategory(String category){
        ArrayList<Item> result = new ArrayList<>();
        String selection = ic + " = ?";
        String[] selectionArgs = {category};
        SQLiteDatabase db = this.getReadableDatabase();
        Cursor cursor = db.query(ITEM_TABLE_NAME,item_columns,selection,selectionArgs,null,null,null);

        if (cursor.moveToFirst()) {
            do {
                result.add(new Item(cursor.getString(0),cursor.getString(1),cursor.getString(2),cursor.getString(3),cursor.getString(4),cursor.getString(5)));

            } while (cursor.moveToNext());
        }
        cursor.close();
        //https://stackoverflow.com/questions/23293572/android-cannot-perform-this-operation-because-the-connection-pool-has-been-clos/23293930?noredirect=1#23293930
        //db.close();
        return result;
    }
    public ArrayList<Item> allItems() {

        ArrayList<Item> shoppingList = new ArrayList<Item>();

        SQLiteDatabase db = this.getReadableDatabase();
        Cursor cursor = db.query(CART_ITEM_TABLE_NAME,cart_columns,null,null,null,null,null);

        if (cursor.moveToFirst()) {
            do {
                shoppingList.add(new Item(cursor.getString(0),cursor.getString(1),cursor.getString(2),cursor.getString(3),cursor.getString(4),cursor.getString(5)));
                System.out.println("quantity: "+cursor.getString(6));

            } while (cursor.moveToNext());
        }
        cursor.close();
        //db.close();
        return shoppingList;
    }
}
