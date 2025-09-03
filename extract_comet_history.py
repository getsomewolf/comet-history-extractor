#!/usr/bin/env python3
"""
Script to extract all Comet browser history data into a structured format for AI processing.
Following MVT (Model-View-Template) and DRY principles.
"""

import sqlite3
import json
import csv
import sys
import argparse
import re
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple
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

class ChunkingHelper:
    """Helper class for handling LLM-compatible chunking"""
    
    @staticmethod
    def parse_chunk_size(chunk_size_str: str) -> int:
        """Parse chunk size string (e.g., '200k', '1M') to number of tokens"""
        if not chunk_size_str:
            return 200000  # Default 200k tokens
        
        chunk_size_str = chunk_size_str.upper().strip()
        
        # Extract number and unit
        match = re.match(r'^(\d+(?:\.\d+)?)\s*([KM]?)$', chunk_size_str)
        if not match:
            raise ValueError(f"Invalid chunk size format: {chunk_size_str}. Use formats like '200k' or '1M'")
        
        number, unit = match.groups()
        number = float(number)
        
        if unit == 'K':
            result = int(number * 1000)
        elif unit == 'M':
            result = int(number * 1000000)
        else:
            result = int(number)
        
        # Reject zero or negative values
        if result <= 0:
            raise ValueError(f"Chunk size must be positive: {chunk_size_str}")
        
        return result
    
    @staticmethod
    def estimate_tokens(obj: Any) -> int:
        """Estimate token count for any object using character count heuristic"""
        # Convert object to JSON string and count characters
        json_str = json.dumps(obj, ensure_ascii=False)
        char_count = len(json_str)
        
        # Rough approximation: 4 characters per token for English text
        # This is a common heuristic used in the industry
        return max(1, char_count // 4)

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
    
    def chunk_history(self, max_tokens_per_chunk: int) -> List[Tuple[List[HistoryEntry], Dict[str, Any]]]:
        """
        Split history entries into chunks based on token limits
        Returns list of (entries, chunk_metadata) tuples
        """
        if not self.history_entries:
            return []
        
        chunks = []
        current_chunk = []
        current_tokens = 0
        chunk_counter = 1
        
        # Base metadata structure for each chunk
        base_metadata = {
            "extraction_date": datetime.now(timezone.utc).isoformat(),
            "categories": list(set(entry.category for entry in self.history_entries))
        }
        
        for entry in self.history_entries:
            # Estimate tokens for this entry
            entry_tokens = ChunkingHelper.estimate_tokens(asdict(entry))
            
            # If this entry alone exceeds chunk limit, put it in its own chunk
            if entry_tokens > max_tokens_per_chunk:
                # Save current chunk if it has entries
                if current_chunk:
                    chunk_metadata = {
                        **base_metadata,
                        "chunk_id": chunk_counter,
                        "total_entries": len(current_chunk),
                        "estimated_tokens": current_tokens
                    }
                    chunks.append((current_chunk.copy(), chunk_metadata))
                    chunk_counter += 1
                    current_chunk = []
                    current_tokens = 0
                
                # Create chunk with just this large entry
                large_entry_metadata = {
                    **base_metadata,
                    "chunk_id": chunk_counter,
                    "total_entries": 1,
                    "estimated_tokens": entry_tokens,
                    "warning": "This chunk exceeds the requested token limit due to a single large entry"
                }
                chunks.append(([entry], large_entry_metadata))
                chunk_counter += 1
                continue
            
            # If adding this entry would exceed the limit, start a new chunk
            if current_tokens + entry_tokens > max_tokens_per_chunk and current_chunk:
                chunk_metadata = {
                    **base_metadata,
                    "chunk_id": chunk_counter,
                    "total_entries": len(current_chunk),
                    "estimated_tokens": current_tokens
                }
                chunks.append((current_chunk.copy(), chunk_metadata))
                chunk_counter += 1
                current_chunk = []
                current_tokens = 0
            
            current_chunk.append(entry)
            current_tokens += entry_tokens
        
        # Don't forget the last chunk
        if current_chunk:
            chunk_metadata = {
                **base_metadata,
                "chunk_id": chunk_counter,
                "total_entries": len(current_chunk),
                "estimated_tokens": current_tokens
            }
            chunks.append((current_chunk, chunk_metadata))
        
        # Update total_chunks in all metadata
        total_chunks = len(chunks)
        for entries, metadata in chunks:
            metadata["total_chunks"] = total_chunks
        
        return chunks
    
    def save_chunks(self, chunks: List[Tuple[List[HistoryEntry], Dict[str, Any]]], 
                   base_filename: str = "comet_history_chunk") -> bool:
        """Save chunked history data to multiple JSON files"""
        try:
            saved_files = []
            
            for entries, metadata in chunks:
                chunk_id = metadata["chunk_id"]
                filename = f"{base_filename}_{chunk_id}.json"
                
                # Create the chunk data structure
                chunk_data = {
                    "chunk_info": metadata,
                    "history": [asdict(entry) for entry in entries]
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(chunk_data, f, indent=2, ensure_ascii=False)
                
                saved_files.append(filename)
                print(f"💾 Chunk {chunk_id}/{metadata['total_chunks']} saved to: {filename} "
                      f"({metadata['total_entries']} entries, ~{metadata['estimated_tokens']:,} tokens)")
            
            print(f"\n✅ All {len(chunks)} chunks saved successfully!")
            print("📁 Files created:")
            for filename in saved_files:
                print(f"  • {filename}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error saving chunks: {e}")
            return False

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Extract Comet browser history data for AI processing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python extract_comet_history.py                    # Default extraction (single file)
  python extract_comet_history.py --chunk-size 200k  # Split into 200k token chunks
  python extract_comet_history.py --chunk-size 1M    # Split into 1M token chunks
        '''
    )
    
    parser.add_argument(
        '--chunk-size',
        type=str,
        help='Split output into chunks of specified token size (e.g., "200k", "1M"). '
             'If not specified, outputs a single file.'
    )
    
    parser.add_argument(
        '--db-path',
        type=str,
        default="comet_history_temp.db",
        help='Path to the Comet browser history database (default: comet_history_temp.db)'
    )
    
    return parser.parse_args()

def main():
    """Main function to extract and save browser history"""
    args = parse_arguments()
    
    print("🚀 Starting Comet Browser History Extraction")
    print("=" * 50)
    
    extractor = HistoryExtractor(args.db_path)
    
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
    
    # Check if chunking is requested
    if args.chunk_size:
        try:
            max_tokens = ChunkingHelper.parse_chunk_size(args.chunk_size)
            print(f"🔄 Chunking data into {max_tokens:,} token chunks...")
            
            # Estimate total tokens for all data
            total_estimated_tokens = sum(
                ChunkingHelper.estimate_tokens(asdict(entry)) 
                for entry in extractor.history_entries
            )
            print(f"📊 Estimated total tokens: {total_estimated_tokens:,}")
            
            # Create chunks
            chunks = extractor.chunk_history(max_tokens)
            
            if not chunks:
                print("❌ No data to chunk")
                sys.exit(1)
            
            print(f"✂️  Created {len(chunks)} chunks")
            
            # Save chunks
            if extractor.save_chunks(chunks):
                print("✅ Chunked data saved successfully")
            else:
                print("❌ Failed to save chunks")
                sys.exit(1)
                
        except ValueError as e:
            print(f"❌ Error with chunk size: {e}")
            sys.exit(1)
    else:
        # Original behavior - single file output
        print("📄 Saving as single file (no chunking)...")
        
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
