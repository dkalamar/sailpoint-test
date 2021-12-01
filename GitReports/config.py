import os


class Config:
    GITHUB_ACCESS_TOKEN = os.environ.get('GITHUB_ACCESS_TOKEN')
    SENDGRID_EMAIL = os.environ.get('SENDGRID_EMAIL ')
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')