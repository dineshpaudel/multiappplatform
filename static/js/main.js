document.addEventListener('DOMContentLoaded', function() {
    // Initialize mobile navigation
    initMobileNav();
    
    // Initialize toast notifications
    initToastSystem();
});

/**
 * Initialize mobile navigation toggle
 */
function initMobileNav() {
    const navToggle = document.getElementById('nav-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (navToggle && navLinks) {
        navToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            
            // Toggle icon between bars and X
            const icon = navToggle.querySelector('i');
            if (icon.classList.contains('fa-bars')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
        
        // Close nav when clicking outside
        document.addEventListener('click', function(event) {
            const isClickInside = navToggle.contains(event.target) || navLinks.contains(event.target);
            
            if (!isClickInside && navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
                const icon = navToggle.querySelector('i');
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
    }
}

/**
 * Initialize toast notification system
 */
function initToastSystem() {
    // Method to show toast notifications
    window.showToast = function(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        document.body.appendChild(toast);
        
        // Show toast
        setTimeout(() => toast.classList.add('show'), 100);
        
        // Remove toast after 3 seconds
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    };
}

/**
 * Handle form loading states
 * @param {HTMLElement} form - The form element
 * @param {HTMLElement} submitButton - The submit button
 * @param {string} loadingText - Text to display while loading
 * @param {string} originalText - Original button text
 */
function handleFormSubmit(form, submitButton, loadingText = 'Processing...', originalText = null) {
    if (!form || !submitButton) return;
    
    // Store original text if not provided
    if (!originalText) {
        originalText = submitButton.textContent;
    }
    
    form.addEventListener('submit', function() {
        // Create or find spinner
        let spinner = submitButton.querySelector('.loading-spinner');
        if (!spinner) {
            spinner = document.createElement('span');
            spinner.className = 'loading-spinner';
            submitButton.appendChild(spinner);
        }
        
        // Update button state
        submitButton.disabled = true;
        submitButton.textContent = loadingText;
        submitButton.appendChild(spinner);
        
        // Add a timeout to restore button after 30 seconds if no response
        setTimeout(() => {
            if (submitButton.disabled) {
                submitButton.disabled = false;
                submitButton.textContent = originalText;
                window.showToast('Request is taking longer than expected. Please try again.', 'error');
            }
        }, 30000);
    });
}

/**
 * Generic function to fetch data from API endpoints
 * @param {string} url - API endpoint URL
 * @param {Object} options - Fetch options
 * @returns {Promise} - Promise with the response data
 */
async function fetchFromAPI(url, options = {}) {
    try {
        const response = await fetch(url, options);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        window.showToast(error.message || 'Error fetching data', 'error');
        throw error;
    }
}