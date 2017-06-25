#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 17:04:29 2017

@author: sophie
"""

import os
import logging
import time

print('Loading function')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def diagnose_diabetes(intent_request):
    slots = intent_request['currentIntent']['slots']
    source = intent_request['invocationSource']
    gender = slots['gender']
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    intent_name = intent_request['currentIntent']['name']
    
    if source == 'DialogCodeHook':
        validation_result = validate_gender(gender)
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])
        
        if gender in ['male', 'm']:
            slots['pregnant'] = 'no'
        elif gender in ['female', 'f']:
            is_pregnant = slots['pregnant']
            logger.debug('pregnant={}'.format(is_pregnant))
            validation_result = validate_pregnant(is_pregnant)
            if not validation_result['isValid']:
                logger.debug('eclicit bla')
                return elicit_slot(session_attributes,
                                   intent_name,
                                   slots,
                                   'pregnant',
                                   {
                                       'contentType': 'PlainText',
                                       'content':'Are you pregnant? (yes/no)'
                                   })
        return delegate(session_attributes, intent_request['currentIntent']['slots'])
    
    return close(intent_request['sessionAttributes'],
                'Fulfilled',
                {
                    'contentType': 'PlainText',
                    'content': 'Thank you, good bye.'
                })


def validate_gender(gender):
    genders = ['male', 'female', 'm', 'f']
    logger.debug('gender={}'.format(gender))
    if gender is not None and gender.lower() not in genders:
        return build_validation_result(False, 'gender', 'I did not understand that, what is your biological gender (male(m)/female(f)?')
    return build_validation_result(True, None, None)

def validate_pregnant(is_pregnant):
    if is_pregnant is None or is_pregnant.lower() not in ['yes', 'no']:
        logger.debug('pregnant none')
        return build_validation_result(False, 'pregnant', 'I did not understand that, are you pregnant (yes/no)?')
    return build_validation_result(True, None, None)



""" --- utilities functions --- """
def build_validation_result(is_valid, violated_slot, message_content):
    if message_content is None:
        return {
            "isValid": is_valid,
            "violatedSlot": violated_slot,
        }

    return {
        'isValid': is_valid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }
    
def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }
    
def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }
        
def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response
    
""" --- Intents --- """


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'DiagnoseDiabetes':
        return diagnose_diabetes(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')


""" --- Main handler --- """


def handle(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)
