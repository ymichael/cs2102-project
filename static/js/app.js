$(function() {
    // Search box.
    $searchInput = $("#searchInput");
    $searchInput.keypress(function(e) {     
        if (e.which == 13) {
            e.preventDefault();
            if ($searchInput.val()) {
                $("#searchForm").submit();
            }
        }
    });
});
