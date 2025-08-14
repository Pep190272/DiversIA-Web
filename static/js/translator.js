// Advanced Translation System for DiversIA
let googleTranslateInstance = null;
let isTranslateReady = false;

// Initialize Google Translate with multiple fallback strategies
function googleTranslateElementInit() {
    console.log('Initializing Google Translate...');
    
    // Create hidden element for Google Translate
    let translateDiv = document.getElementById('google_translate_element');
    if (!translateDiv) {
        translateDiv = document.createElement('div');
        translateDiv.id = 'google_translate_element';
        translateDiv.style.display = 'none';
        translateDiv.style.position = 'absolute';
        translateDiv.style.top = '-9999px';
        document.body.appendChild(translateDiv);
    }

    // Initialize with retry mechanism
    let initAttempts = 0;
    const maxInitAttempts = 5;
    
    function attemptInit() {
        try {
            if (typeof google !== 'undefined' && google.translate && google.translate.TranslateElement) {
                googleTranslateInstance = new google.translate.TranslateElement({
                    pageLanguage: 'es',
                    includedLanguages: 'en,fr,de,it,pt,ar,zh,ja,es',
                    layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
                    autoDisplay: false,
                    multilanguagePage: true
                }, 'google_translate_element');
                
                isTranslateReady = true;
                console.log('Google Translate initialized successfully');
                
                // Hide Google Translate toolbar
                setTimeout(hideGoogleTranslateElements, 1000);
                
            } else {
                throw new Error('Google Translate not available');
            }
        } catch (error) {
            initAttempts++;
            console.warn(`Google Translate init attempt ${initAttempts} failed:`, error);
            
            if (initAttempts < maxInitAttempts) {
                setTimeout(attemptInit, 1000);
            } else {
                console.error('Google Translate failed to initialize after all attempts');
                // Fallback to basic translation system
                initializeFallbackTranslation();
            }
        }
    }
    
    attemptInit();
}

// Hide Google Translate UI elements
function hideGoogleTranslateElements() {
    const style = document.createElement('style');
    style.textContent = `
        .goog-te-banner-frame.skiptranslate,
        .goog-te-gadget-simple .goog-te-menu-value span:first-child,
        #google_translate_element .goog-te-gadget-simple .goog-te-menu-value span:first-child {
            display: none !important;
        }
        body {
            top: 0px !important;
        }
        #google_translate_element {
            display: none !important;
        }
        .goog-text-highlight {
            background-color: transparent !important;
            box-shadow: none !important;
        }
    `;
    document.head.appendChild(style);
}

// Load Google Translate script dynamically
function loadGoogleTranslate() {
    return new Promise((resolve, reject) => {
        if (typeof google !== 'undefined' && google.translate) {
            resolve();
            return;
        }
        
        const script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = 'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
        script.onerror = () => reject(new Error('Failed to load Google Translate'));
        script.onload = () => resolve();
        
        document.head.appendChild(script);
    });
}

// Main translation function
function translateTo(languageCode) {
    console.log('Translate to:', languageCode);
    
    if (languageCode === 'es') {
        resetTranslation();
        return;
    }

    // Show loading indicator
    updateLanguageIndicator(languageCode, true);
    
    // Wait for Google Translate to be ready
    let attempts = 0;
    const maxAttempts = 20;
    
    function attemptTranslation() {
        attempts++;
        
        if (!isTranslateReady) {
            if (attempts < maxAttempts) {
                setTimeout(attemptTranslation, 500);
                return;
            } else {
                console.error('Google Translate not ready after waiting');
                showTranslationError();
                return;
            }
        }

        // Find Google Translate select element
        const selectElement = document.querySelector('.goog-te-combo');
        if (selectElement) {
            try {
                selectElement.value = languageCode;
                
                // Trigger change event
                const changeEvent = new Event('change', { bubbles: true });
                selectElement.dispatchEvent(changeEvent);
                
                // Store preference
                localStorage.setItem('diversia_language', languageCode);
                
                // Update indicator
                setTimeout(() => updateLanguageIndicator(languageCode, false), 1000);
                
                console.log('Translation to', languageCode, 'successful');
                
            } catch (error) {
                console.error('Error during translation:', error);
                showTranslationError();
            }
        } else {
            if (attempts < maxAttempts) {
                setTimeout(attemptTranslation, 300);
            } else {
                console.error('Translation select not found');
                showTranslationError();
            }
        }
    }
    
    attemptTranslation();
}

