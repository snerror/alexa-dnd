from __future__ import print_function

import json

# --------------- Helpers that build all of the responses ----------------------
from player_class import PlayerClass

# Phases
from room import Room

INTRO_PHASE = 'INTRO'
COMBAT_PHASE = 'COMBAT_PHASE'
EXPLORATION_PHASE = 'EXPLORATION_PHASE'

# Classes
WARRIOR = "warrior"
WIZARD = "wizard"


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Dungeons and Dragons on Alexa. Adventurer are you ready to choose your class?"
    reprompt_text = "My patience is thin, I shan't ask again"
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. Have a nice day! "
    should_end_session = True

    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def into_choose_player_class(intent, session):
    session_attributes = {"phase": INTRO_PHASE, "room": Room().toJSON()}
    should_end_session = False

    card_title = "IntroSetPlayerClass"
    speech_output = "Shall you be a warrior or a wizard?"
    reprompt_text = "My patience is thin, I shan't ask again"

    return build_response(session_attributes, build_speechlet_response(
        card_title,
        speech_output, reprompt_text, should_end_session))


def into_set_player_class(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Class' in intent['slots']:
        player_class = PlayerClass(intent['slots']['Class']['value'])
        session_attributes = {"phase": INTRO_PHASE, "room": session['attributes']['room'],
                              "player": player_class.toJSON()}

        speech_output = "Welcome to our world young " + player_class.class_name + ". Are you ready to begin?"
        reprompt_text = "I'm becoming impatient"
    else:
        speech_output = "That is not on the table. Choose again."
        reprompt_text = "That is not on the table. Choose again."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def intro_begin_dungeon(intent, session):
    session_attributes = {}

    room = json.loads(session['attributes']['room'])

    card_title = "Begin Dungeon"

    speech_output = "Some intro text. You enter the first room and start looking around. It was " + room['description']
    reprompt_text = "My patience is thin, I shan't ask again"

    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def core_player_details(intent, session):
    session_attributes = {}

    player = json.loads(session['attributes']['player'])

    card_title = "Class Details"
    speech_output = "The " + player['class_name'] + " has the following attributes:" \
                                                    "Health: " + str(player['hp']) + \
                    ". AC: " + str(player['ac']) + \
                    ". Surge: " + str(player['surge'])
    reprompt_text = "My patience is thin, I shan't ask again"

    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    if intent_name == "IntroStartConfirm":
        return into_choose_player_class(intent, session)
    if intent_name == "IntroChooseClass":
        return into_set_player_class(intent, session)
    if intent_name == "IntroBeginDungeon":
        return intro_begin_dungeon(intent, session)
    if intent_name == "CorePlayerDetails":
        return core_player_details(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
