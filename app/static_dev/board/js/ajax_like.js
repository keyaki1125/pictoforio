$(document).ready(function (event) {
    $(document).on('click', '#ajax-like', function (event) {
        event.preventDefault();
        let post_id = parseInt($(this).attr('name'), 10);
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: {
                'post_id': post_id,
            },
            datatype: 'json',
        }).done(function (response) {
            let selector = document.getElementsByName(response["post_id"] + "-like-btn");
            if (response["liked"]) {
                $(selector).html("<i class='fas fa-heart like-red' style=\"color: #e8383d\"></i>");
            } else {
                $(selector).html("<i class='far fa-heart'></i>");
            }
            let selector2 = document.getElementsByName(response["post_id"] + "-like-count");
            $(selector2).text("いいね！ " + response["like_count"] + " 件");
        });
    });
});