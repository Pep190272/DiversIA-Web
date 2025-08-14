// Google Translate Integration for DiversIA
let googleTranslateInstance = null;

// This function is called automatically by Google Translate
function googleTranslateElementInit() {
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeTranslate);
    } else {
        initializeTranslate();
    }
}

function initializeTranslate() {
    // Create hidden element for Google Translate if it doesn't exist
    let translateDiv = document.getElementById('google_translate_element');
    if (!translateDiv) {
        translateDiv = document.createElement('div');
        translateDiv.id = 'google_translate_element';
        translateDiv.style.display = 'none';
        document.body.appendChild(translateDiv);
    }

    // Initialize Google Translate
    try {
        googleTranslateInstance = new google.translate.TranslateElement({
            pageLanguage: 'es',
            includedLanguages: 'en,fr,de,it,pt,ar,zh,ja,es',
            layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
            autoDisplay: false
        }, 'google_translate_element');
        
        console.log('Google Translate initialized successfully');
    } catch (error) {
        console.error('Error initializing Google Translate:', error);
    }
}

function translateTo(languageCode) {
    if (languageCode === 'es') {
        resetTranslation();
        return;
    }

    // Wait for Google Translate to be ready with retries
    let retryCount = 0;
    const maxRetries = 10;
    
    function attemptTranslation() {
        if (typeof google === 'undefined' || !google.translate) {
            retryCount++;
            if (retryCount < maxRetries) {
                setTimeout(attemptTranslation, 500);
            } else {
                console.error('Google Translate failed to load after multiple attempts');
            }
            return;
        }

        // Find and trigger the Google Translate select
        const selectElement = document.querySelector('.goog-te-combo');
        if (selectElement) {
            selectElement.value = languageCode;
            selectElement.dispatchEvent(new Event('change'));
            
            // Store current language preference
            localStorage.setItem('diversia_language', languageCode);
            
            // Update language indicator
            updateLanguageIndicator(languageCode);
            console.log('Translation to', languageCode, 'initiated');
        } else {
            retryCount++;
            if (retryCount < maxRetries) {
                setTimeout(attemptTranslation, 500);
            } else {
                console.error('Google Translate select element not found after multiple attempts');
            }
        }
    }
    
    attemptTranslation();
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

function updateLanguageIndicator(languageCode) {
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
        const icon = dropdownToggle.querySelector('i[data-lucide="globe"]');
        const text = `${flags[languageCode] || '🌐'} ${languageNames[languageCode] || 'Idioma'}`;
        dropdownToggle.innerHTML = `${icon ? icon.outerHTML : '<i data-lucide="globe"></i>'} ${text}`;
        
        // Reinitialize lucide icons if necessary
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }
}

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