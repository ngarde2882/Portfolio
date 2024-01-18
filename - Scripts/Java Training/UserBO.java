import java.sql.SQLException;

public class UserBO {
    UserDAO userDao = new UserDAO();
    public void insertUser(User u) throws SQLException, ClassNotFoundException {
        String emailId = u.getEmailId();
        if(emailId.contains(".com")) {
            int result = userDao.insertUser(u);
            if(result>0)
                System.out.println("User inserted successfully");
            else
                System.out.println("User insertion failed");
        }
        else {
            System.out.println("Please enter a valid email Id");
        }
    }
    public void displayUserDetails() throws ClassNotFoundException {
        userDao.displayUserDetails();
    }
}