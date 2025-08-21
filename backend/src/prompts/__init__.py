"""
Prompt templates for different AI interactions.
"""


def translation_prompt(user_message: str) -> str:
    """
    Create a translation prompt to ensure the message is in English.
    
    Args:
        user_message: The user's message that needs to be translated to English
        
    Returns:
        Complete prompt for the AI model
    """
    return f"""You are an english language expert. You will receive a user message and you have to make sure it's written in english. 
If the message is written in english? just say it back as it is (don't change a single character). 
if the message is written in another language? detect the language and translate the prompt to english. Don't explicitly translate but say it as how an english native guy will say it. 

You must just reply with the english sentence. 
You must not say anything before the pormpt. 
You must not say anything after the prompt. 
Don't even say 'Here is the translation ... '

{user_message}"""


def therapy_prompt(user_issue: str) -> str:
    """
    Create a therapy prompt for psychological guidance.
    
    Args:
        user_issue: The user's problem or issue
        
    Returns:
        Complete prompt for the AI model
    """
    return f"""You are a psychological therapist; please respond to any user problem with a single, concise sentence that resolves the issue and provides comfort. Your should help user feel better, feel piece, and cure his pain. The sentence should be the English translation of a verse from the Quran that addresses the user's issue. 
You must not say anything before the sentence. 
You must not even say "Here is the sentence:..."
You must not say anything after the sentence. 
JUST REPLY WITH THE SENTENCE

Here is the user issue:
{user_issue}"""
