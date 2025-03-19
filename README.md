# HemLMS - Learning Management System 📚

HemLMS is a **Learning Management System (LMS)** designed to provide a seamless experience for both learners and instructors. This system enables course creation, user authentication, progress tracking, and more, while being efficiently containerized with **Docker** and integrated with a **message broker system (RabbitMQ)**.

## 🚀 Tech Stack

### **Backend:**

- **Framework:** FastAPI ⚡ (Python)
- **Database ORM:** SQLAlchemy 🐍
- **Migrations:** Alembic 📜
- **Validation:** Pydantic ✅
- **Message Broker:** RabbitMQ 📩
- **Authentication:** JWT Token with encryption & decryption 🔐

### **Frontend:**

- **Framework:** Vue.js 🌿
- **State Management:** Vuex ⚙️
- **UI Libraries:** Bulma with Vue-based components 🎨

### **Containerization & Deployment:**

- **Docker** 🐳 (Backend, Frontend, Database)
- **Database:** PostgreSQL / MySQL 🗄️

## 🔧 Features & Functionalities

### ✅ **Backend Features**

- **User Authentication:** Login, Signup, JWT-based authentication
- **Account Management:** Models & schemas for user accounts
- **Course Management:** Create, update, delete courses
- **Lesson Management:** CRUD for lessons & content display
- **Comments & Reviews:** Users can add, validate, and view comments
- **Quiz System:** Structured quizzes, user participation, and results tracking
- **Progress Tracking:** Monitor lesson completion, track user engagement
- **File Uploads:** Support for images and other static files
- **Message Broker:** RabbitMQ for handling async operations

### ✅ **Frontend Features**

- **Homepage & About Page:** Landing pages with course highlights
- **Authentication Pages:** Login & Signup with JWT token handling
- **User Dashboard:** My Account, active courses, tracking progress
- **Course & Lesson Pages:** Detailed course view, embedded videos, and quizzes
- **Admin Section:** Manage categories, courses, lessons, and user interactions
- **Search & Filtering:** Category search for easy course discovery

## 🏗️ Setup & Installation

### **Clone the Repository**

```sh
git clone https://github.com/hemdai/HemLMS.git
cd hemlms
```

### Contact me for environment varriable hemanta.adhikari86@gmail.com or you can add yourself also

### **Run Entire Application (Dockerized)**

```sh
docker-compose up --build
```

## 🛠️ Development Roadmap

### 🔹 **Completed Tasks**

- User authentication with JWT ✅
- Course & Lesson Management ✅
- Commenting & Validation ✅
- Quiz system implementation ✅
- Progress tracking ✅
- Video embedding & file serving ✅

### 🔸 **Upcoming Features**

- Implementing **user-generated courses** (draft/review/published)
- Improving admin dashboard & moderation tools
- Enhancing UI with better state management (Vuex)
- Adding **category-based search & filtering**

## 🤝 Contribution

Want to contribute? Follow these steps:

1. Fork the repo 🍴
2. Create a new branch for your feature 🔀
3. Commit your changes ✅
4. Open a Pull Request 🚀

## 📜 License

This project is licensed under the **MIT License**.

---

🚀 Stay tuned for more updates as we enhance HemLMS! 😊
