/**
 * DiversIA Accessible Carousel
 * Custom carousel functionality with accessibility features
 */

(function() {
    'use strict';
    
    let carousels = [];
    
    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        initializeCarousels();
    });
    
    /**
     * Initialize all carousels on the page
     */
    function initializeCarousels() {
        const carouselElements = document.querySelectorAll('.carousel');
        
        carouselElements.forEach(function(element) {
            const carousel = new AccessibleCarousel(element);
            carousels.push(carousel);
        });
    }
    
    /**
     * Accessible Carousel Class
     */
    function AccessibleCarousel(element) {
        this.carousel = element;
        this.slides = element.querySelectorAll('.carousel-item');
        this.indicators = element.querySelectorAll('.carousel-indicators button');
        this.prevBtn = element.querySelector('[data-bs-slide="prev"]');
        this.nextBtn = element.querySelector('[data-bs-slide="next"]');
        this.currentIndex = 0;
        this.isPlaying = false;
        this.playInterval = null;
        this.touchStartX = 0;
        this.touchEndX = 0;
        
        this.init();
    }
    
    AccessibleCarousel.prototype = {
        /**
         * Initialize the carousel
         */
        init: function() {
            this.setupAccessibility();
            this.bindEvents();
            this.updateSlides();
            this.announceSlide();
        },
        
        /**
         * Set up accessibility attributes
         */
        setupAccessibility: function() {
            // Set up carousel container
            this.carousel.setAttribute('role', 'region');
            this.carousel.setAttribute('aria-roledescription', 'carousel');
            this.carousel.setAttribute('aria-label', 'Testimonios de usuarios');
            
            // Set up slides
            this.slides.forEach((slide, index) => {
                slide.setAttribute('role', 'group');
                slide.setAttribute('aria-roledescription', 'slide');
                slide.setAttribute('aria-label', `${index + 1} de ${this.slides.length}`);
                
                if (index === 0) {
                    slide.setAttribute('aria-hidden', 'false');
                } else {
                    slide.setAttribute('aria-hidden', 'true');
                }
            });
            
            // Set up navigation buttons
            if (this.prevBtn) {
                this.prevBtn.setAttribute('aria-label', 'Ir al testimonio anterior');
                this.prevBtn.setAttribute('aria-controls', this.carousel.id || 'carousel');
            }
            
            if (this.nextBtn) {
                this.nextBtn.setAttribute('aria-label', 'Ir al siguiente testimonio');
                this.nextBtn.setAttribute('aria-controls', this.carousel.id || 'carousel');
            }
            
            // Set up indicators
            this.indicators.forEach((indicator, index) => {
                indicator.setAttribute('role', 'tab');
                indicator.setAttribute('aria-label', `Ir al testimonio ${index + 1}`);
                indicator.setAttribute('aria-controls', this.carousel.id || 'carousel');
                
                if (index === 0) {
                    indicator.setAttribute('aria-selected', 'true');
                } else {
                    indicator.setAttribute('aria-selected', 'false');
                }
            });
        },
        
        /**
         * Bind event listeners
         */
        bindEvents: function() {
            const self = this;
            
            // Navigation buttons
            if (this.prevBtn) {
                this.prevBtn.addEventListener('click', function(e) {
                    e.preventDefault();
                    self.goToPrevious();
                });
            }
            
            if (this.nextBtn) {
                this.nextBtn.addEventListener('click', function(e) {
                    e.preventDefault();
                    self.goToNext();
                });
            }
            
            // Indicators
            this.indicators.forEach((indicator, index) => {
                indicator.addEventListener('click', function(e) {
                    e.preventDefault();
                    self.goToSlide(index);
                });
            });
            
            // Keyboard navigation
            this.carousel.addEventListener('keydown', function(e) {
                self.handleKeydown(e);
            });
            
            // Touch/swipe support
            this.carousel.addEventListener('touchstart', function(e) {
                self.handleTouchStart(e);
            }, { passive: true });
            
            this.carousel.addEventListener('touchend', function(e) {
                self.handleTouchEnd(e);
            }, { passive: true });
            
            // Pause on hover/focus
            this.carousel.addEventListener('mouseenter', function() {
                self.pause();
            });
            
            this.carousel.addEventListener('mouseleave', function() {
                self.resume();
            });
            
            this.carousel.addEventListener('focusin', function() {
                self.pause();
            });
            
            this.carousel.addEventListener('focusout', function() {
                self.resume();
            });
        },
        
        /**
         * Handle keyboard navigation
         */
        handleKeydown: function(e) {
            switch (e.key) {
                case 'ArrowLeft':
                case 'ArrowUp':
                    e.preventDefault();
                    this.goToPrevious();
                    break;
                case 'ArrowRight':
                case 'ArrowDown':
                    e.preventDefault();
                    this.goToNext();
                    break;
                case 'Home':
                    e.preventDefault();
                    this.goToSlide(0);
                    break;
                case 'End':
                    e.preventDefault();
                    this.goToSlide(this.slides.length - 1);
                    break;
                case ' ':
                case 'Enter':
                    // Let buttons handle their own events
                    break;
            }
        },
        
        /**
         * Handle touch start
         */
        handleTouchStart: function(e) {
            this.touchStartX = e.touches[0].clientX;
        },
        
        /**
         * Handle touch end (swipe detection)
         */
        handleTouchEnd: function(e) {
            this.touchEndX = e.changedTouches[0].clientX;
            this.handleSwipe();
        },
        
        /**
         * Handle swipe gestures
         */
        handleSwipe: function() {
            const swipeThreshold = 50;
            const swipeLength = this.touchEndX - this.touchStartX;
            
            if (Math.abs(swipeLength) > swipeThreshold) {
                if (swipeLength > 0) {
                    // Swipe right - go to previous
                    this.goToPrevious();
                } else {
                    // Swipe left - go to next
                    this.goToNext();
                }
            }
        },
        
        /**
         * Go to previous slide
         */
        goToPrevious: function() {
            const newIndex = this.currentIndex === 0 ? this.slides.length - 1 : this.currentIndex - 1;
            this.goToSlide(newIndex);
        },
        
        /**
         * Go to next slide
         */
        goToNext: function() {
            const newIndex = this.currentIndex === this.slides.length - 1 ? 0 : this.currentIndex + 1;
            this.goToSlide(newIndex);
        },
        
        /**
         * Go to specific slide
         */
        goToSlide: function(index) {
            if (index < 0 || index >= this.slides.length || index === this.currentIndex) {
                return;
            }
            
            const previousIndex = this.currentIndex;
            this.currentIndex = index;
            
            this.updateSlides();
            this.announceSlide();
            
            // Trigger custom event
            const event = new CustomEvent('slideChanged', {
                detail: {
                    previousIndex: previousIndex,
                    currentIndex: this.currentIndex,
                    slide: this.slides[this.currentIndex]
                }
            });
            this.carousel.dispatchEvent(event);
        },
        
        /**
         * Update slide visibility and states
         */
        updateSlides: function() {
            // Update slides
            this.slides.forEach((slide, index) => {
                const isActive = index === this.currentIndex;
                
                slide.classList.toggle('active', isActive);
                slide.setAttribute('aria-hidden', isActive ? 'false' : 'true');
                
                // Manage focus within slides
                const focusableElements = slide.querySelectorAll('a, button, input, select, textarea, [tabindex]:not([tabindex="-1"])');
                focusableElements.forEach(el => {
                    el.setAttribute('tabindex', isActive ? '0' : '-1');
                });
            });
            
            // Update indicators
            this.indicators.forEach((indicator, index) => {
                const isActive = index === this.currentIndex;
                
                indicator.classList.toggle('active', isActive);
                indicator.setAttribute('aria-selected', isActive ? 'true' : 'false');
            });
            
            // Update button states
            if (this.prevBtn && this.nextBtn) {
                // For looping carousel, buttons are always enabled
                this.prevBtn.removeAttribute('disabled');
                this.nextBtn.removeAttribute('disabled');
            }
        },
        
        /**
         * Announce current slide to screen readers
         */
        announceSlide: function() {
            const slideContent = this.slides[this.currentIndex].textContent.trim();
            const announcement = `Mostrando testimonio ${this.currentIndex + 1} de ${this.slides.length}`;
            
            // Create or update live region
            let liveRegion = document.getElementById('carousel-announcements');
            if (!liveRegion) {
                liveRegion = document.createElement('div');
                liveRegion.id = 'carousel-announcements';
                liveRegion.setAttribute('aria-live', 'polite');
                liveRegion.setAttribute('aria-atomic', 'false');
                liveRegion.className = 'visually-hidden';
                document.body.appendChild(liveRegion);
            }
            
            // Set announcement
            liveRegion.textContent = announcement;
        },
        
        /**
         * Start auto-play (if enabled)
         */
        play: function() {
            if (!this.isPlaying && this.carousel.dataset.interval !== 'false') {
                this.isPlaying = true;
                const interval = parseInt(this.carousel.dataset.interval) || 5000;
                
                this.playInterval = setInterval(() => {
                    this.goToNext();
                }, interval);
            }
        },
        
        /**
         * Pause auto-play
         */
        pause: function() {
            if (this.isPlaying) {
                this.isPlaying = false;
                clearInterval(this.playInterval);
                this.playInterval = null;
            }
        },
        
        /**
         * Resume auto-play
         */
        resume: function() {
            // Only resume if carousel was originally set to auto-play
            if (this.carousel.dataset.ride === 'carousel') {
                this.play();
            }
        },
        
        /**
         * Destroy carousel and cleanup
         */
        destroy: function() {
            this.pause();
            // Remove event listeners and restore original state
            // This would be implemented for dynamic content scenarios
        }
    };
    
    // Utility function to get carousel instance
    function getCarousel(element) {
        const carouselElement = element.closest('.carousel');
        return carousels.find(carousel => carousel.carousel === carouselElement);
    }
    
    // Expose carousel functionality globally
    window.DiversiaCarousel = {
        getInstance: getCarousel,
        initializeCarousels: initializeCarousels
    };
    
    // Handle reduced motion preference
    function handleReducedMotion() {
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches ||
                                    document.body.classList.contains('reduce-motion');
        
        if (prefersReducedMotion) {
            carousels.forEach(carousel => {
                carousel.pause();
                // Remove transition classes for instant changes
                carousel.slides.forEach(slide => {
                    slide.style.transition = 'none';
                });
            });
        }
    }
    
    // Check for reduced motion on load and when settings change
    window.addEventListener('load', handleReducedMotion);
    
    if (window.matchMedia) {
        const reducedMotionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
        reducedMotionQuery.addEventListener('change', handleReducedMotion);
    }
    
    // Listen for accessibility setting changes
    document.addEventListener('accessibilityChanged', handleReducedMotion);
    
})();
