package dao;

import model.Transaction;
import util.DBUtil;

import java.sql.*;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

public class TransactionDAO {
    public void addTransaction(Transaction tx) {
        String sql = "INSERT INTO transactions (account_id, date, type, amount, description) VALUES (?, ?, ?, ?, ?)";
        try (Connection conn = DBUtil.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setInt(1, tx.getAccountId());
            ps.setTimestamp(2, Timestamp.valueOf(tx.getDate()));
            ps.setString(3, tx.getType());
            ps.setDouble(4, tx.getAmount());
            ps.setString(5, tx.getDescription());
            ps.executeUpdate();
        } catch (SQLException ex) {
            ex.printStackTrace();
        }
    }

    public List<Transaction> getTransactionsByAccountId(int accountId) {
        List<Transaction> list = new ArrayList<>();
        String sql = "SELECT * FROM transactions WHERE account_id=? ORDER BY date DESC";
        try (Connection conn = DBUtil.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setInt(1, accountId);
            ResultSet rs = ps.executeQuery();
            while (rs.next()) {
                list.add(new Transaction(
                    rs.getInt("id"),
                    rs.getInt("account_id"),
                    rs.getTimestamp("date").toLocalDateTime(),
                    rs.getString("type"),
                    rs.getDouble("amount"),
                    rs.getString("description")
                ));
            }
        } catch (SQLException ex) {
            ex.printStackTrace();
        }
        return list;
    }
}