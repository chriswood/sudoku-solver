relocate = function(data) {
    window.location.href = data.data.url;
};

$(document).ready(function() {
    $('#sample').click({url: '/sudoku/sample/'}, relocate);
    $('#clear').click({url: '/sudoku/'}, relocate);
    $('#solve-9000').click(function() {
        // Switch the form action then submit. The GET variable will let
        // the view know to handle this diffrently.
        $('#puzzle-values-form').attr('action', '/sudoku/all/');
        $('#puzzle-values-form').submit();
    });
});