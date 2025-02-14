## Installation Guide

Follow the steps below to set up the project on your system:

1. System Update
Update your system to ensure all packages are up to date.

sudo apt update && sudo apt upgrade -y

2. Enable SSH Access
Follow this guide to enable SSH access:
Enable SSH Access Guide

3. Install Required Packages
Install Python, pip for managing Python packages, virtual environment tools, npm (for Vue.js CLI), Curl, and Vim.

sudo apt install -y python3 python3-pip python3-venv npm curl vim build-essential

4. Install Nginx
Install Nginx web server.

sudo apt install nginx

5. Create Directories for Virtual Environment and Static Files
Create the necessary directories for the virtual environment and static files.

cd ..
mkdir www-data
cd www-data

6. Set Up Virtual Environment
Create and activate a Python virtual environment for your project.

python3 -m venv venv
source venv/bin/activate  # Only in the directory where the venv folder is located

7. Install Project Dependencies
Install Django, Gunicorn, OSC, Requests, Django Rest Framework, and CORS headers.

pip install django requests python-osc djangorestframework django-cors-headers
pip3 install gunicorn

8. Create Django Project
Create a new Django project named Kinderabholsystem.

django-admin startproject Kinderabholsystem

9. Configure Static Files
Create the directory for static files and set the correct permissions.

sudo mkdir -p /var/www/static
sudo chown -R www-data:www-data /var/www/static
sudo chmod -R 755 /var/www/static

10. Update Nginx Configuration
Edit the Nginx configuration to serve static files and proxy API requests to the Django backend.

Add the configuration file from the repository at /etc/nginx/sites-available/default

sudo systemctl restart nginx

11. Set Up Gunicorn as a Service
Create a systemd service for Gunicorn to run the Django app.

sudo nano /etc/systemd/system/gunicorn.service
Add the following content:

[Unit]
Description=gunicorn daemon for Django project "Kinderabholsystem"
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/www-data/Kinderabholsystem
ExecStart=/www-data/venv/bin/gunicorn --workers 1 --bind 127.0.0.1:8000 Kinderabholsystem.wsgi:application

[Install]
WantedBy=multi-user.target
Enable and start the Gunicorn service:

sudo systemctl enable gunicorn
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl status gunicorn

12. Configure Firewall
Allow necessary ports through the firewall for HTTP,  SSH access.

sudo ufw allow 80/tcp
sudo ufw allow 22/tcp
sudo ufw status

13. Give Django and Gunicorn Access to the Database
Ensure that Django and Gunicorn can access the database by setting the correct permissions.

sudo chown -R www-data:www-data /www-data/Kinderabholsystem/db.sqlite3
sudo chmod -R 755 /www-data/Kinderabholsystem/db.sqlite3

14. Final Configuration
Make sure your Django settings.py file is properly configured, including database settings, static file paths, and any other project-specific configurations.

15. Deploy Vue.js Project
To build and deploy the Vue.js frontend:

Install Vue.js CLI (if not already installed):
npm install -g @vue/cli
Build the Vue.js project:
Navigate to the downloaded Vue.js project directory from the repository and build the production version.

cd /path/to/vue-project
npm run build
This will generate a dist/ directory containing the production build of your Vue.js project.
Move the build files to Nginx static directory:
Move the generated dist/ directory into /var/www/static so that Nginx can serve the files.

sudo mv /path/to/vue-project/dist /var/www/static/
sudo chown -R www-data:www-data /var/www/static/dist
Verify the frontend deployment:
Open a browser and navigate to your server's IP address to check if the frontend is being served correctly via Nginx.

16. Upload Files to Raspberry Pi Pico
To upload files to the Raspberry Pi Pico, you can use tools thonny
