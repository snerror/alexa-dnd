/* eslint-disable  func-names */
/* eslint quote-props: ["error", "consistent"]*/
/**
 * This sample demonstrates a simple skill built with the Amazon Alexa Skills
 * nodejs skill development kit.
 * This sample supports multiple lauguages. (en-US, en-GB, de-DE).
 * The Intent Schema, Custom Slots and Sample Utterances for this skill, as well
 * as testing instructions are located at https://github.com/alexa/skill-sample-nodejs-fact
 **/

'use strict';
const Alexa = require('alexa-sdk');
const http = require('http');

//=========================================================================================================================================
//TODO: The items below this comment need your attention.
//=========================================================================================================================================

//Replace with your app ID (OPTIONAL).  You can find this value at the top of your skill's page on http://developer.amazon.com.
//Make sure to enclose your value in quotes, like this: const APP_ID = 'amzn1.ask.skill.bb4045e6-b3e8-4133-b650-72923c5980f1';
const APP_ID = 'amzn1.ask.skill.50a9b122-b3b3-486a-8a6b-5fdac390470d';

const SKILL_NAME = 'Alexa Dungeons and Dragons';
const IMPATIENT_REPROMPT = 'I am growing impatient, hurry up mortal!';
const GET_FACT_MESSAGE = "Here's your fact: ";
const HELP_MESSAGE = 'You can say tell me a space fact, or, you can say exit... What can I help you with?';
const HELP_REPROMPT = 'What can I help you with?';
const STOP_MESSAGE = 'Goodbye!';

//=========================================================================================================================================
//TODO: Replace this data with your own.  You can find translations of this data at http://github.com/alexa/skill-sample-node-js-fact/data
//=========================================================================================================================================
const data = [
    'A year on Mercury is just 88 days long.',
    'Despite being farther from the Sun, Venus experiences higher temperatures than Mercury.',
    'Venus rotates counter-clockwise, possibly because of a collision in the past with an asteroid.',
    'On Mars, the Sun appears about half the size as it does on Earth.',
    'Earth is the only planet not named after a god.',
    'Jupiter has the shortest day of all the planets.',
    'The Milky Way galaxy will collide with the Andromeda Galaxy in about 5 billion years.',
    'The Sun contains 99.86% of the mass in the Solar System.',
    'The Sun is an almost perfect sphere.',
    'A total solar eclipse can happen once every 1 to 2 years. This makes them a rare event.',
    'Saturn radiates two and a half times more energy into space than it receives from the sun.',
    'The temperature inside the Sun can reach 15 million degrees Celsius.',
    'The Moon is moving approximately 3.8 cm away from our planet every year.',
];

//=========================================================================================================================================
//Editing anything below this line might break your skill.
//=========================================================================================================================================

const API_ENDPOINT = 'http://172.104.224.219:8080';

const handlers = {
    'LaunchRequest': function () {
        let speechOutput = 'Welcome to Dungeons and Dragons on Alexa, adventure awaits. You must choose between 3 classes, in order to begin the game. Shall you be a fighter, rogue or cleric?';

        this.response.speak(speechOutput).listen(IMPATIENT_REPROMPT);
        this.emit(':responseReady');
    },
    'SetPlayerClass': function () {
        const classValue = this.event.request.intent.slots.Class.value;

        http.get(API_ENDPOINT + '/player/class/' + classValue, (resp) => {
            let data = '';

            resp.on('data', (chunk) => {
                data += chunk;
            });

            resp.on('end', () => {
                this.response.speak(JSON.parse(data).alexaResponse).listen(IMPATIENT_REPROMPT);
                this.emit(':responseReady');
            });
        }).on("error", (err) => {
            console.log("Error: " + err.message);
        });
    },
    'GetPlayerDetails': function () {
        http.get(API_ENDPOINT + '/player', (resp) => {
            let data = '';

            resp.on('data', (chunk) => {
                data += chunk;
            });

            resp.on('end', () => {
                this.response.speak(JSON.parse(data).alexaResponse).listen(IMPATIENT_REPROMPT);
                this.emit(':responseReady');
            });
        }).on("error", (err) => {
            console.log("Error: " + err.message);
        });
    },
    'MovePlayer': function () {
        const direction = this.event.request.intent.slots.Direction.value;

        http.get(API_ENDPOINT + '/player/move/' + direction, (resp) => {
            let data = '';

            resp.on('data', (chunk) => {
                data += chunk;
            });

            resp.on('end', () => {
                this.response.speak(JSON.parse(data).alexaResponse).listen(IMPATIENT_REPROMPT);
                this.emit(':responseReady');
            });
        }).on("error", (err) => {
            console.log("Error: " + err.message);
        });
    },
    'PlayerAttack': function () {
        const ability = this.event.request.intent.slots.Ability.value;

        http.get(API_ENDPOINT + '/player/attack/' + ability, (resp) => {
            let data = '';

            resp.on('data', (chunk) => {
                data += chunk;
            });

            resp.on('end', () => {
                this.response.speak(JSON.parse(data).alexaResponse).listen(IMPATIENT_REPROMPT);
                this.emit(':responseReady');
            });
        }).on("error", (err) => {
            console.log("Error: " + err.message);
        });
    },
    'ResetDungeon': function () {
        http.get(API_ENDPOINT + '/reset', (resp) => {
            let data = '';

            resp.on('data', (chunk) => {
                data += chunk;
            });

            resp.on('end', () => {
                this.response.speak(JSON.parse(data).alexaResponse).listen(IMPATIENT_REPROMPT);
                this.emit(':responseReady');
            });
        }).on("error", (err) => {
            console.log("Error: " + err.message);
        });
    },
    'AMAZON.HelpIntent': function () {
        const speechOutput = HELP_MESSAGE;
        const reprompt = HELP_REPROMPT;

        this.response.speak(speechOutput).listen(reprompt);
        this.emit(':responseReady');
    },
    'AMAZON.CancelIntent': function () {
        this.response.speak(STOP_MESSAGE);
        this.emit(':responseReady');
    },
    'AMAZON.StopIntent': function () {
        this.response.speak(STOP_MESSAGE);
        this.emit(':responseReady');
    },
};

exports.handler = function (event, context, callback) {
    const alexa = Alexa.handler(event, context, callback);
    alexa.APP_ID = 'amzn1.ask.skill.50a9b122-b3b3-486a-8a6b-5fdac390470d';
    alexa.registerHandlers(handlers);
    alexa.execute();
};
