$(document).ready(function() {
    $('.user-pic').click(function(event) {
        event.stopPropagation(); // Prevent this click event from propagating to the document
        $('.user-pic-dropdown').addClass('dropdown-open');
    });

    $('.register-btn').click(function(event) {
        event.stopPropagation(); // Prevent this click event from propagating to the document
        $('.register-dropdown').addClass('dropdown-open-menu');
    });

    // Add a click event listener to the entire document
    $(document).click(function(event) {
        // Check if the clicked element is not a part of user-pic or user-pic-dropdown
        if (!$(event.target).closest('.user-pic').length && !$(event.target).closest('.user-pic-dropdown').length) {
            $('.user-pic-dropdown').removeClass('dropdown-open');
            $('.register-dropdown').removeClass('dropdown-open-menu');
        }
    });
});