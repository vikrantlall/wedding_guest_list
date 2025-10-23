/**
 * JavaScript for Wedding Guest List Application
 */

// Auto-hide flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.style.animation = 'slideOut 0.3s ease';
            setTimeout(function() {
                message.remove();
            }, 300);
        }, 5000);
    });
});

// Add slideOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

/**
 * Edit guest inline
 */
function editGuest(guestId) {
    const row = document.getElementById(`guest-row-${guestId}`);

    // Hide display elements
    row.querySelectorAll('.guest-name, .guest-count, .guest-side, .guest-attendance').forEach(el => {
        el.style.display = 'none';
    });

    // Show edit inputs
    row.querySelectorAll('.edit-input').forEach(el => {
        el.style.display = 'inline-block';
    });

    // Toggle buttons
    row.querySelector('.btn-edit').style.display = 'none';
    row.querySelector('.btn-delete').style.display = 'none';
    row.querySelector('.btn-save').style.display = 'inline-block';
    row.querySelector('.btn-cancel').style.display = 'inline-block';
}

/**
 * Save guest changes
 */
function saveGuest(guestId) {
    const row = document.getElementById(`guest-row-${guestId}`);
    const inputs = row.querySelectorAll('.edit-input');

    const name = inputs[0].value;
    const count = inputs[1].value;
    const side = inputs[2].value;
    const attendance = inputs[3].value;

    // Create form and submit
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/update_guest/${guestId}`;

    const fields = {
        'name': name,
        'count': count,
        'side': side,
        'attendance': attendance
    };

    for (const [key, value] of Object.entries(fields)) {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = key;
        input.value = value;
        form.appendChild(input);
    }

    document.body.appendChild(form);
    form.submit();
}

/**
 * Cancel edit mode
 */
function cancelEdit(guestId) {
    const row = document.getElementById(`guest-row-${guestId}`);

    // Show display elements
    row.querySelectorAll('.guest-name, .guest-count, .guest-side, .guest-attendance').forEach(el => {
        el.style.display = '';
    });

    // Hide edit inputs
    row.querySelectorAll('.edit-input').forEach(el => {
        el.style.display = 'none';
    });

    // Toggle buttons
    row.querySelector('.btn-edit').style.display = 'inline-block';
    row.querySelector('.btn-delete').style.display = 'inline-block';
    row.querySelector('.btn-save').style.display = 'none';
    row.querySelector('.btn-cancel').style.display = 'none';
}

/**
 * Confirm deletion
 */
function confirmDelete(guestName) {
    return confirm(`Are you sure you want to delete ${guestName}?`);
}