# Friendflare

Friendflare is a Django-based web application that serves as a social media platform connecting students and company HR professionals. The platform is designed to facilitate networking, internship opportunities, and collaboration between students and potential employers.

## Features
1) Student Profiles: Create and manage your student profile, showcasing your skills, education, and projects.
2) HR Profiles: HR professionals can create profiles to connect with potential candidates, post job opportunities, and engage with the student community.
3) Messaging System: A built-in messaging system to foster communication between students and HR representatives.(under developmet)
4) Broadcast Board: HR professionals can post job opportunities, internships, and projects for students to explore and apply.
5) Events: Stay updated on networking events, career fairs, and other relevant activities.

## Installation

### Prerequisites
```bash
python ~= 3.10
Django ~= 4.1.13
djongo ~=1.3.6
pymongo ~= 3.12.3
```
### clone the repository
```bash
git clone https://github.com/Azhar1327/Friendflare.git
cd Friendflare
```

### Apply migrations
```bash
python manage.py migrate
```

### Run the Development Server
```bash
python manage.py runserver
```

## Usage
Access the admin panel at http://localhost:8000/admin to manage users, posts, and other content.

