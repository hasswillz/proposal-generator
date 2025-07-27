#ai_generator.py
from flask_babel import get_locale
from openai import OpenAI, AuthenticationError
from flask import current_app
from datetime import datetime

def generate_proposal(proposal_data):

    """Generates a project proposal using OpenAI's latest API (v1.9.5+)"""
    try:
        # Initialize the OpenAI client (automatically reads OPENAI_API_KEY from env)
        client = OpenAI(api_key=current_app.config['OPENAI_API_KEY'])

        # Test the key first
        try:
            client.models.list()  # Simple API call to verify key
        except AuthenticationError as auth_err:
            current_app.logger.error(f"API Key Validation Failed: {str(auth_err)}")
            raise ValueError("Invalid OpenAI API key configured")

        # Determine the language based on the current session/locale
        current_language = get_locale()
        if current_language == "en":
            language_instruction = "Generate the proposal in English."  # Default
        else:
            language_instruction = "Generate the proposal in Swahili."

        # Prepare the prompt
        prompt = f"""
        Generate a comprehensive {proposal_data['writing_style']} project proposal for:

        **Project Title:** {proposal_data['project_name']}
        **Project Type:** {proposal_data['project_type']}
        **Target Audience:** {proposal_data['audience']} 
                            +{proposal_data['mobile_number']}
        **Technical Level:** {proposal_data['complexity']}

        Project Description:
        {proposal_data['description']}

        **Budget:** Tsh{proposal_data['budget']:,.2f}
        **Duration:** {proposal_data['duration_weeks']} weeks
     

        **Instructions:**
        1.{language_instruction}
        2. Use {proposal_data['writing_style']} writing style
        3. Include all standard proposal sections such as
             -Project Description
             -Objectives
             -Methodology
             - Project Activities
             -Budget Breakdown
             -Timeline
             -Expected Outcomes and expectations
             - Sustainability 
             -Conclusion
        4. Format using Markdown (Arial font, Arial, font heading 12,  body 11 )
        """

        # Make the API call (updated for OpenAI 1.9.5+)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",  # or "gpt-4-turbo"
            messages=[
                {"role": "system", "content": "You are a professional proposal writer."},
                {"role": "user", "content": prompt}
            ],
            seed=42,
            temperature=0.7,
            max_tokens=2000,
            stream= False,
            response_format={"type": "text"}  # Explicitly request text output (new in 1.9.5)
        )

        # Extract the content (same as v1.0.0)
        generated_content = response.choices[0].message.content

        # Add metadata
        proposal_meta = f"""# {proposal_data['project_name']}

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Author:** {proposal_data.get('contact_email', '')}  
**Project Type:** {proposal_data['project_type']}  
__Budget:__ Tsh{proposal_data['budget']:,.2f}  
__Duration:__ {proposal_data['duration_weeks']} weeks  

---
"""
        return proposal_meta + generated_content

    except Exception as e:
        current_app.logger.error(f"AI generation failed: {str(e)}")
        raise Exception("Failed to generate proposal. Please try again later.")
