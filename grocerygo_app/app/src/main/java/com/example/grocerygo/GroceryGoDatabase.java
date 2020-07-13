package com.example.grocerygo;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

import java.util.ArrayList;

public class GroceryGoDatabase extends SQLiteOpenHelper{
    private static final int DATABASE_VERSION = 1;
    private static final String DATABASE_NAME = "GroceryGoDB";

    private static final String TABLE_NAME = "GroceryGoShoppingList";
    private static final String KEY_ID = "item_id";

    private static final String KEY_QUENTITY = "quantity";
    private static final String[] COLUMNS = { KEY_ID, KEY_QUENTITY};

    private static final String ITEM_TABLE = "GroceryGoItem";
    private static final String ggcart="GGCart";

    String ii = "item_id";
    String in = "item_name";
    String ic = "item_category";
    String ib = "item_brand";
    String sb = "source_brand";
    String is = "img_src";
    String quan = "quantity";
    String[] columns = {ii,in,ic,ib,sb,is};
    String[] cartcolumns = {ii,in,ic,ib,sb,is,quan};
    public GroceryGoDatabase(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
    }
    @Override
    public void onCreate(SQLiteDatabase db) {
        String CREATION_TABLE = "CREATE TABLE GroceryGoShoppingList ( "
                + "item_id VARCHAR PRIMARY KEY, " + "quantity INTEGER)";

        db.execSQL(CREATION_TABLE);

    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        // you can implement here migration process
        db.execSQL("DROP TABLE IF EXISTS " + TABLE_NAME);
        this.onCreate(db);
    }
    public void onetime(){
        //String CREATION_TABLE2 = "CREATE TABLE GroceryGoItem ( "
        String CREATION_TABLE2 = "CREATE TABLE GGCart ( "
                + "item_id VARCHAR PRIMARY KEY, " + "item_name VARCHAR, item_category VARCHAR, item_brand VARCHAR,  source_brand VARCHAR, img_src VARCHAR, quantity INTEGER)";
        SQLiteDatabase db = this.getWritableDatabase();
        db.execSQL(CREATION_TABLE2);
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
        db.insert(ITEM_TABLE,null, values);
        db.close();

        //System.out.println("added to db: "+item.toString());
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
        values.put(KEY_QUENTITY, quantity);
        // insert
        db.insert(ggcart,null, values);
        db.close();

        System.out.println("added to db: "+item.toString());
    }
    public ArrayList<Item> getByCategory(String category){
        ArrayList<Item> result = new ArrayList<>();
        String selection = ic + " = ?";
        String[] selectionArgs = {category};
        SQLiteDatabase db = this.getWritableDatabase();
        Cursor cursor = db.query(ITEM_TABLE,columns,selection,selectionArgs,null,null,null);

        if (cursor.moveToFirst()) {
            do {
                result.add(new Item(cursor.getString(0),cursor.getString(1),cursor.getString(2),cursor.getString(3),cursor.getString(4),cursor.getString(5)));

            } while (cursor.moveToNext());
        }
        return result;
    }
    public ArrayList<Item> allItems() {

        ArrayList<Item> shoppingList = new ArrayList<Item>();

        SQLiteDatabase db = this.getWritableDatabase();
        Cursor cursor = db.query(ggcart,cartcolumns,null,null,null,null,null);

        if (cursor.moveToFirst()) {
            do {
                shoppingList.add(new Item(cursor.getString(0),cursor.getString(1),cursor.getString(2),cursor.getString(3),cursor.getString(4),cursor.getString(5)));
                System.out.println("quantity: "+cursor.getString(6));

            } while (cursor.moveToNext());
        }

        return shoppingList;
    }
}
