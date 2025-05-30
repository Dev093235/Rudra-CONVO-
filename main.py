import requests
import os
import time

# --- Configuration ---
# आप यहां अपना पासवर्ड सेट कर सकते हैं। वास्तविक अनुप्रयोगों में, इसे एन्क्रिप्टेड रखा जाना चाहिए।
SECRET_PASSWORD = "your_secret_password_here" # इसे बदल दें!

# --- Facebook Graph API Base URL ---
GRAPH_API_URL = "https://graph.facebook.com/v19.0/" # Facebook Graph API का नवीनतम संस्करण

def send_message(access_token, recipient_id, message_text):
    """
    Facebook Graph API का उपयोग करके एक मैसेंजर संदेश भेजता है।
    """
    url = f"{GRAPH_API_URL}me/messages"
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "access_token": access_token
    }
    payload = {
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    }
    
    try:
        response = requests.post(url, headers=headers, params=params, json=payload)
        response.raise_for_status() # HTTP errors के लिए
        data = response.json()
        if "error" in data:
            print(f"Error sending message to {recipient_id}: {data['error']['message']}")
            return False
        else:
            print(f"Message sent successfully to {recipient_id}. Message ID: {data['message_id']}")
            return True
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return False

def main():
    """
    मुख्य फ़ंक्शन जो इनपुट लेता है और संदेश भेजने की प्रक्रिया को नियंत्रित करता है।
    """
    print("--- Messenger Bot Tool ---")

    # 1. पासवर्ड इनपुट
    entered_password = input("Enter password to use the tool: ")
    if entered_password != SECRET_PASSWORD:
        print("Incorrect password. Exiting.")
        return

    # 2. Facebook Access Token इनपुट
    fb_access_token = input("Enter your Facebook Page Access Token: ")
    if not fb_access_token:
        print("Facebook Access Token cannot be empty. Exiting.")
        return

    # 3. लक्ष्य Facebook UID इनपुट
    target_uid = input("Enter the target Facebook User ID (UID): ")
    if not target_uid:
        print("Target UID cannot be empty. Exiting.")
        return

    # 4. Np File पाथ इनपुट
    np_file_path = input("Enter the path to your Np File (.txt with messages): ")
    if not np_file_path:
        print("Np File path cannot be empty. Exiting.")
        return

    if not os.path.exists(np_file_path):
        print(f"Error: Np File not found at '{np_file_path}'. Exiting.")
        return

    messages = []
    try:
        with open(np_file_path, 'r', encoding='utf-8') as f:
            messages = [line.strip() for line in f if line.strip()] # खाली लाइनों को छोड़ दें
        if not messages:
            print("Np File is empty or contains no valid messages. Exiting.")
            return
        print(f"Loaded {len(messages)} messages from '{np_file_path}'.")
    except Exception as e:
        print(f"Error reading Np File: {e}. Exiting.")
        return

    # 5. संदेश भेजने की प्रक्रिया
    print("\n--- Starting message sending process ---")
    print(f"Sending messages to UID: {target_uid}")

    for i, msg in enumerate(messages):
        print(f"\nAttempting to send message {i+1}/{len(messages)}: '{msg}'")
        success = send_message(fb_access_token, target_uid, msg)
        if success:
            print(f"Successfully sent message {i+1}.")
        else:
            print(f"Failed to send message {i+1}.")
        
        # आप यहां संदेशों के बीच एक देरी जोड़ सकते हैं ताकि रेट लिमिट से बचा जा सके।
        # उदाहरण के लिए, 2 सेकंड की देरी:
        time.sleep(2) 

    print("\n--- Message sending process completed ---")

if __name__ == "__main__":
    main()
