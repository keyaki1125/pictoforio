$(document).ready(function (event) {
    $(document).on('submit', '#ajax-comment-del', function (event) {
        event.preventDefault();
        let post_id = parseInt($(this).data('post-id'), 10)
        let comment_id = parseInt($(this).data('comment-id'), 10)
        var confirm = window.confirm("コメントを削除しますか？");
        if (confirm) {
            $.ajax({
                type: 'POST',
                url: $(this).attr('action'),
                data: {
                    'post_id': post_id,
                    'comment_id': comment_id,
                },
                datatype: 'json',
            }).done(function (response) {
                $('.main-comment-section').html(response['form']);
            }).fail(function (response, e) {
                console.log(response.responseText);
            });
        }
    });
});