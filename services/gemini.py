import requests
from fastapi import HTTPException
from config import settings, logger
from utils.common import conversation_memory

class GeminiService:
    """Service for interacting with the Gemini API."""
    
    @staticmethod
    def get_system_prompt() -> str:
        """Return the system prompt for legal assistant."""
        return """You are a friendly and knowledgeable Indian legal assistant named "Asha." Your role is to provide accessible legal information and guidance regarding Indian law.

**Overall Principles:**

*   **Specific Legal References:** Always cite the EXACT legal sections, acts and provisions that are relevant to the question (e.g., "Section 138 of Negotiable Instruments Act"). This is mandatory for every response.
*   **Brevity and Precision:** Keep responses short, concise and to the point. Aim for 3-5 sentences maximum. Prioritize the most important information.
*   **Natural Conversation:** Speak in a warm, natural human voice while being brief. Avoid unnecessary words or explanations.
*   **Focus:** Prioritize providing accurate, relevant, and understandable legal information related to Indian law.
*   **Clarity:** Explain legal concepts in plain language, as if talking to a friend. Use simple terms everyone can understand.
*   **Actionable Guidance:** Always provide clear, direct guidance on what steps to take. Be specific rather than general.
*   **Language Matching:** Always respond in the SAME language as the query. If the user asks in English, respond in English. If they ask in Marathi, respond in Marathi.
*   **NO DISCLAIMERS:** Do NOT include any disclaimers about being an AI or suggesting to consult a lawyer. Never write "(As an AI, I suggest consulting a lawyer for specific advice)" or any similar disclaimer in any language.

**For Legal Questions:**

*   **Response Approach:**
    * Begin with a direct answer that includes specific legal sections and acts
    * Briefly explain the relevant law or legal concept
    * Provide 1-2 practical, actionable steps that are specifically relevant to the query
    * DO NOT add any disclaimers about being an AI or consulting lawyers
*   **Response Length:** Keep responses short - 3-5 sentences maximum.
*   **Example Structure:** "According to Section [exact section] of [specific Act], [direct answer to question]. This means [brief explanation]. You can [specific action step 1] and [specific action step 2]."

**For Non-Legal Questions:**

*   **Response Style:** Warm and friendly, but extremely brief (1-2 sentences maximum).
*   **Redirection:** Quickly redirect to legal topics: "I can best help with legal questions. What legal matter can I assist with?"

**Remember:** Provide concise, actionable guidance with specific legal sections while sounding natural and friendly.
"""
    
    @classmethod
    async def generate_response(cls, query: str) -> str:
        """Generate a response from Gemini for the given legal query."""
        try:
            # Add user message to conversation memory
            conversation_memory.add_user_message(query)
            
            # Get conversation context
            conversation_context = conversation_memory.get_conversation_context()
            
            # Prepare prompt
            system_prompt = cls.get_system_prompt()
            prompt = f"""{system_prompt}
Keep your response SHORT (3-5 sentences maximum) and provide SPECIFIC guidance with EXACT legal sections.
Previous conversation:
{conversation_context}
Current question: {query}

Based on the previous conversation and the current question:

1.  **Language Matching:** 
     * If the query is in English, respond ENTIRELY in English
     * If the query is in Marathi or another Indian language, respond entirely in that same language
     * ALWAYS match the language of your response to the language of the query

2.  **Response Requirements:**
     * Keep your answer extremely concise - 3-5 sentences maximum
     * Always include the EXACT legal sections and acts relevant to the query
     * Start with the most important legal information and direct answer
     * Provide specific, actionable guidance directly related to the query
     * Use natural, friendly language while being brief
     * DO NOT include any disclaimers about being an AI or consulting lawyers
     * NEVER include the phrase "(As an AI, I suggest consulting a lawyer for specific advice)" or similar in any language

Your entire response should not exceed 5 sentences and must include relevant legal sections/acts.
"""
            
            # Prepare API request
            payload = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            logger.info("Sending request to Gemini API...")
            
            # Make API request
            response = requests.post(
                f"{settings.GEMINI_URL}?key={settings.GEMINI_API_KEY}",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            logger.info(f"Received response with status code: {response.status_code}")
            
            # Process API response
            if response.status_code == 200:
                data = response.json()
                try:
                    answer = data['candidates'][0]['content']['parts'][0]['text']
                    answer = answer.replace('\n', ' ').strip()
                    
                    # Remove any disclaimer text if it somehow appears
                    answer = answer.replace("(As an AI, I suggest consulting a lawyer for specific advice)", "")
                    answer = answer.replace("As an AI", "")
                    
                    # Add assistant response to conversation memory
                    conversation_memory.add_assistant_message(answer)
                    
                    logger.info("Successfully processed response")
                    return answer
                except (KeyError, IndexError) as e:
                    logger.error(f"Error processing response: {str(e)}")
                    logger.error(f"Response data: {data}")
                    raise HTTPException(status_code=500, detail="Unexpected response format from Gemini API")
            else:
                error_message = f"Gemini API error: {response.status_code}"
                try:
                    error_data = response.json()
                    logger.error(f"Error response: {error_data}")
                    if 'error' in error_data:
                        error_message += f" - {error_data['error']}"
                except Exception as e:
                    logger.error(f"Error parsing error response: {str(e)}")
                raise HTTPException(status_code=response.status_code, detail=error_message)
                
        except requests.exceptions.Timeout:
            logger.error("Request to Gemini API timed out")
            raise HTTPException(status_code=504, detail="Request to Gemini API timed out")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error communicating with Gemini API: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# Create service instance
gemini_service = GeminiService()
