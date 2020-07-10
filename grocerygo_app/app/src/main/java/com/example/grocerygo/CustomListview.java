package com.example.grocerygo;

import android.app.Activity;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.AsyncTask;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Filter;
import android.widget.Filterable;
import android.widget.ImageView;
import android.widget.TextView;

import com.squareup.picasso.Picasso;


import java.io.IOException;
import java.io.InputStream;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;


public class CustomListview extends ArrayAdapter<Item> implements Filterable {
    Activity context;
    ArrayList<Item> items;
    ArrayList<Item> forFilter;
    private CustomeFilter customeFilter;

    public CustomeFilter getCustomeFilter() {
        if(customeFilter==null){
            customeFilter=new CustomeFilter();
        }
        return customeFilter;
    }

    public CustomListview(Activity context, ArrayList<Item> pro) {
        super(context, R.layout.activity_item_list_element,pro );

        this.context=context;
        this.items= pro;
        this.forFilter=pro;
    }

    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        View r=convertView;
        ViewHolder viewHolder=null;
        if(r==null){
            LayoutInflater layoutInflater=context.getLayoutInflater();
            r=layoutInflater.inflate(R.layout.activity_item_list_element,null,true);
            viewHolder=new ViewHolder(r);
            r.setTag(viewHolder);
        }
        else{
            viewHolder=(ViewHolder)r.getTag();
        }
        System.out.println("Position:   "+position);


        //Picasso.with(getContext()).load(items.get(position).getImg_src()).into(viewHolder.ivw);
        viewHolder.downloadImg(items.get(position).getImg_src());
        viewHolder.tvw1.setText(items.get(position).getItem_name());
        viewHolder.tvw2.setText(items.get(position).getItem_brand());

        return r;



    }

    class CustomeFilter extends Filter{
        @Override
        protected FilterResults performFiltering(CharSequence constraint){
            FilterResults results=new FilterResults();
            if(constraint!=null&&constraint.length()>0){
                constraint=constraint.toString().toLowerCase();
                ArrayList<Item> toPresent=new ArrayList<>();
                for(int x=0;x<forFilter.size();x++){
                    if(forFilter.get(x).getItem_name().toLowerCase().contains(constraint)){
                        Item p=new Item(forFilter.get(x));
                        toPresent.add(p);
                    }
                }
                results.count=toPresent.size();
                results.values=toPresent;
                System.out.println("Size:"+toPresent.size());
            }
            else{
                System.out.println("query not found:  "+constraint.toString());
                results.values=forFilter;
            }
            return results;
        }
        @Override
        protected  void publishResults(CharSequence constraint, FilterResults results){
            items=(ArrayList<Item>)results.values;
            notifyDataSetChanged();
        }


    }
    @Override
    public int getCount() {



        return items.size();
    }
    class ViewHolder{
        TextView tvw1;
        TextView tvw2;
        ImageView ivw;

        DownloadImageTask di;

        public void downloadImg(String img_url) {
            new DownloadImageTask((ImageView) ivw)
                    .execute(img_url);
        }

        ViewHolder(View v){
            tvw1=(TextView)v.findViewById(R.id.title);
            tvw2=(TextView)v.findViewById(R.id.description);
            ivw=(ImageView) v.findViewById(R.id.imageView);
        }
        private class DownloadImageTask extends AsyncTask<String, Void, Bitmap> {
            ImageView bmImage;

            public DownloadImageTask(ImageView bmImage) {
                this.bmImage = bmImage;
            }

            protected Bitmap doInBackground(String... urls) {
                String urldisplay = urls[0];
                System.out.println(urldisplay);
                Bitmap mIcon11 = null;
                try {
                    InputStream in = new java.net.URL(urldisplay).openStream();
                    mIcon11 = BitmapFactory.decodeStream(in);
                } catch (Exception e) {
                    Log.e("Error", e.getMessage());
                    e.printStackTrace();
                }
                return mIcon11;
            }

            protected void onPostExecute(Bitmap result) {
                bmImage.setImageBitmap(Bitmap.createScaledBitmap(result, 240, 240, false));
            }
        }


    }
}
