import java.util.Random;
import java.util.Scanner;
import java.util.ArrayList;
import java.util.Collections;
import javax.swing.JOptionPane;

public class StatGen {
    public static void main(String[] args) {
        Random random = new Random();
        ArrayList<Integer> numbers = new ArrayList<>();

        final int lowest_stat_min = 5;
        final int lowest_stat_max = 9;
        final int highest_stat_min = 15;
        final int highest_stat_max = 17;
        final double average_max = 13;
        final double average_min = 12;

        int x = 4; 
        int y = 6; 

        int total = 10; 

        for (int j = 0; j < y; j++) { 
            total = 10; 
            for (int i = 0; i < x; i++) {
                int randomNumber = random.nextInt(6) + 1;

                if (randomNumber % 2 == 0) {
                    total += randomNumber; 
                } else {
                    total -= randomNumber;
                }
            }
            if (total < 1 || total > 20) {

                if (total < 1) 
                {
                    total = 1;
                    numbers.add(total); 
                }; 

                if (total > 20) 
                {
                    total = 20;
                    numbers.add(total); 
                } 

            } else {
                numbers.add(total);  
            }

            // Calculate the mean of the numbers in the list
            double mean = 0;
            if (!numbers.isEmpty()) {
                int sum = 0;
                for (int num : numbers) {
                    sum += num;
                }
                mean = (double) sum / numbers.size();
            }

            // Check if the mean is out of bounds
            if ( (numbers.size() == 6 && mean <= average_min) 
            || (numbers.size() == 6 && mean >= average_max) 
            || (numbers.size() == 6 && Collections.min(numbers) < lowest_stat_min) 
            || (numbers.size() == 6 && Collections.max(numbers) <= highest_stat_min)
            || (numbers.size() == 6 && Collections.min(numbers) >= lowest_stat_max)
            || (numbers.size() == 6 && Collections.max(numbers) > highest_stat_max)) {
                numbers.clear();
                j = -1; // Reset `j` to -1 so it becomes 0 after the next iteration of the loop
            } else {
            }
        }
        System.out.println("\nFinal: " + numbers);
    }
}