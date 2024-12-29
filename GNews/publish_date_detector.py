import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import os

def get_clean_text(url):
    """
    Retrieves and cleans the text content of the <body> tag from the specified URL,
    preserving meaningful content within tags like <header>, <h1>, <p>, <a>, etc.

    Parameters:
        url (str): The URL of the webpage to retrieve.

    Returns:
        str: Clean text content of the webpage's body if successful.
        None: If there was an error during the request or processing.
    """
    try:
        # Define headers to mimic a browser visit
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }

        # Send a GET request to the URL with a timeout of 10 seconds
        response = requests.get(url, headers=headers, timeout=10)

        # Raise an HTTPError if the response was unsuccessful (e.g., 404, 500)
        response.raise_for_status()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the <body> tag
        body = soup.body
        if not body:
            print("No <body> tag found in the HTML.")
            return None

        # Remove all <script> and <style> elements from the body
        for element in body(['script', 'style']):
            element.decompose()

        # Extract text from the body, separating blocks with newline characters
        text = body.get_text(separator='\n', strip=True)

        # Further clean the text by removing extra whitespace and blank lines
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        clean_text = '\n'.join(lines)

        return clean_text

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # HTTP error
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")  # Network problem
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")  # Timeout
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")  # Any other error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")  # Other exceptions
    return None

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_GNEWS_KEY"),  # This is the default and can be omitted
)

def extract_publish_date(article_text):
    """
    Extracts publish_date mentioned in a news article using OpenAI's API.
    :param article_text: The text of the news article.
    :return: a publish date or None if can't do it.
    """

    prompt = f"""
    Please parse the following web page content for a news article and extract the publish date. It's usually listed close to the beginning of the content.

    Output should just be a simple date formatted string with only digits and dash and no any other words in it, such as: 

    2024-06-02 

    If you can't find any date in the content, please return one word "None".

    Here is the web page content: 

    {article_text}
    """

    # Extract all the locations (e.g., cities, states, countries, landmarks, etc.) mentioned in the following news article:
    
    try:
        # Call the GPT-4 Turbo model
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an assistant skilled at extracting information from text."},
                {"role": "user", "content": prompt}
            ],
            temperature=0  # For consistent and precise outputs
        )
        
        # Extract locations from the response
        result = response.choices[0].message.content.strip()
        print(f"result:{result}")
        if result == "None": 
            result = None
        return result
    except Exception as e:
        print(f"Error: {e}")
        return None

def save_text_to_file(text, filename):
    """
    Saves the provided text to a file.

    Parameters:
        text (str): The text content to save.
        filename (str): The name of the file to save the text in.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"Text successfully saved to {filename}")
    except Exception as e:
        print(f"Failed to save text to file: {e}")

if __name__ == "__main__":
    # Prompt the user to enter a URL
    url = input("Enter the URL: ").strip()

    # Retrieve clean text from the URL
    clean_text = get_clean_text(url)

    if clean_text:
        print("\nClean text content retrieved successfully!\n")
        # To avoid overwhelming the console, we'll print the first 1000 characters
        print(clean_text[:1000] + '...')  # Adjust as needed

        publish_date = extract_publish_date(clean_text)
        print("Publish date:", publish_date)

        # Optionally, save the clean text to a file
        save_option = input("\nWould you like to save the text to a file? (y/n): ").strip().lower()
        if save_option == 'y':
            filename = input("Enter the filename (e.g., output.txt): ").strip()
            save_text_to_file(clean_text, filename)
    else:
        print("Failed to retrieve clean text content.")

    