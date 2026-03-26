"""Parse CV PDF and extract relevant keywords and skills"""
from pathlib import Path
from typing import List, Dict
import re

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

class CVParser:
    """Extract skills and keywords from CV"""
    
    SKILL_KEYWORDS = {
        # Technical
        'python', 'gis', 'r', 'sql', 'excel', 'data analysis', 'geospatial',
        # Sector
        'ngo', 'environmental', 'conservation', 'sustainability', 'climate',
        'forestry', 'forest governance', 'land rights', 'tenure',
        # Geographic
        'southeast asia', 'thailand', 'indonesia', 'asia-pacific', 'myanmar', 'cambodia',
        'laos', 'vietnam', 'philippines',
        # Methods
        'facilitation', 'training', 'workshop', 'monitoring', 'evaluation', 'mel',
        'donor reporting', 'grants management', 'project management',
        'policy analysis', 'policy advisory', 'research',
        # Issues
        'indigenous peoples', 'indigenous', 'community', 'stakeholder engagement',
        'land and resource rights', 'political ecology', 'tenure security'
    }
    
    def __init__(self, cv_path: str):
        """Initialize with CV file path"""
        self.cv_path = Path(cv_path)
    
    def extract_text(self) -> str:
        """Extract text from PDF CV"""
        if not self.cv_path.exists():
            raise FileNotFoundError(f"CV file not found: {self.cv_path}")
        
        if self.cv_path.suffix.lower() == '.pdf':
            return self._extract_from_pdf()
        else:
            with open(self.cv_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
    
    def _extract_from_pdf(self) -> str:
        """Extract text from PDF file"""
        if PdfReader is None:
            return ""
        
        try:
            reader = PdfReader(str(self.cv_path))
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return ""
    
    def extract_keywords(self) -> List[str]:
        """Extract relevant keywords from CV"""
        try:
            text = self.extract_text().lower()
        except:
            return []
        
        found_keywords = []
        for keyword in self.SKILL_KEYWORDS:
            if keyword.lower() in text:
                found_keywords.append(keyword)
        
        return list(set(found_keywords))
    
    def extract_experience_years(self) -> int:
        """Estimate years of experience from CV"""
        text = self.extract_text()
        
        year_patterns = [
            r'(\d+)\s*years?\s*(?:of\s*)?(?:experience|exp)',
            r'(20\d{2})\s*[-–]\s*(20\d{2})',
            r'(20\d{2})\s*[-–]\s*present',
        ]
        
        years = []
        for pattern in year_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    try:
                        years.append(int(match[1]) - int(match[0]))
                    except (ValueError, IndexError):
                        pass
                else:
                    try:
                        years.append(int(match))
                    except ValueError:
                        pass
        
        return max(years) if years else 5
    
    def get_summary(self) -> Dict:
        """Get CV summary"""
        return {
            'keywords': self.extract_keywords(),
            'experience_years': self.extract_experience_years(),
            'has_sector_experience': any(
                kw in self.extract_keywords() 
                for kw in ['ngo', 'environmental', 'conservation']
            ),
            'has_asia_experience': any(
                kw in self.extract_keywords() 
                for kw in ['southeast asia', 'thailand', 'asia-pacific']
            ),
            'has_mel_experience': any(
                kw in self.extract_keywords() 
                for kw in ['monitoring', 'evaluation', 'mel']
            )
        }