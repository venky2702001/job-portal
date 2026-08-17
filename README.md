# Job Portal

A full-stack Job Portal built with **Django, MySQL, Bootstrap, and JavaScript**.  
This project allows recruiters to post jobs, candidates to apply, and admins to manage users and applications.

---

## 🚀 Features
- User authentication (Signup/Login with role-based access: Candidate, Recruiter, Admin)
- Recruiter dashboard to post jobs and view applications
- Candidate dashboard to search, filter, and apply for jobs
- Admin panel to manage users and jobs
- SQLPlus reports for analytics (e.g., top applied jobs, monthly applications)
- Responsive UI with Bootstrap
- Deployed backend and frontend (to be added once live)

---

## 🛠️ Tech Stack
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Backend:** Python (Django)
- **Database:** MySQL + SQLPlus
- **Version Control:** Git & GitHub
- **Deployment:** Heroku / Netlify / AWS (planned)

---

## 📂 Project Structure
```
jobportal/
│── accounts/        # User authentication and roles
│── jobs/            # Job posting and management
│── applications/    # Candidate applications
│── templates/       # HTML templates
│── static/          # CSS, JS, images
│── manage.py
```
---

## ⚙️ Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/venky2702001/job-portal.git
   cd job-portal
2.Create a virtual environment and install dependencies:
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
3.Configure database settings in settings.py (MySQL).
4.Run migrations:
    python manage.py migrate
5.Start the server:
    python manage.py runserver
6.Open http://127.0.0.1:8000/ in your browser.
---
## 📸 Screenshots
(Add screenshots of your UI once built)
---
## 📊 Future Enhancements
- Resume upload for candidates
- Email notifications for job applications
- Advanced search with filters (location, salary, skills)
- Deployment on cloud (Heroku/AWS)

---
## 👨‍💻 Author
**Venkatesh K**

- LinkedIn: [linkedin.com/in/venkateshk2702001](https://linkedin.com/in/venkateshk2702001)  
- GitHub: [github.com/venky2702001](https://github.com/venky2702001)  
- LeetCode: [leetcode.com/u/venkatesh_2702](https://leetcode.com/u/venkatesh_2702)
