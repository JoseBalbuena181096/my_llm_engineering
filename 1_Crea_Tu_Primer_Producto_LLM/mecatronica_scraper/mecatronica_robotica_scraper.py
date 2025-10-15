#!/usr/bin/env python3
"""
Scraper especializado para ofertas de trabajo en Mecatrónica y Robótica
Busca en Indeed y OCC (Organización de Carreras Comerciales)
"""

import json
import time
import datetime
from typing import List, Dict
from advanced_scraper import AdvancedWebScraper
import urllib.parse

class MecatronicaRoboticaScraper:
    """
    Scraper especializado para ofertas de trabajo en Mecatrónica y Robótica
    """
    
    def __init__(self, headless: bool = True):
        """
        Inicializa el scraper especializado
        
        Args:
            headless: Si ejecutar Chrome en modo headless
        """
        self.scraper = AdvancedWebScraper(headless=headless, enable_ai_analysis=True)
        self.results = []
        
        # Términos de búsqueda relacionados con mecatrónica y robótica
        self.search_terms = [
            "mecatrónica",
            "mecatronica", 
            "robótica",
            "robotica",
            "automatización",
            "automatizacion",
            "control industrial",
            "sistemas embebidos",
            "PLC",
            "Arduino",
            "Raspberry Pi",
            "ingeniería mecatrónica",
            "ingeniero mecatrónico",
            "técnico mecatrónico",
            "automation engineer",
            "robotics engineer"
        ]
    
    def get_indeed_urls(self, location: str = "Colombia") -> List[Dict]:
        """
        Genera URLs de búsqueda para Indeed
        
        Args:
            location: Ubicación para la búsqueda
            
        Returns:
            Lista de diccionarios con URLs y términos de búsqueda
        """
        base_url = "https://co.indeed.com/jobs"
        urls = []
        
        for term in self.search_terms[:8]:  # Limitar a 8 términos principales
            encoded_term = urllib.parse.quote(term)
            encoded_location = urllib.parse.quote(location)
            
            url = f"{base_url}?q={encoded_term}&l={encoded_location}&sort=date"
            
            urls.append({
                'url': url,
                'search_term': term,
                'platform': 'Indeed',
                'location': location
            })
        
        return urls
    
    def get_occ_urls(self, location: str = "Colombia") -> List[Dict]:
        """
        Genera URLs de búsqueda para OCC (OCCMundial)
        
        Args:
            location: Ubicación para la búsqueda
            
        Returns:
            Lista de diccionarios con URLs y términos de búsqueda
        """
        base_url = "https://www.occ.com.mx/empleos/de"
        urls = []
        
        for term in self.search_terms[:6]:  # Limitar a 6 términos principales para OCC
            encoded_term = urllib.parse.quote(term.replace(" ", "-"))
            
            url = f"{base_url}-{encoded_term}"
            
            urls.append({
                'url': url,
                'search_term': term,
                'platform': 'OCC',
                'location': location
            })
        
        return urls
    
    def analyze_job_content(self, content: str, search_term: str) -> Dict:
        """
        Analiza el contenido de ofertas de trabajo con AI especializado
        
        Args:
            content: Contenido scrapeado
            search_term: Término de búsqueda usado
            
        Returns:
            Análisis especializado del contenido
        """
        specialized_prompt = f"""Analiza el siguiente contenido de un portal de empleo buscando ofertas relacionadas con "{search_term}".

Extrae y estructura la siguiente información:

1. **OFERTAS DE TRABAJO ENCONTRADAS:**
   - Títulos de puestos específicos
   - Empresas que ofrecen los empleos
   - Ubicaciones de trabajo
   - Salarios mencionados (si están disponibles)

2. **HABILIDADES TÉCNICAS REQUERIDAS:**
   - Software especializado (AutoCAD, SolidWorks, MATLAB, etc.)
   - Lenguajes de programación (Python, C++, etc.)
   - Tecnologías específicas (PLC, HMI, SCADA, etc.)
   - Certificaciones mencionadas

3. **NIVEL DE EXPERIENCIA:**
   - Puestos para recién egresados
   - Puestos de nivel intermedio
   - Puestos senior/especialistas

4. **SECTORES INDUSTRIALES:**
   - Automotriz, manufactura, energía, etc.

5. **TENDENCIAS OBSERVADAS:**
   - Demanda del mercado
   - Tecnologías emergentes mencionadas

Contenido a analizar:"""
        
        return self.scraper.analyze_with_ai(content, 'custom')
    
    def scrape_job_portals(self, location: str = "Colombia") -> List[Dict]:
        """
        Ejecuta el scraping en Indeed y OCC para ofertas de mecatrónica y robótica
        
        Args:
            location: Ubicación para la búsqueda
            
        Returns:
            Lista de resultados del scraping
        """
        print("🤖 Iniciando búsqueda de ofertas de Mecatrónica y Robótica")
        print("=" * 60)
        
        # Obtener URLs de ambas plataformas
        indeed_urls = self.get_indeed_urls(location)
        occ_urls = self.get_occ_urls(location)
        
        all_urls = indeed_urls + occ_urls
        
        results = []
        
        for i, url_info in enumerate(all_urls, 1):
            print(f"\n📊 Procesando {i}/{len(all_urls)}: {url_info['platform']}")
            print(f"🔍 Término: {url_info['search_term']}")
            print(f"🔗 URL: {url_info['url']}")
            print("-" * 40)
            
            try:
                # Scrapear el contenido
                scrape_result = self.scraper.smart_scrape(url_info['url'])
                
                if scrape_result['success']:
                    print(f"✅ Scraping exitoso - {len(scrape_result['text'])} caracteres")
                    
                    # Analizar con AI especializado
                    if len(scrape_result['text']) > 200:
                        analysis = self.analyze_job_content(
                            scrape_result['text'], 
                            url_info['search_term']
                        )
                        
                        if analysis['success']:
                            print(f"🧠 Análisis AI completado - {analysis.get('tokens_used', 'N/A')} tokens")
                        else:
                            print(f"⚠️ Error en análisis AI: {analysis.get('error', 'Desconocido')}")
                    else:
                        analysis = {
                            'analysis': 'Contenido insuficiente para análisis',
                            'success': False
                        }
                    
                    result = {
                        'timestamp': datetime.datetime.now().isoformat(),
                        'platform': url_info['platform'],
                        'search_term': url_info['search_term'],
                        'location': url_info['location'],
                        'url': url_info['url'],
                        'title': scrape_result.get('title', ''),
                        'content_length': len(scrape_result['text']),
                        'content_preview': scrape_result['text'][:500] + "..." if len(scrape_result['text']) > 500 else scrape_result['text'],
                        'analysis': analysis,
                        'scrape_success': True
                    }
                    
                else:
                    print(f"❌ Error en scraping: {scrape_result.get('error', 'Desconocido')}")
                    result = {
                        'timestamp': datetime.datetime.now().isoformat(),
                        'platform': url_info['platform'],
                        'search_term': url_info['search_term'],
                        'location': url_info['location'],
                        'url': url_info['url'],
                        'error': scrape_result.get('error', 'Error desconocido'),
                        'scrape_success': False
                    }
                
                results.append(result)
                
                # Delay entre requests para ser respetuoso
                time.sleep(2)
                
            except Exception as e:
                print(f"💥 Error inesperado: {e}")
                results.append({
                    'timestamp': datetime.datetime.now().isoformat(),
                    'platform': url_info['platform'],
                    'search_term': url_info['search_term'],
                    'url': url_info['url'],
                    'error': str(e),
                    'scrape_success': False
                })
        
        return results
    
    def generate_report(self, results: List[Dict]) -> Dict:
        """
        Genera un reporte consolidado de los resultados
        
        Args:
            results: Lista de resultados del scraping
            
        Returns:
            Reporte consolidado
        """
        successful_scrapes = [r for r in results if r.get('scrape_success', False)]
        failed_scrapes = [r for r in results if not r.get('scrape_success', False)]
        
        # Análisis por plataforma
        indeed_results = [r for r in successful_scrapes if r['platform'] == 'Indeed']
        occ_results = [r for r in successful_scrapes if r['platform'] == 'OCC']
        
        # Términos más exitosos
        term_success = {}
        for result in successful_scrapes:
            term = result['search_term']
            if term not in term_success:
                term_success[term] = 0
            term_success[term] += 1
        
        report = {
            'timestamp': datetime.datetime.now().isoformat(),
            'summary': {
                'total_searches': len(results),
                'successful_scrapes': len(successful_scrapes),
                'failed_scrapes': len(failed_scrapes),
                'success_rate': f"{(len(successful_scrapes)/len(results)*100):.1f}%" if results else "0%"
            },
            'platform_breakdown': {
                'Indeed': {
                    'total': len([r for r in results if r['platform'] == 'Indeed']),
                    'successful': len(indeed_results),
                    'avg_content_length': sum(r.get('content_length', 0) for r in indeed_results) / len(indeed_results) if indeed_results else 0
                },
                'OCC': {
                    'total': len([r for r in results if r['platform'] == 'OCC']),
                    'successful': len(occ_results),
                    'avg_content_length': sum(r.get('content_length', 0) for r in occ_results) / len(occ_results) if occ_results else 0
                }
            },
            'most_successful_terms': sorted(term_success.items(), key=lambda x: x[1], reverse=True)[:5],
            'detailed_results': results
        }
        
        return report
    
    def save_results(self, results: List[Dict], filename: str = None) -> str:
        """
        Guarda los resultados en un archivo JSON
        
        Args:
            results: Lista de resultados
            filename: Nombre del archivo (opcional)
            
        Returns:
            Nombre del archivo guardado
        """
        if not filename:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"mecatronica_robotica_jobs_{timestamp}.json"
        
        report = self.generate_report(results)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return filename
    
    def close(self):
        """Cierra el scraper"""
        self.scraper.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def main():
    """Función principal para ejecutar el scraper"""
    print("🤖 Scraper de Ofertas de Trabajo - Mecatrónica y Robótica")
    print("=" * 60)
    
    location = input("Ingresa la ubicación de búsqueda (default: Colombia): ").strip() or "Colombia"
    
    with MecatronicaRoboticaScraper(headless=True) as scraper:
        try:
            # Ejecutar scraping
            results = scraper.scrape_job_portals(location)
            
            # Guardar resultados
            filename = scraper.save_results(results)
            
            print(f"\n📊 RESUMEN FINAL")
            print("=" * 40)
            print(f"Total de búsquedas: {len(results)}")
            print(f"Scraping exitoso: {len([r for r in results if r.get('scrape_success', False)])}")
            print(f"Errores: {len([r for r in results if not r.get('scrape_success', False)])}")
            print(f"Resultados guardados en: {filename}")
            
        except KeyboardInterrupt:
            print("\n⏹️ Proceso interrumpido por el usuario")
        except Exception as e:
            print(f"\n💥 Error inesperado: {e}")


if __name__ == "__main__":
    main()