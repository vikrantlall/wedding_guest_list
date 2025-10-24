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

/**
 * Enhanced sort table that works with filters
 */
function sortTable(columnIndex) {
    const table = document.getElementById('guestTable');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr.guest-row'));
    const th = table.querySelectorAll('th.sortable')[columnIndex];

    // Determine sort direction
    const isAsc = th.classList.contains('asc');

    // Remove all sort classes
    table.querySelectorAll('th.sortable').forEach(header => {
        header.classList.remove('asc', 'desc');
    });

    // Add appropriate class
    if (isAsc) {
        th.classList.add('desc');
    } else {
        th.classList.add('asc');
    }

    // Sort rows
    rows.sort((a, b) => {
        let aValue, bValue;

        if (columnIndex === 1) {
            // Count column - sort numerically
            aValue = parseInt(a.cells[columnIndex].querySelector('.guest-count').textContent);
            bValue = parseInt(b.cells[columnIndex].querySelector('.guest-count').textContent);
        } else if (columnIndex === 2 || columnIndex === 3) {
            // Side or Attendance - get badge text
            aValue = a.cells[columnIndex].querySelector('.badge').textContent.trim().toLowerCase();
            bValue = b.cells[columnIndex].querySelector('.badge').textContent.trim().toLowerCase();
        } else {
            // Name column - sort alphabetically
            aValue = a.cells[columnIndex].querySelector('.guest-name').textContent.trim().toLowerCase();
            bValue = b.cells[columnIndex].querySelector('.guest-name').textContent.trim().toLowerCase();
        }

        if (aValue < bValue) return isAsc ? 1 : -1;
        if (aValue > bValue) return isAsc ? -1 : 1;
        return 0;
    });

    // Reorder rows
    rows.forEach(row => tbody.appendChild(row));

    // Reapply filters after sorting
    filterTable();
}

/**
 * Filter and search table
 */
function filterTable() {
    const searchInput = document.getElementById('searchInput').value.toLowerCase();
    const filterSide = document.getElementById('filterSide').value.toLowerCase();
    const filterAttendance = document.getElementById('filterAttendance').value.toLowerCase();

    const table = document.getElementById('guestTable');
    const rows = table.getElementsByClassName('guest-row');
    const noResults = document.getElementById('noResults');

    let visibleCount = 0;

    for (let i = 0; i < rows.length; i++) {
        const row = rows[i];
        const name = row.querySelector('.guest-name').textContent.toLowerCase();
        const side = row.querySelector('[data-side]').getAttribute('data-side');
        const attendance = row.querySelector('[data-attendance]').getAttribute('data-attendance');

        // Check if row matches all filters
        const matchesSearch = name.includes(searchInput);
        const matchesSide = filterSide === '' || side === filterSide;
        const matchesAttendance = filterAttendance === '' || attendance === filterAttendance;

        if (matchesSearch && matchesSide && matchesAttendance) {
            row.style.display = '';
            visibleCount++;
        } else {
            row.style.display = 'none';
        }
    }

    // Update visible count
    document.getElementById('visibleCount').textContent = visibleCount;

    // Show/hide no results message
    if (visibleCount === 0 && rows.length > 0) {
        noResults.style.display = 'block';
        table.style.display = 'none';
    } else {
        noResults.style.display = 'none';
        table.style.display = 'table';
    }
}

/**
 * Clear all filters
 */
function clearFilters() {
    document.getElementById('searchInput').value = '';
    document.getElementById('filterSide').value = '';
    document.getElementById('filterAttendance').value = '';
    filterTable();
}

/**
 * Open add guest modal
 */
function openAddGuestModal() {
    const modal = document.getElementById('addGuestModal');
    modal.classList.add('active');

    // Focus on first input
    setTimeout(() => {
        modal.querySelector('input[name="name"]').focus();
    }, 100);

    // Prevent body scroll
    document.body.style.overflow = 'hidden';
}

/**
 * Close add guest modal
 */
function closeAddGuestModal() {
    const modal = document.getElementById('addGuestModal');
    modal.classList.remove('active');

    // Reset form
    modal.querySelector('form').reset();

    // Restore body scroll
    document.body.style.overflow = 'auto';
}

/**
 * Close modal when clicking outside
 */
window.onclick = function(event) {
    const modal = document.getElementById('addGuestModal');
    if (event.target === modal) {
        closeAddGuestModal();
    }
}

/**
 * Close modal with Escape key
 */
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        const modal = document.getElementById('addGuestModal');
        if (modal.classList.contains('active')) {
            closeAddGuestModal();
        }
    }
});