$(document).ready(function (event) {
    $(document).on('submit', '#ajax-search-post', function (event) {
        event.preventDefault();
        $.ajax({
            type: 'GET',
            url: $(this).attr('action'),
            data: {
                'content': $('#id-content').val(),
            },
            datatype: 'json',
            cache: false,
        }).done(function (response) {
            $('.post-list').html(response['html']);
        }).fail(function (response, e) {
            console.log(response.responseText);
        });
    });
});