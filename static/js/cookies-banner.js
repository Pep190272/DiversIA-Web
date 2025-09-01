// Cookie Consent Banner - RGPD Compliant
class CookieBanner {
    constructor() {
        this.cookieName = 'diversia_cookie_consent';
        this.cookieExpiry = 365; // días
        this.init();
    }

    init() {
        // Esperar un poco antes de verificar consentimiento para evitar parpadeo
        setTimeout(() => {
            // Solo mostrar banner si no hay consentimiento previo
            if (!this.hasConsent()) {
                this.showBanner();
            } else {
                // Cargar scripts según consentimiento guardado
                const consent = this.getConsent();
                this.loadScripts(consent);
            }
        }, 500); // Esperar 500ms
    }

    hasConsent() {
        return localStorage.getItem(this.cookieName) !== null;
    }

    getConsent() {
        const consent = localStorage.getItem(this.cookieName);
        return consent ? JSON.parse(consent) : null;
    }

    saveConsent(preferences) {
        const consentData = {
            necessary: true, // siempre true
            analytics: preferences.analytics || false,
            marketing: preferences.marketing || false,
            functional: preferences.functional || false,
            timestamp: new Date().toISOString(),
            version: '1.0'
        };
        
        localStorage.setItem(this.cookieName, JSON.stringify(consentData));
        
        // También guardar en cookie para el servidor
        const expires = new Date();
        expires.setTime(expires.getTime() + (this.cookieExpiry * 24 * 60 * 60 * 1000));
        document.cookie = `${this.cookieName}=${JSON.stringify(consentData)}; expires=${expires.toUTCString()}; path=/; SameSite=Lax`;
        
        this.loadScripts(consentData);
    }

    showBanner() {
        const banner = document.createElement('div');
        banner.id = 'cookie-banner';
        banner.className = 'cookie-banner';
        banner.innerHTML = `
            <div class="cookie-banner-content">
                <div class="cookie-banner-text">
                    <h4>🍪 Gestión de Cookies</h4>
                    <p>
                        Utilizamos cookies necesarias para el funcionamiento del sitio y opcionales para análisis y mejora. 
                        Puedes aceptar todas o gestionar tus preferencias.
                    </p>
                </div>
                <div class="cookie-banner-actions">
                    <button id="cookie-accept-all" class="btn btn-primary">
                        Aceptar todas
                    </button>
                    <button id="cookie-reject-all" class="btn btn-outline-secondary">
                        Solo necesarias
                    </button>
                    <button id="cookie-settings" class="btn btn-outline-primary">
                        Configurar
                    </button>
                </div>
                <div class="cookie-banner-links">
                    <a href="/politica-cookies" target="_blank" class="text-muted small">Política de Cookies</a> | 
                    <a href="/politica-privacidad" target="_blank" class="text-muted small">Privacidad</a>
                </div>
            </div>
        `;

        // Estilos CSS
        const style = document.createElement('style');
        style.textContent = `
            .cookie-banner {
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                background: #fff;
                border-top: 3px solid #0d6efd;
                box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
                z-index: 10000;
                padding: 20px;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }
            .cookie-banner-content {
                max-width: 1200px;
                margin: 0 auto;
            }
            .cookie-banner-text h4 {
                margin: 0 0 10px 0;
                color: #333;
                font-size: 18px;
            }
            .cookie-banner-text p {
                margin: 0 0 15px 0;
                color: #666;
                line-height: 1.5;
            }
            .cookie-banner-actions {
                display: flex;
                gap: 10px;
                margin-bottom: 10px;
                flex-wrap: wrap;
            }
            .cookie-banner-actions button {
                padding: 10px 20px;
                border: 1px solid #ddd;
                border-radius: 5px;
                cursor: pointer;
                font-size: 14px;
                transition: all 0.3s;
            }
            .cookie-banner-actions .btn-primary {
                background: #0d6efd;
                color: white;
                border-color: #0d6efd;
            }
            .cookie-banner-actions .btn-primary:hover {
                background: #0b5ed7;
            }
            .cookie-banner-actions .btn-outline-primary {
                background: transparent;
                color: #0d6efd;
                border-color: #0d6efd;
            }
            .cookie-banner-actions .btn-outline-primary:hover {
                background: #0d6efd;
                color: white;
            }
            .cookie-banner-actions .btn-outline-secondary {
                background: transparent;
                color: #6c757d;
                border-color: #6c757d;
            }
            .cookie-banner-actions .btn-outline-secondary:hover {
                background: #6c757d;
                color: white;
            }
            .cookie-banner-links {
                font-size: 12px;
            }
            .cookie-banner-links a {
                color: #6c757d;
                text-decoration: none;
            }
            .cookie-banner-links a:hover {
                text-decoration: underline;
            }
            @media (max-width: 768px) {
                .cookie-banner {
                    padding: 15px;
                }
                .cookie-banner-actions {
                    flex-direction: column;
                }
                .cookie-banner-actions button {
                    width: 100%;
                }
            }
        `;
        
        document.head.appendChild(style);
        document.body.appendChild(banner);

        // Event listeners
        document.getElementById('cookie-accept-all').addEventListener('click', () => {
            this.acceptAll();
        });

        document.getElementById('cookie-reject-all').addEventListener('click', () => {
            this.rejectAll();
        });

        document.getElementById('cookie-settings').addEventListener('click', () => {
            this.showSettings();
        });
    }

