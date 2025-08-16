# 🚗 RideMate: Vehicle Rental Management System

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A comprehensive Vehicle Rental Management System with both command-line and GUI interfaces, built with C and Python.

## 🌟 Features

### Core Functionality
- **User Authentication**
  - Customer registration and login
  - Secure admin authentication
  - User session management

### Vehicle Management
- Add, view, update, and soft delete vehicles
- Filter and search vehicles by various criteria
- Track vehicle availability and status

### Customer Management
- Customer profile management
- View and update customer information
- Track rental history

### Rental Operations
- Book vehicles with flexible time slots
- View rental history and receipts
- Calculate rental costs

### Technical Features
- **Backend**: High-performance C core with Python bindings
- **Frontend**: Modern Tkinter-based GUI
- **Data Persistence**: CSV-based storage
- **Modular Architecture**: Clean separation of concerns
- **Input Validation**: Robust error handling

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- C Compiler (GCC, MSVC, or compatible)
- pip (Python package manager)

### Installation
1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd ridemate
   ```

2. Set up a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Build and install the C extension:
   ```bash
   pip install -e .
   ```

### Running the Application

#### GUI Mode (Recommended)
```bash
python ridemate_gui.py
```

#### Command Line Interface
```bash
python main.py
```

## 📂 Project Structure
```
ridemate/
├── src/                  # C source files
│   ├── customer.c/h      # Customer management
│   ├── vehicle.c/h       # Vehicle management
│   ├── rental.c/h        # Rental operations
│   └── utils.c/h         # Utility functions
├── ridemate_bridge.c     # Python-C bridge
├── ridemate_gui.py       # Tkinter GUI
└── data/                 # Data storage
    ├── customers.csv
    ├── vehicles.csv
    └── rentals.csv
```

## 📝 Usage

### For Customers
1. Register a new account or log in
2. Browse available vehicles
3. Book a vehicle for your desired dates
4. View your rental history

### For Administrators
1. Log in with admin credentials
2. Manage vehicles (add/update/remove)
3. View and manage customer accounts
4. Monitor rental operations
5. Generate reports

## 🤝 Contributing
Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact
For any queries, please open an issue or contact the project maintainers.

---
Built with ❤️ by the RideMate Team
- Menu-driven, real-world project structure
- Persistent file save/load
- Customer & admin modules
- Scalable & extendable codebase

## Build Instructions

- Clone this repository:
  ```sh
  git clone https://github.com/tanjimislam04/RideMate--Your-Smart-Ride-Booking-Platform.git
  cd RideMate--Your-Smart-Ride-Booking-Platform
  ```
- Compile (Linux/Mac):
  ```sh
  gcc main.c utils.c vehicle.c customer.c rental.c -o ridemate
  ```
- Run:
  ```sh
  ./ridemate
  ```
- **Windows users:**  
  Use CodeBlocks, Dev-C++, or any compatible C IDE.  
  Or, in Command Prompt (after compiling with GCC/MinGW):
  ```
  ridemate.exe
  ```

## How to Use

- On start, select Customer or Admin.
- Register or log in with your credentials.
- Customers can view/update their profile, browse vehicles, and book rentals.
- Admins can manage vehicles, customers, and view rental history.
- Data is saved automatically in files (`vehicles.csv`, `customers.csv`, `rentals.csv`, etc.)

## Roadmap

- [x] Core version with linked list-based storage
- [x] Modular structure & menu-driven UI
- [x] Strict input validation & error handling
- [ ] Role-based authentication (Admin/Customer/Driver)
- [ ] Advanced features (CSV export/import, search/filter, analytics, soft delete)
- [ ] Pro-level features (promo code, calendar view, graphical output, etc.)

## Author

- Md. Tanjim Islam  
  Software Engineering Student, Daffodil International University

## Note

This project is for academic and learning purposes. More features and advanced data structures will be added step by step.
