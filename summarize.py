import csv
from pydantic import BaseModel
from pydantic_settings import BaseSettings
import re
from openai import OpenAI
from openai import OpenAIError  # Corrected import statement
import sys


# Custom configuration class to suppress Pydantic warnings
class CustomConfig(BaseSettings):
    class Config:
        # Set the protected_namespaces attribute to an empty tuple to suppress warnings
        protected_namespaces = ()

# Set your OpenAI API key
api_key = ''

def extract_url(message):
    # Use regular expression to extract URLs from the message
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
    return urls

def get_summary(url):
    # Initialize OpenAI client
    openai_client = OpenAI(api_key=api_key)

    # Define the conversation prompt
    prompt = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"What is a summary of {url}?"}
    ]

    # Generate text completion for summarizing the URL
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt
    )

    # Extract the completion from the response
    completion = response.choices[0].text.strip()

    return completion




def main():
    # Open the CSV file containing website URLs
    with open('messages2.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Create a new CSV file to store summaries
        with open('summaries.csv', 'w', newline='', encoding='utf-8') as summaryfile:
            fieldnames = ['Message ID', 'Date', 'Sender ID', 'Message', 'URL', 'Summary']
            writer = csv.DictWriter(summaryfile, fieldnames=fieldnames)
            writer.writeheader()
            
            # Process only the first 10 rows
            for _ in range(10):
                row = next(reader)
                message_id = row['Message ID']
                date = row['Date']
                sender_id = row['Sender ID']
                message = row['Message']
                
                # Extract URLs from the message
                urls = extract_url(message)
                
                # Iterate over each URL
                for url in urls:
                    # Get summary for the URL
                    try:
                        summary = get_summary(url)
                    except OpenAIError as e:  # Corrected exception name
                        print(f"Error processing URL {url}: {e}")
                        summary = ""  # Set summary to empty string in case of error
                    
                    # Write message details, URL, and summary to the CSV file
                    writer.writerow({'Message ID': message_id, 'Date': date, 'Sender ID': sender_id, 'Message': message, 'URL': url, 'Summary': summary})

if __name__ == "__main__":
    main()
