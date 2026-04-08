# Import Groq client from configuration file
from source.Api_config import client


#  Task 1: Conversation Manager
# This class manages chat history and automatically summarizes conversations
# after a fixed number of turns using an LLM.

''' 1 create a class named cm
    2 default turns are 3
    3 create a list where we want to store chat
   4 store maximum number of turns
   5 count the chat turn'''



class ConversationManager:                        
    def __init__(self, k=3):                        
        self.history = []          ## Initialize conversation history list                         
        self.k = k                 ##  k defines after how many messages summarization will happen                   
        self.turn_count = 0         ## Counter to track number of messages exchanged                   



    ''' 1 create a function to add messages to the list we created above 
    2 append msgs in such a way that it include role and content 
    3 if we received and send message its count increases
    '''
    def add_message(self, role, content):

        """
        Adds a message to conversation history
        Parameters:
        - role: "user" or "assistant"
        - content: actual message text
        
         Also increments turn count and triggers summarization
        after every k messages
        """
        #  Store message in structured format
        self.history.append({"role": role, "content": content})
    # Increase message count
        self.turn_count += 1

        ''' 1 we will check the count of msgs if count will be divisible by k .. we summarize the entire chat'''
        #  If number of messages is divisible by k → summarize history
        if self.turn_count % self.k == 0:
            self.summarize_history()
    

    
    '''Correct: summarize the entire history into a short text; first concatenate all messages into one string
    '''

    def summarize_history(self):
        """
         Summarizes the entire conversation history
        
        Steps:
        1. Combine all messages into a single string
        2. Send it to LLM for summarization
        3. Replace full history with summarized version
        
        Purpose:
        - Reduce token usage
        - Maintain context efficiently
        """
        # Convert conversation history into a single text block
        text_to_summarize = ""
        for m in self.history:
            text_to_summarize += f"{m['role']}: {m['content']}\n"
         
        # Send request to Groq LLM for summarization
        '''here we find out the response of the model 
        1  Call client.chat.completions.create to ask model for summary,
        
        2 response parameters are = model,messages
        3  use groq  model llama 3.1
        4 in messages  we see that msgs send to the system it summarize after 3 chats and return history     '''
        response = client.chat.completions.create(       ## client = groq connection,chat = chat style api,completion = jo adhuri baat reh gayi usko pura karna,create= create new connection
            model="llama-3.1-8b-instant",    
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Summarize the conversation briefly."},
                {"role": "user", "content": text_to_summarize}            ## to give user's actual message here
            ]
        )
        #  Extract summarized text from response
        ## response = when we call model it sends a response object,
        summary = response.choices[0].message.content   ## pehle answer ka actual text
        
        #  Replace full history with summarized version
        # This keeps context short and efficient for future interactions
        self.history = [{"role": "system", "content": f"Summary: {summary}"}]
        ## it replaces the old history in single summarized version kyunki next wale mein well set context mile bda nahi