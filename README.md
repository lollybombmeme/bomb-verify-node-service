# Bomb Guard API

## Overview

The Bomb Guard API is designed to handle the process of sending task evidence to workers via an evidence endpoint. Workers will wait for sufficient block confirmations and then send their signatures back to the main API. This API ensures secure and reliable evidence collection and signature verification.

## Features

-   Send task evidence to workers

## Installation

To get started with the Bomb Guard API, follow these steps:
Requirement: Python 3.11.x, Docker compose

2. **Install dependencies:**

    ```bash
    python3 install -r requirements.txt
    ```

3. **Set up environment variables:**
   Create a `.env` file in the root directory and add the necessary environment variables:
4. **Run the server:**
    ```bash
    docker compose up -d --build
    ```

## Usage

Once the server is running, you can interact with the API using HTTP requests. Below are examples of the available endpoints and their usage.

### API Endpoints

#### Send Task Evidence

-   **Endpoint:** `POST /api-guard/iapi/evident`
-   **Description:** Send task evidence to a worker.
-   **Request Body:**
    ```json
    {
        "amount": "amount",
        "tx_hash": "tx_hash",
        "contract_address": "contract_address",
        "user_address": "user_address",
        "from_chain_id": "from_chain_id",
        "to_chain_id": "to_chain_id"
    }
    ```
