console.log("mystyle.js is loaded!");



function confirmFormSubmission(formId, message) {
    document.getElementById(formId).addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent default form submission

        Swal.fire({
            title: "Confirm Submission",
            text: message, // Custom message
            icon: "warning",
            showCancelButton: true,
            confirmButtonText: "Yes Submit",
            cancelButtonText: "No",
            customClass: {
                title: 'swal-title',
                content: 'swal-content',
                confirmButton: 'swal-confirm-button',
                cancelButton: 'swal-cancel-button'
            }
        }).then((result) => {
            if (result.isConfirmed) {
                this.submit(); // Submit the form if confirmed
            }
        });
    });
}

// Usage Example: Call this function for any form dynamically
confirmFormSubmission("product-form-id", "Do you want to submit this data?");