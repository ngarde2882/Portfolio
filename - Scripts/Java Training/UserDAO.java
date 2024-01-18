import java.sql.*;

public class UserDAO {
    public int insertUser(User u) throws SQLException, ClassNotFoundException {
        Connection con = DBConnection.getConnection();
        Statement stmt = con.createStatement();
        int i = stmt.executeUpdate("insert into user values("+u.getId()+",'"+u.getName()+"','"+u.getEmailId()+"',"+u.getContactNo()+")");
        return i;
    }
    public void displayUserDetails() throws ClassNotFoundException {
        try{
            Connection con = DBConnection.getConnection();
            Statement stmt = con.createStatement();
            ResultSet rs = stmt.executeQuery("select * from user");
            while(rs.next())
            System.out.println(rs.getInt(1)+"  "+rs.getString(2)+"  "+rs.getString(3)+"  "+rs.getLong(4));
            con.close();
        }
        catch(Exception e) {
            System.out.println(e);
        }
    }
}