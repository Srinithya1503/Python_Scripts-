import json
import pandas as pd
import re

# Load the JSON file
with open('assembly_data_report_696.json') as f:
    data = json.load(f)

# Function to format organism name: replace spaces and special characters with underscores
def format_organism_name(name):
    return re.sub(r'[^A-Za-z0-9]', '_', name)

# Initialize lists to store the extracted data
species_list = []
accession_list = []
all_assembly_stats = []

# Iterate over the species data
for species in data:
    try:
        # Extract organismName and format it, default to 'NA' if not present
        organism_name = species.get('organism', {}).get('organismName', 'NA')
        formatted_organism_name = format_organism_name(organism_name)
        
        # Extract accession, default to 'NA' if not present
        accession = species.get('accession', 'NA')
        
        # Extract the assemblyStats section dynamically, default to 'NA' if not present
        assembly_stats = {k: v if v is not None else 'NA' for k, v in species.get('assemblyStats', {}).items()}
        
        # Append the extracted fields to their respective lists
        species_list.append(formatted_organism_name)
        accession_list.append(accession)
        
        # Append all assemblyStats to a separate list
        all_assembly_stats.append(assembly_stats)
    
    except Exception as e:
        print(f"Error processing species: {species}. Error: {e}")

# Create a DataFrame for the fixed columns (without unnecessary fields)
df_fixed = pd.DataFrame({
    'OrganismName': species_list,
    'Accession': accession_list,
})

# Create a DataFrame for the dynamic assemblyStats columns, filling missing values with 'NA'
df_dynamic = pd.DataFrame(all_assembly_stats).fillna('NA')

# Concatenate the fixed and dynamic columns
df_combined = pd.concat([df_fixed, df_dynamic], axis=1)

# Save the DataFrame to an Excel file
df_combined.to_excel('assembly_stats_696.xlsx', index=False)

print("Data extraction complete and saved to species_data_with_all_info.xlsx")

