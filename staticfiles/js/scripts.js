$(document).ready(function() {
    $("form").on("submit", function(event) {
        // Form validation logic
        var isValid = true;

        $(this).find("input").each(function() {
            if ($(this).val() === "") {
                isValid = false;
                $(this).css("border-color", "red");
            } else {
                $(this).css("border-color", "#ccc");
            }
        });

        if (!isValid) {
            event.preventDefault();
            alert("Please fill out all fields.");
        }
    });
});
