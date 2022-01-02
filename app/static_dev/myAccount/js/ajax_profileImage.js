$('#profileImage_croppie').ready(function (event) {
    $('#profileImage_croppie').css('display', 'none');
});

$(document).ready(function (event) {
    viewportWidth = 200 //クロッピングするサイズ（横幅 ピクセル表記）
    viewportHeight = 200 //クロッピングするサイズ（縦幅 ピクセル表記）
    boundaryWidth = 300 //クロッピング元画像のサイズ（横幅 ピクセル表記）
    boundaryHeight = 300 //クロッピング元画像のサイズ（縦幅 ピクセル表記）

    // croppieの初期設定
    $image_crop = $('#profileImage_croppie').croppie({
        enableExif: true,
        viewport: {
            width: viewportWidth,
            height: viewportHeight,
            type: 'circle' //円形にクロッピングしたい際はここをcircleとする
        },
        boundary: {
            width: boundaryWidth,
            height: boundaryHeight
        }
    });
    $('#upload_image').on('change', function () {
        var reader = new FileReader();
        reader.onload = function (event) {
            $image_crop.croppie('bind', {
                url: event.target.result
            }).then(function () {
                // console.log('Bind complete');
            });
        }
        $('#profileImage_croppie').css('display', 'block');
        reader.readAsDataURL(this.files[0]);
    });
    $(document).on('click', '#post_image', function (event) {
        event.preventDefault();
        var url = $(this).data('href')
        var ex_file_path = $('#avatar-image').attr('src')
        var result = window.confirm("プロフィール画像を登録してよろしいですか？");
        if (result) {
            $image_crop.croppie('result', 'base64').then(function (response) {
                $.ajax({
                    url: url,
                    type: "POST",
                    data: {
                        "image": response,
                        // "ex_file_path": ex_file_path,
                    },
                    dataType: 'json',
                    // ここに後述のResponse処理が入ります
                }).done(function (data) {
                    // console.log('done');
                    $('input[type=file]').val('');  //inputファイルを空にする
                    $('#cancel').click()
                    $('#profileImage_croppie').css('display', 'none');
                    $('#profile-image').html('<img class="img-thumbnail mx-auto d-block" id="avatar-image" alt="avatar_image" style="border-radius: 50%;">')
                    // console.log('1');
                    $('#navbarDropdownMenuLink').html('<img class="img-fluid" id="avatar-image-nav" alt="avatar_image" style="width: 30px;border-radius: 50%;">')
                    // console.log('2');
                    $('#avatar-image').attr('src', data["imageURL"]);
                    // console.log('3');
                    $('#avatar-image-nav').attr('src', data["imageURL"]);
                    // console.log('4');
                });
            });
        }
    });
});