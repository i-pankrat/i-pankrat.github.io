# i-pankrat.github.io

Steps how to serve flask application with uwsgi and nginx on ubuntu according to the [article](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-20-04). Read it to get more into the topic!

How to start the site on ubuntu server?

1. Connect to server

``` shell
ssh [your_username_on_server]@[server IP] -i [path_to_private_key]
```
2. Clone your github repository to the server

``` git
git clone -b [branchname] [url_for_your_repository]
```

3. Create wsgi.py in the working directory with the content:

```python
from main import app

if __name__ == "__main__":
    app.run()
```
4. Create main.ini in the working directory with the content:

``` ini
[uwsgi]
module = wsgi:app
logto = /var/log/uwsgi/%n.log

master = true
processes = 5
enable-threads = true

socket = /tmp/[name_of_your_socket].sock
chmod-socket = 660
vacuum = true

die-on-term = true
buffer-size=8192
```

5. Install nginx

``` shell
sudo apt install nginx
```

6. Install python
``` shell
sudo apt install python3
```
7. Install gcc

``` shell
sudo apt install gcc
```
8. Isntall pip

``` shell
sudo apt install pip
```

9. Install python3 venv

``` shell
sudo apt install python3.10-venv
```
10. Create python3 venv

``` shell
python3 -m venv venv
```
11. Activate python venv

``` shell
. venv/bin/activate
```
12. Install the necessary libraries

``` shell
pip install -r requirements.txt
```
13. Install uwsgi

``` shell
pip install uwsgi
```

14. Create a file

``` shell
sudo touch /etc/systemd/system/[name_of_your_service].service
```
15.  Insert the contents of the file. You may set your own description.

``` service
[Unit]
Description=uWSGI instance to serve personal site
After=network.target

[Service]
User=[your_username_on_server]
Group=www-data
WorkingDirectory=[absolute_path_to_your_git_rep]
Environment="PATH=[absolute_path_to_your_git_rep]/venv/bin/"
ExecStart=[absolute_path_to_your_git_rep]/venv/bin/uwsgi --ini [absolute_path_to_your_git_rep]/main.ini

[Install]
WantedBy=multi-user.target
```

16. Create the directory for uwsgi logs

``` shell
sudo mkdir /var/log/uwsgi
```
17. Change user and group

``` shell
sudo chown -R [your_username]:www-data /var/log/uwsgi
```

18. Launch service and check it status

``` shell
sudo systemctl start [name_of_your_service]
sudo systemctl status [name_of_your_service]
```

19. Update the content of /etc/nginx/sites-enabled/default, find and replace location / { .... } by

``` shell
location / {
                include uwsgi_params;
                client_max_body_size 70M;
                uwsgi_pass unix:/tmp/[name_of_your_socket].sock;
        }
```

19. Check if everything is correct

``` shell
sudo nginx -t
```

20.  Restart nginx. Everything is ready! Check your site.

``` shell
sudo systemctl restart nginx
``` 