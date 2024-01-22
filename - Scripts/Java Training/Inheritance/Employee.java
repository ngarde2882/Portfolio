package Inheritance;

class Employee {
    private int empno;
    private String name;
    protected float salary; // protected allows child class to access
    private String dname;

    public Employee() {
        empno=0;
        name="";
        salary=0.0F;
        dname="";
    }
    public Employee(int empno, String name, float salary, String dname){
        this.empno=empno;
        this.name=name;
        this.salary=salary;
        this.dname=dname;
    }

    public float computeNetSalary(int all, int ded){
        return salary+all-ded;
    }
}

class Manager extends Employee {
    int no_of_sub;
    public Manager() {
        super(); // inherits all of parent variables and methods
        no_of_sub=0;
    }
    public Manager(int empno, String name, float salary, String dname, int no_of_sub){
        super(empno,name,salary,dname);
        this.no_of_sub=no_of_sub;
    }
    public float computeNetSalary(int all, int ded){
        return salary+all*2-ded;
    }
}

class Programmer extends Employee {
    int no_of_lines_code;
    String project_name;
    public Programmer() {
        super(); // inherits all of parent variables and methods
        no_of_lines_code=0;
        project_name="reservation";
    }
    public Programmer(int empno, String name, float salary, String dname, int no_of_lines_code, String project_name){
        super(empno,name,salary,dname);
        this.no_of_lines_code=no_of_lines_code;
        this.project_name=project_name;
    }
    public float computeNetSalary(int all, int ded){
        return salary+all+500-ded;
    }
    // Extensibility child has methods not in parent class
    // cannot be used by manager(sibling) or employee(parent)
    public boolean evaluate(String Code) {
        return true;
    }
}

class Hr {
    public static void main(String []s){
        Employee e=new Employee(101,"jhon",12000F,"Production");
        Manager m=new Manager(102,"Pal",10000F,"Sales",5);
        Programmer p=new Programmer(103,"Me",10000F,"Production",1000,"Java Training");
        System.out.println(e.computeNetSalary(500,100));
        System.out.println(m.computeNetSalary(1000,300));
        System.out.println(p.computeNetSalary(1000,300));
        System.out.println(p.evaluate("some data"));
    }
}