// A console-based ATM management system built with C++.

#include <ctime>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <string>
#include <unordered_map>

using namespace std;

const string USERS_FILE = "data/users.txt";
const string TRANSACTION_FILE_SUFFIX = "_transactions.txt";
const double MAX_WITHDRAWAL_LIMIT = 50000.00;

struct User {
    string id;
    string password;
    double balance;
};

void clearInput() {
    cin.clear();
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
}

int getMenuChoice(const string& prompt) {
    int choice;

    while (true) {
        cout << prompt;
        cin >> choice;

        if (!cin.fail()) {
            return choice;
        }

        cout << "Invalid input. Please enter a number.\n";
        clearInput();
    }
}

double getAmount(const string& prompt) {
    double amount;

    while (true) {
        cout << prompt;
        cin >> amount;

        if (!cin.fail() && amount > 0) {
            return amount;
        }

        cout << "Invalid amount. Please enter a positive value.\n";
        clearInput();
    }
}

unordered_map<string, User> loadUsers() {
    unordered_map<string, User> users;
    ifstream inputFile(USERS_FILE);

    if (!inputFile.is_open()) {
        cout << "User data file not found.\n";
        cout << "Create data/users.txt using data/users.example.txt before running the application.\n";
        return users;
    }

    string id;
    string password;
    double balance;

    while (inputFile >> id >> password >> balance) {
        users[id] = User{id, password, balance};
    }

    return users;
}

void saveUsers(const unordered_map<string, User>& users) {
    ofstream outputFile(USERS_FILE);

    for (const auto& pair : users) {
        const User& user = pair.second;
        outputFile << user.id << " " << user.password << " " << fixed << setprecision(2)
                   << user.balance << "\n";
    }
}

string getTransactionFilePath(const string& userId) {
    return "data/" + userId + TRANSACTION_FILE_SUFFIX;
}

string getCurrentTimestamp() {
    time_t currentTime = time(nullptr);
    tm* localTime = localtime(&currentTime);

    char buffer[30];
    strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", localTime);

    return string(buffer);
}

void saveTransaction(const string& userId, const string& transactionType, double amount, double balance) {
    ofstream transactionFile(getTransactionFilePath(userId), ios::app);

    transactionFile << getCurrentTimestamp() << " | " << transactionType
                    << " | Amount: " << fixed << setprecision(2) << amount
                    << " | Balance: " << balance << "\n";
}

void showTransactionHistory(const string& userId) {
    ifstream transactionFile(getTransactionFilePath(userId));
    string line;

    cout << "\n----- Transaction History -----\n";

    if (!transactionFile.is_open()) {
        cout << "No transaction history available.\n";
        return;
    }

    while (getline(transactionFile, line)) {
        cout << line << "\n";
    }
}

bool authenticateUser(const unordered_map<string, User>& users, string& userId) {
    string password;

    cout << "\n========== Welcome to ATM Management System ==========\n";
    cout << "Enter user ID: ";
    cin >> userId;

    cout << "Enter password: ";
    cin >> password;

    auto user = users.find(userId);

    if (user != users.end() && user->second.password == password) {
        cout << "\nLogin successful.\n";
        return true;
    }

    cout << "\nInvalid user ID or password.\n";
    return false;
}

void showMainMenu() {
    cout << "\n----- Main Menu -----\n";
    cout << "1. Check account balance\n";
    cout << "2. Deposit money\n";
    cout << "3. Withdraw money\n";
    cout << "4. View transaction history\n";
    cout << "5. Exit\n";
}

void checkBalance(double balance) {
    cout << "\nCurrent account balance: " << fixed << setprecision(2) << balance << "\n";
}

void depositMoney(User& user) {
    double amount = getAmount("Enter deposit amount: ");

    user.balance += amount;
    saveTransaction(user.id, "Deposit", amount, user.balance);

    cout << "Deposit successful.\n";
    checkBalance(user.balance);
}

void withdrawMoney(User& user) {
    double amount = getAmount("Enter withdrawal amount: ");

    if (amount > MAX_WITHDRAWAL_LIMIT) {
        cout << "Withdrawal failed. Maximum withdrawal limit is " << fixed << setprecision(2)
             << MAX_WITHDRAWAL_LIMIT << ".\n";
        return;
    }

    if (amount > user.balance) {
        cout << "Withdrawal failed. Insufficient balance.\n";
        return;
    }

    user.balance -= amount;
    saveTransaction(user.id, "Withdrawal", amount, user.balance);

    cout << "Withdrawal successful.\n";
    checkBalance(user.balance);
}

int main() {
    unordered_map<string, User> users = loadUsers();

    if (users.empty()) {
        return 0;
    }

    string userId;

    if (!authenticateUser(users, userId)) {
        return 0;
    }

    bool isRunning = true;

    while (isRunning) {
        showMainMenu();

        int choice = getMenuChoice("Select an option: ");

        switch (choice) {
            case 1:
                checkBalance(users[userId].balance);
                break;

            case 2:
                depositMoney(users[userId]);
                saveUsers(users);
                break;

            case 3:
                withdrawMoney(users[userId]);
                saveUsers(users);
                break;

            case 4:
                showTransactionHistory(userId);
                break;

            case 5:
                isRunning = false;
                break;

            default:
                cout << "Invalid option. Please select a valid menu option.\n";
        }
    }

    saveUsers(users);

    cout << "\nThank you for using the ATM Management System.\n";
    return 0;
}