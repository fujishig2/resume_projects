package com.example.cardiobook;

import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.List;

/**<p>Main activity class/app home screen
 *
 * Sources used to create this entire app:
 * <url>https://medium.com/mindorks/custom-array-adapters-made-easy-b6c4930560dd</url>,
 * <url>https://android--code.blogspot.com/2015/08/android-listview-text-color.html</url>,
 * <url>https://stackoverflow.com/questions/19217582/implicit-submit-after-hitting-done-on-the-keyboard-at-the-last-edittext</url>,
 * <url>https://android--code.blogspot.com/2015/08/android-listview-item-click.html</url>,
 * <url>https://www.dev2qa.com/passing-data-between-activities-android-tutorial/</url>,
 * <url>https://www.techjini.com/blog/passing-objects-via-intent-in-android/</url>
 * <url>https://stackoverflow.com/questions/18259644/how-to-check-if-a-string-matches-a-specific-format</url></p>
 *
 *
 * @author kyle
 * @version 1.0
 */
public class MainActivity extends AppCompatActivity {

    /**<p>MyArrayAdapter has been formally made like this to ensure that entries in
     * the listview can have their background colours changed, depending on
     * information given.
     *
     * Acknowledgements:
     * <url>https://medium.com/mindorks/custom-array-adapters-made-easy-b6c4930560dd</url>,
     * <url>https://android--code.blogspot.com/2015/08/android-listview-text-color.html</url></p>
     *
     * @author kyle
     * @version 1.0
     */
    public class MyArrayAdapter extends ArrayAdapter<BPs> {
        private Context mContext;
        private List<BPs> BPList = new ArrayList<>();

        /** <p>When called, it makes mContext equal to the context, and BPList equal to list.</p>
         * @param context
         * @param res
         * @param list
         */
        public MyArrayAdapter(Context context, int res, ArrayList<BPs> list) {
            super (context, res, list);
            mContext = context;
            BPList = list;
        }

        /**<p>Used to ensure that the background colour of an entry is red when there's
         * a blood pressure entry that isn't healthy/normal. Otherwise it'll be green.
         * @param position Position in the arrayadapter list</p>
         * @param convertView
         * @param parent
         * @return row BP entry
         */
        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            View row = super.getView(position, convertView, parent);

