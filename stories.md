## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot

## query_corona_location_path
* query_corona_location
  - action_query_corona_location

## corona_query_path 1

* query_corona
  - utter_query_corona
* goodbye
  - utter_goodbye

## corona_query_path 2
* query_corona
  - utter_query_corona
* query_corona_symptoms
  - utter_query_corona_symptoms

## corona_query_path 3
* query_corona
  - utter_query_corona
* query_corona_spread
  - utter_query_corona_spread

## corona_query_path 4
* query_corona_spread
  - utter_query_corona_spread

## corona_query_path 5
* query_corona_symptoms
  - utter_query_corona_symptoms
* query_corona_more_info
  - utter_query_corona_symptoms

## corona_query_path 6
* query_corona
  - utter_query_corona

## corona_query_path 7
* query_corona_spread_person_sexually
  - utter_query_corona_spread_person_sexually

## corona_query_path 8

* query_corona_isolation
  - utter_query_corona_isolation

## corona_query_path 9
* query_corona_protection
  - utter_query_corona_protection

## corona_query_path 10

* query_corona_protection_others
  - utter_query_corona_protection_others

## corona_query_path 11

* query_corona_protection_methods_contact
  - utter_query_corona_protection_methods_contact

## corona_query_path 13

* query_corona_age
  - utter_query_corona_age

## corona_query_path 14

* query_corona_vaccination
  - utter_query_corona_vaccination

## corona_query_path 15

* query_corona_symptoms_develop
  - utter_query_corona_symptoms_develop

## corona_query_path 16

* query_corona_surface_lifetime
  - utter_query_corona_surface_lifetime

## corona_query_path 17

* query_corona_self_cure
  - utter_query_corona_self_cure

## corona_query_path 18

* query_corona_transmission_grocery
  - utter_query_corona_transmission_grocery

## corona_query_path 19

* query_corona_symptoms
  - utter_query_corona_symptoms
* query_corona_symptoms_develop
  - utter_query_corona_symptoms_develop

## corona_query_path 20

* query_corona_symptoms
  - utter_query_corona_symptoms
* query_corona_age
  - utter_query_corona_age
* query_corona_more_info
  - utter_query_corona_symptoms
  - utter_query_corona_age

## corona_query_path 21
* query_corona_protection
  - utter_query_corona_protection
* query_corona_more_info
  - utter_query_corona_protection
