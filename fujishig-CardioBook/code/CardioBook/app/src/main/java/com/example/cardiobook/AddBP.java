package com.example.cardiobook;

/**<p>AddBP is used to add a new blood pressure entry by using the abstract data
 * type BPs. It can either be called with a comment or without a comment.</p>
 * @author kyle
 * @version 1.0
 * @see BPs
 */
public class AddBP extends BPs {

    /**<p>AddBP is used to add a new blood pressure entry by using the abstract data
     * type BPs. This will make a new BP without a comment.</p>
     * @param day date of the new BP to be entered
     * @param time time of the new BP to be entered
     * @param systolic systolic pressure of the new BP to be entered
     * @param diastolic diastolic pressure of the new BP to be entered
     * @param rate heart rate of the new BP to be entered
     * @param position position of the new BP to be entered
     * @throws InvalidInt exception called when entry is invalid
     */
    public AddBP(String day, String time, int systolic,
                 int diastolic, int rate, int position) throws InvalidInt{
        super(day, time, systolic, diastolic, rate, position);
    }

    /**<p>AddBP is used to add a new blood pressure entry by using the abstract data
     * type BPs. This will make a new BP with a comment.</p>
     * @param day date of the new BP to be entered
     * @param time time of the new BP to be entered
     * @param systolic systolic pressure of the new BP to be entered
     * @param diastolic diastolic pressure of the new BP to be entered
     * @param rate heart rate of the new BP to be entered
     * @param position position of the new BP to be entered
     * @param comment comment of the new BP to be entered
     * @throws InvalidInt
     */
    public AddBP(String day, String time, int systolic,
                 int diastolic, int rate, int position, String comment) throws InvalidInt{
        super(day, time, systolic, diastolic, rate, position, comment);
    }

}
