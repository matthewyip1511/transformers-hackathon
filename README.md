# An Intro to our Telegram Bot
Hello!

We created this bot drawing inspiration from the COVID-19 pandemic in Singapore. 

Back in 2021, Singapore faced a surge of COVID-19 cases that overwhelmed the Ministry of Health in Singapore. Most people called the MOH hotline when they were unsure what to do with regard to COVID-19, but this flooded their hotlines and they were not able to answer most of their concerns. This was because they had no way to filter the urgency level of incoming messages and therefore had to answer to them one by one manually.

We created this telegram bot to overcome this challange. We made use of the text classification ability of GPT-3 to classify incoming messages to the bot based on their urgency levels, and the right level of assistance would then be provided. 

**How we created the telegram bot:**

Step 1: Create a bot using telegram botfather and obtain the unique API token 
![image](https://user-images.githubusercontent.com/95226664/198872494-a8cec197-3156-4114-bf15-3ba07d53c5df.png)

Step 2: Obtain OpenAI API key to access GPT-3 models
![image](https://user-images.githubusercontent.com/95226664/198872427-14e0304d-929f-46df-8930-74882dafa574.png)

Step 3: Train the model with sample messages and their labelled urgencies
![image](https://user-images.githubusercontent.com/95226664/198872648-e3a36aec-f3e6-4990-b017-2446bba7eeef.png)


Step 4: Test the model with user-generated messages to check its accuracy

**Urgency levels we chose to adopt:**

0 - Spam, nonsense messages. Unrelated to health issues.
Eg. What is your favourite colour?

1 - User needs help but it is not time-critical at all, users can read the answers themselves on the Ministry of Health website
Eg. What is the covid situation in Singapore now?

2 - User needs help but help can be provided through an automated chatbot / text
Eg. A family member is sick with Covid at home, can I still go to work? 

3 - User has serious issues that require the immediate attention of a call centre
Eg. My throat hurts really badly.. where do I go?

