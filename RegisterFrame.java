package gui;

import service.BankService;

import javax.swing.*;
import java.awt.*;

public class RegisterFrame extends JFrame {
    private JTextField usernameField;
    private JPasswordField passwordField;
    private JComboBox<String> accountTypeCombo;
    private BankService bankService;

    public RegisterFrame(BankService service) {
        this.bankService = service;
        setTitle("Register");
        setSize(300, 200);
        setLocationRelativeTo(null);

        JPanel panel = new JPanel(new GridLayout(4,2));
        panel.add(new JLabel("Username:"));
        usernameField = new JTextField();
        panel.add(usernameField);

        panel.add(new JLabel("Password:"));
        passwordField = new JPasswordField();
        panel.add(passwordField);

        panel.add(new JLabel("Account Type:"));
        accountTypeCombo = new JComboBox<>(new String[]{"SAVINGS", "CHECKING"});
        panel.add(accountTypeCombo);

        JButton registerBtn = new JButton("Register");
        panel.add(registerBtn);

        registerBtn.addActionListener(e -> {
            String username = usernameField.getText();
            String password = new String(passwordField.getPassword());
            String accType = (String) accountTypeCombo.getSelectedItem();
            boolean success = bankService.registerUser(username, password, accType);
            if (success) {
                JOptionPane.showMessageDialog(this, "Registration successful!");
                dispose();
            } else {
                JOptionPane.showMessageDialog(this, "Registration failed! Username may exist.");
            }
        });

        add(panel);
    }
}