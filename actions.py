# Helper functions that perform actions

def swipe_left(d):
    """Swipe left."""
    d.swipe(0.3, 0.3, 0.7, 0.3, 0.1)

def swipe_right(d):
    """Swipe right."""
    d.swipe(0.7, 0.7, 0.3, 0.7, 0.1)