    acceptAll() {
        this.saveConsent({
            analytics: true,
            marketing: true,
            functional: true
        });
        this.hideBanner();
    }

    rejectAll() {
        this.saveConsent({
            analytics: false,
            marketing: false,
            functional: false
        });
        this.hideBanner();
    }

    showSettings() {
        const modal = document.createElement('div');
        modal.id = 'cookie-settings-modal';
        modal.className = 'cookie-modal';
        modal.innerHTML = `
            <div class="cookie-modal-backdrop" onclick="document.getElementById('cookie-settings-modal').remove()"></div>
            <div class="cookie-modal-content">
                <div class="cookie-modal-header">
                    <h3>Configuración de Cookies</h3>
                    <button onclick="document.getElementById('cookie-settings-modal').remove()" class="cookie-modal-close">&times;</button>
                </div>
                <div class="cookie-modal-body">
                    <div class="cookie-category">
                        <div class="cookie-category-header">
                            <input type="checkbox" id="necessary" checked disabled>
                            <label for="necessary"><strong>Cookies Necesarias</strong></label>
                        </div>
                        <p class="cookie-category-description">
                            Estas cookies son esenciales para el funcionamiento del sitio web y no se pueden desactivar.
                        </p>
                    </div>
                    
                    <div class="cookie-category">
                        <div class="cookie-category-header">
                            <input type="checkbox" id="analytics">
                            <label for="analytics"><strong>Cookies de Análisis</strong></label>
                        </div>
                        <p class="cookie-category-description">
                            Nos ayudan a entender cómo los visitantes interactúan con nuestro sitio web mediante la recopilación y el informe de información de forma anónima.
                        </p>
                    </div>
                    
                    <div class="cookie-category">
                        <div class="cookie-category-header">
                            <input type="checkbox" id="functional">
                            <label for="functional"><strong>Cookies Funcionales</strong></label>
                        </div>
                        <p class="cookie-category-description">
                            Estas cookies permiten que el sitio web proporcione una funcionalidad y personalización mejoradas, como recordar tus preferencias.
                        </p>
                    </div>
                    
                    <div class="cookie-category">
                        <div class="cookie-category-header">
                            <input type="checkbox" id="marketing">
                            <label for="marketing"><strong>Cookies de Marketing</strong></label>
                        </div>
                        <p class="cookie-category-description">
                            Se utilizan para rastrear a los visitantes en los sitios web para mostrar anuncios que sean relevantes y atractivos.
                        </p>
                    </div>
                </div>
                <div class="cookie-modal-footer">
                    <button onclick="document.getElementById('cookie-settings-modal').remove()" class="btn btn-outline-secondary">Cancelar</button>
                    <button onclick="window.cookieBanner.saveSettings()" class="btn btn-primary">Guardar configuración</button>
                </div>
            </div>
        `;

        const modalStyle = document.createElement('style');
        modalStyle.textContent = `
            .cookie-modal {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                z-index: 10001;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .cookie-modal-backdrop {
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0,0,0,0.5);
            }
            .cookie-modal-content {
                position: relative;
                background: white;
                border-radius: 8px;
                max-width: 600px;
                width: 90%;
                max-height: 80vh;
                overflow-y: auto;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            }
            .cookie-modal-header {
                padding: 20px 20px 0;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 1px solid #eee;
                padding-bottom: 15px;
                margin-bottom: 20px;
            }
            .cookie-modal-header h3 {
                margin: 0;
                color: #333;
            }
            .cookie-modal-close {
                background: none;
                border: none;
                font-size: 24px;
                cursor: pointer;
                color: #999;
            }
            .cookie-modal-close:hover {
                color: #333;
            }
            .cookie-modal-body {
                padding: 0 20px;
            }
            .cookie-category {
                margin-bottom: 25px;
                padding: 15px;
                border: 1px solid #eee;
                border-radius: 5px;
            }
            .cookie-category-header {
                display: flex;
                align-items: center;
                margin-bottom: 10px;
            }
            .cookie-category-header input {
                margin-right: 10px;
            }
            .cookie-category-header label {
                margin: 0;
                cursor: pointer;
            }
            .cookie-category-description {
                margin: 0;
                color: #666;
                font-size: 14px;
                line-height: 1.4;
            }
            .cookie-modal-footer {
                padding: 20px;
                border-top: 1px solid #eee;
                display: flex;
                justify-content: flex-end;
                gap: 10px;
            }
            .cookie-modal-footer button {
                padding: 10px 20px;
                border: 1px solid #ddd;
                border-radius: 5px;
                cursor: pointer;
                font-size: 14px;
            }
            .cookie-modal-footer .btn-primary {
                background: #0d6efd;
                color: white;
                border-color: #0d6efd;
            }
            .cookie-modal-footer .btn-outline-secondary {
                background: transparent;
                color: #6c757d;
                border-color: #6c757d;
            }
        `;

        document.head.appendChild(modalStyle);
        document.body.appendChild(modal);

        // Cargar configuración actual si existe
        const currentConsent = this.getConsent();
        if (currentConsent) {
            document.getElementById('analytics').checked = currentConsent.analytics;
            document.getElementById('functional').checked = currentConsent.functional;
            document.getElementById('marketing').checked = currentConsent.marketing;
        }
    }

