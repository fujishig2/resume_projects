package com.example.cardiobook;

import android.support.annotation.NonNull;

import java.io.Serializable;

/**<p>BPs is an abstract data type which holds all the information on a blood pressure
 * entry. It implements serializable because if it can be serialized, it can be sent
 * to various activities using intent.putExtra() and received using
 * intent.getSerializableExtra()
 *
 * Acknowledgements:
 *<url>https://www.techjini.com/blog/passing-objects-via-intent-in-android/</url></p>
 *
 * @see Serializable
 */
public abstract class BPs implements Serializable {

    private String day;
    private String time;
    private int systolic;
    private int diastolic;
    private int rate;
    private String comment;
    private int position;

    /**<p>getDay is used to get the date of this particular blood pressure entry.</p>
     * @return day Returns the date
     */
    public String getDay() {
        return day;
    }

    /**<p>setDay is used to set the date of this particular blood pressure entry.</p>
     * @param day day to be entered by the user.
     */
    public void setDay(String day) {
        this.day = day;
    }

    /**<p>getTime is used to get the time of this particular blood pressure entry.</p>
     * @return time Returns the time.
     */
    public String getTime() {
        return time;
    }

    /**<p>setTime is used to set the time of this particular blood pressure entry.</p>
     * @param time time to be entered by the user.
     */
    public void setTime(String time) {
        this.time = time;
    }

    /**<p>getRate is used to get the heart rate of this particular blood pressure entry.</p>
     * @return rate Returns the heart rate.
     */
    public int getRate() {
        return rate;
    }

    /**<p>setRate is used to set the heart rate of this particular blood pressure entry.</p>
     * @param rate heart rate to be entered by the user.
     * @see InvalidInt
     */
    public void setRate(int rate) throws InvalidInt {
        if(rate >= 0){
            this.rate = rate;
        }
        else {
            throw new InvalidInt();
        }
    }

    /**<p>getSystolic is used to get the systolic pressure of this particular blood
     * pressure entry.</p>
     * @return systolic Returns the Systolic pressure.
     */
    public int getSystolic() {
        return systolic;
    }

    /**<p>setSystolic is used to set the systolic pressure of this particular blood
     * pressure entry.</p>
     * @param systolic systolic pressure to be entered by the user.
     * @see InvalidInt
     */
    public void setSystolic(int systolic) throws InvalidInt {
        if (systolic >= 0) {
            this.systolic = systolic;
        }
        else {
            throw new InvalidInt();
        }
    }

    /**<p>getDiastolic is used to get the diastolic pressure of this particular blood
     * pressure entry.</p>
     * @return diastolic Returns the Diastolic pressure.
     */
    public int getDiastolic() {
        return diastolic;
    }

    /**<p>setDiastolic is used to set the diastolic pressure of this particular blood
     * pressure entry.</p>
     * @param diastolic diastolic pressure to be entered by the user.
     * @see InvalidInt
     */
    public void setDiastolic(int diastolic) throws InvalidInt {
        if (diastolic >= 0) {
            this.diastolic = diastolic;
        }
        else {
            throw new InvalidInt();
        }
    }

    /**<p>getComment is used to get the comment of this particular blood pressure entry.</p>
     * @return comment Returns the comment.
     */
    public String getComment() {
        return comment;
    }

    /**<p>setComment is used to set the comment of this particular blood pressure entry.</p>
     * @param comment comment to be entered by the user.
     * @see InvalidInt
     */
    public void setComment(String comment) throws InvalidInt{
        if (comment.length() <= 20) {
            this.comment = comment;
        }
        else {
            throw new InvalidInt();
        }
    }

    /**<p>getPosition is used to get the current position/index of this particular blood
     * pressure entry.</p>
     * @return position Returns the position/index of this BP.
     */
    public int getPosition() {
        return position;
    }

    /**<p>setPosition is used to set the current position/index of this particular blood
     * pressure entry.</p>
     * @param position position/index of this BP.
     */
    public void setPosition(int position) {
        this.position = position;
    }

    /**<p>Method used to create a new BP entry. Calling this method will create a new
     * BP with its comment blank.</p>
     * @param day date of the new BP to be entered
     * @param time time of the new BP to be entered
     * @param systolic systolic pressure of the new BP to be entered
     * @param diastolic diastolic pressure of the new BP to be entered
     * @param rate heart rate of the new BP to be entered
     * @param position position of the new BP to be entered
     */
    public BPs (String day, String time, int systolic, int diastolic,
                int rate, int position) {
        this.setDay(day);
        this.setTime(time);
        this.setSystolic(systolic);
        this.setDiastolic(diastolic);
        this.setRate(rate);
        this.setPosition(position);
        this.setComment("");
    }

    /**<p>Method used to create a new BP entry. Calling this method will create a new BP.</p>
     * @param day date of the new BP to be entered
     * @param time time of the new BP to be entered
     * @param systolic systolic pressure of the new BP to be entered
     * @param diastolic diastolic pressure of the new BP to be entered
     * @param rate heart rate of the new BP to be entered
     * @param position position of the new BP to be entered
     * @param comment comment of the new BP to be entered
     */
    public BPs (String day, String time, int systolic, int diastolic,
                int rate, int position, String comment) {
        this.setDay(day);
        this.setTime(time);
        this.setSystolic(systolic);
        this.setDiastolic(diastolic);
        this.setRate(rate);
        this.setPosition(position);
        this.setComment(comment);
    }


    /**<p>toString will return the current BP in a string format</p>
     * @return BP entry converted to string in an easy to read format
     */
    @NonNull
    @Override
    public String toString() {
        if (comment.length() > 0) {
            return "Date: " + day + " " + time + " | Systolic: "
                    + systolic + " | Diastolic: " + diastolic
                    + " | Heart rate: " + rate + " | Comment: " + comment;
        }
        else {
            return "Date: " + day + " " + time + " | Systolic: "
                    + systolic + " | Diastolic: " + diastolic
                    + " | Heart rate: " + rate;
        }

    }
}
