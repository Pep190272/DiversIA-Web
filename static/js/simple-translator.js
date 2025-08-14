// Simple and Reliable Translation System for DiversIA
(function() {
    'use strict';
    
    let isGoogleTranslateLoaded = false;
    let currentLanguage = 'es';
    
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
    
    // Initialize Google Translate
    window.googleTranslateElementInit = function() {
        try {
            new google.translate.TranslateElement({
                pageLanguage: 'es',
                includedLanguages: 'en,fr,de,it,pt,ar,zh,ja,es',
                layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
                autoDisplay: false
            }, 'google_translate_element');
            
            isGoogleTranslateLoaded = true;
            console.log('✅ Google Translate loaded successfully');
            
            // Hide Google UI
            setTimeout(hideGoogleUI, 500);
            
        } catch (error) {
            console.error('❌ Google Translate initialization failed:', error);
        }
    };
    
    // Hide Google Translate UI
    function hideGoogleUI() {
        const style = document.createElement('style');
        style.innerHTML = `
            .goog-te-banner-frame.skiptranslate { display: none !important; }
            body { top: 0px !important; }
            #google_translate_element { display: none !important; }
            .goog-text-highlight { background: none !important; box-shadow: none !important; }
        `;
        document.head.appendChild(style);
    }
    
    // Main translate function
    window.translateTo = function(langCode) {
        console.log('🌐 Translating to:', langCode);
        
        if (langCode === 'es') {
            resetTranslation();
            return;
        }
        
        updateLanguageButton(langCode, true);
        
        // Wait for Google Translate and trigger translation
        let attempts = 0;
        const maxAttempts = 30;
        
        function doTranslate() {
            if (!isGoogleTranslateLoaded) {
                attempts++;
                if (attempts < maxAttempts) {
                    setTimeout(doTranslate, 200);
                    return;
                }
                showError('El traductor no pudo cargar');
                updateLanguageButton('es', false);
                return;
            }
            
            const select = document.querySelector('.goog-te-combo');
            if (select) {
                select.value = langCode;
                select.dispatchEvent(new Event('change'));
                
                currentLanguage = langCode;
                localStorage.setItem('diversia_language', langCode);
                
                setTimeout(() => updateLanguageButton(langCode, false), 1000);
                console.log('✅ Translation completed');
            } else {
                attempts++;
                if (attempts < maxAttempts) {
                    setTimeout(doTranslate, 200);
                } else {
                    showError('Error al activar la traducción');
                    updateLanguageButton('es', false);
                }
            }
        }
        
        doTranslate();
    };
    
    // Reset translation
    window.resetTranslation = function() {
        const select = document.querySelector('.goog-te-combo');
        if (select) {
            select.value = '';
            select.dispatchEvent(new Event('change'));
        }
        
        currentLanguage = 'es';
        localStorage.removeItem('diversia_language');
        updateLanguageButton('es', false);
        console.log('🔄 Translation reset to Spanish');
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
    
    // Show error message
    function showError(message) {
        const alert = document.createElement('div');
        alert.className = 'alert alert-warning position-fixed';
        alert.style.cssText = 'top: 80px; right: 20px; z-index: 9999; max-width: 300px;';
        alert.innerHTML = `
            <strong>⚠️ Error de traducción</strong><br>
            ${message}
            <button type="button" class="btn-close ms-2" onclick="this.parentElement.remove()"></button>
        `;
        document.body.appendChild(alert);
        
        setTimeout(() => alert.remove(), 4000);
    }
    
    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        console.log('🚀 Initializing translation system...');
        
        // Load Google Translate script
        const script = document.createElement('script');
        script.src = 'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
        script.async = true;
        script.onerror = function() {
            console.error('❌ Failed to load Google Translate script');
            showError('No se pudo cargar el servicio de traducción');
        };
        document.head.appendChild(script);
        
        // Restore saved language
        const savedLang = localStorage.getItem('diversia_language');
        if (savedLang && savedLang !== 'es') {
            setTimeout(() => {
                console.log('🔄 Restoring saved language:', savedLang);
                translateTo(savedLang);
            }, 3000);
        }
    });
    
})();