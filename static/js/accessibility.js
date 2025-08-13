/**
 * DiversIA Accessibility Controls
 * Provides font size adjustment, dark mode, high contrast, and animation controls
 */

(function() {
    'use strict';
    
    // State management
    let currentSettings = {
        fontSize: 'normal',
        darkMode: false,
        highContrast: false,
        animationsEnabled: true
    };
    
    // Initialize accessibility controls when DOM is loaded
    document.addEventListener('DOMContentLoaded', function() {
        loadSettings();
        initializeControls();
        applySettings();
    });
    
    /**
     * Load settings from localStorage
     */
    function loadSettings() {
        try {
            const saved = localStorage.getItem('diversia-accessibility');
            if (saved) {
                currentSettings = { ...currentSettings, ...JSON.parse(saved) };
            }
        } catch (e) {
            console.warn('Could not load accessibility settings:', e);
        }
    }
    
    /**
     * Save settings to localStorage
     */
    function saveSettings() {
        try {
            localStorage.setItem('diversia-accessibility', JSON.stringify(currentSettings));
        } catch (e) {
            console.warn('Could not save accessibility settings:', e);
        }
    }
    
    /**
     * Initialize control buttons
     */
    function initializeControls() {
        // Font size toggle
        const fontSizeBtn = document.getElementById('font-size-toggle');
        if (fontSizeBtn) {
            fontSizeBtn.addEventListener('click', toggleFontSize);
            fontSizeBtn.setAttribute('title', 'Cambiar tamaño de texto');
        }
        
        // Dark mode toggle
        const darkModeBtn = document.getElementById('dark-mode-toggle');
        if (darkModeBtn) {
            darkModeBtn.addEventListener('click', toggleDarkMode);
            darkModeBtn.setAttribute('title', 'Activar/desactivar modo oscuro');
        }
        
        // High contrast toggle
        const contrastBtn = document.getElementById('high-contrast-toggle');
        if (contrastBtn) {
            contrastBtn.addEventListener('click', toggleHighContrast);
            contrastBtn.setAttribute('title', 'Activar/desactivar alto contraste');
        }
        
        // Animations toggle
        const animationsBtn = document.getElementById('animations-toggle');
        if (animationsBtn) {
            animationsBtn.addEventListener('click', toggleAnimations);
            animationsBtn.setAttribute('title', 'Activar/desactivar animaciones');
        }
        
        // Keyboard shortcuts
        document.addEventListener('keydown', handleKeyboardShortcuts);
        
        // Update button states
        updateButtonStates();
    }
    
    /**
     * Apply current settings to the page
     */
    function applySettings() {
        const body = document.body;
        
        // Apply font size
        body.classList.remove('large-text');
        if (currentSettings.fontSize === 'large') {
            body.classList.add('large-text');
        }
        
        // Apply dark mode
        body.classList.remove('dark-mode');
        if (currentSettings.darkMode) {
            body.classList.add('dark-mode');
        }
        
        // Apply high contrast
        body.classList.remove('high-contrast');
        if (currentSettings.highContrast) {
            body.classList.add('high-contrast');
        }
        
        // Apply animation settings
        body.classList.remove('reduce-motion');
        if (!currentSettings.animationsEnabled) {
            body.classList.add('reduce-motion');
        }
        
        updateButtonStates();
    }
    
    /**
     * Update button states based on current settings
     */
    function updateButtonStates() {
        // Font size button
        const fontSizeBtn = document.getElementById('font-size-toggle');
        if (fontSizeBtn) {
            fontSizeBtn.classList.toggle('active', currentSettings.fontSize === 'large');
            fontSizeBtn.setAttribute('aria-pressed', currentSettings.fontSize === 'large');
            
            const icon = fontSizeBtn.querySelector('i');
            if (icon) {
                icon.setAttribute('data-lucide', currentSettings.fontSize === 'large' ? 'type' : 'type');
            }
        }
        
        // Dark mode button
        const darkModeBtn = document.getElementById('dark-mode-toggle');
        if (darkModeBtn) {
            darkModeBtn.classList.toggle('active', currentSettings.darkMode);
            darkModeBtn.setAttribute('aria-pressed', currentSettings.darkMode);
            darkModeBtn.setAttribute('aria-label', currentSettings.darkMode ? 'Desactivar modo oscuro' : 'Activar modo oscuro');
            
            const icon = darkModeBtn.querySelector('i');
            if (icon) {
                icon.setAttribute('data-lucide', currentSettings.darkMode ? 'sun' : 'moon');
            }
        }
        
        // High contrast button
        const contrastBtn = document.getElementById('high-contrast-toggle');
        if (contrastBtn) {
            contrastBtn.classList.toggle('active', currentSettings.highContrast);
            contrastBtn.setAttribute('aria-pressed', currentSettings.highContrast);
            contrastBtn.setAttribute('aria-label', currentSettings.highContrast ? 'Desactivar alto contraste' : 'Activar alto contraste');
        }
        
        // Animations button
        const animationsBtn = document.getElementById('animations-toggle');
        if (animationsBtn) {
            animationsBtn.classList.toggle('active', !currentSettings.animationsEnabled);
            animationsBtn.setAttribute('aria-pressed', !currentSettings.animationsEnabled);
            animationsBtn.setAttribute('aria-label', currentSettings.animationsEnabled ? 'Desactivar animaciones' : 'Activar animaciones');
            
            const icon = animationsBtn.querySelector('i');
            if (icon) {
                icon.setAttribute('data-lucide', currentSettings.animationsEnabled ? 'pause' : 'play');
            }
        }
        
        // Refresh Lucide icons if available
        if (typeof lucide !== 'undefined' && lucide.createIcons) {
            lucide.createIcons();
        }
    }
    
    /**
     * Toggle font size between normal and large
     */
    function toggleFontSize() {
        currentSettings.fontSize = currentSettings.fontSize === 'large' ? 'normal' : 'large';
        applySettings();
        saveSettings();
        
        // Announce change to screen readers
        announceChange(`Tamaño de texto cambiado a ${currentSettings.fontSize === 'large' ? 'grande' : 'normal'}`);
    }
    
    /**
     * Toggle dark mode
     */
    function toggleDarkMode() {
        currentSettings.darkMode = !currentSettings.darkMode;
        
        // Disable high contrast when enabling dark mode
        if (currentSettings.darkMode) {
            currentSettings.highContrast = false;
        }
        
        applySettings();
        saveSettings();
        
        announceChange(`Modo oscuro ${currentSettings.darkMode ? 'activado' : 'desactivado'}`);
    }
    
    /**
     * Toggle high contrast mode
     */
    function toggleHighContrast() {
        currentSettings.highContrast = !currentSettings.highContrast;
        
        // Disable dark mode when enabling high contrast
        if (currentSettings.highContrast) {
            currentSettings.darkMode = false;
        }
        
        applySettings();
        saveSettings();
        
        announceChange(`Alto contraste ${currentSettings.highContrast ? 'activado' : 'desactivado'}`);
    }
    
    /**
     * Toggle animations
     */
    function toggleAnimations() {
        currentSettings.animationsEnabled = !currentSettings.animationsEnabled;
        applySettings();
        saveSettings();
        
        announceChange(`Animaciones ${currentSettings.animationsEnabled ? 'activadas' : 'desactivadas'}`);
    }
    
    /**
     * Handle keyboard shortcuts
     */
    function handleKeyboardShortcuts(e) {
        // Only handle if Alt + Shift is pressed
        if (!e.altKey || !e.shiftKey) return;
        
        switch (e.key) {
            case 'F':
                e.preventDefault();
                toggleFontSize();
                break;
            case 'D':
                e.preventDefault();
                toggleDarkMode();
                break;
            case 'C':
                e.preventDefault();
                toggleHighContrast();
                break;
            case 'A':
                e.preventDefault();
                toggleAnimations();
                break;
        }
    }
    
    /**
     * Announce changes to screen readers
     */
    function announceChange(message) {
        // Create or update live region
        let liveRegion = document.getElementById('accessibility-announcements');
        if (!liveRegion) {
            liveRegion = document.createElement('div');
            liveRegion.id = 'accessibility-announcements';
            liveRegion.setAttribute('aria-live', 'polite');
            liveRegion.setAttribute('aria-atomic', 'true');
            liveRegion.className = 'visually-hidden';
            document.body.appendChild(liveRegion);
        }
        
        // Clear and set new message
        liveRegion.textContent = '';
        setTimeout(() => {
            liveRegion.textContent = message;
        }, 100);
    }
    
    /**
     * Detect user's preferred settings on first visit
     */
    function detectPreferences() {
        // Check for first visit
        if (!localStorage.getItem('diversia-accessibility')) {
            // Check for prefers-reduced-motion
            if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
                currentSettings.animationsEnabled = false;
            }
            
            // Check for prefers-color-scheme
            if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
                currentSettings.darkMode = true;
            }
            
            // Check for prefers-contrast
            if (window.matchMedia('(prefers-contrast: high)').matches) {
                currentSettings.highContrast = true;
                currentSettings.darkMode = false; // High contrast takes precedence
            }
            
            applySettings();
            saveSettings();
        }
    }
    
    // Detect preferences on load
    window.addEventListener('load', detectPreferences);
    
    // Listen for system preference changes
    if (window.matchMedia) {
        const reducedMotionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
        reducedMotionQuery.addEventListener('change', function(e) {
            if (!localStorage.getItem('diversia-accessibility-motion-manual')) {
                currentSettings.animationsEnabled = !e.matches;
                applySettings();
                saveSettings();
            }
        });
        
        const darkModeQuery = window.matchMedia('(prefers-color-scheme: dark)');
        darkModeQuery.addEventListener('change', function(e) {
            if (!localStorage.getItem('diversia-accessibility-theme-manual')) {
                currentSettings.darkMode = e.matches;
                currentSettings.highContrast = false;
                applySettings();
                saveSettings();
            }
        });
    }
    
    /**
     * Reset all accessibility settings
     */
    function resetSettings() {
        currentSettings = {
            fontSize: 'normal',
            darkMode: false,
            highContrast: false,
            animationsEnabled: true
        };
        applySettings();
        saveSettings();
        announceChange('Configuración de accesibilidad restaurada');
    }
    
    // Expose reset function globally for potential use
    window.DiversiaAccessibility = {
        reset: resetSettings,
        getSettings: () => ({ ...currentSettings }),
        applySettings: applySettings
    };
    
    // Add helpful keyboard shortcuts information
    const keyboardHelp = `
    Atajos de teclado de accesibilidad:
    - Alt + Shift + F: Cambiar tamaño de texto
    - Alt + Shift + D: Modo oscuro
    - Alt + Shift + C: Alto contraste
    - Alt + Shift + A: Animaciones
    `;
    
    // Add keyboard help to page (hidden by default)
    document.addEventListener('DOMContentLoaded', function() {
        const helpElement = document.createElement('div');
        helpElement.id = 'keyboard-shortcuts-help';
        helpElement.className = 'visually-hidden';
        helpElement.textContent = keyboardHelp;
        document.body.appendChild(helpElement);
    });
    
})();
