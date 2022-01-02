$(document).ready(function (event) {
    $(document).on('submit', '#ajax-comment', function (event) {
        event.preventDefault();
        let post_id = parseInt($(this).attr('name'), 10)
        console.log($(this).serialize());
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: {
                'post_id': post_id,
                'text': $('#id_text').val(),
            },
            datatype: 'json',
        }).done(function (response) {
            $('.main-comment-section').html(response['form']);
        }).fail(function (response, e) {
            console.log(response.responseText);
        });
    });
});