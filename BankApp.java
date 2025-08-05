package com;

import gui.LoginFrame;
import service.BankService;

import javax.swing.*;

public class BankApp {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            BankService service = new BankService();
            new LoginFrame(service).setVisible(true);
        });
    }
}