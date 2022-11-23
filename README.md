# Vending machine api
This is a task for  FlapKap’s Backend challenge built using django framework.
## Installation and setup
1. [Insatall poetry](https://python-poetry.org/docs/) from its official website
2. Make sure your running python version is between (3.8 and 3.10) to ensure compatibility with one specified in `pyproject.toml`
3. After cloning the repo make sure you are in the main repo folder (`vending-machine-api`) and run this command from terminal `poetry install`
4. Activate poetry shell by running `poetry shell`
5. Change directory to `vending_machine_api` and run `poetry run python manage.py migrate`
6. From the same directory run this command to run the server `poetry run python manage.py runserver`

## API endpoints
1. `http://127.0.0.1:8000/api/register/` - `POST`.
    * Create a new user and returns the Token that shloud be used for authentication.
2. `http://127.0.0.1:8000/api/users/` - `GET` .
    * Using the provided token from registering will return a list of all existing users.
3. `http://127.0.0.1:8000/api/users/:id` - `GET , PUT , PATCH , DELETE`.
    * Using the provided token from registering will retrieve , update or delete a a single user details by id (*Not allowed update details of another user*).
4. `http://127.0.0.1:8000/api/users/deposit/` - `PATCH`.
    * Using the provided token from registering will deposit coins into user account.
5. `http://127.0.0.1:8000/api/users/reset/` - `PATCH`.
    * Using the provided token from registering will reset user deposit (*Not allowed update details of another user*).
6. `http://127.0.0.1:8000/api/products/` - `GET , POST`.
     * Using the provided token from registering will retrieve all existing products or create a new product using POST.
7. `http://127.0.0.1:8000/api/products/:id` - `GET , PUT , PATCH , DELETE`.
     * Using the provided token from registering will retrieve , update , delete a single product.
8. `http://127.0.0.1:8000/api/products/buy/` - `POST`.
    * Using the provided token from registering will buy requested product.
