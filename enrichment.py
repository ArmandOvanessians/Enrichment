import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import PowerNorm
import seaborn as sns
import data_prep as dp

# Function to conduct enrichment
def panther_enrichment(gene_list, organism='9606', annotDataSet='GO:0008150', enrichmentTestType='FISHER',
                       correction='FDR'):
    """
    Use PANTHER Tools - Enrichment (Overrepresentation) test to perform gene enrichment analysis.

    Parameters:
        gene_list: List of genes for analysis.
        organism: Organism taxid. Default is 9606 (Homo sapiens).
        annotDataSet: Annotation data set. Default is 'GO:0008150'.
        enrichmentTestType: Enrichment test type. Default is 'FISHER'.
        correction: Correction method. Default is 'FDR'.

    Returns:
        Resulting data or error message.
    """
    base_url = "https://pantherdb.org/services/oai/pantherdb/enrich/overrep"
    params = {
        "geneInputList": ",".join(gene_list),
        "organism": organism,
        "annotDataSet": annotDataSet,
        "enrichmentTestType": enrichmentTestType,
        "correction": correction
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        # Return resulting data
        # You can modify this to better suit how you'd like to handle the response
        return response.json()
    else:
        return f"Error {response.status_code}: {response.text}"

# targetome_file = dataset of top ranked proteins
# affinity_file = dataset of screenings
# n = is the number of top n proteins that the small molecule has the highest affinity towards
# x = the amount of highlighly enriched pathways that you want to display
def conduct_enrichment_top_n(df, n, x=20):
    #df = dp.prepare_data(targetome_file, affinity_file)
    df_top_n = df.iloc[:n]
    # turn gene names from df format to a list
    entry_list = df_top_n['Entry'].tolist()
    # Enter that list into the panther enrichment function
    enrich_d = panther_enrichment(entry_list)
    # enrichment formatted in a df
    df_e = pd.DataFrame(enrich_d['results']['result'])
    # postprocessing of enrichment
    df_e = pd.concat([df_e.drop(['term'], axis=1), df_e['term'].apply(pd.Series)], axis=1)
    df_e['lab'] = df_e['id'].astype(str) + "_" + df_e['label'].astype(str)
    # get a uniform column
    df_e.columns = ['matches', 'Fold Enrichment', 'FDR', 'Expected', 'nmumber in reference', 'p-value', 'plus_minus', 'ID',  'label', 'lab']
    # get only signficant pathways
    df_e = df_e[df_e['p-value'] < 0.05]
    df_e = df_e[df_e['FDR'] < 0.05]
    # sort the pathways by enrichment score
    df_e = df_e.sort_values(by="Fold Enrichment", ascending=False)
    # get the top x pathways (set to 20 as a default)
    df_e = df_e.iloc[:x]
    return df_e

def plot_enrichment(df, n, drug):
    norm = PowerNorm(0.5, df['FDR'].min(), df['FDR'].max())
    sm = plt.cm.ScalarMappable(cmap="viridis_r", norm=norm)
    sm.set_array([])
    # print(df)
    plt.figure(figsize=(40, 40))
    # print(sm.to_rgba(df['FDR']))
    # Use the adjusted color map for the palette argument in barplot
    sns.barplot(x='Fold Enrichment', y='lab', data=df, palette=sm.to_rgba(df['FDR']))

    # Decorate the plot
    plt.title(f'Fold Enrichment of GO Terms ({drug}), TOP {n}', fontsize=55)
    plt.xlabel('Fold Enrichment', fontsize=40)
    plt.ylabel(f'GO Biological Process Enrichment Analysis', fontsize=40)
    plt.xticks(fontsize=40)
    plt.yticks(fontsize=40)

    # Add colorbar with label
    cbar = plt.colorbar(sm, orientation="vertical", pad=0.02, ax=plt.gca())
    cbar.set_label('FDR', fontsize=50)

    sns.despine(left=True, bottom=True)  # Remove the top and right borders for a cleaner look
    plt.tight_layout()
    plt.savefig(f"top{n}_{drug}.png")
    plt.show()
    return 0

# # Parameters inputted by the users
# targetome_file = "Data.xlsx"
# affinity_file = "BAP_affinities.txt"
# n = [75,100,125]
# drug = "BaP"
# # call of function to do the enrichment
# df = dp.prepare_data(targetome_file, affinity_file)
# if isinstance(n, int):
#     df_enriched = conduct_enrichment_top_n(df, n)
#     plot_enrichment(df_enriched, n, drug)
# elif type(n) is list:
#     for i in n:
#         df_enriched = conduct_enrichment_top_n(df, i)
#         plot_enrichment(df_enriched, i, drug)
