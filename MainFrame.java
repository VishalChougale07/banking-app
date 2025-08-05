package gui;

import model.Account;
import model.Transaction;
import model.User;
import service.BankService;

import javax.swing.*;
import java.awt.*;
import java.util.List;

public class MainFrame extends JFrame {
    private BankService bankService;
    private User user;
    private JComboBox<Account> accountComboBox;
    private JTextArea txArea;

    public MainFrame(BankService service, User user) {
        this.bankService = service;
        this.user = user;

        setTitle("Bank - Welcome " + user.getUsername());
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(500, 400);
        setLocationRelativeTo(null);

        JPanel topPanel = new JPanel(new FlowLayout());
        topPanel.setBackground(new Color(30, 144, 255)); // Dodger Blue

        accountComboBox = new JComboBox<>();
        accountComboBox.setBackground(new Color(240, 248, 255)); // Alice Blue
        accountComboBox.setFont(new Font("Arial", Font.PLAIN, 14));
        refreshAccountList();
        JLabel selLabel = new JLabel("Select Account:");
        selLabel.setFont(new Font("Arial", Font.BOLD, 16));
        selLabel.setForeground(Color.WHITE);
        topPanel.add(selLabel);
        topPanel.add(accountComboBox);

        JButton depositBtn = new JButton("Deposit");
        JButton withdrawBtn = new JButton("Withdraw");
        JButton txBtn = new JButton("Transactions");
        JButton detailsBtn = new JButton("Show Details");
        JButton backBtn = new JButton("Back");

        Color btnBg = new Color(0, 123, 167); // Custom blue
        Color btnFg = Color.WHITE;
        Font btnFont = new Font("Arial", Font.BOLD, 14);

        JButton[] buttons = {depositBtn, withdrawBtn, txBtn, detailsBtn};
        for (JButton btn : buttons) {
            btn.setBackground(btnBg);
            btn.setForeground(btnFg);
            btn.setFont(btnFont);
        }
        backBtn.setBackground(Color.RED);
        backBtn.setForeground(Color.WHITE);
        backBtn.setFont(btnFont);

        topPanel.add(depositBtn);
        topPanel.add(withdrawBtn);
        topPanel.add(txBtn);
        topPanel.add(detailsBtn);
        topPanel.add(backBtn);

        add(topPanel, BorderLayout.NORTH);

        txArea = new JTextArea();
        txArea.setEditable(false);
        txArea.setBackground(new Color(250, 250, 240));
        txArea.setFont(new Font("Consolas", Font.PLAIN, 13));
        txArea.setForeground(new Color(33, 33, 33));
        add(new JScrollPane(txArea), BorderLayout.CENTER);

        depositBtn.addActionListener(e -> doDeposit());
        withdrawBtn.addActionListener(e -> doWithdraw());
        txBtn.addActionListener(e -> showTransactions());
        detailsBtn.addActionListener(e -> showAccountDetails());
        backBtn.addActionListener(e -> {
            this.dispose();
            new LoginFrame(bankService).setVisible(true);
        });
    }

    private void refreshAccountList() {
        accountComboBox.removeAllItems();
        List<Account> accs = bankService.getAccounts(user.getId());
        for (Account acc : accs) {
            accountComboBox.addItem(acc);
        }
    }

    private Account getSelectedAccount() {
        return (Account) accountComboBox.getSelectedItem();
    }

    private void doDeposit() {
        Account acc = getSelectedAccount();
        if (acc != null) {
            String input = JOptionPane.showInputDialog(this, "Amount to deposit:");
            try {
                double amt = Double.parseDouble(input);
                if (bankService.deposit(acc.getId(), amt)) {
                    JOptionPane.showMessageDialog(this, "Deposit successful.");
                    refreshAccountList();
                } else {
                    JOptionPane.showMessageDialog(this, "Deposit failed.");
                }
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(this, "Invalid amount.");
            }
        }
    }

    private void doWithdraw() {
        Account acc = getSelectedAccount();
        if (acc != null) {
            String input = JOptionPane.showInputDialog(this, "Amount to withdraw:");
            try {
                double amt = Double.parseDouble(input);
                if (bankService.withdraw(acc.getId(), amt)) {
                    JOptionPane.showMessageDialog(this, "Withdrawal successful.");
                    refreshAccountList();
                } else {
                    JOptionPane.showMessageDialog(this, "Insufficient balance or invalid amount.");
                }
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(this, "Invalid amount.");
            }
        }
    }

    private void showTransactions() {
        Account acc = getSelectedAccount();
        if (acc != null) {
            List<Transaction> txs = bankService.getTransactions(acc.getId());
            StringBuilder sb = new StringBuilder();
            sb.append("Transactions for Account ID: ").append(acc.getId()).append("\n");
            sb.append("-------------------------------------------------\n");
            for (Transaction t : txs) {
                sb.append(t.getDate()).append(" | ")
                  .append(t.getType()).append(" | ")
                  .append(t.getAmount()).append(" | ")
                  .append(t.getDescription()).append("\n");
            }
            txArea.setText(sb.toString());
        }
    }

    private void showAccountDetails() {
        List<String> details = bankService.getAccountDetailsWithUserName(user.getId());
        StringBuilder sb = new StringBuilder();
        sb.append("Account Details:\n");
        sb.append("-------------------------------------------------\n");
        for (String d : details) {
            sb.append(d).append("\n");
        }
        txArea.setText(sb.toString());
    }
}