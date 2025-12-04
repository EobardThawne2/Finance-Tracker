/**
 * Finance Tracker - Main JavaScript
 */

// Auto-dismiss flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.style.opacity = '0';
            message.style.transform = 'translateY(-10px)';
            setTimeout(function() {
                message.remove();
            }, 300);
        }, 5000);
    });
});

// Confirm before delete actions
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item?');
}

// Format currency
function formatCurrency(amount, currency = 'INR') {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 2
    }).format(amount);
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Smooth scroll to element
function scrollToElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Toggle mobile menu (if needed)
function toggleMobileMenu() {
    const navMenu = document.querySelector('.nav-menu');
    if (navMenu) {
        navMenu.classList.toggle('active');
    }
}

// Form validation helper
function validateForm(formElement) {
    const requiredFields = formElement.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(function(field) {
        if (!field.value.trim()) {
            isValid = false;
            field.classList.add('error');
        } else {
            field.classList.remove('error');
        }
    });
    
    return isValid;
}

// Currency conversion preview
async function previewConversion(amount, fromCurrency, targetElement) {
    if (!amount || fromCurrency === 'INR') {
        targetElement.style.display = 'none';
        return;
    }
    
    try {
        const response = await fetch(`/api/convert?amount=${amount}&from=${fromCurrency}&to=INR`);
        const data = await response.json();
        
        if (data.success) {
            targetElement.textContent = formatCurrency(data.converted, 'INR');
            targetElement.style.display = 'block';
        }
    } catch (error) {
        console.error('Conversion error:', error);
    }
}

// Debounce function for performance
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Chart resize handler
window.addEventListener('resize', debounce(function() {
    // Handle chart resizing if needed
    const chartImages = document.querySelectorAll('.chart-image');
    chartImages.forEach(function(img) {
        img.style.maxWidth = '100%';
        img.style.height = 'auto';
    });
}, 250));

// Print functionality
function printPage() {
    window.print();
}

// Export data (placeholder)
function exportData(format) {
    alert(`Export to ${format} - Feature coming soon!`);
}

// Initialize tooltips (if any)
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    tooltipElements.forEach(function(element) {
        element.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.dataset.tooltip;
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
            tooltip.style.left = rect.left + (rect.width - tooltip.offsetWidth) / 2 + 'px';
        });
        
        element.addEventListener('mouseleave', function() {
            const tooltips = document.querySelectorAll('.tooltip');
            tooltips.forEach(t => t.remove());
        });
    });
}

// Run on page load
document.addEventListener('DOMContentLoaded', function() {
    initTooltips();
});
