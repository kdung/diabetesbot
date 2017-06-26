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
                                       'content':'Are you pregnant?'
                                   },
                                   {
                                      'version': 1,
                                      'contentType':'application/vnd.amazonaws.card.generic',
                                      'genericAttachments': [
                                          {
                                             'title': 'Are you pregnant?',
                                             'subTitle':'this information will help me diagnose if you have gestational diabetes',
                                             'imageUrl':None,
                                             'attachmentLinkUrl':None,
                                             'buttons':[ 
                                                 {  
                                                    'text':'no',
                                                    'value':'no'
                                                 },
                                                 {
                                                    'text':'yes',
                                                    'value':'yes'
                                                 }
                                              ]
                                           } 
                                       ] 
                                    }
                                )
        if gender is not None and slots['pregnant'] is not None and slots['age'] is not None:
            is_pregnant = slots['pregnant'] == 'yes'
            if is_empty_slot('ogtt', slots):
                ogtt_subtitle = None
                if is_pregnant:
                    ogtt_subtitle = 'Reference ranges: healthy (<= 7.7mmol/L), unhealthy (>7.7mmol/L)'
                else:
                    ogtt_subtitle = 'Reference ranges: healthy (< 11.1mmol/L), unhealthy (>=11.1mmol/L)'
                return elicit_slot(session_attributes,
                                       intent_name,
                                       slots,
                                       'ogtt',
                                       {
                                           'contentType': 'PlainText',
                                           'content':'Is your blood glucose level (mmol/L) shown in 2-hours post Oral Glucose Tolerance test (OGTT) in healthy range?'
                                       },
                                       {
                                          'version': 1,
                                          'contentType':'application/vnd.amazonaws.card.generic',
                                          'genericAttachments': [
                                              {
                                                 'title': 'Your Oral Glucose Tolerance test status:',
                                                 'subTitle':ogtt_subtitle,
                                                 'imageUrl':None,
                                                 'attachmentLinkUrl':None,
                                                 'buttons':[ 
                                                     {
                                                        'text':'healthy',
                                                        'value':'healthy'
                                                     },
                                                     {
                                                        'text':'unhealthy',
                                                        'value':'unhealthy'
                                                     },
                                                     {
                                                        'text':'I don\'t know',
                                                        'value':'not available'
                                                     }
                                                  ]
                                               } 
                                           ] 
                                        }
                                    )
            
            if not is_pregnant:
                if is_empty_slot('fpg', slots):
                    return elicit_slot(session_attributes,
                                       intent_name,
                                       slots,
                                       'fpg',
                                       {
                                           'contentType': 'PlainText',
                                           'content':'Is your blood glucose level (mmol/L) shown in Fasting Plasma Glucose test (FPG) in healthy range?'
                                       },
                                       {
                                          'version': 1,
                                          'contentType':'application/vnd.amazonaws.card.generic',
                                          'genericAttachments': [
                                              {
                                                 'title': 'Your Fasting Plasma Glucose test (FPG) test status:',
                                                 'subTitle':'Reference ranges (mmol/L): healthy (< 6.1), at risk (6.1-6.9), unhealthy (>7.0)',
                                                 'imageUrl':None,
                                                 'attachmentLinkUrl':None,
                                                 'buttons':[ 
                                                     {
                                                        'text':'healthy',
                                                        'value':'healthy'
                                                     },
                                                     {
                                                        'text':'at risk',
                                                        'value':'at risk'
                                                     },
                                                     {
                                                        'text':'unhealthy',
                                                        'value':'unhealthy'
                                                     },
                                                     {
                                                        'text':'I don\'t know',
                                                        'value':'not available'
                                                     }
                                                  ]
                                               } 
                                           ] 
                                        }
                                    )
                if is_empty_slot('cpg', slots):
                    return elicit_slot(session_attributes,
                                       intent_name,
                                       slots,
                                       'cpg',
                                       {
                                           'contentType': 'PlainText',
                                           'content':'How much is your blood glucose level (mmol/L) shown in Casual Plasma Glucose test (CPG)?'
                                       },
                                       {
                                          'version': 1,
                                          'contentType':'application/vnd.amazonaws.card.generic',
                                          'genericAttachments': [
                                              {
                                                 'title': 'Your Casual Plasma Glucose test (CPG) status:',
                                                 'subTitle':'Reference ranges: healthy (< 11.1mmol/L), unhealthy (>=11.1mmol/L)',
                                                 'imageUrl':None,
                                                 'attachmentLinkUrl':None,
                                                 'buttons':[ 
                                                     {
                                                        'text':'healthy',
                                                        'value':'healthy'
                                                     },
                                                     {
                                                        'text':'unhealthy',
                                                        'value':'unhealthy'
                                                     },
                                                     {
                                                        'text':'I don\'t know',
                                                        'value':'not available'
                                                     }
                                                  ]
                                               } 
                                           ] 
                                        }
                                    )
                if is_empty_slot('bmi', slots):
                    return elicit_slot(session_attributes,
                                       intent_name,
                                       slots,
                                       'bmi',
                                       {
                                           'contentType': 'PlainText',
                                           'content':'How is your Body Mass Index (BMI)?'
                                       },
                                       {
                                          'version': 1,
                                          'contentType':'application/vnd.amazonaws.card.generic',
                                          'genericAttachments': [
                                              {
                                                 'title': 'Your Body Mass Index (BMI) indicates:',
                                                 'subTitle':'Reference ranges: obesity (>30), overweight (from 25 to 29.9), normal (< 25)',
                                                 'imageUrl':None,
                                                 'attachmentLinkUrl':None,
                                                 'buttons':[ 
                                                     {
                                                        'text':'obesity',
                                                        'value':'obesity'
                                                     },
                                                     {
                                                        'text':'overweight',
                                                        'value':'overweight'
                                                     },
                                                     {
                                                        'text':'normal',
                                                        'value':'normal'
                                                     }
                                                  ]
                                               } 
                                           ] 
                                        }
                                    )
            elif is_empty_slot('gestationalHistory', slots):
                return elicit_slot(session_attributes,
                                       intent_name,
                                       slots,
                                       'gestationalHistory',
                                       {
                                           'contentType': 'PlainText',
                                           'content':'Do you have history of gestational diabetes or having baby with over 4kg (yes/no)?'
                                       },
                                       {
                                          'version': 1,
                                          'contentType':'application/vnd.amazonaws.card.generic',
                                          'genericAttachments': [
                                              {
                                                 'title':'Do you have history of gestational diabetes or having baby with over 4kg?',
                                                 'subTitle':'this information will help me diagnose if you have gestational diabetes',
                                                 'imageUrl':None,
                                                 'attachmentLinkUrl':None,
                                                 'buttons':[ 
                                                     {
                                                        'text':'yes',
                                                        'value':'yes'
                                                     },
                                                     {
                                                        'text':'no',
                                                        'value':'no'
                                                     }
                                                  ]
                                               } 
                                           ] 
                                        }
                                    )
            
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

def is_empty_slot(slot_name, slots):
    return slots[slot_name] is None


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
    
def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message, response_card):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message,
            'responseCard': response_card
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
