public class User {
    int id;
    String name;
    String emailId;
    long contactNo;
    public User() {}
    public User(int id, String name, String emailId, long contactNo) {
        super();
        this.id = id;
        this.name = name;
        this.emailId = emailId;
        this.contactNo = contactNo;
    }
    public int getId() {
        return id;
    }
    public void setId(int id) {
        this.id = id;
    }
    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }
    public String getEmailId() {
        return emailId;
    }
    public void setEmailId(String emailId) {
        this.emailId = emailId;
    }
    public long getContactNo() {
        return contactNo;
    }
    public void setEmailId(long contactNo) {
        this.contactNo = contactNo;
    }
}