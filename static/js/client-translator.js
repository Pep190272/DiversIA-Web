// Client-Side Translation System for DiversIA
(function() {
    'use strict';
    
    let currentLanguage = 'es';
    
    // Translation dictionaries for key interface elements
    const translations = {
        'en': {
            // Navigation
            'Inicio': 'Home',
            'Personas ND': 'ND People',
            'Empresas': 'Companies',
            'Comunidad': 'Community',
            'Asociaciones': 'Associations',
            'Nosotros': 'About Us',
            'Idioma': 'Language',
            
            // Main content
            'Talento que piensa distinto': 'Talent that thinks differently',
            'Conectando talento neurodivergente con oportunidades laborales inclusivas': 'Connecting neurodivergent talent with inclusive job opportunities',
            'Regístrate como persona neurodivergente': 'Register as a neurodivergent person',
            'Regístrate como empresa inclusiva': 'Register as an inclusive company',
            'Únete a nuestra comunidad': 'Join our community',
            'Explora asociaciones': 'Explore associations',
            
            // Footer
            'Contacto': 'Contact',
            'Enlaces': 'Links',
            'Síguenos': 'Follow Us',
            'Política de Privacidad': 'Privacy Policy',
            'Aviso Legal': 'Legal Notice',
            'Términos y Condiciones': 'Terms and Conditions',
            'Sobre Nosotros': 'About Us',
            'Todos los derechos reservados': 'All rights reserved',
            'Construido con accesibilidad en mente': 'Built with accessibility in mind',
            
            // Main content expanded
            'Más información': 'More information',
            'Tests especializados': 'Specialized tests',
            'Evaluaciones gratuitas': 'Free evaluations',
            'Registro especializado': 'Specialized registration',
            'Gamificación': 'Gamification',
            'Perfil personalizado': 'Personalized profile',
            'Encuentra tu trabajo ideal': 'Find your ideal job',
            'Conecta con empresas inclusivas': 'Connect with inclusive companies',
            
            // Accessibility
            'Accesibilidad': 'Accessibility',
            'Cambiar tamaño de texto': 'Change text size',
            'Activar modo oscuro': 'Enable dark mode',
            'Activar alto contraste': 'Enable high contrast',
            'Desactivar animaciones': 'Disable animations',
            
            // TDAH section
            'TDAH': 'ADHD',
            'Trastorno por Déficit de Atención e Hiperactividad': 'Attention Deficit Hyperactivity Disorder',
            
            // TEA section
            'TEA': 'ASD',
            'Trastorno del Espectro Autista': 'Autism Spectrum Disorder',
            
            // Dislexia section
            'Dislexia': 'Dyslexia',
            'Dificultades Específicas de Aprendizaje': 'Specific Learning Difficulties'
        },
        
        'fr': {
            // Navigation
            'Inicio': 'Accueil',
            'Personas ND': 'Personnes ND',
            'Empresas': 'Entreprises',
            'Comunidad': 'Communauté',
            'Asociaciones': 'Associations',
            'Nosotros': 'À propos',
            'Idioma': 'Langue',
            
            // Main content
            'Talento que piensa distinto': 'Des talents qui pensent différemment',
            'Conectando talento neurodivergente con oportunidades laborales inclusivas': 'Connecter les talents neurodivergents avec des opportunités d\'emploi inclusives',
            'Regístrate como persona neurodivergente': 'S\'inscrire comme personne neurodivergente',
            'Regístrate como empresa inclusiva': 'S\'inscrire comme entreprise inclusive',
            'Únete a nuestra comunidad': 'Rejoindre notre communauté',
            'Explora asociaciones': 'Explorer les associations',
            
            // Footer
            'Contacto': 'Contact',
            'Enlaces': 'Liens',
            'Síguenos': 'Suivez-nous',
            'Política de Privacidad': 'Politique de confidentialité',
            'Aviso Legal': 'Mentions légales',
            'Términos y Condiciones': 'Conditions générales',
            'Sobre Nosotros': 'À propos de nous',
            'Todos los derechos reservados': 'Tous droits réservés',
            'Construido con accesibilidad en mente': 'Conçu avec l\'accessibilité à l\'esprit',
            
            // Conditions
            'TDAH': 'TDAH',
            'TEA': 'TSA',
            'Dislexia': 'Dyslexie'
        },
        
        'de': {
            // Navigation
            'Inicio': 'Startseite',
            'Personas ND': 'ND-Personen',
            'Empresas': 'Unternehmen',
            'Comunidad': 'Gemeinschaft',
            'Asociaciones': 'Verbände',
            'Nosotros': 'Über uns',
            'Idioma': 'Sprache',
            
            // Main content
            'Talento que piensa distinto': 'Talente, die anders denken',
            'Conectando talento neurodivergente con oportunidades laborales inclusivas': 'Neurodivergente Talente mit inklusiven Arbeitsmöglichkeiten verbinden',
            'Regístrate como persona neurodivergente': 'Als neurodivergente Person registrieren',
            'Regístrate como empresa inclusiva': 'Als inklusives Unternehmen registrieren',
            'Únete a nuestra comunidad': 'Unserer Gemeinschaft beitreten',
            'Explora asociaciones': 'Verbände erkunden',
            
            // Footer
            'Contacto': 'Kontakt',
            'Enlaces': 'Links',
            'Síguenos': 'Folgen Sie uns',
            'Todos los derechos reservados': 'Alle Rechte vorbehalten',
            'Construido con accesibilidad en mente': 'Mit Barrierefreiheit im Sinn entwickelt',
            
            // Conditions
            'TDAH': 'ADHS',
            'TEA': 'ASS',
            'Dislexia': 'Dyslexie'
        },
        
        'it': {
            // Navigation
            'Inicio': 'Home',
            'Personas ND': 'Persone ND',
            'Empresas': 'Aziende',
            'Comunidad': 'Comunità',
            'Asociaciones': 'Associazioni',
            'Nosotros': 'Chi siamo',
            'Idioma': 'Lingua',
            
            // Main content
            'Talento que piensa distinto': 'Talenti che pensano diversamente',
            'Conectando talento neurodivergente con oportunidades laborales inclusivas': 'Connettere talenti neurodivergenti con opportunità lavorative inclusive',
            'Regístrate como persona neurodivergente': 'Registrati come persona neurodivergente',
            'Regístrate como empresa inclusiva': 'Registrati come azienda inclusiva',
            'Únete a nuestra comunidad': 'Unisciti alla nostra comunità',
            'Explora asociaciones': 'Esplora associazioni',
            
            // Footer
            'Contacto': 'Contatto',
            'Enlaces': 'Collegamenti',
            'Síguenos': 'Seguici',
            'Todos los derechos reservados': 'Tutti i diritti riservati',
            'Construido con accesibilidad en mente': 'Costruito con l\'accessibilità in mente',
            
            // Conditions
            'TDAH': 'ADHD',
            'TEA': 'TSA',
            'Dislexia': 'Dislessia'
        },
        
        'pt': {
            // Navigation
            'Inicio': 'Início',
            'Personas ND': 'Pessoas ND',
            'Empresas': 'Empresas',
            'Comunidad': 'Comunidade',
            'Asociaciones': 'Associações',
            'Nosotros': 'Sobre nós',
            'Idioma': 'Idioma',
            
            // Main content
            'Talento que piensa distinto': 'Talentos que pensam diferente',
            'Conectando talento neurodivergente con oportunidades laborales inclusivas': 'Conectando talentos neurodivergentes com oportunidades de trabalho inclusivas',
            'Regístrate como persona neurodivergente': 'Registre-se como pessoa neurodivergente',
            'Regístrate como empresa inclusiva': 'Registre-se como empresa inclusiva',
            'Únete a nuestra comunidad': 'Junte-se à nossa comunidade',
            'Explora asociaciones': 'Explore associações',
            
            // Footer
            'Contacto': 'Contato',
            'Enlaces': 'Links',
            'Síguenos': 'Siga-nos',
            'Todos los derechos reservados': 'Todos os direitos reservados',
            'Construido con accesibilidad en mente': 'Construído com acessibilidade em mente',
            
            // Conditions
            'TDAH': 'TDAH',
            'TEA': 'TEA',
            'Dislexia': 'Dislexia'
        }
    };
    
    // Language configuration
    const languages = {
        'es': { name: 'Español', flag: '🇪🇸' },
        'en': { name: 'English', flag: '🇺🇸' },
        'fr': { name: 'Français', flag: '🇫🇷' },
        'de': { name: 'Deutsch', flag: '🇩🇪' },
        'it': { name: 'Italiano', flag: '🇮🇹' },
        'pt': { name: 'Português', flag: '🇵🇹' },
        'ar': { name: 'العربية', flag: '🇸🇦' },
        'zh': { name: '中文', flag: '🇨🇳' },
        'ja': { name: '日本語', flag: '🇯🇵' }
    };
    
    // Main translate function
    window.translateTo = function(langCode) {
        console.log('Translating to:', langCode);
        
        if (langCode === 'es') {
            resetTranslation();
            return;
        }
        
        updateLanguageButton(langCode, true);
        
        // Apply translations
        setTimeout(() => {
            try {
                applyTranslations(langCode);
                currentLanguage = langCode;
                localStorage.setItem('diversia_language', langCode);
                updateLanguageButton(langCode, false);
                showSuccessMessage(languages[langCode].name);
            } catch (error) {
                console.error('Translation error:', error);
                showErrorMessage();
                updateLanguageButton('es', false);
            }
        }, 500);
    };
    
    // Apply translations to page elements
    function applyTranslations(langCode) {
        const dictionary = translations[langCode];
        if (!dictionary) return;
        
        // Translate all text content recursively
        function translateElement(element) {
            // Skip script, style, and chat widget elements
            if (element.tagName === 'SCRIPT' || 
                element.tagName === 'STYLE' || 
                element.id === 'diversia-chat-widget') {
                return;
            }
            
            // Translate direct text content
            if (element.childNodes) {
                element.childNodes.forEach(node => {
                    if (node.nodeType === Node.TEXT_NODE) {
                        const text = node.textContent.trim();
                        if (text && dictionary[text]) {
                            node.textContent = node.textContent.replace(text, dictionary[text]);
                        } else {
                            // Try partial matches for longer texts
                            let translatedText = node.textContent;
                            Object.keys(dictionary).forEach(key => {
                                if (translatedText.includes(key)) {
                                    translatedText = translatedText.replace(key, dictionary[key]);
                                }
                            });
                            if (translatedText !== node.textContent) {
                                node.textContent = translatedText;
                            }
                        }
                    } else if (node.nodeType === Node.ELEMENT_NODE) {
                        translateElement(node);
                    }
                });
            }
        }
        
        // Start translation from body
        translateElement(document.body);
        
        // Translate specific attributes
        document.querySelectorAll('[aria-label]').forEach(element => {
            const originalLabel = element.getAttribute('aria-label');
            if (dictionary[originalLabel]) {
                element.setAttribute('aria-label', dictionary[originalLabel]);
            }
        });
        
        document.querySelectorAll('[title]').forEach(element => {
            const originalTitle = element.getAttribute('title');
            if (dictionary[originalTitle]) {
                element.setAttribute('title', dictionary[originalTitle]);
            }
        });
        
        document.querySelectorAll('[placeholder]').forEach(element => {
            const originalPlaceholder = element.getAttribute('placeholder');
            if (dictionary[originalPlaceholder]) {
                element.setAttribute('placeholder', dictionary[originalPlaceholder]);
            }
        });
    }
    
    // Reset translation
    window.resetTranslation = function() {
        currentLanguage = 'es';
        localStorage.removeItem('diversia_language');
        updateLanguageButton('es', false);
        // Reload page to restore original Spanish text
        window.location.reload();
    };
    
    // Update language button
    function updateLanguageButton(langCode, loading) {
        const button = document.getElementById('languageDropdown');
        if (!button) return;
        
        if (loading) {
            button.innerHTML = '<i data-lucide="loader-2"></i> Traduciendo...';
        } else {
            const lang = languages[langCode] || languages['es'];
            button.innerHTML = `<i data-lucide="globe"></i> ${lang.flag} ${lang.name}`;
        }
        
        // Reinitialize icons
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }
    
    // Show success message
    function showSuccessMessage(languageName) {
        const alert = document.createElement('div');
        alert.className = 'alert alert-success position-fixed';
        alert.style.cssText = 'top: 80px; right: 20px; z-index: 9999; max-width: 300px;';
        alert.innerHTML = `
            <strong>Traducción exitosa</strong><br>
            Página traducida a ${languageName}
            <button type="button" class="btn-close ms-2" onclick="this.parentElement.remove()"></button>
        `;
        document.body.appendChild(alert);
        
        setTimeout(() => alert.remove(), 3000);
    }
    
    // Show error message
    function showErrorMessage() {
        const alert = document.createElement('div');
        alert.className = 'alert alert-warning position-fixed';
        alert.style.cssText = 'top: 80px; right: 20px; z-index: 9999; max-width: 300px;';
        alert.innerHTML = `
            <strong>Error de traducción</strong><br>
            No se pudo completar la traducción
            <button type="button" class="btn-close ms-2" onclick="this.parentElement.remove()"></button>
        `;
        document.body.appendChild(alert);
        
        setTimeout(() => alert.remove(), 4000);
    }
    
    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Client translation system initialized');
        
        // Restore saved language
        const savedLang = localStorage.getItem('diversia_language');
        if (savedLang && savedLang !== 'es' && translations[savedLang]) {
            setTimeout(() => {
                translateTo(savedLang);
            }, 1000);
        }
    });
    
})();