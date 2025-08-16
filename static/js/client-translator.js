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
            
            // Full page content
            'Cómo funciona DiversIA': 'How DiversIA Works',
            'Tests gamificados': 'Gamified Tests',
            'Evaluaciones neurocognitivas diseñadas como juegos para identificar tus fortalezas únicas.': 'Neurocognitive assessments designed as games to identify your unique strengths.',
            'Empleo inclusivo': 'Inclusive Employment',
            'Conectamos tu perfil con empresas que buscan específicamente talento neurodivergente.': 'We connect your profile with companies specifically seeking neurodivergent talent.',
            'Community': 'Community',
            'Únete a una comunidad de apoyo donde compartir experiencias y crecer profesionalmente.': 'Join a supportive community to share experiences and grow professionally.',
            'Tus datos, bajo tu control': 'Your data, under your control',
            'Cumplimos con GDPR y garantizamos la máxima privacidad. Tus datos solo se comparten con tu consentimiento explícito.': 'We comply with GDPR and guarantee maximum privacy. Your data is only shared with your explicit consent.',
            
            // Company info and footer details
            'Equipo Eternals': 'Eternals Team',
            'AI Stars League': 'AI Stars League',
            'Avda Espoia, 762': 'Avda Espoia, 762',
            '08789 Barcelona, España': '08789 Barcelona, Spain',
            'diversiaeternals@gmail.com': 'diversiaeternals@gmail.com',
            'Construido con accesibilidad en mente 🌟': 'Built with accessibility in mind 🌟',
            
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
            'Plataforma de inclusión laboral': 'Plateforme d\'inclusion professionnelle',
            'para personas neurodivergentes': 'pour personnes neurodivergentes',
            'Talento que piensa distinto': 'Des talents qui pensent différemment',
            'Conectando talento neurodivergente con oportunidades laborales inclusivas': 'Connecter les talents neurodivergents avec des opportunités d\'emploi inclusives',
            'Conectamos talento neurodivergente con empresas inclusivas': 'Nous connectons le talent neurodivergent avec des entreprises inclusives',
            'Regístrate como persona neurodivergente': 'S\'inscrire comme personne neurodivergente',
            'Regístrate como empresa inclusiva': 'S\'inscrire comme entreprise inclusive',
            'Únete a nuestra comunidad': 'Rejoindre notre communauté',
            'Explora asociaciones': 'Explorer les associations',
            
            // How it works section
            'Cómo funciona DiversIA': 'Comment fonctionne DiversIA',
            'Tests gamificados': 'Tests gamifiés',
            'Evaluaciones neurocognitivas diseñadas como juegos para identificar tus fortalezas únicas.': 'Évaluations neurocognitives conçues comme des jeux pour identifier vos forces uniques.',
            'Empleo inclusivo': 'Emploi inclusif',
            'Conectamos tu perfil con empresas que buscan específicamente talento neurodivergente.': 'Nous connectons votre profil avec des entreprises recherchant spécifiquement du talent neurodivergent.',
            'Community': 'Communauté',
            'Únete a una comunidad de apoyo donde compartir experiencias y crecer profesionalmente.': 'Rejoignez une communauté de soutien pour partager des expériences et grandir professionnellement.',
            
            // Privacy section
            'Tus datos, bajo tu control': 'Vos données, sous votre contrôle',
            'Cumplimos con GDPR y garantizamos la máxima privacidad. Tus datos solo se comparten con tu consentimiento explícito.': 'Nous respectons le RGPD et garantissons une confidentialité maximale. Vos données ne sont partagées qu\'avec votre consentement explicite.',
            
            // Company info and footer details
            'Equipo Eternals': 'Équipe Eternals',
            'AI Stars League': 'AI Stars League',
            'Avda Espoia, 762': 'Avda Espoia, 762',
            '08789 Barcelona, España': '08789 Barcelone, Espagne',
            'diversiaeternals@gmail.com': 'diversiaeternals@gmail.com',
            
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
            'Plataforma de inclusión laboral': 'Plattform für berufliche Inklusion',
            'para personas neurodivergentes': 'für neurodivergente Personen',
            'Talento que piensa distinto': 'Talente, die anders denken',
            'Conectando talento neurodivergente con oportunidades laborales inclusivas': 'Neurodivergente Talente mit inklusiven Arbeitsmöglichkeiten verbinden',
            'Conectamos talento neurodivergente con empresas inclusivas': 'Wir verbinden neurodivergente Talente mit inklusiven Unternehmen',
            'Regístrate como persona neurodivergente': 'Als neurodivergente Person registrieren',
            'Regístrate como empresa inclusiva': 'Als inklusives Unternehmen registrieren',
            'Únete a nuestra comunidad': 'Unserer Gemeinschaft beitreten',
            'Explora asociaciones': 'Verbände erkunden',
            
            // How it works section
            'Cómo funciona DiversIA': 'Wie DiversIA funktioniert',
            'Tests gamificados': 'Gamifizierte Tests',
            'Evaluaciones neurocognitivas diseñadas como juegos para identificar tus fortalezas únicas.': 'Neurokognitive Bewertungen als Spiele entwickelt, um Ihre einzigartigen Stärken zu identifizieren.',
            'Empleo inclusivo': 'Inklusive Beschäftigung',
            'Conectamos tu perfil con empresas que buscan específicamente talento neurodivergente.': 'Wir verbinden Ihr Profil mit Unternehmen, die gezielt neurodivergente Talente suchen.',
            'Community': 'Gemeinschaft',
            'Únete a una comunidad de apoyo donde compartir experiencias y crecer profesionalmente.': 'Treten Sie einer unterstützenden Gemeinschaft bei, um Erfahrungen zu teilen und beruflich zu wachsen.',
            
            // Privacy section
            'Tus datos, bajo tu control': 'Ihre Daten, unter Ihrer Kontrolle',
            'Cumplimos con GDPR y garantizamos la máxima privacidad. Tus datos solo se comparten con tu consentimiento explícito.': 'Wir halten uns an die DSGVO und garantieren maximale Privatsphäre. Ihre Daten werden nur mit Ihrer ausdrücklichen Zustimmung geteilt.',
            
            // Company info and footer details
            'Equipo Eternals': 'Team Eternals',
            'AI Stars League': 'AI Stars League',
            'Avda Espoia, 762': 'Avda Espoia, 762',
            '08789 Barcelona, España': '08789 Barcelona, Spanien',
            'diversiaeternals@gmail.com': 'diversiaeternals@gmail.com',
            
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
            'Plataforma de inclusión laboral': 'Piattaforma di inclusione lavorativa',
            'para personas neurodivergentes': 'per persone neurodivergenti',
            'Talento que piensa distinto': 'Talenti che pensano diversamente',
            'Conectando talento neurodivergente con oportunidades laborales inclusivas': 'Connettere talenti neurodivergenti con opportunità lavorative inclusive',
            'Conectamos talento neurodivergente con empresas inclusivas': 'Colleghiamo talenti neurodivergenti con aziende inclusive',
            'Regístrate como persona neurodivergente': 'Registrati come persona neurodivergente',
            'Regístrate como empresa inclusiva': 'Registrati come azienda inclusiva',
            'Únete a nuestra comunidad': 'Unisciti alla nostra comunità',
            'Explora asociaciones': 'Esplora associazioni',
            
            // How it works section
            'Cómo funciona DiversIA': 'Come funziona DiversIA',
            'Tests gamificados': 'Test gamificati',
            'Evaluaciones neurocognitivas diseñadas como juegos para identificar tus fortalezas únicas.': 'Valutazioni neurocognitive progettate come giochi per identificare le tue forze uniche.',
            'Empleo inclusivo': 'Impiego inclusivo',
            'Conectamos tu perfil con empresas que buscan específicamente talento neurodivergente.': 'Colleghiamo il tuo profilo con aziende che cercano specificamente talenti neurodivergenti.',
            'Community': 'Comunità',
            'Únete a una comunidad de apoyo donde compartir experiencias y crecer profesionalmente.': 'Unisciti a una comunità di supporto dove condividere esperienze e crescere professionalmente.',
            
            // Privacy section
            'Tus datos, bajo tu control': 'I tuoi dati, sotto il tuo controllo',
            'Cumplimos con GDPR y garantizamos la máxima privacidad. Tus datos solo se comparten con tu consentimiento explícito.': 'Rispettiamo il GDPR e garantiamo la massima privacy. I tuoi dati vengono condivisi solo con il tuo consenso esplicito.',
            
            // Company info and footer details
            'Equipo Eternals': 'Team Eternals',
            'AI Stars League': 'AI Stars League',
            'Avda Espoia, 762': 'Avda Espoia, 762',
            '08789 Barcelona, España': '08789 Barcellona, Spagna',
            'diversiaeternals@gmail.com': 'diversiaeternals@gmail.com',
            
            // Footer
            'Contacto': 'Contatto',
            'Enlaces': 'Collegamenti',
            'Síguenos': 'Seguici',
            'Política de Privacidad': 'Politica sulla Privacy',
            'Aviso Legal': 'Note Legali',
            'Términos y Condiciones': 'Termini e Condizioni',
            'Sobre Nosotros': 'Chi Siamo',
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
            'Plataforma de inclusión laboral': 'Plataforma de inclusão laboral',
            'para personas neurodivergentes': 'para pessoas neurodivergentes',
            'Talento que piensa distinto': 'Talentos que pensam diferente',
            'Conectando talento neurodivergente con oportunidades laborales inclusivas': 'Conectando talentos neurodivergentes com oportunidades de trabalho inclusivas',
            'Conectamos talento neurodivergente con empresas inclusivas': 'Conectamos talentos neurodivergentes com empresas inclusivas',
            'Regístrate como persona neurodivergente': 'Registre-se como pessoa neurodivergente',
            'Regístrate como empresa inclusiva': 'Registre-se como empresa inclusiva',
            'Únete a nuestra comunidad': 'Junte-se à nossa comunidade',
            'Explora asociaciones': 'Explore associações',
            
            // How it works section
            'Cómo funciona DiversIA': 'Como funciona a DiversIA',
            'Tests gamificados': 'Testes gamificados',
            'Evaluaciones neurocognitivas diseñadas como juegos para identificar tus fortalezas únicas.': 'Avaliações neurocognitivas projetadas como jogos para identificar suas forças únicas.',
            'Empleo inclusivo': 'Emprego inclusivo',
            'Conectamos tu perfil con empresas que buscan específicamente talento neurodivergente.': 'Conectamos seu perfil com empresas que procuram especificamente talentos neurodivergentes.',
            'Community': 'Comunidade',
            'Únete a una comunidad de apoyo donde compartir experiencias y crecer profesionalmente.': 'Junte-se a uma comunidade de apoio onde compartilhar experiências e crescer profissionalmente.',
            
            // Privacy section
            'Tus datos, bajo tu control': 'Seus dados, sob seu controle',
            'Cumplimos con GDPR y garantizamos la máxima privacidad. Tus datos solo se comparten con tu consentimiento explícito.': 'Cumprimos com o RGPD e garantimos máxima privacidade. Seus dados são compartilhados apenas com seu consentimento explícito.',
            
            // Company info and footer details
            'Equipo Eternals': 'Equipe Eternals',
            'AI Stars League': 'AI Stars League',
            'Avda Espoia, 762': 'Avda Espoia, 762',
            '08789 Barcelona, España': '08789 Barcelona, Espanha',
            'diversiaeternals@gmail.com': 'diversiaeternals@gmail.com',
            
            // Footer
            'Contacto': 'Contato',
            'Enlaces': 'Links',
            'Síguenos': 'Siga-nos',
            'Política de Privacidad': 'Política de Privacidade',
            'Aviso Legal': 'Aviso Legal',
            'Términos y Condiciones': 'Termos e Condições',
            'Sobre Nosotros': 'Sobre Nós',
            'Todos los derechos reservados': 'Todos os direitos reservados',
            'Construido con accesibilidad en mente': 'Construído com acessibilidade em mente',
            
            // Conditions
            'TDAH': 'TDAH',
            'TEA': 'TEA',
            'Dislexia': 'Dislexia'
        },
        
        'ar': {
            // Navigation (Arabic)
            'Inicio': 'الرئيسية',
            'Personas ND': 'الأشخاص ND',
            'Empresas': 'الشركات',
            'Comunidad': 'المجتمع',
            'Asociaciones': 'الجمعيات',
            'Nosotros': 'من نحن',
            'Idioma': 'اللغة',
            
            // Main content
            'Plataforma de inclusión laboral': 'منصة الإدماج المهني',
            'para personas neurodivergentes': 'للأشخاص ذوي التنوع العصبي',
            'Conectamos talento neurodivergente con empresas inclusivas': 'نربط المواهب ذات التنوع العصبي بالشركات الشاملة',
            'Regístrate como persona neurodivergente': 'سجل كشخص ذو تنوع عصبي',
            'Regístrate como empresa inclusiva': 'سجل كشركة شاملة',
            
            // Footer
            'Contacto': 'اتصل بنا',
            'Enlaces': 'روابط',
            'Síguenos': 'تابعنا',
            'Todos los derechos reservados': 'جميع الحقوق محفوظة',
            
            // Conditions
            'TDAH': 'اضطراب نقص الانتباه',
            'TEA': 'طيف التوحد',
            'Dislexia': 'عسر القراءة'
        },
        
        'zh': {
            // Navigation (Chinese)
            'Inicio': '首页',
            'Personas ND': '神经多样性人群',
            'Empresas': '企业',
            'Comunidad': '社区',
            'Asociaciones': '协会',
            'Nosotros': '关于我们',
            'Idioma': '语言',
            
            // Main content
            'Plataforma de inclusión laboral': '职业包容平台',
            'para personas neurodivergentes': '为神经多样性人群',
            'Conectamos talento neurodivergente con empresas inclusivas': '我们连接神经多样性人才与包容性企业',
            'Regístrate como persona neurodivergente': '注册为神经多样性人员',
            'Regístrate como empresa inclusiva': '注册为包容性企业',
            
            // Footer
            'Contacto': '联系我们',
            'Enlaces': '链接',
            'Síguenos': '关注我们',
            'Todos los derechos reservados': '版权所有',
            
            // Conditions
            'TDAH': '注意力缺陷多动障碍',
            'TEA': '自闭症谱系障碍',
            'Dislexia': '阅读障碍'
        },
        
        'ja': {
            // Navigation (Japanese)
            'Inicio': 'ホーム',
            'Personas ND': 'ND の人々',
            'Empresas': '企業',
            'Comunidad': 'コミュニティ',
            'Asociaciones': '協会',
            'Nosotros': '私たちについて',
            'Idioma': '言語',
            
            // Main content
            'Plataforma de inclusión laboral': '職業包摂プラットフォーム',
            'para personas neurodivergentes': 'ニューロダイバージェントの人々のため',
            'Conectamos talento neurodivergente con empresas inclusivas': 'ニューロダイバージェントな才能と包摂的企業を結ぶ',
            'Regístrate como persona neurodivergente': 'ニューロダイバージェントとして登録',
            'Regístrate como empresa inclusiva': '包摂的企業として登録',
            
            // Footer
            'Contacto': 'お問い合わせ',
            'Enlaces': 'リンク',
            'Síguenos': 'フォローする',
            'Todos los derechos reservados': 'すべての権利を保有',
            
            // Conditions
            'TDAH': 'ADHD',
            'TEA': '自閉症スペクトラム障害',
            'Dislexia': 'ディスレクシア'
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
    
    // Store original content on first load
    let originalContent = null;
    
    // Main translate function
    window.translateTo = function(langCode) {
        console.log('Translating to:', langCode);
        
        // Store original content if not already stored
        if (!originalContent) {
            originalContent = document.body.innerHTML;
        }
        
        if (langCode === 'es') {
            resetTranslation();
            return;
        }
        
        updateLanguageButton(langCode, true);
        
        // Apply translations
        setTimeout(() => {
            try {
                // Reset to original before applying new translation
                if (currentLanguage !== 'es') {
                    document.body.innerHTML = originalContent;
                    // Reinitialize icons and chat
                    if (typeof lucide !== 'undefined') {
                        lucide.createIcons();
                    }
                    if (window.initializeChatWidget) {
                        window.initializeChatWidget();
                    }
                }
                
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
    
    // Reset function
    function resetTranslation() {
        if (originalContent) {
            document.body.innerHTML = originalContent;
            
            // Reinitialize scripts
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
            
            // Reinitialize chat widget
            if (window.initializeChatWidget) {
                window.initializeChatWidget();
            }
        }
        
        currentLanguage = 'es';
        localStorage.setItem('diversia_language', 'es');
        updateLanguageButton('es', false);
    }
    
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
    
    // Reset function
    function resetTranslation() {
        if (originalContent) {
            document.body.innerHTML = originalContent;
            
            // Reinitialize scripts
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
            
            // Reinitialize chat widget
            if (window.initializeChatWidget) {
                window.initializeChatWidget();
            }
        }
        
        currentLanguage = 'es';
        localStorage.setItem('diversia_language', 'es');
        updateLanguageButton('es', false);
    }
    
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