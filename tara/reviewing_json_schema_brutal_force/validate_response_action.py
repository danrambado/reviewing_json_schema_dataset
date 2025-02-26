from tara.lib.action import Action
import jsonschema
import json
class ValidateResponseAction(Action):
    def __init__(self):
        super().__init__()

    def validate_response(self,row):
        if row['JSON_RESPONSE']==None:
            return {"validate": False,
                    "error_code": 3,
                    "error_message":"Empty JSON"}
            
        try:
        # If no exception is raised by validate(), the instance is valid.
            schema=json.loads(row['schema'])
            response=json.loads(row['JSON_RESPONSE'])
            jsonschema.validate(response, schema=schema)

            return {"validate": True,
                    "error_code": 0,
                    "error_message":"Valid JSON"}
        except jsonschema.exceptions.SchemaError as e:
            return {"validate": False,
                    "error_code": 1, #schema
                    "error_message": f"{e.message}"}
        except jsonschema.exceptions.ValidationError as e: 
            error_message=self.validate_response_all_errors(row)
            output={"validate": False,
            "error_code": 2,
            "error_message": error_message}
            return output
        except Exception as e:
            return {"validate": False,
                    "error_code": 3,
                    "error_message":f"Exception {e}"}

    def validate_response_all_errors(self,row):
            schema=json.loads(row['schema'])
            response=json.loads(row['JSON_RESPONSE'])
            errors=jsonschema.Draft202012Validator(schema).iter_errors(response)
            error_message=[]
            for e in errors:
                error_message.append({
    "message": f'{e.message}',
    "validator": f'{e.validator}',
    "validator_type": f'{e.validator_value}',
    "json_path": e.json_path,
    #"json_path": e.relative_path,
    #"context": e.context,
    #"cause": e.cause
    })
            return error_message


