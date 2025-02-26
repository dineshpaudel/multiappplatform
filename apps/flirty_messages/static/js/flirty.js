/**
 * Initialize the message generation form
 * @param {string} generateUrl - The URL for the generate endpoint
 */
function initializeMessageForm(generateUrl) {
    const messageForm = document.getElementById('message-form');
    const generateBtn = document.getElementById('generate-btn');
    const resultCard = document.getElementById('result-card');
    const messageResult = document.getElementById('message-result');
    const copyBtn = document.getElementById('copy-btn');
    const newMessageBtn = document.getElementById('new-message-btn');
    const apiProviderSelect = document.getElementById('api_provider');
    const apiModelSelect = document.getElementById('api_model');
    
    if (!messageForm || !generateBtn) return;
    
    // Handle form submission
    messageForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Show loading state
        const btnText = generateBtn.querySelector('.btn-text');
        const btnSpinner = generateBtn.querySelector('.loading-spinner');
        
        generateBtn.disabled = true;
        if (btnText) btnText.textContent = 'Generating...';
        if (btnSpinner) btnSpinner.style.display = 'inline-block';
        
        try {
            // Get form data
            const formData = new FormData(messageForm);
            
            // Send request to generate messages
            const response = await fetch(generateUrl, {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.success) {
                // Display the result
                messageResult.textContent = data.generated_text;
                resultCard.style.display = 'block';
                
                // Scroll to the result card
                resultCard.scrollIntoView({ behavior: 'smooth' });
            } else {
                throw new Error(data.error || 'Failed to generate message');
            }
        } catch (error) {
            console.error('Error generating message:', error);
            showToast(error.message || 'Error generating message', 'error');
        } finally {
            // Reset button state
            generateBtn.disabled = false;
            if (btnText) btnText.textContent = 'Generate Message';
            if (btnSpinner) btnSpinner.style.display = 'none';
        }
    });
    
    // Handle API provider change
    if (apiProviderSelect && apiModelSelect) {
        apiProviderSelect.addEventListener('change', async function() {
            const provider = this.value;
            try {
                const response = await fetch(`/stories/get_models/${provider}`);
                const data = await response.json();
                
                // Update model options
                apiModelSelect.innerHTML = '';
                data.models.forEach(model => {
                    const option = document.createElement('option');
                    option.value = model;
                    option.textContent = model;
                    apiModelSelect.appendChild(option);
                });
            } catch (error) {
                console.error('Error fetching models:', error);
                showToast('Error loading models', 'error');
            }
        });
    }
    
    // Handle copy button
    if (copyBtn && messageResult) {
        copyBtn.addEventListener('click', function() {
            const text = messageResult.textContent;
            copyToClipboard(text);
            showToast('Message copied to clipboard!', 'success');
        });
    }
    
    // Handle new message button
    if (newMessageBtn && resultCard) {
        newMessageBtn.addEventListener('click', function() {
            resultCard.style.display = 'none';
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
}

/**
 * Copy text to clipboard
 * @param {string} text - The text to copy
 */
function copyToClipboard(text) {
    // Create temporary textarea
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.setAttribute('readonly', '');
    textarea.style.position = 'absolute';
    textarea.style.left = '-9999px';
    document.body.appendChild(textarea);
    
    // Select and copy the text
    textarea.select();
    document.execCommand('copy');
    
    // Remove the textarea
    document.body.removeChild(textarea);
}