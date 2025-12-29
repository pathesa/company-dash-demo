import os
import requests
import pandas as pd
import numpy as np
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("ZENDESK_TOKEN")
HEADERS = {"Authorization": f"Bearer {API_TOKEN}", "Accept": "application/json"}

def fetch_data(dataset):
    all_data = []
    url = f"https://api.getbase.com/v2/{dataset}?page=1&per_page=100"
    while url:
        print(f"Fetching {dataset} from: {url}")
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            break
        data = response.json()
        all_data.extend(data.get("items", []))
        url = data.get("meta", {}).get("links", {}).get("next_page")
    return all_data

def clean_deals(deals, contacts, stages):

    # Helper to flatten custom fields
    def extract_custom_fields(row):
        if isinstance(row, list):
            return {item['name']: item['value'] for item in row if 'name' in item}
        return row if isinstance(row, dict) else {}

    # Flatten Deals
    custom_df = pd.DataFrame(deals['custom_fields'].apply(extract_custom_fields).tolist())
    custom_df.columns = [f"custom {col}" if not col.startswith("custom") else col for col in custom_df.columns]
    deals = pd.concat([deals.reset_index(drop=True), custom_df.reset_index(drop=True)], axis=1)

    # Flatten Contacts
    contact_customs = pd.DataFrame(contacts['custom_fields'].apply(extract_custom_fields).tolist())
    contact_customs.columns = [f"custom (contact) {col}" for col in contact_customs.columns]
    contacts = pd.concat([contacts.reset_index(drop=True), contact_customs.reset_index(drop=True)], axis=1)

    # Map stage names
    stage_map = dict(zip(stages['id'], stages['name']))
    deals['stage_name'] = deals['stage_id'].map(stage_map)

    deals['decimal_value'] = pd.to_numeric(deals['value'], errors='coerce').fillna(0)
    
    date_cols = ['custom Event Start', 'last_activity_at', 'last_stage_change_at', 'updated_at']
    for col in date_cols:
        if col in deals.columns:
            deals[col] = pd.to_datetime(deals[col], errors='coerce')

    # Filter Dates & Stages
    deals['added_at'] = pd.to_datetime(deals['added_at'], errors='coerce').dt.tz_convert(None)
    deals = deals[deals['added_at'] >= '2022-01-01'].copy()
    deals = deals[deals['stage_name'].isin(['Event Complete', 'Cancelled', 'Unqualified'])].copy()
    deals['converted'] = deals['stage_name'] == 'Event Complete'

    # Merge with Contacts 
    contacts_subset = contacts[['id', 'custom (contact) Client Segment']].copy()
    deals = deals.merge(contacts_subset, left_on='contact_id', right_on='id', how="left")

    deals['custom Client Segment'] = np.where(
        pd.isna(deals['custom Client Segment']), 
        deals['custom (contact) Client Segment'], 
        deals['custom Client Segment']
    )

    segment_mapping = {
        "Event Design Planning + Production": "Event Designer Planning and Production",
        "Photo + Design": "Photo",
        "In-House Company": "In-house Company",
        "Catering Company": "Catering Company/Florist",
        "Conference + Trade Show Producter": "Conference or Trade Show",
        "Trade Show Vendor": "Conference or Trade Show"
    }
    deals['custom Client Segment'] = deals['custom Client Segment'].replace(segment_mapping)
    
    deals = deals.rename(columns={
        'custom Event Start': 'event_start_date',
        'custom Product total': 'product_total',
        'custom Client Segment': 'client_segment',
        'custom Client Type': 'client_type'
    })

    # Lead Time & Deal Bands
    deals = deals[~deals['client_segment'].isin(['Stager', 'Consumer (Nomad)', 'Exhibitor/Showroom', 'Real Estate Broker'])]
    deals['lead_time'] = (deals['event_start_date'] - deals['added_at']).dt.days
    deals['deal_band'] = pd.cut(
        deals['decimal_value'], 
        bins=[0, 5000, 10000, 20000, 30000, float('inf')],
        labels=['$0-5K', '$5-10K', '$10-20K', '$20-30K', '$30K+'],
        include_lowest=True
    )
    
    # Drop sensitive columns
    cols_to_drop = [
        'name', 
        'custom_fields', 
        'custom RW Invoice number', 
        'custom Tax ID (if tax exempt)',
        'contact_id', 'id_x', 'id_y', 'dropbox_email'
    ]
    deals = deals.drop(columns=cols_to_drop, errors='ignore')

    return deals

