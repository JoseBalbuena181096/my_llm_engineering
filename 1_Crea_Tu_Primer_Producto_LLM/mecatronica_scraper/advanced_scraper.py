#!/usr/bin/env python3
"""
Advanced Web Scraper Module
Provides enhanced web scraping capabilities with AI analysis support
"""

import requests
from bs4 import BeautifulSoup
import time
import random
from typing import Dict, List, Optional
import json

class AdvancedWebScraper:
    """
    Advanced web scraper with enhanced capabilities
    """
    
    def __init__(self, headless: bool = True, enable_ai_analysis: bool = False):
        """
        Initialize the advanced web scraper
        
        Args:
            headless: Whether to run in headless mode (for compatibility)
            enable_ai_analysis: Whether to enable AI analysis features
        """
        self.headless = headless
        self.enable_ai_analysis = enable_ai_analysis
        self.session = requests.Session()
        
        # Set up headers to mimic a real browser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.session.headers.update(self.headers)
    
    def get_page_content(self, url: str, wait_time: float = 1.0) -> Optional[BeautifulSoup]:
        """
        Get page content using requests and BeautifulSoup
        
        Args:
            url: URL to scrape
            wait_time: Time to wait between requests
            
        Returns:
            BeautifulSoup object or None if failed
        """
        try:
            # Add random delay to avoid being blocked
            time.sleep(random.uniform(0.5, wait_time))
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
            
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def extract_job_listings(self, soup: BeautifulSoup, site_type: str = "generic") -> List[Dict]:
        """
        Extract job listings from a page
        
        Args:
            soup: BeautifulSoup object of the page
            site_type: Type of job site (indeed, occ, generic)
            
        Returns:
            List of job dictionaries
        """
        jobs = []
        
        if site_type == "indeed":
            # Indeed-specific selectors
            job_cards = soup.find_all(['div'], class_=lambda x: x and ('job' in x.lower() or 'result' in x.lower()))
            
            for card in job_cards:
                job = self._extract_indeed_job(card)
                if job:
                    jobs.append(job)
                    
        elif site_type == "occ":
            # OCC-specific selectors
            job_cards = soup.find_all(['div', 'article'], class_=lambda x: x and ('trabajo' in x.lower() or 'empleo' in x.lower()))
            
            for card in job_cards:
                job = self._extract_occ_job(card)
                if job:
                    jobs.append(job)
        else:
            # Generic job extraction
            job_cards = soup.find_all(['div', 'article'], class_=lambda x: x and any(keyword in x.lower() for keyword in ['job', 'trabajo', 'empleo', 'position']))
            
            for card in job_cards:
                job = self._extract_generic_job(card)
                if job:
                    jobs.append(job)
        
        return jobs
    
    def _extract_indeed_job(self, card) -> Optional[Dict]:
        """Extract job information from Indeed job card"""
        try:
            job = {}
            
            # Title
            title_elem = card.find(['h2', 'a'], class_=lambda x: x and 'title' in x.lower())
            if not title_elem:
                title_elem = card.find('a', attrs={'data-jk': True})
            job['title'] = title_elem.get_text(strip=True) if title_elem else "N/A"
            
            # Company
            company_elem = card.find(['span', 'div'], class_=lambda x: x and 'company' in x.lower())
            job['company'] = company_elem.get_text(strip=True) if company_elem else "N/A"
            
            # Location
            location_elem = card.find(['div', 'span'], class_=lambda x: x and 'location' in x.lower())
            job['location'] = location_elem.get_text(strip=True) if location_elem else "N/A"
            
            # Link
            link_elem = card.find('a', href=True)
            if link_elem:
                href = link_elem['href']
                job['link'] = href if href.startswith('http') else f"https://indeed.com{href}"
            else:
                job['link'] = "N/A"
            
            # Description snippet
            desc_elem = card.find(['div', 'span'], class_=lambda x: x and any(word in x.lower() for word in ['summary', 'snippet', 'description']))
            job['description'] = desc_elem.get_text(strip=True) if desc_elem else "N/A"
            
            return job if job['title'] != "N/A" else None
            
        except Exception as e:
            print(f"Error extracting Indeed job: {e}")
            return None
    
    def _extract_occ_job(self, card) -> Optional[Dict]:
        """Extract job information from OCC job card"""
        try:
            job = {}
            
            # Title
            title_elem = card.find(['h2', 'h3', 'a'], class_=lambda x: x and any(word in x.lower() for word in ['titulo', 'title', 'puesto']))
            job['title'] = title_elem.get_text(strip=True) if title_elem else "N/A"
            
            # Company
            company_elem = card.find(['span', 'div'], class_=lambda x: x and 'empresa' in x.lower())
            job['company'] = company_elem.get_text(strip=True) if company_elem else "N/A"
            
            # Location
            location_elem = card.find(['div', 'span'], class_=lambda x: x and any(word in x.lower() for word in ['ubicacion', 'location', 'lugar']))
            job['location'] = location_elem.get_text(strip=True) if location_elem else "N/A"
            
            # Link
            link_elem = card.find('a', href=True)
            if link_elem:
                href = link_elem['href']
                job['link'] = href if href.startswith('http') else f"https://occ.com.mx{href}"
            else:
                job['link'] = "N/A"
            
            # Description
            desc_elem = card.find(['div', 'p'], class_=lambda x: x and any(word in x.lower() for word in ['descripcion', 'resumen', 'summary']))
            job['description'] = desc_elem.get_text(strip=True) if desc_elem else "N/A"
            
            return job if job['title'] != "N/A" else None
            
        except Exception as e:
            print(f"Error extracting OCC job: {e}")
            return None
    
    def _extract_generic_job(self, card) -> Optional[Dict]:
        """Extract job information from generic job card"""
        try:
            job = {}
            
            # Try to find title in various ways
            title_elem = card.find(['h1', 'h2', 'h3', 'h4']) or card.find('a')
            job['title'] = title_elem.get_text(strip=True) if title_elem else "N/A"
            
            # Try to find company
            company_elem = card.find(text=lambda text: text and any(word in text.lower() for word in ['company', 'empresa']))
            job['company'] = company_elem.strip() if company_elem else "N/A"
            
            # Try to find location
            location_elem = card.find(text=lambda text: text and any(word in text.lower() for word in ['location', 'ubicación']))
            job['location'] = location_elem.strip() if location_elem else "N/A"
            
            # Link
            link_elem = card.find('a', href=True)
            job['link'] = link_elem['href'] if link_elem else "N/A"
            
            # Description
            job['description'] = card.get_text(strip=True)[:200] + "..." if len(card.get_text(strip=True)) > 200 else card.get_text(strip=True)
            
            return job if job['title'] != "N/A" else None
            
        except Exception as e:
            print(f"Error extracting generic job: {e}")
            return None
    
    def analyze_with_ai(self, content: str) -> Dict:
        """
        Placeholder for AI analysis functionality
        
        Args:
            content: Content to analyze
            
        Returns:
            Analysis results dictionary
        """
        if not self.enable_ai_analysis:
            return {"analysis": "AI analysis disabled"}
        
        # This would integrate with an AI service in a real implementation
        return {
            "analysis": "AI analysis placeholder",
            "relevance_score": 0.5,
            "keywords_found": [],
            "summary": "Content analysis not implemented"
        }
    
    def close(self):
        """Close the scraper session"""
        self.session.close()