#  Set up environment to use Do My Research

pip3 install gdown

cd api/

# Sentiment Classifer weights
gdown --id 1-rEbHlMb6xTwrslUaY-pa0XF4IuHBB4A

# Tokenizer
gdown --id 1G774iAUMf2ojzaxYtw2NrEfX6tdvEpzV

# Set up virtual environment for Flask
python3 -m venv venv
source venv/bin/activate
pip3 install -r ../requirements.txt

echo "Dependencies have been setup!"