// Show translation error
function showTranslationError() {
    const toast = document.createElement('div');
    toast.className = 'alert alert-warning position-fixed';
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; max-width: 300px;';
    toast.innerHTML = `
        <strong>Error de traducción</strong><br>
        El servicio de traducción no está disponible temporalmente.
        <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
    `;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        if (toast.parentElement) {
            toast.remove();
        }
    }, 5000);
}

function resetTranslation() {
    // Remove any existing translation
    const selectElement = document.querySelector('.goog-te-combo');
    if (selectElement) {
        selectElement.value = '';
        selectElement.dispatchEvent(new Event('change'));
    }
    
    // Clear stored preference
    localStorage.removeItem('diversia_language');
    
    // Update language indicator
    updateLanguageIndicator('es');
}

function updateLanguageIndicator(languageCode, isLoading = false) {
    const languageNames = {
        'es': 'Español',
        'en': 'English',
        'fr': 'Français',
        'de': 'Deutsch',
        'it': 'Italiano',
        'pt': 'Português',
        'ar': 'العربية',
        'zh': '中文',
        'ja': '日本語'
    };
    
    const flags = {
        'es': '🇪🇸',
        'en': '🇺🇸',
        'fr': '🇫🇷',
        'de': '🇩🇪',
        'it': '🇮🇹',
        'pt': '🇵🇹',
        'ar': '🇸🇦',
        'zh': '🇨🇳',
        'ja': '🇯🇵'
    };
    
    const dropdownToggle = document.getElementById('languageDropdown');
    if (dropdownToggle) {
        const icon = isLoading ? 
            '<i data-lucide="loader-2" class="animate-spin"></i>' : 
            '<i data-lucide="globe"></i>';
        
        const text = isLoading ? 'Traduciendo...' : 
            `${flags[languageCode] || '🌐'} ${languageNames[languageCode] || 'Idioma'}`;
        
        dropdownToggle.innerHTML = `${icon} ${text}`;
        
        // Reinitialize lucide icons
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }
}

// Fallback translation system using browser API
function initializeFallbackTranslation() {
    console.log('Initializing fallback translation system');
    
    // Simple client-side translation using browser APIs
    window.translateText = async function(text, targetLang) {
        try {
            // This is a simplified fallback - in production you might want to use a translation API
            return text; // Return original text as fallback
        } catch (error) {
            console.error('Fallback translation failed:', error);
            return text;
        }
    };
}

// Initialize translation system when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing translation system');
    
    // Load Google Translate
    loadGoogleTranslate()
        .then(() => {
            console.log('Google Translate script loaded successfully');
        })
        .catch((error) => {
            console.error('Failed to load Google Translate:', error);
            initializeFallbackTranslation();
        });
    
    // Auto-restore language preference
    const savedLanguage = localStorage.getItem('diversia_language');
    if (savedLanguage && savedLanguage !== 'es') {
        setTimeout(() => {
            translateTo(savedLanguage);
        }, 2000);
    }
});

// Auto-restore language preference on page load
document.addEventListener('DOMContentLoaded', function() {
    const savedLanguage = localStorage.getItem('diversia_language');
    if (savedLanguage && savedLanguage !== 'es') {
        // Wait a bit for Google Translate to initialize
        setTimeout(() => {
            translateTo(savedLanguage);
        }, 1000);
    }
});

// Hide Google Translate bar and customize appearance
function hideGoogleTranslateBar() {
    const style = document.createElement('style');
    style.textContent = `
        .goog-te-banner-frame.skiptranslate {
            display: none !important;
        }
        body {
            top: 0px !important;
        }
        #google_translate_element {
            display: none !important;
        }
        .goog-te-combo {
            display: none !important;
        }
        /* Custom styles for better integration */
        .goog-text-highlight {
            background-color: transparent !important;
            box-shadow: none !important;
        }
        .goog-text-highlight:hover {
            background-color: rgba(255, 193, 7, 0.2) !important;
        }
    `;
    document.head.appendChild(style);
}

// Apply custom styles when DOM is ready
document.addEventListener('DOMContentLoaded', hideGoogleTranslateBar);

// Also apply styles after a delay to catch dynamically loaded content
setTimeout(hideGoogleTranslateBar, 1000);