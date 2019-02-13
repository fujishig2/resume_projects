package com.example.cardiobook;

import android.content.Intent;
import android.graphics.Color;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.KeyEvent;
import android.view.View;
import android.view.inputmethod.EditorInfo;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

/**<p>Activity class that is used for editing and deleting blood pressures</p>
 * @author kyle
 * @version 1.0
 */
public class EditBP extends AppCompatActivity {
    public int position;
    public BPs BP;

    /**<p>onCreate method will be called first when this activity is called.</p>
     * @param savedInstanceState Bundle savedInstanceState
     */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_edit_bp);

        EditText editText = findViewById(R.id.comText2);
        final Button submit = findViewById(R.id.finishButton);

        editText.setOnEditorActionListener(new TextView.OnEditorActionListener() {
            /**<p>This method ensures that when the user presses the done button on the
             * keyboard, it will press the button which adds the measurement to the
             * main activity.
             *
             * Acknowledgements:
             * https://stackoverflow.com/questions/19217582/implicit-submit-after-hitting-done-on-the-keyboard-at-the-last-edittext</p>
             *
             * @param v TextView v
             * @param actionId int ID of the button pressed on the keyboard by the user.
             * @param event keyEvent event that caused this method to be called.
             * @return boolean value which is either true when the user presses done,
             *          or false otherwise.
             */
            @Override
            public boolean onEditorAction(TextView v, int actionId, KeyEvent event) {
                if ((event != null && (event.getKeyCode() == KeyEvent.KEYCODE_ENTER))
                        || (actionId == EditorInfo.IME_ACTION_DONE)) {
                    submit.performClick();
                }
                return false;
            }
        });

        /*This section gets the blood pressures from the intent sent from the
        main activity. Then it fills all the entry boxes with the values found
        from the BP that was sent in the intent.
         */
        Intent intent = getIntent();
        BP = (BPs)intent.getSerializableExtra("key");

        TextView textView = findViewById(R.id.dateText2);
        textView.setText(BP.getDay());

        textView = findViewById(R.id.timeText2);
        textView.setText(BP.getTime());

        textView = findViewById(R.id.sysText2);
        textView.setText(Integer.toString(BP.getSystolic()));

        textView = findViewById(R.id.diaText2);
        textView.setText(Integer.toString(BP.getDiastolic()));

        textView = findViewById(R.id.rateText2);
        textView.setText(Integer.toString(BP.getRate()));

        editText.setText(BP.getComment());

        position = BP.getPosition();
    }

    /**<p>onEditPressed gets called when the Update button gets pressed. This method
     * will create an abstract data type BPs BP, which will have all its entries
     * filled by the textviews inputs.</p>
     *
     * Sources used to create this method:
     * <url>https://stackoverflow.com/questions/18259644/how-to-check-if-a-string-matches-a-specific-format</url>
     *
     *
     * @param view View view
     */
    public void onEditPressed(View view) {
        Intent intent = new Intent(this, MainActivity.class);
        Boolean pass = Boolean.TRUE;

        /*Check to see if the entries inputted by the user are valid. This means
        we are checking to see if the date is in the format YYYY-MM-DD. If it
        isn't, we set the edittext background to red, and pass is set to false.
         */
        EditText text = findViewById(R.id.dateText2);
        String dateText = text.getText().toString();
        text.setBackgroundColor(Color.parseColor("#89520091"));
        if (!dateText.matches("\\d{4}-\\d{2}-\\d{2}")) {
            text.setBackgroundColor(Color.RED);
            pass = Boolean.FALSE;
        }

        /*Check to see if the entries inputted by the user are valid. This means
        we are checking to see if the time is in the format HH:MM. If it
        isn't, we set the edittext background to red, and pass is set to false.
         */
        text = findViewById(R.id.timeText2);
        String timeText = text.getText().toString();
        text.setBackgroundColor(Color.parseColor("#89520091"));
        if (!timeText.matches("\\d{2}:\\d{2}")) {
            text.setBackgroundColor(Color.RED);
            pass = Boolean.FALSE;
        }

        /*Check to see if the entries inputted by the user are valid. This means
        we are checking to see if the systolic is a non-negative integer. If it
        isn't, we set the edittext background to red, and pass is set to false.
         */
        text = findViewById(R.id.sysText2);
        int sysText = 0;
        text.setBackgroundColor(Color.parseColor("#89520091"));
        try {
            sysText = Integer.parseInt(text.getText().toString());
            if (sysText < 0) {
                text.setBackgroundColor(Color.RED);
                pass = Boolean.FALSE;
            }
        } catch (NumberFormatException e) {
            text.setBackgroundColor(Color.RED);
            pass = Boolean.FALSE;
        }

        /*Check to see if the entries inputted by the user are valid. This means
        we are checking to see if the diastolic is a non-negative integer. If it
        isn't, we set the edittext background to red, and pass is set to false.
         */
        text = findViewById(R.id.diaText2);
        int diaText = 0;
        text.setBackgroundColor(Color.parseColor("#89520091"));
        try {
            diaText = Integer.parseInt(text.getText().toString());
            if (diaText < 0) {
                text.setBackgroundColor(Color.RED);
                pass = Boolean.FALSE;
            }
        } catch (NumberFormatException e) {
            text.setBackgroundColor(Color.RED);
            pass = Boolean.FALSE;
        }

        /*Check to see if the entries inputted by the user are valid. This means
        we are checking to see if the heart rate is a non-negative integer. If it
        isn't, we set the edittext background to red, and pass is set to false.
         */
        text = findViewById(R.id.rateText2);
        int rateText = 0;
        text.setBackgroundColor(Color.parseColor("#89520091"));
        try {
            rateText = Integer.parseInt(text.getText().toString());
            if (rateText < 0) {
                text.setBackgroundColor(Color.RED);
                pass = Boolean.FALSE;
            }
        } catch (NumberFormatException e) {
            text.setBackgroundColor(Color.RED);
            pass = Boolean.FALSE;
        }

        //check to see if the comment text area is less than or equal to 20 characters
        //in length.
        text = findViewById(R.id.comText2);
        String comText = text.getText().toString();
        text.setBackgroundColor(Color.parseColor("#89520091"));
        if (comText.length() > 20) {
            text.setBackgroundColor(Color.RED);
            pass = Boolean.FALSE;
        }

        //if any of the entries caused pass to be false, add button won't finish. This
        //forces the user to input proper entries.
        if (pass == Boolean.FALSE)
            return;

        //create a new BP based off of the entries inputted. Place it in the intent using
        //putExtra method.
        if (comText.length() > 0) {
            BP = new AddBP(dateText, timeText, sysText, diaText, rateText, position, comText);
            intent.putExtra("editKey", BP);
        } else {
            BP = new AddBP(dateText, timeText, sysText, diaText, rateText, position);
            intent.putExtra("editKey", BP);
        }

        //https://www.dev2qa.com/passing-data-between-activities-android-tutorial/
        //used to understand and implement startActivityForResult.
        setResult(RESULT_OK, intent);
        finish();
    }

    /**<p>onDeletePressed gets called when the user presses the delete button. When this
     * happens, the entry that's been selected gets removed from the list of blood
     * pressures in the main activity. This is ensured by making the name entry in
     * putExtra the deletekey.</p>
     * @param view View view
     */
    public void onDeletePressed(View view) {
        Intent intent = new Intent(this, MainActivity.class);
        intent.putExtra("deleteKey", BP);
        setResult(RESULT_OK, intent);
        finish();
    }

    /**<p>Used to ensure that when the back button is pressed, we set the result
     * to be result canceled. This ensures no data will be changed.</p>
     */
    @Override
    public void onBackPressed() {
        Intent intent = new Intent();
        setResult(RESULT_CANCELED, intent);
        finish();
    }


}
