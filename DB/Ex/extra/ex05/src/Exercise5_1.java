import java.sql.*;
import java.util.Scanner;

public class Exercise5_1 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        //Ask for the user id and password
        System.out.println("User ID: ");
        String userID = sc.nextLine();
        System.out.println("Password: ");
        String passwd = sc.nextLine();
        try{
            Connection conn = DriverManager.getConnection("jdbc:postgresql://hera.hs-regensburg.de:5432/"+userID, userID, passwd);
            PreparedStatement preparedStatement;
            ResultSet resultSet;
            int rowCount = 0;
            do{
                //Ask for an input.
                System.out.println("Search Substring(id (if empty, it ends): ");
                String query = sc.nextLine();
                preparedStatement = conn.prepareStatement("select id name from ");
            }while(rowCount == 0);
        }catch(SQLException e){
            System.out.println("SQL Exception" + e);
        }

    }
}
