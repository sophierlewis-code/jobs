import re
from pathlib import Path
from typing import List, Dict, Set
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class BookmarkParser:
    """Parse HTML bookmark files and extract job source URLs"""
    
    def __init__(self, bookmark_path: str):
        self.bookmark_path = Path(bookmark_path)
    
    def extract_urls(self) -> List[Dict[str, str]]:
        """
        Extract URLs and titles from bookmark HTML file.
        Returns list of dicts with 'url', 'title', 'folder' keys.
        """
        if not self.bookmark_path.exists():
            raise FileNotFoundError(f"Bookmark file not found: {self.bookmark_path}")
        
        with open(self.bookmark_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        urls = []
        
        # Traverse all <A> tags which contain bookmarks
        for link in soup.find_all('a'):
            href = link.get('href', '')
            title = link.get_text(strip=True)
            
            # Only include http/https links
            if href.startswith('http://') or href.startswith('https://'):
                urls.append({
                    'url': href,
                    'title': title,
                    'domain': urlparse(href).netloc
                })
        
        return urls
    
    def extract_job_sources(self) -> List[Dict[str, str]]:
        """
        Extract URLs that are likely job sources.
        Filters for job boards and career sites.
        """
        all_urls = self.extract_urls()
        job_sites = self._get_job_site_keywords()
        
        job_sources = []
        seen = set()  # Avoid duplicates
        
        for url_data in all_urls:
            url = url_data['url']
            domain = url_data['domain'].lower()
            title = url_data['title'].lower()
            
            # Check if domain or title matches job site keywords
            is_job_site = any(
                keyword in domain or keyword in title 
                for keyword in job_sites
            )
            
            if is_job_site and url not in seen:
                job_sources.append(url_data)
                seen.add(url)
        
        return job_sources
    
    def _get_job_site_keywords(self) -> Set[str]:
        """Common job site keywords to filter"""
        return {
            'indeed', 'linkedin', 'glassdoor', 'monster',
            'devops', 'stackoverflow', 'github',
            'jobs', 'career', 'recruitment', 'hire',
            'application', 'opportunity', 'vacancy',
            'ngo', 'charity', 'volunteer', 'grant',
            'consultant', 'freelance', 'upwork', 'toptal',
            'devex', 'reliefweb', 'idealist', 'globalgiving'
        }
    
    def create_source_list(self, output_path: str = "config/job_sources.md"):
        """
        Create a curated markdown list of job sources.
        User can then edit to add descriptions and enable/disable sources.
        """
        job_sources = self.extract_job_sources()
        
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output, 'w') as f:
            f.write("# Curated Job Sources\n\n")
            f.write("Sources extracted from bookmarks for job searching.\n")
            f.write("Mark sources as ENABLED or DISABLED. Add descriptions as needed.\n\n")
            
            for source in sorted(job_sources, key=lambda x: x['domain']):
                f.write(f"## {source['domain']}\n")
                f.write(f"- **URL**: [{source['url']}]({source['url']})\n")
                f.write(f"- **Title**: {source['title']}\n")
                f.write("- **Status**: ENABLED\n")
                f.write("- **Description**: \n")
                f.write("- **API Available**: \n\n")
        
        return output_path
