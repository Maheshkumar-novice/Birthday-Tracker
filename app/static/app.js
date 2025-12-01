// Birthday App - Event Handlers

// Delete confirmation handler
document.addEventListener('DOMContentLoaded', () => {
    // Handle delete form submissions with confirmation
    const deleteForms = document.querySelectorAll('.delete-form');
    deleteForms.forEach(form => {
        form.addEventListener('submit', (e) => {
            if (!confirm('Are you sure you want to delete this birthday?')) {
                e.preventDefault();
            }
        });
    });
});