if __name__ == '__main__':
    # Check if the correct number of arguments is provided
    row={}
    row['schema']='''{"type": "object", "properties": {"experienceName": {"type": "string"}, "experienceCategory": {"type": "string", "enum": ["Historical Sites", "Museums and Galleries", "Festivals and Events", "Performing Arts", "Culinary Experiences", "Craft and Workshops", "Religious and Spiritual Sites", "Archaeological Sites", "Cultural Heritage Trails", "Indigenous Culture", "Local Community Immersion"]}, "location": {"type": "object", "properties": {"country": {"type": "string"}, "city": {"type": "string"}, "address": {"type": "string"}, "coordinates": {"type": "object", "properties": {"latitude": {"type": "number"}, "longitude": {"type": "number"}}, "required": ["latitude", "longitude"]}, "region": {"type": "string"}, "zipCode": {"type": "string"}}, "required": ["country", "city"]}, "culturalThemes": {"type": "array", "items": {"type": "string", "enum": ["History", "Art", "Music", "Dance", "Literature", "Architecture", "Cuisine", "Traditions", "Religion", "Language", "Social customs", "Local folklore", "Handicrafts"]}, "minItems": 1}, "duration": {"type": "object", "properties": {"value": {"type": "number"}, "unit": {"type": "string", "enum": ["minutes", "hours", "days"]}}, "required": ["value", "unit"]}, "price": {"type": "object", "properties": {"currency": {"type": "string"}, "amount": {"type": "number", "minimum": 0}, "priceType": {"type": "string", "enum": ["per person", "per group", "free", "variable"]}}, "required": ["currency", "amount"]}, "accessibility": {"type": "object", "properties": {"wheelchairAccessible": {"type": "boolean"}, "hearingAssistance": {"type": "boolean"}, "visualAssistance": {"type": "boolean"}, "languageSupport": {"type": "array", "items": {"type": "string"}}}, "required": ["wheelchairAccessible", "hearingAssistance", "visualAssistance"]}, "targetAudience": {"type": "array", "items": {"type": "string", "enum": ["Families", "Solo travelers", "Couples", "Groups", "Seniors", "Students", "Children", "Adults"]}}, "bookingOptions": {"type": "object", "properties": {"website": {"type": "string"}, "phoneNumber": {"type": "string"}, "email": {"type": "string"}, "bookingPlatforms": {"type": "array", "items": {"type": "string"}}}, "additionalProperties": false}, "schedule": {"type": "object", "properties": {"openingHours": {"type": "string"}, "closingHours": {"type": "string"}, "daysOfWeek": {"type": "array", "items": {"type": "string", "enum": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}}, "seasonalAvailability": {"type": "array", "items": {"type": "string", "enum": ["Spring", "Summer", "Autumn", "Winter", "Year-round"]}}, "specialEvents": {"type": "array", "items": {"type": "object", "properties": {"eventName": {"type": "string"}, "startDate": {"type": "string"}, "endDate": {"type": "string"}, "description": {"type": "string"}}, "required": ["eventName", "startDate", "endDate"]}}}, "additionalProperties": false}, "provider": {"type": "object", "properties": {"name": {"type": "string"}, "organization": {"type": "string"}, "contactDetails": {"type": "object", "properties": {"phone": {"type": "string"}, "email": {"type": "string"}}, "additionalProperties": false}}, "required": ["name"]}, "userReviews": {"type": "array", "items": {"type": "object", "properties": {"userId": {"type": "string"}, "rating": {"type": "integer", "minimum": 1, "maximum": 5}, "comment": {"type": "string"}, "reviewDate": {"type": "string"}}, "required": ["userId", "rating", "comment", "reviewDate"]}}, "averageRating": {"type": "number", "minimum": 1, "maximum": 5}, "relatedExperiences": {"type": "array", "items": {"type": "string"}}, "media": {"type": "object", "properties": {"images": {"type": "array", "items": {"type": "string"}}, "videos": {"type": "array", "items": {"type": "string"}}}, "additionalProperties": false}, "amenities": {"type": "array", "items": {"type": "string", "enum": ["Restrooms", "Parking", "Gift shop", "Cafe", "Restaurant", "Guided tours", "Information desk", "Wifi"]}}, "highlights": {"type": "array", "items": {"type": "string"}}, "description": {"type": "string"}, "termsAndConditions": {"type": "string"}, "additionalInfo": {"type": "object", "additionalProperties": {"type": "string"}}}, "required": ["experienceName", "experienceCategory", "location", "culturalThemes", "duration", "price", "accessibility", "targetAudience", "bookingOptions", "schedule", "provider", "userReviews", "averageRating", "description"]}'''

    row['JSON_RESPONSE']='''{
  "type": "object",
  "properties": {
    "experienceName": {
      "type": "string"
    },
    "experienceCategory": {
      "type": "string",
      "enum": [
        "Historical Sites",
        "Museums and Galleries",
        "Festivals and Events",
        "Performing Arts",
        "Culinary Experiences",
        "Craft and Workshops",
        "Religious and Spiritual Sites",
        "Archaeological Sites",
        "Cultural Heritage Trails",
        "Indigenous Culture",
        "Local Community Immersion"
      ]
    },
    "location": {
      "type": "object",
      "properties": {
        "country": {
          "type": "string"
        },
        "city": {
          "type": "string"
        },
        "address": {
          "type": "string"
        },
        "coordinates": {
          "type": "object",
          "properties": {
            "latitude": {
              "type": "number"
            },
            "longitude": {
              "type": "number"
            }
          },
          "required": [
            "latitude",
            "longitude"
          ]
        },
        "region": {
          "type": "string"
        },
        "zipCode": {
          "type": "string"
        }
      },
      "required": [
        "country",
        "city"
      ]
    },
    "culturalThemes": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": [
          "History",
          "Art",
          "Music",
          "Dance",
          "Literature",
          "Architecture",
          "Cuisine",
          "Traditions",
          "Religion",
          "Language",
          "Social customs",
          "Local folklore",
          "Handicrafts"
        ]
      },
      "minItems": 1
    },
    "duration": {
      "type": "object",
      "properties": {
        "value": {
          "type": "number"
        },
        "unit": {
          "type": "string",
          "enum": [
            "minutes",
            "hours",
            "days"
          ]
        }
      },
      "required": [
        "value",
        "unit"
      ]
    },
    "price": {
      "type": "object",
      "properties": {
        "currency": {
          "type": "string"
        },
        "amount": {
          "type": "number",
          "minimum": 0
        },
        "priceType": {
          "type": "string",
          "enum": [
            "per person",
            "per group",
            "free",
            "variable"
          ]
        }
      },
      "required": [
        "currency",
        "amount"
      ]
    },
    "accessibility": {
      "type": "object",
      "properties": {
        "wheelchairAccessible": {
          "type": "boolean"
        },
        "hearingAssistance": {
          "type": "boolean"
        },
        "visualAssistance": {
          "type": "boolean"
        },
        "languageSupport": {
          "type": "array",
          "items": {
            "type": "string"
          }
        }
      },
      "required": [
        "wheelchairAccessible",
        "hearingAssistance",
        "visualAssistance"
      ]
    },
    "targetAudience": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": [
          "Families",
          "Solo travelers",
          "Couples",
          "Groups",
          "Seniors",
          "Students",
          "Children",
          "Adults"
        ]
      }
    },
    "bookingOptions": {
      "type": "object",
      "properties": {
        "website": {
          "type": "string"
        },
        "phoneNumber": {
          "type": "string"
        },
        "email": {
          "type": "string"
        },
        "bookingPlatforms": {
          "type": "array",
          "items": {
            "type": "string"
          }
        }
      },
      "additionalProperties": false
    },
    "schedule": {
      "type": "object",
      "properties": {
        "openingHours": {
          "type": "string"
        },
        "closingHours": {
          "type": "string"
        },
        "daysOfWeek": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": [
              "Monday",
              "Tuesday",
              "Wednesday",
              "Thursday",
              "Friday",
              "Saturday",
              "sunday"
            ]
          }
        },
        "seasonalAvailability": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": [
              "Spring",
              "Summer",
              "Autumn",
              "Winter",
              "Year-round"
            ]
          }
        },
        "specialEvents": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "eventName": {
                "type": "string"
              },
              "startDate": {
                "type": "string"
              },
              "endDate": {
                "type": "string"
              },
              "description": {
                "type": "string"
              }
            },
            "required": [
              "eventName",
              "startDate",
              "endDate"
            ]
          }
        }
      },
      "additionalProperties": false
    },
    "provider": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string"
        },
        "organization": {
          "type": "string"
        },
        "contactDetails": {
          "type": "object",
          "properties": {
            "phone": {
              "type": "string"
            },
            "email": {
              "type": "string"
            }
          },
          "additionalProperties": false
        }
      },
      "required": [
        "name"
      ]
    },
    "userReviews": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "userId": {
            "type": "string"
          },
          "rating": {
            "type": "integer",
            "minimum": 1,
            "maximum": 5
          },
          "comment": {
            "type": "string"
          },
          "reviewDate": {
            "type": "string"
          }
        },
        "required": [
          "userId",
          "rating",
          "comment",
          "reviewDate"
        ]
      }
    },
    "averageRating": {
      "type": "number",
      "minimum": 1,
      "maximum": 5
    },
    "relatedExperiences": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "media": {
      "type": "object",
      "properties": {
        "images": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "videos": {
          "type": "array",
          "items": {
            "type": "string"
          }
        }
      },
      "additionalProperties": false
    },
    "amenities": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": [
          "Restrooms",
          "Parking",
          "Gift shop",
          "Cafe",
          "Restaurant",
          "Guided tours",
          "Information desk",
          "Wifi"
        ]
      }
    },
    "highlights": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "description": {
      "type": "string"
    },
    "termsAndConditions": {
      "type": "string"
    },
    "additionalInfo": {
      "type": "object",
      "additionalProperties": {
        "type": "string"
      }
    }
  },
  "required": [
    "experienceName",
    "experienceCategory",
    "location",
    "culturalThemes",
    "duration",
    "price",
    "accessibility",
    "targetAudience",
    "bookingOptions",
    "schedule",
    "provider",
    "userReviews",
    "averageRating",
    "description"
  ]
}'''

    action = ValidateResponseAction()
    print(action.validate_response_all_errors(row))
    #print(action.validate_response(row))