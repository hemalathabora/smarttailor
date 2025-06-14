
# 👔 SmartTailor: Digitally Augmented Tailoring Workflow Management

SmartTailor is a cloud-based micro-ERP solution specifically built for **local tailoring shops** to streamline and digitize their stitching workflows. This platform empowers both tailors and customers with intuitive dashboards to manage orders, fabric inventory, measurements, and more — all with a mobile-friendly, AI-augmented experience.

---

## 🚀 Project Overview

**SmartTailor** bridges the gap between manual tailoring workflows and modern technology. The system allows:
- Customers to place orders online and track their progress.
- Tailors to manage tasks, update order statuses, and optimize their stitching pipeline.

This project was built using the Django framework and includes a responsive front-end with Bootstrap and a secure backend powered by Django ORM and PostgreSQL (or SQLite for local testing).

---

## 🎯 Features

### ✅ Customer-Side
- 🧵 **Place Orders**: Select fabric, style notes, delivery date, and upload a design image.
- 📏 **AI-based Measurement Uploads** (optional): Upload a body photo to estimate measurements.
- 📋 **Track Orders**: Real-time order status like "Received", "Cutting", "Stitching", "Trial", etc.
- 🔁 **Reorder Past Orders**: Repeat favorite designs from order history.

### ✅ Tailor Dashboard
- 📬 **View All Orders**: Each order includes customer details, fabric, and design preview.
- 📦 **Update Status**: Modify current status to “Cutting Started”, “Stitching”, “Completed”, etc.
- 📥 **Download Design Images**: Review uploaded customer designs easily.
- 📆 **Manage Deadlines**: Stay on top of deliveries.

---

## 🧠 Optional AI Features
- 📸 **AI-Based Body Measurement Estimation** *(Implemented in backend)*: Estimating key tailoring sizes from uploaded images using computer vision.
- 💬 **WhatsApp Bot Integration** *(planned)*: To place orders via WhatsApp for non-app users.
- 📈 **Productivity Tracker** *(planned)*: Helps tailors plan daily work schedules.

---

## 🏗️ Tech Stack

| Technology     | Purpose                                |
|----------------|----------------------------------------|
| Django         | Backend framework                      |
| SQLite/PostgreSQL | Database                            |
| HTML + Bootstrap | Frontend UI                         |
| Pillow         | Handling image uploads                 |
| Django Forms   | For uploading measurements & design    |
| Git & GitHub   | Version control                        |
| OBS Studio     | Screen recording for demo              |
| Render         | Deployment platform                    |

---

## 📁 Project Structure

```

smarttailor/
├── core/                  # Main Django app
│   ├── models.py          # Order, Fabric, Customer, Tailor, Measurement
│   ├── views.py           # Dashboard logic (Tailor + Customer)
│   ├── forms.py           # OrderForm with image upload
│   └── templates/         # HTML files
├── media/                 # Uploaded design images
├── static/                # CSS, JS
├── db.sqlite3             # Default database (can use PostgreSQL)
├── manage.py              # Django project manager
└── requirements.txt       # Python dependencies

````

---

## ⚙️ Setup Instructions (Local)

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/smarttailor.git
cd smarttailor

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Run server
python manage.py runserver
````

Visit: `http://127.0.0.1:8000`


