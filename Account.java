package model;

public class Account {
    private int id;
    private int userId;
    private String type; // "SAVINGS", "CHECKING"
    private double balance;

    public Account(int id, int userId, String type, double balance) {
        this.id = id;
        this.userId = userId;
        this.type = type;
        this.balance = balance;
    }
    // Getters and setters
    public int getId() { return id; }
    public int getUserId() { return userId; }
    public String getType() { return type; }
    public double getBalance() { return balance; }
    public void setBalance(double balance) { this.balance = balance; }
    @Override
    public String toString() {
        return "Account " + id + " (" + type + ") - Balance: " + balance;
    }
}