    saveSettings() {
        const preferences = {
            analytics: document.getElementById('analytics').checked,
            functional: document.getElementById('functional').checked,
            marketing: document.getElementById('marketing').checked
        };

        this.saveConsent(preferences);
        document.getElementById('cookie-settings-modal').remove();
        this.hideBanner();
    }

    hideBanner() {
        const banner = document.getElementById('cookie-banner');
        if (banner) {
            banner.remove();
        }
    }

    loadScripts(consent) {
        // Cargar Metricool solo si se acepta analytics
        if (consent.analytics) {
            this.loadMetricool();
        }

        // Cargar otros scripts según consentimiento
        if (consent.functional) {
            // Cargar scripts funcionales
            console.log('Loading functional scripts');
        }

        if (consent.marketing) {
            // Cargar scripts de marketing
            console.log('Loading marketing scripts');
        }
    }

    loadMetricool() {
        // Solo cargar si no está ya cargado
        if (!document.querySelector('script[src*="metricool"]')) {
            const script = document.createElement('script');
            script.innerHTML = `
                function loadScript(a){
                    var b=document.getElementsByTagName("head")[0],
                    c=document.createElement("script");
                    c.type="text/javascript",
                    c.src="https://tracker.metricool.com/resources/be.js",
                    c.onload=a,
                    c.onerror=function(){
                        console.warn('Metricool script failed to load')
                    },
                    b.appendChild(c)
                }
                loadScript(function(){
                    beTracker.t({hash:"fabe37fc5c74e614c28f4a6b6d224a76"})
                });
            `;
            document.head.appendChild(script);
        }
    }

    // Método para revocar consentimiento (para el footer)
    revokeConsent() {
        localStorage.removeItem(this.cookieName);
        document.cookie = `${this.cookieName}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
        this.showBanner();
    }
}

// Inicializar cuando se carga el DOM
document.addEventListener('DOMContentLoaded', function() {
    window.cookieBanner = new CookieBanner();
});

// Método global para revocar desde footer
window.revokeCookieConsent = function() {
    if (window.cookieBanner) {
        window.cookieBanner.revokeConsent();
    }
};