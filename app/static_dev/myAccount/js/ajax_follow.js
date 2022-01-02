$(document).ready(function (event) {
    $(document).on('click', '#follow', function (event) {
        event.preventDefault();
        let follow_target_id = parseInt($(this).attr('name'), 10)
        $.ajax({
            type: 'POST',
            url: $('#follow-form').attr('action'),
            data: {
                'follow_target_id': follow_target_id,
            },
            datatype: 'json',
            success: function (response) {
                selector = document.getElementsByName(response["follow_target_id"] + "-follow-btn");
                if (response["relation"]) {
                    $(selector).removeClass('btn-outline-primary');
                    $(selector).addClass('btn-outline-danger');
                    $(selector).text('Follow中');
                } else {
                    $(selector).removeClass('btn-outline-danger');
                    $(selector).addClass('btn-outline-primary');
                    $(selector).text('Followする');
                }
            }
        });
    });
});