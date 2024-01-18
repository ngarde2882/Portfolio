import java.io.*;

public class Main {
    public static void main(String[] args) throws ClassNotFoundException, NumberFormatException, IOException, SQLException {
        // TODO Auto-generated method stub
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int choice = 0;
        UserBO userBo = new UserBO();
        do {
            System.out.println("Select menu\n1. Insert user\n2. Display User details\n3. Exit");
            choice = Integer.parseInt(br.readLine());
            if(choice == 1) {
                System.out.println("Enter user id: ");
                int id = Integer.parseInt(br.readLine());
                System.out.println("Enter user name: ");
                String name = br.readLine();
                System.out.println("Enter user Email id: ");
                String emailId = br.readLine();
                System.out.println("Enter user contact no: ");
                long contactNo = Long.parseLong(br.readLine());
                User u = new User(id, name, emailId, contactNo);
                userBo.insertUser(u);
            }
            if(choice==2) {
                userBo.displayUserDetails();
            }
        }while(choice!=3);
    }
}