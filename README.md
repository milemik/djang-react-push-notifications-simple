# Python send push notification test


## Start frontend app

1. enter fronted
    ```shell
      cd frontend
    ```
2. Install dependencies
    ```shell
   npm install
    ```
3. Run react app
    ```shell
   npm start
    ```

4. To see if app is running open url http://localhost:3000/


## Send notification using python script

1. Install python dependencies
    ```shell
   poetry install
    ```
2. run main.py file
    ```shell
   poetry run python main.py
    ```

## Setup django - backend app
1. Migrate data:
   ```shell
   python manage.py migrate
   ```
2. Run django server
   ```shell
   python manage.py runserver
   ```
3. Create django superuser
   ```shell
   python manage.py createsuperuser
   ```
   
## Send push from backend
1. Open admin panel: open url http://localhost:8000/admin/
2. From action select: 'send push notifications'

NOTE: there are two actions for sending push notifications.
First one will send push notifications and users will see it.
Second one will send push notifications on dry - users will not really
see notifications - good for testing!