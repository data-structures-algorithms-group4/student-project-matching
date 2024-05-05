$(document).ready(function() {
    console.log("Script is running!"); // Add this line to check if the script is executing

    // Initially hide match title and dashboard
    $('#match_title, .dashboard').hide();

    // Hide tables
    $('.data-tables').hide();

    $('#uploadForm').submit(function(event) {
        event.preventDefault(); // Prevent default form submission
        
        // Show the match title and dashboard after submitting the form
        $('#match_title, .dashboard').show();

        // Perform AJAX form submission or other actions here
        // For now, let's simulate a delay of 3 seconds before displaying the results
        setTimeout(function() {
            // Simulated data for demonstration
            var studentsData = "<p>Sample student preferences data</p>";
            var projectsData = "<p>Sample project preferences data</p>";
            var matchData = "<p>Sample match results data</p>";

            // Update the content of student preferences, project preferences, and match results
            $('#studentsData').html(studentsData);
            $('#projectsData').html(projectsData);
            $('#matches').html(matchData);

            // Show tables
            $('.data-tables').show();
        }, 3000); // Change 3000 to the actual delay in milliseconds if needed
    });
});