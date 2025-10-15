#!/usr/bin/env python3
"""
Script de prueba para la funcionalidad de cambio de idioma
del generador de folletos empresariales.

Este script demuestra cómo usar la nueva función generate_custom_brochure
con diferentes idiomas.
"""

from brochure_generator import generate_custom_brochure

def test_different_languages():
    """
    Prueba la generación de folletos en diferentes idiomas.
    """
    print("🧪 Probando la funcionalidad de cambio de idioma")
    print("=" * 50)
    
    # Configuración de la empresa de prueba
    company_name = "Frogames Formación"
    url = "https://cursos.frogamesformacion.com"
    
    # Lista de idiomas a probar
    languages_to_test = [
        "Inglés",
        "Francés", 
        "Alemán",
        "Italiano"
    ]
    
    print(f"🏢 Empresa: {company_name}")
    print(f"🌐 URL: {url}")
    print(f"🗣️ Idiomas a probar: {', '.join(languages_to_test)}")
    print("\n" + "=" * 50)
    
    # Probar cada idioma
    for language in languages_to_test:
        print(f"\n🌍 Probando idioma: {language}")
        print("-" * 30)
        
        try:
            # Generar folleto en el idioma especificado
            result, output_file = generate_custom_brochure(
                company_name=company_name,
                url=url,
                language=language
            )
            
            if result:
                print(f"✅ Folleto generado exitosamente en {language}")
                print(f"📁 Archivo: {output_file}")
            else:
                print(f"❌ Error generando folleto en {language}")
                
        except Exception as e:
            print(f"❌ Error inesperado con {language}: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Pruebas de idioma completadas!")

if __name__ == "__main__":
    test_different_languages()