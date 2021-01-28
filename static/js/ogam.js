$(document).ready(function () {
    let id_list = [];
    let cnt = 0;
    const max = 3;
    $(".box").click(function () {
        if ($(this).hasClass("rounded")) {
            $(this).removeClass("rounded");
            $(this).addClass("img-thumbnail");
            const elmId = $(this).attr("id");
            id_list.push(elmId);
            cnt++;
        }
        if (cnt >= max) {
            location.href = '/seoul?ogamId=' + id_list
        }
    });
});