            if (getItem(position).getSystolic() > 140
                    || getItem(position).getSystolic() < 90
                    || getItem(position).getDiastolic() > 90
                    || getItem(position).getDiastolic() < 60) {
                row.setBackgroundColor(Color.RED);
            } else {
                row.setBackgroundColor(Color.GREEN);
            }
            return row;
        }
    }

    private static final int addCode = 1;
    private static final int editCode = 2;
    private static final String FILENAME = "file.sav";
    private ArrayList<BPs> list;
    private MyArrayAdapter adapter;
    private ListView BPList;

    /**<p>onCreate method will be called first when this activity is created.</p>
     * @param savedInstanceState Bundle savedInstanceState
     */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        list = new ArrayList<>();
        BPList = findViewById(R.id.BPList);
        BPList.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            /**<p>onItemClick is called when an item in the listview within the main activity gets
             * called. This means when a user clicks an item in the main page, this method gets
             * called.
             *
             * Acknowledgements:
             * https://android--code.blogspot.com/2015/08/android-listview-item-click.html</p>
             *
             * @param parent the adapterview of the current adapter.
             * @param view View
             * @param position index/position of item that was clicked by user.
             * @param id
             */
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                BPs BP = (BPs) parent.getItemAtPosition(position);
                BP.setPosition(position);
                Intent intent = new Intent(MainActivity.this, EditBP.class);
                intent.putExtra("key", BP);
                //https://www.dev2qa.com/passing-data-between-activities-android-tutorial/
                //used to understand and implement startActivityForResult.
                startActivityForResult(intent, editCode);
            }
        });
    }

    /**<p>AddMeasurement is called when a user pressed the add button. This changes
     * the current activity to the add activity, where a user can input an
     * activity to add.</p>
     * @param view
     */
    public void AddMeasurement(View view){
        Intent intent = new Intent(this, Measurements.class);
        //https://www.dev2qa.com/passing-data-between-activities-android-tutorial/
        //used to understand and implement startActivityForResult.
        startActivityForResult(intent, addCode);
    }

    /**<p>onActivityResult is called when an activity that has been invoked using
     * startActivityForResult has finished. Depending on which activity was
     * previously being used, an entry will either be added, edited or deleted.
     *
     * Acknowledgements:
     * <url>https://www.dev2qa.com/passing-data-between-activities-android-tutorial/</url></p>
     *
     * @param actCode Code of the activity that was called. Either addCode or
     *               editCode.
     * @param resultCode Result of the activity that was called.
     * @param intent intent that was passed from the activity that was called
     */
    @Override
    public void onActivityResult(int actCode, int resultCode, Intent intent) {
        if (actCode == addCode) {
            if (resultCode == RESULT_OK) {
                BPList = findViewById(R.id.BPList);
                BPs BP = (BPs) intent.getSerializableExtra("key");
                list.add(BP);
                adapter = new MyArrayAdapter(this, R.layout.list_view, list);
                saveInFile();
                BPList.setAdapter(adapter);
                adapter.notifyDataSetChanged();
            }
        } else if(actCode == editCode) {
            if (resultCode == RESULT_OK) {
                BPList = findViewById(R.id.BPList);
                //check to see if the key that was called was either the edit key or delete key.
                if (intent.hasExtra("editKey")) {
                    BPs BP = (BPs) intent.getSerializableExtra("editKey");
                    list.set(BP.getPosition(), BP);
                    adapter = new MyArrayAdapter(this, R.layout.list_view, list);
                    saveInFile();
                    BPList.setAdapter(adapter);
                    adapter.notifyDataSetChanged();
                }

                else if(intent.hasExtra("deleteKey")) {
                    BPs BP = (BPs) intent.getSerializableExtra("deleteKey");
                    list.remove(BP.getPosition());
                    adapter = new MyArrayAdapter(this, R.layout.list_view, list);
                    saveInFile();
                    BPList.setAdapter(adapter);
                    adapter.notifyDataSetChanged();
                }
            }
        }
    }

    /**<p>loadFromFile does exactly what it sounds like it does. It loads data
     * from the file FILENAME. It then inputs the data into the arraylist.</p>
     */
    private void loadFromFile() {
        try {
            FileInputStream fis = openFileInput(FILENAME);
            BufferedReader in = new BufferedReader(new InputStreamReader(fis));
            Gson gson = new Gson();
            Type listType = new TypeToken<ArrayList<AddBP>>() {}.getType();
            list = gson.fromJson(in, listType);
        } catch (FileNotFoundException e) {
            // TODO Auto-generated catch block
            list = new ArrayList<>();
        }
    }

    /**<p>saveInFile saves the ArrayList data into a file at FILENAME.</p>
     *
     */
    private void saveInFile() {
        try {
            FileOutputStream fos = openFileOutput(FILENAME,
                    0);
            OutputStreamWriter writer = new OutputStreamWriter(fos);
            Gson gson = new Gson();
            gson.toJson(list, writer);
            writer.flush();
            fos.close();
        } catch (FileNotFoundException e) {
            throw new RuntimeException(e);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }


    /**<p>onStart is called when the main activity page gets loaded after it was
     * previously created once before. In this onStart method, we ensure that
     * we are loading the data from the file, and setting up the arrayadapter.</p>
     */
    @Override
    protected void onStart() {
        // TODO Auto-generated method stub
        super.onStart();
        loadFromFile();
        adapter = new MyArrayAdapter(this, R.layout.list_view, list);
        BPList.setAdapter(adapter);
        adapter.notifyDataSetChanged();
    }


}
