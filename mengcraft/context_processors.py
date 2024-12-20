def cookie_consent(request):
    """
    Context processor to add cookie consent variables to all templates
    """
    return {
        'ga_tracking_id': 'G-RV9ZCEST94',  # Replace with your actual GA tracking ID
    }