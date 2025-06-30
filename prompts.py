def build_story_prompt(age, character, setting, genre, moral):
    return f"""
You are a creative children's storyteller. Write a short story for a child aged {age}.
Make the main character {character}, set the story in a {setting}, and write it in a {genre} style.
End with a moral about {moral}. Use simple, fun language. Keep it under 300 words.
"""