package com.example.grocerygo;

import java.io.Serializable;

public class Item implements Serializable {
    private String item_id;
    private String item_name;
    private String item_category;
    private String item_brand;
    private String source_brand;
    private String price;
    private String img_src;
    private String description;
    private String ingredient;

    public Item(Item source) {
        this.item_id = source.getItem_id();
        this.item_name = source.getItem_name();
        this.item_category = source.getItem_category();
        this.item_brand = source.getItem_brand();
        this.source_brand = source.getSource_brand();
        this.img_src = source.getImg_src();
    }

    public Item(String item_id, String item_name, String item_category, String item_brand, String source_brand, String img_src) {
        this.item_id = item_id;
        this.item_name = item_name;
        this.item_category = item_category;
        this.item_brand = item_brand;
        this.source_brand = source_brand;
        this.img_src = img_src;
    }

    public void fill_missing_attributes(String price, String description, String ingredient) {
        this.price = price;
        this.description = description;
        this.ingredient = ingredient;
    }

    @Override
    public String toString() {
        return "Item{" +
                "item_id='" + item_id + '\'' +
                ", item_name='" + item_name + '\'' +
                ", item_category='" + item_category + '\'' +
                ", item_brand='" + item_brand + '\'' +
                ", source_brand='" + source_brand + '\'' +
                ", price='" + price + '\'' +
                ", img_src='" + img_src + '\'' +
                ", description='" + description + '\'' +
                ", ingredient='" + ingredient + '\'' +
                '}';
    }

    public String getItem_id() {
        return item_id;
    }

    public void setItem_id(String item_id) {
        this.item_id = item_id;
    }

    public String getItem_name() {
        return item_name;
    }

    public void setItem_name(String item_name) {
        this.item_name = item_name;
    }

    public String getItem_category() {
        return item_category;
    }

    public void setItem_category(String item_category) {
        this.item_category = item_category;
    }

    public String getItem_brand() {
        return item_brand;
    }

    public void setItem_brand(String item_brand) {
        this.item_brand = item_brand;
    }

    public String getSource_brand() {
        return source_brand;
    }

    public void setSource_brand(String source_brand) {
        this.source_brand = source_brand;
    }

    public String getPrice() {
        return price;
    }

    public void setPrice(String price) {
        this.price = price;
    }

    public String getImg_src() {
        return img_src;
    }

    public void setImg_src(String img_src) {
        this.img_src = img_src;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getIngredient() {
        return ingredient;
    }

    public void setIngredient(String ingredient) {
        this.ingredient = ingredient;
    }

}
