import pandas as pd
import os
import random
import requests
from io import StringIO
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration from environment variables
SHEET_ID = os.getenv("QUESTION_SHEET_ID")
RESULT_SYNC_URL = os.getenv("RESULT_SYNC_URL")
SECTIONS = ['Quantitative Aptitude', 'Verbal (English)', 'Reasoning', 'Programming'] 
RECORDS_FILE = 'data/records.xlsx' 

def map_answer(row):
    """Convert 'A', 'B', 'C', 'D' or text answer to 1, 2, 3, 4"""
    ans = str(row.get('Answer', '')).strip().upper()
    mapping = {'A': 1, 'B': 2, 'C': 3, 'D': 4}
    if ans in mapping: return mapping[ans]
    if ans == str(row.get('Option A', '')).strip().upper(): return 1
    if ans == str(row.get('Option B', '')).strip().upper(): return 2
    if ans == str(row.get('Option C', '')).strip().upper(): return 3
    if ans == str(row.get('Option D', '')).strip().upper(): return 4
    return 1

def load_random_questions(questions_per_sheet=5):
    """Load questions live from Google Sheets"""
    if not SHEET_ID:
        print("CRITICAL: QUESTION_SHEET_ID not found in environment.")
        return []
        
    all_questions = []
    for section in SECTIONS:
        try:
            url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={section.replace(' ', '%20')}"
            response = requests.get(url)
            if "html" in response.headers.get('Content-Type', '').lower():
                print(f"Access Denied for {section}")
                continue
            df = pd.read_csv(StringIO(response.text))
            if df.empty: continue
            mapped_records = []
            for _, row in df.iterrows():
                mapped_q = {
                    'question': row.get('Question', ''),
                    'option1': row.get('Option A', ''),
                    'option2': row.get('Option B', ''),
                    'option3': row.get('Option C', ''),
                    'option4': row.get('Option D', ''),
                    'correct_option': map_answer(row),
                    'section': section
                }
                if mapped_q['question'] and str(mapped_q['question']) != 'nan':
                    mapped_records.append(mapped_q)
            sample_size = min(len(mapped_records), questions_per_sheet)
            if sample_size > 0:
                all_questions.extend(random.sample(mapped_records, sample_size))
        except Exception as e:
            print(f"Error loading section {section}: {e}")
    return all_questions

def save_record(session_data):
    """Save quiz record locally AND sync to Google Sheet"""
    # 1. Local Backup
    if not os.path.exists('data'): os.makedirs('data')
    try:
        if not os.path.exists(RECORDS_FILE):
            df = pd.DataFrame([session_data])
        else:
            df_old = pd.read_excel(RECORDS_FILE)
            df = pd.concat([df_old, pd.DataFrame([session_data])], ignore_index=True)
        df.to_excel(RECORDS_FILE, index=False)
    except Exception as e:
        print(f"Local Save Error: {e}")

    # 2. Sync to Google Sheet (via Apps Script)
    if RESULT_SYNC_URL:
        try:
            response = requests.post(RESULT_SYNC_URL, json=session_data)
            if response.status_code == 200:
                print("Successfully synced to Google Sheet!")
            else:
                print(f"Failed to sync to Google Sheet: {response.status_code}")
        except Exception as e:
            print(f"Google Sync Error: {e}")
