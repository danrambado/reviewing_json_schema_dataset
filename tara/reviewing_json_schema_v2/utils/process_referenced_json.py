import json

# Sample JSON as a string (you can replace it with your JSON source)
json_string = '''
{
  "riskAssessment": {
    "type": "object",
    "referenced": true,
    "text_reference": "comprehensive risk assessment report",
    "marketRisk": {
      "type": "object",
      "referenced": true,
      "text_reference": "market risk",
      "equityRisk": {
        "type": "object",
        "referenced": true,
        "text_reference": "equity portfolio has a beta of 1.2 relative to the global market index and an annualized volatility of 15%",
        "beta": {
          "type": "number",
          "referenced": true,
          "text_reference": "beta of 1.2"
        },
        "volatility": {
          "type": "number",
          "referenced": true,
          "text_reference": "annualized volatility of 15%"
        },
        "valueAtRisk": {
          "type": "object",
          "referenced": true,
          "text_reference": "Value at Risk (VaR) using Historical Simulation at a 99% confidence level over a 10-day holding period. VaR is calculated at $5,000,000",
          "confidenceLevel": {
            "type": "number",
            "referenced": true,
            "text_reference": "99% confidence level"
          },
          "holdingPeriod": {
            "type": "integer",
            "referenced": true,
            "text_reference": "10-day holding period"
          },
          "varAmount": {
            "type": "number",
            "referenced": true,
            "text_reference": "$5,000,000"
          },
          "methodology": {
            "type": "string",
            "referenced": true,
            "text_reference": "Historical Simulation"
          }
        }
      },
      "interestRateRisk": {
        "type": "object",
        "referenced": true,
        "text_reference": "interest rate risk",
        "duration": {
          "type": "number",
          "referenced": true,
          "text_reference": "Macaulay Duration of 5.5 years"
        }
      }
    }
  }
}
'''

# Load the JSON into a Python dictionary
data = json.loads(json_string)

# Global counters and list for false references
true_count = 0
false_count = 0
false_properties = []

def process_json(obj, parent_key=None):
    global true_count, false_count, false_properties
    if isinstance(obj, dict):
        # Check if current dict has both "referenced" and "text_reference"
        if "referenced" in obj and "text_reference" in obj:
            if obj["referenced"] is True:
                true_count += 1
            else:
                false_count += 1
                # If a parent key is provided, use it as property name; otherwise, use 'unknown'
                prop_name = parent_key if parent_key is not None else 'unknown'
                false_properties.append(prop_name)
        # Recursively process each key-value pair
        for key, value in obj.items():
            process_json(value, parent_key=key)
    elif isinstance(obj, list):
        # If the current object is a list, iterate over its items
        for item in obj:
            process_json(item, parent_key=parent_key)

# Process the loaded JSON
process_json(data)

# Compute total references and percentage of True references
total_references = true_count + false_count
percentage_true = (true_count / total_references * 100) if total_references else 0

print(f"Total references: {total_references}")
print(f"True references: {true_count}")
print(f"False references: {false_count}")
print(f"Percentage of True references: {percentage_true:.2f}%")
print("Properties with False references:", false_properties)