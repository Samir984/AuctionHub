# Auction Platform

An online auction platform built with Django, Django REST Framework, Celery, and Redis, allowing users to list items, place bids, and manage auctions with background tasks.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Celery & Redis Integration](#celery--redis-integration)
- [API Endpoints](#api-endpoints)
- [Usage](#usage)


## Features

- **User Authentication**: Custom user model with email-based authentication, including registration, login, and password reset.
- **Item Management**: Users can create, view, update, and delete items they own.
- **Auction Management**: Users can initiate auctions, set starting bids, and specify end times.
- **Bidding**: Users can place bids on active auctions, with validation to ensure bids are above the current highest bid.
- **Background Tasks**: Celery is used with Redis as the message broker for handling asynchronous tasks, like sending email notifications for password resets and auction reminders.
- **Password Reset**: Users can request password reset emails, with verification codes stored in cache.

## Installation

1. **Clone the Repository**
    ```bash
    git clone <repo link>
    cd AuctionHub
    ```

2. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run Migrations**
    ```bash
    python manage.py migrate
    ```

4. **Set Up Redis**  
   Ensure that Redis is installed and running. You can install it via package managers (e.g., `brew install redis` for macOS, `sudo apt install redis-server` for Ubuntu) and start the server:
    ```bash
    redis-server
    ```

5. **Start Celery**  
   Open a new terminal and run Celery with the Redis broker:
    ```bash
    celery -A auction_platform worker -l info
    ```

6. **Run the Server**
    ```bash
    python manage.py runserver
    ```

## Celery & Redis Integration

This project uses **Celery** for handling background tasks, such as sending email notifications for password resets and auction-related reminders. **Redis** acts as the message broker for Celery to manage task queues and results.

### Setting Up Celery
- **Install Celery and Redis**:
    ```bash
    pip install celery redis
    ```
- **Configuration**: Celery and Redis configurations are set in Django’s `settings.py` file. 
- **Running Celery**: After setting up Redis, start a Celery worker to listen for tasks, as shown in step 5 above.

### Background Tasks
- **Password Reset**: Celery handles email notifications for password reset requests.
- **Auction Notifications**: Set automated reminders and notifications for auction events.

## API Endpoints

### User Authentication
- **`POST /register/`**: Register a new user
- **`POST /login/`**: Log in a user
- **`POST /forgot_password/`**: Request a password reset email
- **`POST /reset_password/`**: Reset password using a verification code

### Items
- **`GET /items/`**: List all items
- **`POST /items/`**: Create a new item (authenticated users only)

### Auctions
- **`GET /auctions/`**: List all active auctions
- **`POST /auctions/`**: Create a new auction (authenticated users only)
- **`PATCH /auctions/<auction_id>/`**: Update auction details (owner only)

### Bids
- **`POST /auctions/<auction_id>/bid/`**: Place a bid on an auction
- **`GET /auctions/<auction_id>/bid/`**: List all bids for an auction

## Usage

1. **Register and Log In**: First, register an account and log in to access the auction features.
2. **List an Item**: Use the `/items/` endpoint to create an item you wish to auction.
3. **Start an Auction**: Use the `/auctions/` endpoint to start an auction with a starting bid and an end time.
4. **Place a Bid**: Bidders can place bids on active auctions using the `/auctions/<auction_id>/bid/` endpoint.
