# banking-app

# Java Banking Application

A simple Java Swing-based Banking Management System connected to a MySQL database. Users can register, log in, view account details, deposit or withdraw money, and view transaction history.

## Features

- User Registration and Login
- Multiple Account Types (Savings, Checking, etc.)
- Deposit and Withdraw Funds
- View Account Balance
- Transaction History
- Simple and colorful Java Swing GUI

## Technologies Used

- Java 8+
- Swing (for GUI)
- MySQL (for database)
- JDBC (for Java-MySQL connectivity)

## Installation & Setup

### Prerequisites

- Java (JDK 8 or above)
- MySQL Server
- IDE (like IntelliJ IDEA, Eclipse, or NetBeans)
- Git

### Clone the Repository

```bash
git clone https://github.com/VishalChougale07/banking-app.git
cd banking-app
```

### Database Setup

1. Create a database called `bankdb` in MySQL.
2. Run the provided SQL scripts in the `/db` folder to create tables and insert sample data.
3. Update your database connection details in `DBUtil.java` if necessary.

### Running the Application

- Open the project in your IDE.
- Build and run the `Main` class.
- The login and registration GUI will appear.

## Usage

- Register a new user or log in with existing credentials.
- Create accounts, deposit, withdraw, and view your account details and transactions.
- Sample Credentials:
    - Username: `testuser`
    - Password: `testpass`

## Screenshots

<!-- Optionally add screenshots here -->

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.
