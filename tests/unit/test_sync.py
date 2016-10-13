import json
import unittest
from unittest.mock import MagicMock
from janrain_mailchimp_connect.actions.sync import *

class TestMyMethods(unittest.TestCase) :
    def test_json_converter (self):
        #setup
        config = {'MC_FIELDS_TO_EXPORT':['familyName', 'givenName']}
        raw_data = """{
                  "result_count": 5,
                  "results": [
                    {
                      "birthday": null,
                      "familyName": "Baker",
                      "zipCode": null,
                      "aDateTime": null,
                      "profiles": [],
                      "sites": [],
                      "id": 1,
                      "registrationSiteName": null,
                      "middleName": null,
                      "emailVerified": "2013-07-16 18:44:04 +0000",
                      "primaryAddress": {
                        "company": null,
                        "address2": null,
                        "stateAbbreviation": null,
                        "zipPlus4": null,
                        "city": null,
                        "address1": null,
                        "phone": null,
                        "zip": null,
                        "mobile": null,
                        "country": null
                      },
                      "gender": null,
                      "lastUpdated": "2013-07-24 21:16:54.208347 +0000",
                      "aInteger": null,
                      "password": {
                        "value": "$2a$04$AVkEHHcoD4KBofztAa4ijebzKOTocNUs6PusKIEkFhDVOUH3cFOSq",
                        "type": "password-bcrypt"
                      },
                      "photos": [],
                      "email": "paul@paul.com",
                      "givenName": "Paul",
                      "branch": null,
                      "currentLocation": null,
                      "barcode": null,
                      "communicationOptIn": null,
                      "deactivateAccount": null,
                      "lastLogin": "2013-07-24 20:36:34 +0000",
                      "businessId": null,
                      "number": null,
                      "created": "2013-06-26 19:22:52.823252 +0000",
                      "location": null,
                      "displayName": null,
                      "uuid": "a08a0bca-3bd5-4094-b7c0-be682404d689",
                      "subscription_lists": [],
                      "aboutMe": null,
                      "optinTest": {
                        "status": null,
                        "note": null,
                        "date": null
                      },
                      "display": null
                    },
                    {
                      "birthday": null,
                      "familyName": "Baker2",
                      "zipCode": null,
                      "aDateTime": null,
                      "profiles": [],
                      "sites": [],
                      "id": 2,
                      "registrationSiteName": null,
                      "middleName": null,
                      "emailVerified": null,
                      "primaryAddress": {
                        "company": null,
                        "address2": null,
                        "stateAbbreviation": null,
                        "zipPlus4": null,
                        "city": null,
                        "address1": null,
                        "phone": null,
                        "zip": null,
                        "mobile": null,
                        "country": null
                      },
                      "gender": null,
                      "lastUpdated": "2013-07-01 19:34:22.140956 +0000",
                      "aInteger": null,
                      "password": null,
                      "photos": [],
                      "email": "paul2@paul2.com",
                      "givenName": "Paul2",
                      "branch": null,
                      "currentLocation": null,
                      "barcode": null,
                      "communicationOptIn": null,
                      "deactivateAccount": null,
                      "lastLogin": null,
                      "businessId": null,
                      "number": null,
                      "created": "2013-06-26 19:43:39.347354 +0000",
                      "location": null,
                      "displayName": null,
                      "uuid": "799a0a62-2ff5-4160-837c-2de2b707d0a4",
                      "subscription_lists": [],
                      "aboutMe": null,
                      "optinTest": {
                        "status": null,
                        "note": null,
                        "date": null
                      },
                      "display": null
                    },
                    {
                      "birthday": null,
                      "familyName": "Baker",
                      "zipCode": null,
                      "aDateTime": null,
                      "profiles": [
                        {
                          "friends": [],
                          "identifier": "https://www.google.com/profiles/104378459748016700309",
                          "domain": "google.com",
                          "id": 1044,
                          "remote_key": null,
                          "accessCredentials": null,
                          "following": [],
                          "provider": null,
                          "profile": {
                            "relationships": [],
                            "utcOffset": null,
                            "ims": [],
                            "status": null,
                            "lookingFor": [],
                            "fashion": null,
                            "birthday": null,
                            "quotes": [],
                            "happiestWhen": null,
                            "movies": [],
                            "activities": [],
                            "children": [],
                            "preferredUsername": "paulbaker",
                            "cars": [],
                            "scaredOf": null,
                            "urls": [
                              {
                                "primary": null,
                                "id": 2349,
                                "value": "https://www.google.com/profiles/104378459748016700309",
                                "type": "profile"
                              }
                            ],
                            "note": null,
                            "anniversary": null,
                            "relationshipStatus": null,
                            "organizations": [],
                            "humor": null,
                            "smoker": null,
                            "livingArrangement": null,
                            "food": [],
                            "accounts": [],
                            "gender": null,
                            "emails": [
                              {
                                "primary": true,
                                "id": 2347,
                                "value": "paulbaker@paulbaker.com",
                                "type": "other"
                              }
                            ],
                            "politicalViews": null,
                            "photos": [],
                            "name": {
                              "familyName": "Baker",
                              "formatted": "Paul Baker",
                              "middleName": null,
                              "givenName": "Paul",
                              "honorificPrefix": null,
                              "honorificSuffix": null
                            },
                            "turnOns": [],
                            "phoneNumbers": [],
                            "currentLocation": {
                              "locality": null,
                              "formatted": null,
                              "longitude": null,
                              "latitude": null,
                              "postalCode": null,
                              "streetAddress": null,
                              "extendedAddress": null,
                              "type": null,
                              "country": null,
                              "region": null,
                              "poBox": null
                            },
                            "turnOffs": [],
                            "languages": [],
                            "ethnicity": null,
                            "tags": [],
                            "romance": null,
                            "sports": [],
                            "interestedInMeeting": [],
                            "music": [],
                            "profileSong": null,
                            "heroes": [],
                            "profileUrl": "https://www.google.com/profiles/104378459748016700309",
                            "addresses": [],
                            "nickname": null,
                            "published": null,
                            "sexualOrientation": null,
                            "bodyType": {
                              "height": null,
                              "build": null,
                              "color": null,
                              "hairColor": null,
                              "eyeColor": null
                            },
                            "drinker": null,
                            "religion": null,
                            "displayName": "Paul Baker",
                            "languagesSpoken": [
                              {
                                "languageSpoken": "en",
                                "id": 2348
                              }
                            ],
                            "interests": [],
                            "aboutMe": null,
                            "updated": null,
                            "profileVideo": null,
                            "tvShows": [],
                            "books": [],
                            "jobInterests": [],
                            "pets": []
                          },
                          "followers": []
                        },
                        {
                          "friends": [],
                          "identifier": "http://www.facebook.com/profile.php?id=100006225871369",
                          "domain": "facebook.com",
                          "id": 1409,
                          "remote_key": null,
                          "accessCredentials": {
                            "scopes": "user_photos,user_birthday,publish_stream,user_hometown,email",
                            "accessToken": "CAAHm4hibMowBAA9s4mSMNTqsvaPNjuHYZCkDeNg9w7HDE4VRB6MOmd7ZAXK27ZAZCVKHs2BSpJeaRVJGKGrpD2glZBXtfEmPI9ZC79qFcmZCcZC3FkklVhMCPkPuzb0ZC1IJLTvbWfndIzCYZCDcIQxHSIKhpPkiFN67QZD",
                            "type": "Facebook",
                            "uid": "100006225871369",
                            "expires": 1382282833
                          },
                          "following": [],
                          "provider": null,
                          "profile": {
                            "relationships": [],
                            "utcOffset": "-07:00",
                            "ims": [],
                            "status": null,
                            "lookingFor": [],
                            "fashion": null,
                            "birthday": "1970-09-01",
                            "quotes": [],
                            "happiestWhen": null,
                            "movies": [],
                            "activities": [],
                            "children": [],
                            "preferredUsername": "PaulBaker",
                            "cars": [],
                            "scaredOf": null,
                            "urls": [
                              {
                                "primary": null,
                                "id": 1544,
                                "value": "https://www.facebook.com/profile.php?id=100006225871369",
                                "type": "profile"
                              }
                            ],
                            "note": null,
                            "anniversary": null,
                            "relationshipStatus": null,
                            "organizations": [
                              {
                                "primary": null,
                                "startDate": null,
                                "department": null,
                                "title": null,
                                "id": 1539,
                                "name": "Janrain",
                                "description": null,
                                "endDate": null,
                                "type": "job",
                                "location": {
                                  "locality": null,
                                  "formatted": null,
                                  "longitude": null,
                                  "latitude": null,
                                  "postalCode": null,
                                  "streetAddress": null,
                                  "extendedAddress": null,
                                  "type": null,
                                  "country": null,
                                  "region": null,
                                  "poBox": null
                                }
                              }
                            ],
                            "humor": null,
                            "smoker": null,
                            "livingArrangement": null,
                            "food": [],
                            "accounts": [],
                            "gender": "male",
                            "emails": [
                              {
                                "primary": true,
                                "id": 1538,
                                "value": "paulbaker@paulbaker2.com",
                                "type": "other"
                              }
                            ],
                            "politicalViews": null,
                            "photos": [
                              {
                                "primary": null,
                                "id": 1540,
                                "value": "https://graph.facebook.com/100006225871369/picture?type=small",
                                "type": "other"
                              },
                              {
                                "primary": true,
                                "id": 1541,
                                "value": "https://graph.facebook.com/100006225871369/picture?type=large",
                                "type": "other"
                              },
                              {
                                "primary": null,
                                "id": 1542,
                                "value": "https://graph.facebook.com/100006225871369/picture?type=square",
                                "type": "other"
                              },
                              {
                                "primary": null,
                                "id": 1543,
                                "value": "https://graph.facebook.com/100006225871369/picture?type=normal",
                                "type": "other"
                              }
                            ],
                            "name": {
                              "familyName": "Baker",
                              "formatted": "Paul Baker",
                              "middleName": null,
                              "givenName": "Paul",
                              "honorificPrefix": null,
                              "honorificSuffix": null
                            },
                            "turnOns": [],
                            "phoneNumbers": [],
                            "currentLocation": {
                              "locality": null,
                              "formatted": "Portland, Oregon",
                              "longitude": null,
                              "latitude": null,
                              "postalCode": null,
                              "streetAddress": null,
                              "extendedAddress": null,
                              "type": "currentLocation",
                              "country": null,
                              "region": null,
                              "poBox": null
                            },
                            "turnOffs": [],
                            "languages": [],
                            "ethnicity": null,
                            "tags": [],
                            "romance": null,
                            "sports": [],
                            "interestedInMeeting": [],
                            "music": [],
                            "profileSong": null,
                            "heroes": [],
                            "profileUrl": "https://www.facebook.com/profile.php?id=100006225871369",
                            "addresses": [
                              {
                                "primary": null,
                                "locality": null,
                                "formatted": "Portland, Oregon",
                                "longitude": null,
                                "latitude": null,
                                "postalCode": null,
                                "id": 1537,
                                "streetAddress": null,
                                "extendedAddress": null,
                                "type": "currentLocation",
                                "country": null,
                                "region": null,
                                "poBox": null
                              }
                            ],
                            "nickname": null,
                            "published": null,
                            "sexualOrientation": null,
                            "bodyType": {
                              "height": null,
                              "build": null,
                              "color": null,
                              "hairColor": null,
                              "eyeColor": null
                            },
                            "drinker": null,
                            "religion": null,
                            "displayName": "Paul Baker",
                            "languagesSpoken": [],
                            "interests": [],
                            "aboutMe": null,
                            "updated": "2013-06-25 23:38:54 +0000",
                            "profileVideo": null,
                            "tvShows": [],
                            "books": [],
                            "jobInterests": [],
                            "pets": []
                          },
                          "followers": []
                        }
                      ],
                      "sites": [],
                      "id": 134,
                      "registrationSiteName": null,
                      "middleName": null,
                      "emailVerified": "2013-07-16 18:44:04 +0000",
                      "primaryAddress": {
                        "company": null,
                        "address2": null,
                        "stateAbbreviation": null,
                        "zipPlus4": null,
                        "city": null,
                        "address1": null,
                        "phone": null,
                        "zip": null,
                        "mobile": null,
                        "country": null
                      },
                      "gender": null,
                      "lastUpdated": "2013-10-28 21:07:03.714206 +0000",
                      "aInteger": null,
                      "password": {
                        "value": "$2a$04$ymMH9UZcnqtx0Gz5ft3UZuvS7bTgU6xDvYmYB8zxMBIfCy9DK1cGO",
                        "type": "password-bcrypt"
                      },
                      "photos": [],
                      "email": "paulbaker@paulbaker3.com",
                      "givenName": "Paul",
                      "branch": null,
                      "currentLocation": null,
                      "barcode": null,
                      "communicationOptIn": null,
                      "deactivateAccount": null,
                      "lastLogin": "2013-10-28 21:07:03 +0000",
                      "businessId": null,
                      "number": null,
                      "created": "2013-06-27 16:52:12.838947 +0000",
                      "location": null,
                      "displayName": "paulbaker1234567",
                      "uuid": "658a3a9c-b0d5-4dfb-90e7-14828abba24b",
                      "subscription_lists": [],
                      "aboutMe": null,
                      "optinTest": {
                        "status": null,
                        "note": null,
                        "date": null
                      },
                      "display": null
                    },
                    {
                      "birthday": null,
                      "familyName": "Baker3",
                      "zipCode": null,
                      "aDateTime": null,
                      "profiles": [],
                      "sites": [],
                      "id": 392,
                      "registrationSiteName": null,
                      "middleName": null,
                      "emailVerified": null,
                      "primaryAddress": {
                        "company": null,
                        "address2": null,
                        "stateAbbreviation": null,
                        "zipPlus4": null,
                        "city": null,
                        "address1": null,
                        "phone": null,
                        "zip": null,
                        "mobile": null,
                        "country": null
                      },
                      "gender": null,
                      "lastUpdated": "2013-07-01 15:46:11.247721 +0000",
                      "aInteger": null,
                      "password": null,
                      "photos": [],
                      "email": "paul3@paul3.com",
                      "givenName": "Paul3",
                      "branch": null,
                      "currentLocation": null,
                      "barcode": null,
                      "communicationOptIn": null,
                      "deactivateAccount": null,
                      "lastLogin": null,
                      "businessId": null,
                      "number": null,
                      "created": "2013-07-01 15:46:11.247721 +0000",
                      "location": null,
                      "displayName": null,
                      "uuid": "75334cb6-f670-4221-be68-d927da985a25",
                      "subscription_lists": [],
                      "aboutMe": null,
                      "optinTest": {
                        "status": null,
                        "note": null,
                        "date": null
                      },
                      "display": null
                    },
                    {
                      "birthday": null,
                      "familyName": "Baker4",
                      "zipCode": null,
                      "aDateTime": null,
                      "profiles": [],
                      "sites": [],
                      "id": 401,
                      "registrationSiteName": null,
                      "middleName": null,
                      "emailVerified": null,
                      "primaryAddress": {
                        "company": null,
                        "address2": null,
                        "stateAbbreviation": null,
                        "zipPlus4": null,
                        "city": null,
                        "address1": null,
                        "phone": null,
                        "zip": null,
                        "mobile": null,
                        "country": null
                      },
                      "gender": null,
                      "lastUpdated": "2013-07-01 19:57:44.935655 +0000",
                      "aInteger": null,
                      "password": null,
                      "photos": [],
                      "email": "Paul4@paul4.com",
                      "givenName": "Paul4",
                      "branch": null,
                      "currentLocation": null,
                      "barcode": null,
                      "communicationOptIn": null,
                      "deactivateAccount": null,
                      "lastLogin": null,
                      "businessId": null,
                      "number": null,
                      "created": "2013-07-01 19:57:06.609112 +0000",
                      "location": null,
                      "displayName": null,
                      "uuid": "d6c873ac-580c-404b-af62-893ee7e18b38",
                      "subscription_lists": [],
                      "aboutMe": null,
                      "optinTest": {
                        "status": null,
                        "note": null,
                        "date": null
                      },
                      "display": null
                    }
                  ],
                  "stat": "ok"
                }"""
        #call
        result = json_converter(raw_data, config)
        #test
        self.assertEqual(result.__len__(), 5, "incorrect number of results")

    def test_record_filter(self):
        #setup
        sync_info = {'last_run':'a_time'}
        logger = MagicMock()
        logger.info = MagicMock()
        #call
        result = record_filter(sync_info, logger)
        #test
        self.assertEqual(result, "lastUpdated > \'a_time\'")

    def test_load_records(self):
        #setuo
        logger = MagicMock()
        logger.info = MagicMock()
        sync_info = {'last_run': 'a_time',
                     'janrain_attributes':[],
                     'capture_schema':"put something here",
                     'queue':"put something here",
                     }
        config = {'MC_FIELDS_TO_EXPORT':['familyName', 'givenName'],
                  'JANRAIN_BATCH_SIZE':'100',
                  }
        #call
        result = load_records(sync_info, config, logger)
        #test