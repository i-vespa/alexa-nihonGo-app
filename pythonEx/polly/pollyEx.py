"""Getting Started Example for Python 2.7+/3.3+"""
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir

#Van: added - for commandline input
import sys
text = sys.argv[1:] #5/20 changed this to text inputText = sys.argv[1:] #should be english text
text = ' '.join(text)#inputText)
print(text)

# Create a client using the credentials and region defined in the [adminuser]
# section of the AWS credentials file (~/.aws/credentials).
#session = Session(profile_name="adminuser")
session = Session(profile_name="pollyTest")

polly = session.client("polly")

#VAN 3-19 TODO: How to get to japanese text to read into polly from python - so far using romaji and pronunciation is wierd

#VAN 3-19 TODO: Get japanese translation of text txt hook to API HERE
engToJ = "inu" #hook to API to tranlate English text to japanese


#--------------TEST: ADDING TRANSLAE FUNCTIONALITY ---------#
# Imports the Google Cloud client library
from google.cloud import translate

# Instantiates a client
translate_client = translate.Client()

# The text to translate
#text = u'It is raining today!'
# The target language
target = 'ja'

# Translates some text into Japanese 
translation = translate_client.translate(
    text,
    target_language=target)

print(u'Text: {}'.format(text))
print(u'Translation: {}'.format(translation['translatedText']))
txt = u'{}'.format(translation['translatedText'])#5/2:replac user input with translation
#--------------TEST ---------#

try:
    # Request speech synthesis
    """response = polly.synthesize_speech(Text=engToJ, OutputFormat="mp3",
                                        VoiceId="Mizuki")"""
    response = polly.synthesize_speech(Text=txt, OutputFormat="mp3",
                                        VoiceId="Mizuki")

except (BotoCoreError, ClientError) as error:
    # The service returned an error, exit gracefully
    print(error)
    sys.exit(-1)

# Access the audio stream from the response
if "AudioStream" in response:
    # Note: Closing the stream is important as the service throttles on the
    # number of parallel connections. Here we are using contextlib.closing to
    # ensure the close method of the stream object will be called automatically
    # at the end of the with statement's scope.
    with closing(response["AudioStream"]) as stream:
        output = os.path.join(gettempdir(), "speech.mp3")

        try:
            # Open a file for writing the output as a binary stream
            with open(output, "wb") as file:
                file.write(stream.read())
        except IOError as error:
            # Could not write to file, exit gracefully
            print(error)
            sys.exit(-1)

else:
    # The response didn't contain audio data, exit gracefully
    print("Could not stream audio")
    sys.exit(-1)

# Play the audio using the platform's default player
if sys.platform == "win32":
    os.startfile(output)
else:
    # the following works on Mac and Linux. (Darwin = mac, xdg-open = linux).
    opener = "open" if sys.platform == "darwin" else "xdg-open"
subprocess.call([opener, output])
