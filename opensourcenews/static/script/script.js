// Function to update the displayed vote count
function updateVoteCounts(button, upvotes, downvotes) {
    const upvoteCountElement = button.closest('.vote-container').querySelector('.upvotes-count');
    const downvoteCountElement = button.closest('.vote-container').querySelector('.downvotes-count');
    
    // Update the vote counts displayed on the page
    upvoteCountElement.textContent = upvotes;
    downvoteCountElement.textContent = downvotes;
}

// Handle upvoting for comments
document.querySelectorAll('.upvote-comment').forEach(button => {
    button.addEventListener('click', function() {
        const commentId = button.getAttribute('data-comment-id');
        fetch(`/comment/${commentId}/upvote/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.upvotes !== undefined) {
                // Update the displayed vote counts on the page
                updateVoteCounts(button, data.upvotes, data.downvotes);
            }
        });
    });
});

// Handle downvoting for comments
document.querySelectorAll('.downvote-comment').forEach(button => {
    button.addEventListener('click', function() {
        const commentId = button.getAttribute('data-comment-id');
        fetch(`/comment/${commentId}/downvote/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.upvotes !== undefined) {
                // Update the displayed vote counts on the page
                updateVoteCounts(button, data.upvotes, data.downvotes);
            }
        });
    });
});

// Helper function to get the CSRF token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
