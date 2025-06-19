# import tomllib

# def load_config():
#     with open("config/config.toml", "rb") as f:
#         return tomllib.load(f)

# def define_ontology_links():
#     config = load_config()

#     # Optional: Validate links against defined object types from config
#     valid_objects = config.get("ontology", {}).get("object_types", [])

#     links = [
#         {
#             "from": "Economy",
#             "relationship": "MEASURED_BY",
#             "to": "LSCI_Measurement",
#             "description": "An economy is measured by one or more LSCI records."
#         },
#         {
#             "from": "LSCI_Measurement",
#             "relationship": "RECORDED_IN",
#             "to": "Time_Period",
#             "description": "Each LSCI measurement is recorded in a specific time period."
#         },
#         {
#             "from": "Economy",
#             "relationship": "BELONGS_TO",
#             "to": "Geographic_Region",
#             "description": "Each economy belongs to one or more geographic regions."
#         },
#         {
#             "from": "Economy",
#             "relationship": "CONNECTED_TO",
#             "to": "Economy",
#             "description": "Represents similarity or trade linkages between economies (derived)."
#         }
#     ]

#     # Optional: validate links
#     if valid_objects:
#         for link in links:
#             if link["from"] not in valid_objects or link["to"] not in valid_objects:
#                 print(f"⚠️ Warning: Link uses undefined object type: {link}")

#     return links

# if __name__ == "__main__":
#     link_defs = define_ontology_links()
#     print("\n🔗 Ontology Link Definitions")
#     print("-" * 50)
#     for link in link_defs:
#         print(f"{link['from']} —[{link['relationship']}]→ {link['to']}")
#         print(f"  ↪ {link['description']}\n")
