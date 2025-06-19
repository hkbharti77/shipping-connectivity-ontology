# import tomllib
# import json
# from pathlib import Path

# def load_config():
#     with open("config/config.toml", "rb") as f:
#         return tomllib.load(f)

# def define_ontology_links():
#     config = load_config()

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

#     return links

# def display_links(links):
#     print("\n📘 Ontology Link Definitions:")
#     for link in links:
#         print(f"\n🔗 {link['from']} —[{link['relationship']}]→ {link['to']}")
#         print(f"   📄 {link['description']}")

# def save_links_to_file(links, path="data/ontology_links.json"):
#     Path(path).parent.mkdir(parents=True, exist_ok=True)
#     with open(path, "w", encoding="utf-8") as f:
#         json.dump(links, f, indent=2)
#     print(f"\n✅ Link definitions saved to: {path}")

# if __name__ == "__main__":
#     link_defs = define_ontology_links()
#     display_links(link_defs)
#     save_links_to_file(link_defs)
