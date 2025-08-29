#!/usr/bin/env python3
"""
Script to extract all Comet browser history data into a structured format for AI processing.
Following MVT (Model-View-Template) and DRY principles.
"""

import sqlite3
import json
import csv
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict

@dataclass
class HistoryEntry:
    """Model for a browser history entry"""
    id: int
    url: str
    title: str
    visit_count: int
    typed_count: int
    last_visit_time: str  # ISO format
    last_visit_timestamp: int  # Original Chrome timestamp
    domain: str
    visits: List[Dict[str, Any]]
    search_terms: List[str]
    category: str  # Will be determined by domain/URL patterns

class HistoryExtractor:
    """Main class for extracting browser history data"""
    
    def __init__(self, db_path: str = "comet_history_temp.db"):
        self.db_path = Path(db_path)
        self.history_entries: List[HistoryEntry] = []
    
    def _chrome_timestamp_to_datetime(self, chrome_timestamp: int) -> str:
        """Convert Chrome timestamp to ISO format datetime string"""
        if chrome_timestamp == 0:
            return ""
        
        # Chrome timestamps are microseconds since January 1, 1601
        # Convert to Unix timestamp first
        unix_timestamp = (chrome_timestamp - 11644473600000000) / 1000000
        dt = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)
        return dt.isoformat()
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        try:
            if url.startswith(('http://', 'https://')):
                return url.split('/')[2].lower()
            return url.split('/')[0].lower()
        except (IndexError, AttributeError):
            return "unknown"
    
    def _categorize_url(self, url: str, title: str) -> str:
        """Categorize URL based on domain and content patterns"""
        domain = self._extract_domain(url)
        url_lower = url.lower()
        title_lower = title.lower()
        
        # Development & Tech
        if any(keyword in domain for keyword in [
            'github', 'stackoverflow', 'dev.to', 'medium', 'hackernews', 
            'reddit.com/r/programming', 'docs.', 'api.', 'developer'
        ]):
            return "Development & Tech"
        
        # Learning & Education
        if any(keyword in domain for keyword in [
            'coursera', 'udemy', 'pluralsight', 'youtube', 'khan', 
            'edx', 'harvard', 'mit', 'university'
        ]) or any(keyword in title_lower for keyword in [
            'tutorial', 'course', 'learn', 'education'
        ]):
            return "Learning & Education"
        
        # Work & Productivity
        if any(keyword in domain for keyword in [
            'slack', 'notion', 'trello', 'jira', 'confluence', 
            'office', 'google.com/drive', 'dropbox'
        ]):
            return "Work & Productivity"
        
        # News & Information
        if any(keyword in domain for keyword in [
            'news', 'bbc', 'cnn', 'reuters', 'techcrunch', 'ars-technica'
        ]):
            return "News & Information"
        
        # Social Media
        if any(keyword in domain for keyword in [
            'facebook', 'twitter', 'linkedin', 'instagram', 'tiktok'
        ]):
            return "Social Media"
        
        # Shopping
        if any(keyword in domain for keyword in [
            'amazon', 'ebay', 'shop', 'store', 'buy', 'market'
        ]):
            return "Shopping"
        
        # Entertainment
        if any(keyword in domain for keyword in [
            'netflix', 'spotify', 'twitch', 'gaming', 'entertainment'
        ]):
            return "Entertainment"
        
        return "Other"
    
    def extract_data(self) -> bool:
        """Extract all history data from the database"""
        if not self.db_path.exists():
            print(f"❌ Database not found at: {self.db_path}")
            return False
        
        try:
            conn = sqlite3.connect(f"file:{self.db_path}?mode=ro", uri=True)
            cursor = conn.cursor()
            
            print("🔍 Extracting URLs and basic info...")
            
            # Get all URLs with their basic information
            cursor.execute("""
                SELECT id, url, title, visit_count, typed_count, last_visit_time, hidden
                FROM urls 
                WHERE hidden = 0 AND url != ''
                ORDER BY last_visit_time DESC
            """)
            
            urls_data = cursor.fetchall()
            print(f"📊 Found {len(urls_data)} URLs")
            
            # Create a mapping for efficient lookups
            url_visits = defaultdict(list)
            url_search_terms = defaultdict(list)
            
            print("🔍 Extracting visit details...")
            
            # Get all visits for each URL
            cursor.execute("""
                SELECT v.url, v.visit_time, v.visit_duration, v.transition, v.external_referrer_url
                FROM visits v
                ORDER BY v.visit_time DESC
            """)
            
            visits_data = cursor.fetchall()
            print(f"📊 Found {len(visits_data)} visits")
            
            # Group visits by URL ID
            for visit in visits_data:
                url_id, visit_time, duration, transition, referrer = visit
                url_visits[url_id].append({
                    'visit_time': self._chrome_timestamp_to_datetime(visit_time),
                    'visit_timestamp': visit_time,
                    'duration': duration,
                    'transition': transition,
                    'referrer': referrer or ""
                })
            
            print("🔍 Extracting search terms...")
            
            # Get search terms
            cursor.execute("""
                SELECT url_id, term
                FROM keyword_search_terms
            """)
            
            search_terms_data = cursor.fetchall()
            print(f"📊 Found {len(search_terms_data)} search terms")
            
            # Group search terms by URL ID
            for url_id, term in search_terms_data:
                url_search_terms[url_id].append(term)
            
            # Process all data into HistoryEntry objects
            print("⚙️  Processing data...")
            
            for url_data in urls_data:
                url_id, url, title, visit_count, typed_count, last_visit_time, hidden = url_data
                
                # Skip empty or invalid URLs
                if not url or url.strip() == '':
                    continue
                
                entry = HistoryEntry(
                    id=url_id,
                    url=url,
                    title=title or "No Title",
                    visit_count=visit_count,
                    typed_count=typed_count,
                    last_visit_time=self._chrome_timestamp_to_datetime(last_visit_time),
                    last_visit_timestamp=last_visit_time,
                    domain=self._extract_domain(url),
                    visits=url_visits.get(url_id, []),
                    search_terms=url_search_terms.get(url_id, []),
                    category=self._categorize_url(url, title or "")
                )
                
                self.history_entries.append(entry)
            
            conn.close()
            
            # Sort by last visit time (most recent first)
            self.history_entries.sort(key=lambda x: x.last_visit_timestamp, reverse=True)
            
            print(f"✅ Successfully processed {len(self.history_entries)} history entries")
            return True
            
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    def save_to_json(self, filename: str = "comet_history.json") -> bool:
        """Save history data to JSON file"""
        try:
            # Convert dataclasses to dictionaries
            data = {
                "metadata": {
                    "total_entries": len(self.history_entries),
                    "extraction_date": datetime.now(timezone.utc).isoformat(),
                    "categories": list(set(entry.category for entry in self.history_entries))
                },
                "history": [asdict(entry) for entry in self.history_entries]
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 JSON data saved to: {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving JSON: {e}")
            return False
    
    def save_to_csv(self, filename: str = "comet_history.csv") -> bool:
        """Save history data to CSV file (flattened format)"""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow([
                    'id', 'url', 'title', 'domain', 'category', 
                    'visit_count', 'typed_count', 'last_visit_time',
                    'total_visits', 'search_terms'
                ])
                
                # Write data
                for entry in self.history_entries:
                    writer.writerow([
                        entry.id,
                        entry.url,
                        entry.title,
                        entry.domain,
                        entry.category,
                        entry.visit_count,
                        entry.typed_count,
                        entry.last_visit_time,
                        len(entry.visits),
                        '; '.join(entry.search_terms)
                    ])
            
            print(f"💾 CSV data saved to: {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving CSV: {e}")
            return False
    
    def generate_summary(self) -> Dict[str, Any]:
        """Generate summary statistics"""
        if not self.history_entries:
            return {}
        
        categories = defaultdict(int)
        domains = defaultdict(int)
        total_visits = 0
        total_search_terms = 0
        
        for entry in self.history_entries:
            categories[entry.category] += 1
            domains[entry.domain] += 1
            total_visits += len(entry.visits)
            total_search_terms += len(entry.search_terms)
        
        # Get top domains
        top_domains = sorted(domains.items(), key=lambda x: x[1], reverse=True)[:20]
        
        return {
            "total_urls": len(self.history_entries),
            "total_visits": total_visits,
            "total_search_terms": total_search_terms,
            "categories": dict(categories),
            "top_domains": dict(top_domains),
            "date_range": {
                "oldest": min((e.last_visit_time for e in self.history_entries if e.last_visit_time), default=""),
                "newest": max((e.last_visit_time for e in self.history_entries if e.last_visit_time), default="")
            }
        }

def main():
    """Main function to extract and save browser history"""
    print("🚀 Starting Comet Browser History Extraction")
    print("=" * 50)
    
    extractor = HistoryExtractor()
    
    # Extract data
    if not extractor.extract_data():
        print("❌ Failed to extract data")
        sys.exit(1)
    
    # Generate and display summary
    summary = extractor.generate_summary()
    print("\n📊 SUMMARY STATISTICS")
    print("=" * 30)
    print(f"📝 Total URLs: {summary.get('total_urls', 0)}")
    print(f"👁️  Total Visits: {summary.get('total_visits', 0)}")
    print(f"🔍 Total Search Terms: {summary.get('total_search_terms', 0)}")
    
    print(f"\n🗂️  Categories:")
    for category, count in sorted(summary.get('categories', {}).items()):
        print(f"   • {category}: {count}")
    
    print(f"\n🌐 Top 10 Domains:")
    for domain, count in list(summary.get('top_domains', {}).items())[:10]:
        print(f"   • {domain}: {count}")
    
    # Save data
    print("\n💾 Saving data...")
    
    # Save JSON (comprehensive format for AI processing)
    if extractor.save_to_json("comet_history_complete.json"):
        print("✅ Comprehensive JSON saved")
    
    # Save CSV (simplified format for quick review)
    if extractor.save_to_csv("comet_history_summary.csv"):
        print("✅ Summary CSV saved")
    
    # Save summary statistics
    try:
        with open("comet_history_statistics.json", 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        print("✅ Statistics saved")
    except Exception as e:
        print(f"❌ Error saving statistics: {e}")
    
    print("\n🎉 Extraction completed successfully!")
    print("\nFiles created:")
    print("  📄 comet_history_complete.json - Full data for AI processing")
    print("  📊 comet_history_summary.csv - Quick overview")
    print("  📈 comet_history_statistics.json - Summary statistics")
    
    print(f"\n💡 You can now use these files with AI tools to filter and organize your {summary.get('total_urls', 0)} URLs!")

if __name__ == "__main__":
    main()
