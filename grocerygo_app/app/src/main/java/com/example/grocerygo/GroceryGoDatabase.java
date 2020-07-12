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
    public void addItem(Item item, int quantity) {
        SQLiteDatabase db = this.getWritableDatabase();
        ContentValues values = new ContentValues();
        values.put(KEY_ID, item.getItem_id());
        values.put(KEY_QUENTITY, quantity);
        // insert
        db.insert(TABLE_NAME,null, values);
        db.close();

        System.out.println("added to db: "+item.toString());
    }
    public ArrayList<String> allItems() {

        ArrayList<String> shoppingList = new ArrayList<String>();
        String query = "SELECT  * FROM " + TABLE_NAME;
        SQLiteDatabase db = this.getWritableDatabase();
        Cursor cursor = db.rawQuery(query, null);

        if (cursor.moveToFirst()) {
            do {
                shoppingList.add(cursor.getString(0));
                System.out.println("quantity: "+cursor.getString(1));

            } while (cursor.moveToNext());
        }

        return shoppingList;
    }
}
