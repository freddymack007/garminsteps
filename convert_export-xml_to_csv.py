#!/usr/bin/env python3

import xml.etree.ElementTree as ET

print("Start parse.")

export = ET.parse('export.xml')
export_root = export.getroot()

## Records

# Find all Record types
print("Finding Record types...")
record_types = []
for record in export_root.findall('Record'):

  if record.get('type') not in record_types:
    record_types.append(record.get('type'))

for record_type in record_types:

  # For each Record type, find all attributes
  print("Finding Attributes for " + record_type)
  attributes = []
  for record in export_root.findall('Record'):
    if(record.get('type') == record_type):
      for attribute_name in record.attrib:
        if attribute_name not in attributes:
          attributes.append(attribute_name)

  # Write a file for each Record type
  filename = record_type + ".csv"
  print("Writing " + filename + "...\n")
  with open(filename, 'w') as output_file:
    # Header
    output_file.write(record_type + "\n")
    output_file.write(','.join(attributes) + "\n")

    # Records
    for r in export_root.findall('Record'):
      if(r.get('type') == record_type):
        for att in attributes:
          value = r.get(att)
          if value is None:
            value = "NULL" # Catch null values

          if(att == "device" and "," in value):
            value = value.replace(',','') # Replace commas in "&lt;&lt;HKDevice: 0x123456789&gt;, name:iPhone, manufacturer:Apple, model:iPhone, hardware:iPhone10,4, software:12.1.1&gt;"

          output_file.write(value + ",")
        output_file.write("\n")

## Workouts

print("Finding Workouts...")
# Find all attributes for workouts
wo_attributes = []
for workout in export_root.findall('Workout'):
  for attribute_name in workout.attrib:
    if attribute_name not in wo_attributes:
      wo_attributes.append(attribute_name)

# Print all workouts
filename = "Workouts.csv"
print("Writing " + filename + "...")
with open(filename, 'w') as output_file:
  # Header
  output_file.write("Workouts\n")
  output_file.write(','.join(wo_attributes) + "\n")

  # Records
  for workout in export_root.findall('Workout'):
    for att in wo_attributes:
      value = workout.get(att)
      if value is None:
        value = "NULL" # Catch null values

      output_file.write(value + ",")
    output_file.write("\n")

print("Done.")
