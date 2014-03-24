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

    // Listing Edit
    $editlistingform = $('#editlistingform');
    $('#editlistingdeletebutton').click(function(e) {
        e.preventDefault();
        if (confirm('Do you really want to delete this entry?')) {
            $editlistingform.submit();
        } else {
            return false;
        }
    })

    // Listing Tabs
    $('#listingTabs a:first').tab('show');

    // Search date
    $("#inputDate").datepicker()
});
