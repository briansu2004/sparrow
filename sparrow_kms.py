#!/usr/bin/env python
import boto3
import base64
import random
import json
from twython import Twython

# Credentials setup
# Loads in 'creds.json' values as a dictionary
with open('creds.json') as f:
    credentials = json.loads(f.read())

# Setup KMS client
kms = boto3.client('kms')

# Use this function in the python shell to encrypt the
# values you will store in the config file
def encrypt(b_plaintext, key_id):
    """Encrypt plaintext with KMS key"""
    kms_result = kms.encrypt(
        # Sample key_id format: 'alias/MyAliasName'
        KeyId = key_id, 
        Plaintext = b_plaintext
    )
    ciphertext = base64.b64encode(kms_result['CiphertextBlob'])
    print ciphertext
    return ciphertext

def decrypt(ciphertext):
    """Decrypt ciphertext with KMS"""
    kms = boto3.client('kms')  
    print 'Decrypting ciphertext with KMS'
    plaintext = kms.decrypt(CiphertextBlob = base64.b64decode(ciphertext))['Plaintext']
    return plaintext

# Decrypts API keys and sets config values from the config file
CONSUMER_KEY = decrypt(credentials["consumer_key"])
CONSUMER_SECRET = decrypt(credentials["consumer_secret"])
ACCESS_TOKEN_KEY = decrypt(credentials["access_token_key"])
ACCESS_TOKEN_SECRET = decrypt(credentials["access_token_secret"])

# Create the Twython Twitter client using our credentials
twitter = Twython(
    CONSUMER_KEY, 
    CONSUMER_SECRET,
    ACCESS_TOKEN_KEY,
    ACCESS_TOKEN_SECRET
)

# Sample random tweets
potential_tweets = [
    'This is my first tweet with Sparrow by @fmcorey - https://github.com/fmcorey/sparrow',
    'Wow! Isn\'t Sparrow by @fmcorey just the coolest! https://github.com/fmcorey/sparrow',
    'Jeez! Everyone should learn about AWS Lambda and Twitter Bots from @fmcorey'
]

def send_tweet(tweet_text):
    """Sends a tweet to Twitter"""
    twitter.update_status(status = tweet_text)

def handler(event,context):
    """Sends random tweet from list of potential tweets"""
    send_tweet(random.choice(potential_tweets))