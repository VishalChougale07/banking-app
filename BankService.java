package service;

import dao.AccountDAO;
import dao.TransactionDAO;
import dao.UserDAO;
import model.Account;
import model.Transaction;
import model.User;

import java.time.LocalDateTime;
import java.util.List;

public class BankService {
    private UserDAO userDAO = new UserDAO();
    private AccountDAO accountDAO = new AccountDAO();
    private TransactionDAO transactionDAO = new TransactionDAO();

    public User authenticate(String username, String password) {
        User user = userDAO.getUserByUsername(username);
        if (user != null && user.getPassword().equals(password)) {
            return user;
        }
        return null;
    }

    public List<Account> getAccounts(int userId) {
        return accountDAO.getAccountsByUserId(userId);
    }

    public boolean registerUser(String username, String password, String accountType) {
        // Check if user exists, then insert user, then account
        if (userDAO.getUserByUsername(username) != null) return false;
        int userId = userDAO.createUser(username, password, "CUSTOMER");
        if (userId > 0) {
            accountDAO.createAccount(userId, accountType, 0.0);
            return true;
        }
        return false;
    }
    
    public boolean deposit(int accountId, double amount) {
        Account acc = accountDAO.getAccountById(accountId);
        if (acc != null && amount > 0) {
            double newBal = acc.getBalance() + amount;
            accountDAO.updateBalance(accountId, newBal);
            transactionDAO.addTransaction(
                new Transaction(0, accountId, LocalDateTime.now(), "DEPOSIT", amount, "Deposit")
            );
            return true;
        }
        return false;
    }

    public boolean withdraw(int accountId, double amount) {
        Account acc = accountDAO.getAccountById(accountId);
        if (acc != null && amount > 0 && acc.getBalance() >= amount) {
            double newBal = acc.getBalance() - amount;
            accountDAO.updateBalance(accountId, newBal);
            transactionDAO.addTransaction(
                new Transaction(0, accountId, LocalDateTime.now(), "WITHDRAW", amount, "Withdraw")
            );
            return true;
        }
        return false;
    }

    public List<Transaction> getTransactions(int accountId) {
        return transactionDAO.getTransactionsByAccountId(accountId);
    }
    
    public List<String> getAccountDetailsWithUserName(int userId) {
        return accountDAO.getAccountDetailsWithUserName(userId);
    }
}