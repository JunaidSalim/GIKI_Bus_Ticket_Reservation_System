# GIKI BUS TICKET RESERVATION SYSTEM
This repository contains our Database Management System (DBMS) Project developed as a digital solution to address the challenges faced by GIKI students regarding bus ticket reservations. The current manual system at GIKI creates numerous hurdles for students seeking to book tickets. Our system aims to simplify the process for both students and administrators by providing a user-friendly interface for booking tickets and an admin panel for managing and maintaining ticket records.

## Features
- User-friendly interface for students to book tickets
- Admin panel for administrators to manage ticket records
- Digital solution to replace the manual bus reservation system
- Streamlined process for booking tickets, reducing hurdles for students
- Efficient record management for administrators

## Technologies Used
- **UI/UX**: Figma, DhiWise<br>
- **Front-End**: HTML, Tailwind CSS<br>
- **Back-End**: Django<br>
- **Database**: PostgreSQL<br>
 
## Repository Structure:
```
📦 GIKI_Bus_Ticket_Reservation_System
├─ gbrs
├─ asset
│  ├─ admin
│  │  ├─ css
│  │  ├─ img
│  │  └─ js
│  ├─ css
│  └─ public
│     ├─ fonts
│     └─ images
├─ node_modules
├─ static
│  ├─ css
│  └─ public
├─ system
│  ├─ backend
│  ├─ migrations
│  ├─ _init_.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ models.py
│  ├─ tests.py
│  └─ views.py
├─ templates
├─ theme
├─ requirements.txt
├─ manage.py
└─ README.md
```

## Demo

https://github.com/JunaidSalim/GIKI_Bus_Ticket_Reservation_System/assets/115392538/4d1d369c-3fda-4fe3-a208-56a34ca6aa60


## Installation and Setup

  ### Clone the repository:
  ```bash
  git clone https://github.com/JunaidSalim/GIKI_Bus_Ticket_Reservation_System.git
  ```
  
  ### Install the required packages:
  ```bash
  pip install -r requirements.txt
  ```
  ### Configure `settings.py`
    Update the `settings.py` file with your database credentials and other necessary configurations. Ensure that the `DATABASES` setting matches your database setup and adjust any other settings such as `EMAIL_HOST`, `DEBUG`, and `STATIC_URL` as needed.

  ### Run migrations
  ```bash
  python manage.py migrate
  ```
  
  ### Start Tailwind CSS:
  ```bash
  python manage.py tailwind start
  ```
  
  ### Run the development server:
  ```bash
  python manage.py runserver
  ```

## Contribution Guidelines

We welcome contributions to the GIKI Bus Ticket Reservation System project! To ensure a smooth collaboration process, please follow these guidelines when contributing:

1. **Fork the Repository**: Start by forking the repository to your GitHub account.
2. **Create a Branch**: Create a new branch for your feature or bug fix.
3. **Make Your Changes**: Implement your changes in your branch. Ensure that your code follows the project's coding standards.
4. **Commit Your Changes**: Write clear and concise commit messages.
5. **Push to Your Branch**: Push your changes to your branch on GitHub.
6. **Create a Pull Request**: Submit a pull request to the `main` branch of the original repository. Include a detailed description of your changes and reference any related issues.

We appreciate your efforts to improve the project and look forward to your contributions!

## Contributors

- [Junaid Saleem](https://github.com/JunaidSalim) - Back-End
- [Hamza Faraz](https://github.com/hamzafaraz1821) - Front-End
- [Muneeb Bin Nasir](https://github.com/JMSNM) - UI/UX
- [Muhammad Taimoor](https://github.com/taimoorgiki) - Database


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.




