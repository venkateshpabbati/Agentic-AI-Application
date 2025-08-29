def build_analysis_prompt(user_query):
    """Generate a prompt for video analysis."""
    return (
        f"Analyze the uploaded video for content and context.\n"
        f"Respond to the following query using video insights and supplementary web research:\n"
        f"{user_query}\n\n"
        f"Provide a detailed, user-friendly, and actionable response."
    )
