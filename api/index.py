from app import app

# Vercel expects this function
def handler(event, context):
    return app(event, context)