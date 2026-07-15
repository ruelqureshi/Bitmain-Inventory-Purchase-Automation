# Bitmain Purchase Automation

## Overview

This project automates the process of purchasing products from the Bitmain store as soon as they become available.

It consists of two scripts working together. The first script continuously monitors the selected product using Bitmain's product API and waits for the product to become available for purchase. Once stock is detected, it automatically launches the purchasing script.

The purchasing script logs into a Bitmain account, opens the checkout page for the selected product, completes the checkout flow, solves the verification CAPTCHA using the 2Captcha service, and submits the order. The requested quantity is automatically adjusted if it exceeds Bitmain's purchase limit for the product.


Note: You need python 3.7 or above to run this program
1 - First install the dependencies by executing this command in CMD pip install -r requirements.txt
2 - Next open the settings.ini file and enter your 2captcha API key, quantity to purchase and Bitmain account credentials.
3 - Open CMD.
4 - In CMD navigate to the folder where the files are located and enter the following command python bitmain_scanner.py.
