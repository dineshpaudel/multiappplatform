/**
 * Initialize form handlers for the story generation page
 */
function initializeStoryForm() {
    // Handle API provider change
    const apiProviderSelect = document.getElementById('api_provider');
    const apiModelSelect = document.getElementById('api_model');
    
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
    
    // Handle age group change
    const ageGroupSelect = document.getElementById('age_group');
    const genreSelect = document.getElementById('genre');
    
    if (ageGroupSelect && genreSelect) {
        ageGroupSelect.addEventListener('change', async function() {
            const ageGroup = this.value;
            try {
                const response = await fetch(`/stories/get_genres/${encodeURIComponent(ageGroup)}`);
                const data = await response.json();
                
                // Update genre options
                genreSelect.innerHTML = '';
                data.genres.forEach(genre => {
                    const option = document.createElement('option');
                    option.value = genre;
                    option.textContent = genre;
                    genreSelect.appendChild(option);
                });
            } catch (error) {
                console.error('Error fetching genres:', error);
                showToast('Error loading genres', 'error');
            }
        });
    }

    // Handle story generation loading state
    const storyForm = document.getElementById('story-form');
    const submitBtn = document.getElementById('submit-btn');
    const loadingOverlay = document.getElementById('loading-overlay');
    const btnSpinner = submitBtn?.querySelector('.loading-spinner');
    const btnText = submitBtn?.querySelector('.btn-text');

    if (storyForm && submitBtn) {
        storyForm.addEventListener('submit', function(e) {
            // Show loading state
            submitBtn.disabled = true;
            if (btnText) btnText.textContent = 'Generating...';
            if (btnSpinner) btnSpinner.style.display = 'inline-block';
            if (loadingOverlay) loadingOverlay.style.display = 'flex';

            // Optional: Add a timeout to show error if it takes too long
            setTimeout(() => {
                if (submitBtn.disabled) {
                    submitBtn.disabled = false;
                    if (btnText) btnText.textContent = 'Generate Story';
                    if (btnSpinner) btnSpinner.style.display = 'none';
                    if (loadingOverlay) loadingOverlay.style.display = 'none';
                    showToast('Story generation is taking longer than expected. Please try again.', 'error');
                }
            }, 30000); // 30 second timeout
        });
    }
}

/**
 * Initialize audio controls for the story page
 * @param {string} generateAudioUrl - The URL for generating audio
 * @param {string} downloadAudioUrl - The URL for downloading audio
 */
function initializeAudioControls(generateAudioUrl, downloadAudioUrl) {
    const audioElement = document.getElementById('story-audio');
    const controls = {
        playBtn: document.getElementById('play-btn'),
        resetBtn: document.getElementById('reset-btn'),
        progressBar: document.getElementById('progress-bar'),
        progressContainer: document.getElementById('progress-container'),
        downloadBtn: document.getElementById('download-btn'),
        voiceSelect: document.getElementById('voice-select'),
        speedSelect: document.getElementById('speed-select')
    };
    
    let audioState = {
        generated: false,
        isGenerating: false,
        currentVoice: null,
        currentSpeed: null
    };
    
    if (!audioElement || !controls.playBtn) return;

    // Voice selection handler
    if (controls.voiceSelect) {
        controls.voiceSelect.addEventListener('change', function() {
            // Reset audio state when voice changes
            if (audioState.generated) {
                resetAudioState(audioElement, controls, audioState);
            }
        });
    }

    // Speed selection handler
    if (controls.speedSelect) {
        controls.speedSelect.addEventListener('change', function() {
            // Reset audio state when speed changes
            if (audioState.generated) {
                resetAudioState(audioElement, controls, audioState);
            }
        });
    }

    // Play button handler
    controls.playBtn.addEventListener('click', async function() {
        if (audioState.isGenerating) return;
        
        // Always regenerate audio if voice or speed has changed
        if (!audioState.generated || 
            audioState.currentVoice !== controls.voiceSelect.value || 
            audioState.currentSpeed !== controls.speedSelect.value) {
            await generateAndPlayAudio(audioElement, controls, audioState, generateAudioUrl, downloadAudioUrl);
        } else {
            togglePlayPause(audioElement, controls.playBtn);
        }
    });
    
    // Reset button handler
    if (controls.resetBtn) {
        controls.resetBtn.addEventListener('click', function() {
            audioElement.currentTime = 0;
            audioElement.pause();
            controls.playBtn.textContent = 'Play';
        });
    }
    
    // Progress bar handler
    if (controls.progressContainer) {
        controls.progressContainer.addEventListener('click', function(e) {
            if (!audioState.generated) return;
            const percent = e.offsetX / this.offsetWidth;
            audioElement.currentTime = percent * audioElement.duration;
        });
    }
    
    // Update progress bar as audio plays
    audioElement.addEventListener('timeupdate', function() {
        const progress = (audioElement.currentTime / audioElement.duration) * 100;
        if (controls.progressBar) {
            controls.progressBar.style.width = `${progress}%`;
        }
    });
    
    // Reset play button when audio ends
    audioElement.addEventListener('ended', function() {
        controls.playBtn.textContent = 'Play';
    });
}

/**
 * Generate and play audio for the story
 */
async function generateAndPlayAudio(audioElement, controls, audioState, generateAudioUrl, downloadAudioUrl) {
    if (typeof storyId === 'undefined') {
        showToast('Story ID not found', 'error');
        return;
    }

    audioState.isGenerating = true;
    controls.playBtn.textContent = 'Generating Audio...';
    controls.playBtn.disabled = true;
    
    try {
        // Get current voice and speed selections
        const selectedVoice = controls.voiceSelect.value;
        const selectedSpeed = controls.speedSelect.value;

        const formData = new FormData();
        formData.append('story_id', storyId);
        formData.append('voice_name', selectedVoice);
        formData.append('speed', selectedSpeed);
        
        const response = await fetch(generateAudioUrl, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            audioElement.src = data.audio_path;
            audioState.generated = true;
            // Update current voice and speed in state
            audioState.currentVoice = selectedVoice;
            audioState.currentSpeed = selectedSpeed;
            
            if (controls.downloadBtn) {
                controls.downloadBtn.style.display = 'inline-block';
                controls.downloadBtn.href = downloadAudioUrl;
            }
            
            // Wait for audio to be loaded before playing
            await new Promise((resolve) => {
                audioElement.addEventListener('loadeddata', resolve, { once: true });
            });
            
            await audioElement.play();
            controls.playBtn.textContent = 'Pause';
        } else {
            throw new Error(data.error || 'Failed to generate audio');
        }
    } catch (error) {
        console.error('Error generating audio:', error);
        controls.playBtn.textContent = 'Retry';
        showToast(error.message || 'Error generating audio', 'error');
    } finally {
        audioState.isGenerating = false;
        controls.playBtn.disabled = false;
    }
}

/**
 * Toggle play/pause for the audio element
 */
function togglePlayPause(audioElement, playBtn) {
    if (audioElement.paused) {
        audioElement.play();
        playBtn.textContent = 'Pause';
    } else {
        audioElement.pause();
        playBtn.textContent = 'Play';
    }
}

/**
 * Reset audio state when voice or speed changes
 */
function resetAudioState(audioElement, controls, audioState) {
    audioState.generated = false;
    audioState.currentVoice = null;
    audioState.currentSpeed = null;
    audioElement.src = '';
    controls.playBtn.textContent = 'Play';
    if (controls.downloadBtn) {
        controls.downloadBtn.style.display = 'none';
    }
}