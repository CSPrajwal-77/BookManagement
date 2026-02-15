document.addEventListener('DOMContentLoaded', () => {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    if (alerts) {
        setTimeout(() => {
            alerts.forEach(alert => {
                const closeBtn = alert.querySelector('.btn-close');
                if (closeBtn) closeBtn.click();
            });
        }, 5000);
    }

    // Client-side confirmation for delete actions
    const deleteLinks = document.querySelectorAll('a[href*="delete"]');
    deleteLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            if (!confirm('Are you strictly sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });

    // Simple password match validation on Sign Up
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', (e) => {
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirmPassword').value;

            if (password !== confirmPassword) {
                e.preventDefault();
                alert('Passwords do not match!');
            }
        });
    }
});
