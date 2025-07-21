def help_text(text):
    """
    Used for adding help text and database comment to a model field.
    """
    return {
        'help_text': text,
        'db_comment': text,
    }