def create_grouped_segments_df(deals):

    """    
    Creates a grouped DataFrame summarizing key metrics by client segment.   

    Parameters:
    - deals: DataFrame containing cleaned deals data.
    """ 

    # Base Stats 
    grouped = deals.groupby('client_segment')['converted'].agg(['sum', 'count']).reset_index()
    grouped.rename(columns={'count': 'total_deals', 'sum': 'converted_deals'}, inplace=True)
    
    # Conversion Rate
    grouped['conversion_rate'] = (grouped['converted_deals'] / grouped['total_deals']).round(2)
    
    # Overall Percentages
    total_deals_overall = grouped['total_deals'].sum()
    grouped['pct_total_deals'] = ((grouped['total_deals'] / total_deals_overall) * 100).round(2)

    # Revenue Calculations 
    converted_only = deals[deals['converted'] == True]
    total_rev_overall = converted_only['decimal_value'].sum() 
    
    rev_stats = converted_only.groupby('client_segment')['decimal_value'].agg(['sum', 'mean']).reset_index()
    rev_stats.rename(columns={'sum': 'segment_revenue', 'mean': 'avg_deal_size'}, inplace=True)
    
    # Lead Time Calculation 
    lead_stats = deals.groupby('client_segment')['lead_time'].mean().reset_index()
    lead_stats.rename(columns={'lead_time': 'avg_lead_time'}, inplace=True)

    final_df = grouped.merge(rev_stats, on='client_segment', how='left')
    final_df = final_df.merge(lead_stats, on='client_segment', how='left')

    final_df['percent_total_revenue'] = ((final_df['segment_revenue'] / total_rev_overall) * 100).round(2)
    final_df['segment_revenue'] = final_df['segment_revenue'].fillna(0).round()
    final_df['avg_deal_size'] = final_df['avg_deal_size'].fillna(0).round()
    final_df['avg_lead_time'] = final_df['avg_lead_time'].round(1)

    return final_df

def create_conv_rate_revenue_band(deals):
    """                                                             
    Creates a detailed DataFrame summarizing conversion rates and revenue by client segment and deal band.  

    Parameters: 

    - deals: DataFrame containing cleaned deals data.
    """ 

    # Calculate overall total revenue from converted deals
    total_rev_overall = deals[deals['converted'] == True]['decimal_value'].sum()

    # Grouping for Base Stats
    conv_rate_band_segments = deals.groupby(['client_segment', 'deal_band'], observed=False)['converted'].agg(['sum', 'count']).reset_index()
    conv_rate_band_segments.rename(columns={'sum': 'converted_deals', 'count': 'total_deals'}, inplace=True)
    
    # Calculate conversion rate
    conv_rate_band_segments['conversion_rate'] = (conv_rate_band_segments['converted_deals'] / conv_rate_band_segments['total_deals'] * 100).fillna(0)

    # Revenue per Segment and Band
    converted_only = deals[deals['converted'] == True].copy()
    pctrevenue_band = converted_only.groupby(['client_segment', 'deal_band'], observed=False).agg({
        'decimal_value': 'sum'
    }).reset_index()
    pctrevenue_band.rename(columns={'decimal_value': 'total_revenue_segment'}, inplace=True)
    
    # Calculate percent of total revenue
    pctrevenue_band['percent_total_revenue'] = (pctrevenue_band['total_revenue_segment'] / total_rev_overall * 100).round(4)

    # Merge and calculate mix
    final_df = conv_rate_band_segments.merge(pctrevenue_band, on=['client_segment', 'deal_band'], how='left')
    final_df['total_revenue_segment'] = final_df['total_revenue_segment'].fillna(0)

    # Revenue Mix within segment
    final_df['percent_rev_within_segment'] = final_df.groupby('client_segment')['percent_total_revenue'].transform(
        lambda x: (x / x.sum() * 100) if x.sum() > 0 else 0
    ).round(2)

    # Expected Value and Average Size
    final_df['avg_deal_size'] = (final_df['total_revenue_segment'] / final_df['converted_deals']).replace([np.inf, -np.inf], 0).fillna(0)
    final_df['expected_value'] = ((final_df['conversion_rate'] / 100) * final_df['avg_deal_size']).round(2)

    # Missed Opportunities
    missed_deals = deals[deals['converted'] == False]
    missed_stats = missed_deals.groupby(['client_segment', 'deal_band'], observed=False).agg(
        missed_revenue=('decimal_value', 'sum'),
        missed_deal_count=('decimal_value', 'count')
    ).reset_index()

    final_df = final_df.merge(missed_stats, on=['client_segment', 'deal_band'], how='left')
    final_df[['missed_revenue', 'missed_deal_count']] = final_df[['missed_revenue', 'missed_deal_count']].fillna(0)
    
    return final_df

if __name__ == "__main__":
    os.makedirs('data', exist_ok=True)
    
    raw_deals = fetch_data("deals")
    raw_contacts = fetch_data("contacts")
    raw_stages = fetch_data("stages")
    
    if raw_deals and raw_contacts and raw_stages:
        df_deals = pd.DataFrame([d['data'] for d in raw_deals])
        df_contacts = pd.DataFrame([c['data'] for c in raw_contacts])
        df_stages = pd.DataFrame([s['data'] for s in raw_stages])
        
        df_master = clean_deals(df_deals, df_contacts, df_stages)
        
        df_segments = create_grouped_segments_df(df_master)
        df_bands = create_conv_rate_revenue_band(df_master)
        
        df_master.to_csv("data/deals_clean.csv", index=False)
        df_segments.to_csv("data/grouped_segments_df.csv", index=False)
        df_bands.to_csv("data/conv_rate_revenue_band.csv", index=False)
        print("Done! All files saved in /data")
        


    