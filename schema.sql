/***************************************************************
    *  MoneyTracker - schema.sql
    *  Created by: Paul Bayfield
    *  Created on: 08/12/2024
    *  Updated on: 09/12/2024
    *  Description: SQL database scheme for the MoneyTracker project
***************************************************************/

CREATE TABLE IF NOT EXISTS public.accounts (
    id INT PRIMARY KEY,
    username VARCHAR(255),
    balance DECIMAL(10, 2) DEFAULT 0.0
);

CREATE TABLE IF NOT EXISTS public.users (
    USERNAME VARCHAR(128) NOT NULL PRIMARY KEY,
    PASSWORD TEXT NOT NULL,
    TOKEN TEXT,
    account INT,
    CONSTRAINT fk_users_account FOREIGN KEY (account) REFERENCES public.accounts (id)
);

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS public.transactions (
    id VARCHAR(36),
    label VARCHAR(255),
    booking_date_time TIMESTAMP,
    is_accounted BOOLEAN,
    are_details_available BOOLEAN,
    amount DECIMAL(10, 2),
    amount_currency VARCHAR(3),
    movement_code_type VARCHAR(255),
    nature VARCHAR(255),
    user_id INT,
    CONSTRAINT pk_transactions PRIMARY KEY (id, label, booking_date_time, amount),
    CONSTRAINT fk_transactions_user_id FOREIGN KEY (user_id) REFERENCES public.accounts (id)
);
