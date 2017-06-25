#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 17:04:29 2017

@author: sophie
"""

import os
import logging
import time
from functools import reduce

print('Loading function')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

cfmap = {'bloodPressure': {'yes':0.2,'no':-0.2,'na':0},
         'familyHistory': {'yes':0.2,'no':-0.2},
         'triglycerides': {'normal':-0.4,'borderline':0.4,'high':0.5},
         'gestationalHistory': {'yes':0.6,'no':-0.6},
         'exercise': {'yes':0.4,'no':-0.4},
         'glucoseTolerance': {'yes':0.4,'no':-0.4,'na':0},
         'pos': {'yes':0.4,'no':-0.4,'na':0},
         'headache': {'yes':0.2,'no':-0.2},
         'blur': {'yes':0.2,'no':-0.2},
         'excessiveUrination': {'yes':0.4,'no':-0.4},
         'polydipsia': {'yes':0.4,'no':-0.4},
         'lostConsciousness': {'yes':0.2,'no':-0.2},
         'nausea': {'yes':0.2,'no':-0.2},
         'polyphagia': {'yes':0.4,'no':-0.4},
         'tiredness': {'yes':0.4,'no':-0.4},
         'loseWeight': {'yes':0.4,'no':-0.4},
         'fraction': {'yes':0.2,'no':-0.2},
         'infection': {'yes':0.4,'no':-0.4},
         'lostSensation': {'yes':0.2,'no':-0.2},
         'coldSweat': {'yes':0.2,'no':-0.2}
         }


def diagnose_diabetes(intent_request):
    slots = intent_request['currentIntent']['slots']
    derived_cf = [0]
    for slot in slots:
        value = slots[slot]
        print(slot, value)
        if slot in cfmap and value in cfmap[slot]:
            derived_cf.append(cfmap[slot][value])
        
    print(derived_cf)
    result = reduce(combine_cf, derived_cf)
    print(result)
    return close(intent_request['sessionAttributes'],
                'Fulfilled',
                {
                    'contentType': 'PlainText',
                    'content': 'Thank you, good bye.'
                })

def combine_cf(cf1, cf2):
    if cf1 >= 0 and cf2 >= 0:
        return cf1 + cf2 * (1 - cf1)
    elif cf1 < 0 and cf2 < 0:
        return cf1 + cf2 * (1 + cf1)
    else:
        return (cf1 + cf2) / (1 - min(abs(cf1), abs(cf2)))

""" --- utilities functions --- """

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
