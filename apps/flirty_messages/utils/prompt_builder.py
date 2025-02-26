def build_prompt(
    audience,
    tone,
    purpose,
    traits,
    emotions,
    context,
    themes,
    language,
    style,
    num_lines,
    additional_text=""
):
    """
    Build the prompt string from the user selections.
    
    Args:
        audience (str): Target audience for the message
        tone (str): Desired tone of the message
        purpose (str): Primary purpose of the message
        traits (str): Traits of the person receiving the message
        emotions (str): Emotions to convey
        context (str): Context or situation for the message
        themes (str): Themes or references to include
        language (str): Language for the message
        style (str): Overall style of the message
        num_lines (str): Number of lines to generate
        additional_text (str, optional): Additional custom details to include
        
    Returns:
        str: The constructed prompt for the AI model
    """
    prompt = (
        f"Please generate a {tone} message in {language} for a {audience} audience, "
        f"with the primary purpose of {purpose}. "
        f"This message should be tailored to someone who is {traits}, "
        f"conveying a sense of {emotions}, and fitting the {context} situation. "
        f"Incorporate the theme(s)/reference(s) of {themes}, "
        f"and ensure the overall style is {style}. "
        f"\n\nGenerate {num_lines} line(s) only."
        "\nPlease ensure the lines are concise, creative, and fit the described context."
    )
    
    # Add additional text if provided
    if additional_text:
        prompt += f"\n\nAdditional details to consider: {additional_text}"
    
    return prompt