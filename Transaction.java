package model;

import java.time.LocalDateTime;

public class Transaction {
    private int id;
    private int accountId;
    private LocalDateTime date;
    private String type; // "DEPOSIT", "WITHDRAW", "TRANSFER"
    private double amount;
    private String description;

    public Transaction(int id, int accountId, LocalDateTime date, String type, double amount, String description) {
        this.id = id;
        this.accountId = accountId;
        this.date = date;
        this.type = type;
        this.amount = amount;
        this.description = description;
    }
    // Getters and setters
    public int getId() { return id; }
    public int getAccountId() { return accountId; }
    public LocalDateTime getDate() { return date; }
    public String getType() { return type; }
    public double getAmount() { return amount; }
    public String getDescription() { return description; }
}