document.addEventListener('DOMContentLoaded', () => {
    // === 1. THEME MANAGEMENT (DARK / LIGHT TOGGLE) ===
    const initTheme = () => {
        const themeBtn = document.getElementById('theme-toggle');
        if (!themeBtn) return;
        
        // Get active theme from localStorage or system preference
        const savedTheme = localStorage.getItem('theme');
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        
        const setTheme = (theme) => {
            document.documentElement.setAttribute('data-bs-theme', theme);
            localStorage.setItem('theme', theme);
            
            // Toggle icon
            const icon = themeBtn.querySelector('i');
            if (icon) {
                if (theme === 'dark') {
                    icon.className = 'bi bi-sun-fill';
                } else {
                    icon.className = 'bi bi-moon-fill';
                }
            }
        };
        
        // Apply initial theme
        if (savedTheme) {
            setTheme(savedTheme);
        } else if (systemPrefersDark) {
            setTheme('dark');
        } else {
            setTheme('light');
        }
        
        // Add click listener
        themeBtn.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-bs-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            setTheme(newTheme);
        });
    };
    
    // === 2. AJAX COMMENT SUBMISSIONS ===
    const initComments = () => {
        const commentForm = document.getElementById('comment-form');
        const commentsContainer = document.getElementById('comments-list');
        const noCommentsAlert = document.getElementById('no-comments-alert');
        const commentCountBadge = document.getElementById('comment-count-badge');
        
        if (!commentForm || !commentsContainer) return;
        
        commentForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const submitBtn = commentForm.querySelector('button[type="submit"]');
            const textarea = commentForm.querySelector('textarea');
            const content = textarea.value.trim();
            const actionUrl = commentForm.getAttribute('action');
            
            if (!content) return;
            
            // Show loading state
            const originalBtnText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Posting...';
            
            try {
                const response = await fetch(actionUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({ content: content })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    // Create and inject new comment element beautifully
                    const newCommentHtml = `
                        <div class="comment-box animate__animated animate__fadeIn" id="comment-${data.id}">
                            <div class="d-flex align-items-start">
                                <img src="${data.profile_pic}" alt="${data.username}" class="comment-avatar me-3">
                                <div class="w-100">
                                    <div class="d-flex justify-content-between align-items-center mb-1">
                                        <h6 class="mb-0 fw-semibold">${data.username}</h6>
                                        <small class="text-muted">${data.created_at}</small>
                                    </div>
                                    <p class="mb-0 text-secondary" style="white-space: pre-wrap;">${escapeHtml(data.content)}</p>
                                </div>
                            </div>
                        </div>
                    `;
                    
                    // Remove "No comments yet" if it exists
                    if (noCommentsAlert) {
                        noCommentsAlert.remove();
                    }
                    
                    // Insert at top of comments list
                    commentsContainer.insertAdjacentHTML('afterbegin', newCommentHtml);
                    
                    // Clear and focus textarea
                    textarea.value = '';
                    
                    // Update comment counts dynamically
                    if (commentCountBadge) {
                        const currentCount = parseInt(commentCountBadge.textContent) || 0;
                        commentCountBadge.textContent = currentCount + 1;
                    }
                    
                    // Display micro feedback toast
                    showFeedbackToast('Comment added successfully!', 'success');
                } else {
                    showFeedbackToast(data.error || 'Failed to submit comment.', 'danger');
                }
            } catch (error) {
                console.error('Comment submission error:', error);
                showFeedbackToast('An error occurred. Please try again.', 'danger');
            } finally {
                // Restore submit button state
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;
            }
        });
    };
    
    // Helper to prevent XSS in comment dynamic updates
    const escapeHtml = (text) => {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, function(m) { return map[m]; });
    };
    
    // Create inline feedback alerts/toasts dynamically
    const showFeedbackToast = (message, category) => {
        const toastContainer = document.createElement('div');
        toastContainer.style.position = 'fixed';
        toastContainer.style.top = '20px';
        toastContainer.style.right = '20px';
        toastContainer.style.zIndex = '9999';
        toastContainer.className = 'animate__animated animate__fadeInRight';
        
        toastContainer.innerHTML = `
            <div class="alert alert-${category} alert-dismissible shadow-lg fade show" role="alert" style="border-radius: 12px; margin-bottom: 0;">
                <i class="bi ${category === 'success' ? 'bi-check-circle-fill' : 'bi-exclamation-triangle-fill'} me-2"></i>
                <strong>${message}</strong>
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        
        document.body.appendChild(toastContainer);
        
        // Auto-remove after 4 seconds
        setTimeout(() => {
            toastContainer.className = 'animate__animated animate__fadeOutRight';
            setTimeout(() => toastContainer.remove(), 500);
        }, 4000);
    };

    // === 3. CHARTS / ANALYTICS WIDGETS ===
    const initAnalyticsCharts = () => {
        const ctx = document.getElementById('categoryChart');
        if (!ctx) return;
        
        // Parse data embedded from backend attributes
        const labels = JSON.parse(ctx.getAttribute('data-labels') || '[]');
        const values = JSON.parse(ctx.getAttribute('data-values') || '[]');
        
        if (labels.length === 0) {
            // Display empty state
            const parent = ctx.parentElement;
            parent.innerHTML = '<p class="text-muted text-center my-5">No category distributions available.</p>';
            return;
        }
        
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Posts count',
                    data: values,
                    backgroundColor: [
                        '#6366f1', // Indigo
                        '#8b5cf6', // Violet
                        '#ec4899', // Pink
                        '#f59e0b', // Amber
                        '#10b981', // Emerald
                        '#3b82f6'  // Blue
                    ],
                    borderColor: 'transparent',
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: document.documentElement.getAttribute('data-bs-theme') === 'dark' ? '#cbd5e1' : '#475569',
                            font: {
                                family: 'Plus Jakarta Sans',
                                weight: 500
                            },
                            padding: 15
                        }
                    }
                },
                cutout: '70%'
            }
        });
    };
    
    // Boot elements
    initTheme();
    initComments();
    initAnalyticsCharts();
});
