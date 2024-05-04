$(document).ready(function() {
    $('.table').css({'background-color': '#000', 'color': '#fff'});
    $('.table th, .table td').css({'background-color': '#000', 'color': '#fff'});

    $('.table tbody tr').hover(function() {
        $(this).css('background-color', '#444');
    }, function() {
        $(this).css('background-color', '#000');
    });
});